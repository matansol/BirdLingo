"""
fetch_bird_images_v2.py
=======================
Fetches 5-10 diverse, high-quality images per bird from Wikimedia Commons.
Keeps existing images and only adds more to reach the target count.

Key improvements over fetch_bird_data.py:
  • 6 different search strategies → visual variety (perched, flying, pair, juvenile…)
  • Perceptual-hash deduplication — no near-identical shots saved
  • CLIP validation with absolute cosine similarity (not softmax) — rejects maps, drawings, etc.
  • CLIP-embedding diversity selection — picks images maximally different from each other
  • Auto-compresses every saved image (max 800px, JPEG Q70)
  • Incremental: keeps existing images, only fetches what's missing

Usage:
  python fetch_bird_images_v2.py blue_tit            # single bird
  python fetch_bird_images_v2.py --all               # all birds
  python fetch_bird_images_v2.py --all --count 7     # target 7 per bird
  python fetch_bird_images_v2.py --all --skip-done   # skip birds already at target
  python fetch_bird_images_v2.py --level 1           # difficulty-1 birds only
  python fetch_bird_images_v2.py --no-clip           # faster, ML-free mode

Requires:
  pip install requests pillow imagehash
  pip install torch open-clip-torch   (for CLIP features; optional but recommended)
"""

import sys, re, time, argparse
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import requests
from pathlib import Path
from PIL import Image
from io import BytesIO

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).parent
BIRDS_DIR = BASE_DIR / "assets" / "birds"

# ── Image compression settings ────────────────────────────────────────────────
MAX_SIZE     = 800    # max width or height in pixels
JPEG_QUALITY = 70
MIN_WIDTH    = 400    # reject images smaller than this
MIN_HEIGHT   = 300

# ── Deduplication settings ────────────────────────────────────────────────────
PHASH_THRESH = 8      # perceptual hash distance; lower = stricter (8 is a good default)

DEFAULT_TARGET = 7

HEADERS = {
    "User-Agent": "BirdWhoBot/2.0 (bird-quiz educational app; contact@birdwho.app) python-requests"
}

# ── Bad-image filename filter ─────────────────────────────────────────────────
_BAD = re.compile(
    r"illustration|drawing|sketch|painting|lithograph|plate|engraving|"
    r"diagram|chart|\bmap\b|range_map|skeleton|skull|bone|fossil|taxidermy|specimen|"
    r"\begg\b|\bnest\b|\bfeather\b|stamp|coin|\blogo\b|icon|emblem|flag|coat_of_arms|"
    r"museum|mount|stuffed|distribution|habitat_map|locator|"
    r"phylogeny|cladogram|taxonomy|captive|\bcage\b",
    re.IGNORECASE,
)


# ── CLIP (lazy-loaded) ────────────────────────────────────────────────────────
_C = {}   # holds: model, prep, tok, dev

def _load_clip(verbose=True):
    if _C:
        return True
    try:
        import torch, open_clip
        if verbose:
            print("  Loading CLIP model…", flush=True)
        dev = "cuda" if torch.cuda.is_available() else "cpu"
        model, _, prep = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained="laion2b_s34b_b79k"
        )
        model = model.to(dev).eval()
        tok = open_clip.get_tokenizer("ViT-B-32")
        _C.update(model=model, prep=prep, tok=tok, dev=dev)
        if verbose:
            print(f"  CLIP ready on {dev}\n")
        return True
    except Exception as e:
        if verbose:
            print(f"  CLIP not available: {e}")
        return False


def _enc_img(img: Image.Image):
    """Encode a PIL image to a normalized CLIP embedding (numpy 1-D array)."""
    import torch
    t = _C["prep"](img.convert("RGB")).unsqueeze(0).to(_C["dev"])
    with torch.no_grad():
        f = _C["model"].encode_image(t)
        f = f / f.norm(dim=-1, keepdim=True)
    return f.squeeze(0).cpu().numpy()


def _enc_txts(texts: list) -> "np.ndarray":
    """Encode a list of text strings to normalized CLIP embeddings (numpy N×D)."""
    import torch
    toks = _C["tok"](texts).to(_C["dev"])
    with torch.no_grad():
        f = _C["model"].encode_text(toks)
        f = f / f.norm(dim=-1, keepdim=True)
    return f.cpu().numpy()


# Pre-compute negative text embeddings once (reused for all birds)
_NEG_EMBS = None

def _get_neg_embs():
    global _NEG_EMBS
    if _NEG_EMBS is None:
        _NEG_EMBS = _enc_txts([
            "a geographic range map or world map with colors",
            "a drawing, illustration or painting of a bird",
            "a museum taxidermy specimen or bird skeleton",
            "a postage stamp, coin, or logo",
            "a chart, diagram, or infographic with text labels",
            "a close-up of feathers, eggs, or a nest with no live bird",
            "a photo of a cat, dog, or other non-bird animal",
            "a human face or portrait photograph",
            "a landscape photograph with no birds visible",
            "a photo of a building, interior, or object",
        ])
    return _NEG_EMBS


def clip_score(img: Image.Image, bird_name: str) -> tuple[float, float]:
    """
    Returns (bird_score, bad_score) using absolute cosine similarity.

    Unlike softmax, this gives a meaningful absolute score:
      bird_score ~0.25-0.32 for a good bird photo
      bird_score ~0.12-0.18 for a map / drawing / unrelated photo
    """
    import numpy as np
    pos_embs = _enc_txts([
        f"a wildlife photograph of a {bird_name}",
        f"a photo of a {bird_name} bird outdoors",
        f"a {bird_name} bird in its natural habitat",
        "a high quality bird photograph in nature",
    ])
    img_emb    = _enc_img(img)                       # (D,)
    bird_score = float(np.mean(pos_embs  @ img_emb)) # avg cosine sim to pos prompts
    bad_score  = float(np.mean(_get_neg_embs() @ img_emb))  # avg cosine sim to neg prompts
    return bird_score, bad_score


# ── Wikimedia Commons API helpers ─────────────────────────────────────────────

def _imageinfo(base_url: str, params: dict) -> list[dict]:
    """Generic helper: call a Wikimedia API and collect imageinfo results."""
    try:
        r = requests.get(base_url, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        pages = r.json().get("query", {}).get("pages", {})
        out = []
        for page in pages.values():
            for ii in page.get("imageinfo", []):
                mime = ii.get("mime", "")
                if mime not in ("image/jpeg", "image/jpg"):
                    continue
                url = ii.get("thumburl") or ii.get("url", "")
                if not url:
                    continue
                out.append({
                    "title": page.get("title", ""),
                    "url":   url,
                    "w":     ii.get("thumbwidth",  ii.get("width",  0)),
                    "h":     ii.get("thumbheight", ii.get("height", 0)),
                })
        return out
    except Exception:
        return []


def _commons_category(sci: str, n: int = 20) -> list[dict]:
    """Fetch from the curated Commons category for the species (highest quality)."""
    return _imageinfo("https://commons.wikimedia.org/w/api.php", {
        "action": "query", "format": "json",
        "generator": "categorymembers",
        "gcmtitle": f"Category:{sci.replace(' ', '_')}",
        "gcmtype": "file", "gcmlimit": n * 4,
        "prop": "imageinfo", "iiprop": "url|mime|size", "iiurlwidth": 900,
    })


def _commons_search(query: str, n: int = 10) -> list[dict]:
    """Full-text search on Wikimedia Commons."""
    return _imageinfo("https://commons.wikimedia.org/w/api.php", {
        "action": "query", "format": "json",
        "generator": "search", "gsrnamespace": 6,
        "gsrsearch": query, "gsrlimit": n * 3,
        "prop": "imageinfo", "iiprop": "url|mime|size", "iiurlwidth": 900,
    })


def _wiki_article_images(sci: str, n: int = 10) -> list[dict]:
    """Get images embedded in the Wikipedia article for the species."""
    try:
        r = requests.get(
            "https://en.wikipedia.org/w/api.php", headers=HEADERS, timeout=15,
            params={"action": "query", "format": "json", "titles": sci,
                    "prop": "images", "imlimit": 25, "redirects": 1},
        )
        r.raise_for_status()
        pages = r.json().get("query", {}).get("pages", {})
        titles = []
        for page in pages.values():
            for img in page.get("images", []):
                t = img.get("title", "")
                if t.lower().endswith((".jpg", ".jpeg")) and not _BAD.search(t):
                    titles.append(t)
        if not titles:
            return []
        return _imageinfo("https://commons.wikimedia.org/w/api.php", {
            "action": "query", "format": "json",
            "titles": "|".join(titles[: n * 2]),
            "prop": "imageinfo", "iiprop": "url|mime|size", "iiurlwidth": 900,
        })
    except Exception:
        return []


def gather_candidates(bird: dict, max_cands: int = 45) -> list[dict]:
    """
    Query 6 different sources/queries per bird to maximise visual variety.
    Deduplicates by URL and applies filename + size filters.
    """
    sci, en = bird["scientific"], bird["en"]
    seen, out = set(), []

    def add(imgs):
        for img in imgs:
            u = img.get("url", "")
            if (u and u not in seen
                    and img.get("w", 0) >= MIN_WIDTH
                    and img.get("h", 0) >= MIN_HEIGHT
                    and not _BAD.search(img.get("title", ""))
                    and u.lower().endswith((".jpg", ".jpeg"))):
                seen.add(u)
                out.append(img)

    # Source 1: Commons species category (curated, best quality)
    add(_commons_category(sci, 20));          time.sleep(0.3)
    # Source 2: Wikipedia article images (handpicked by Wikipedia editors)
    add(_wiki_article_images(sci, 12));        time.sleep(0.3)
    # Source 3: Scientific name search (different angle than category)
    add(_commons_search(f'"{sci}"', 10));      time.sleep(0.3)
    # Source 4: English name → general perched/standing photos
    add(_commons_search(f'"{en}" bird photo', 10)); time.sleep(0.3)
    # Source 5: Flying / in-flight shots → visual variety
    add(_commons_search(f'{en} bird flying',  8)); time.sleep(0.3)
    # Source 6: Male / female / juvenile → colour variety
    add(_commons_search(f'{en} bird male female juvenile', 8)); time.sleep(0.2)

    print(f"  {len(out)} raw candidates gathered")
    return out[:max_cands]


# ── Image I/O helpers ─────────────────────────────────────────────────────────

def download_pil(url: str) -> "Image.Image | None":
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        return Image.open(BytesIO(r.content)).convert("RGB")
    except Exception:
        return None


def phash(img: Image.Image):
    """Perceptual hash; returns None if imagehash is not installed."""
    try:
        import imagehash
        return imagehash.phash(img)
    except ImportError:
        return None
    except Exception:
        return None


def save_compressed(img: Image.Image, path: Path):
    """Resize to ≤ MAX_SIZE px and save as optimised JPEG."""
    if img.width > MAX_SIZE or img.height > MAX_SIZE:
        img.thumbnail((MAX_SIZE, MAX_SIZE), Image.Resampling.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)


# ── Per-bird pipeline ─────────────────────────────────────────────────────────

def process_bird(bird: dict, target: int = DEFAULT_TARGET, use_clip: bool = True) -> int:
    """
    Fetch, validate, deduplicate, diversify, and save images for one bird.
    Returns total number of images in the bird's directory afterwards.
    """
    import numpy as np

    slug     = bird["name"]
    en       = bird["en"]
    bird_dir = BIRDS_DIR / slug
    bird_dir.mkdir(parents=True, exist_ok=True)

    existing = sorted(bird_dir.glob("*.jpg"))
    print(f"  {len(existing)} existing image(s)")

    if len(existing) >= target:
        print(f"  Already at target ({target}) — skipping")
        return len(existing)

    need = target - len(existing)

    # ── Stage 1: gather candidates ────────────────────────────────────────────
    cands = gather_candidates(bird, max_cands=45)
    if not cands:
        print("  ✗ No candidates found")
        return len(existing)

    # ── Stage 2: download candidates ──────────────────────────────────────────
    print(f"  Downloading {len(cands)} candidates…")
    downloaded = []   # list of (pil_image, url, title)
    for c in cands:
        img = download_pil(c["url"])
        if img:
            downloaded.append((img, c["url"], c["title"]))
        time.sleep(0.08)
    print(f"  {len(downloaded)} downloaded successfully")

    if not downloaded:
        return len(existing)

    # ── Stage 3: perceptual-hash deduplication ────────────────────────────────
    existing_hashes = []
    for p in existing:
        h = phash(Image.open(p))
        if h is not None:
            existing_hashes.append(h)

    deduped = []
    seen_hashes = list(existing_hashes)
    for img, url, title in downloaded:
        h = phash(img)
        if h is None:
            # imagehash not installed → keep everything, rely on CLIP
            deduped.append((img, url, title))
            continue
        if all((h - sh) >= PHASH_THRESH for sh in seen_hashes):
            deduped.append((img, url, title))
            seen_hashes.append(h)

    print(f"  {len(deduped)} after perceptual-hash dedup (removed {len(downloaded)-len(deduped)} near-duplicates)")

    if not deduped:
        print("  ✗ All candidates were duplicates of existing images")
        return len(existing)

    # ── Stage 4: CLIP validation (absolute cosine similarity) ─────────────────
    if use_clip:
        try:
            validated = []
            for img, url, title in deduped:
                b_score, bad_score = clip_score(img, en)
                # Pass: bird similarity > bad-content similarity AND above floor
                if b_score > bad_score and b_score > 0.18:
                    validated.append((img, url, title, b_score))
                else:
                    print(f"    ✗ CLIP rejected  bird={b_score:.3f}  bad={bad_score:.3f}  {Path(title).name[:50]}")
            print(f"  {len(validated)} passed CLIP validation (rejected {len(deduped)-len(validated)})")
        except Exception as e:
            print(f"  CLIP validation skipped ({e}) — keeping all deduped images")
            validated = [(img, url, title, 0.0) for img, url, title in deduped]
    else:
        validated = [(img, url, title, 0.0) for img, url, title in deduped]

    if not validated:
        print("  ✗ No images passed validation")
        return len(existing)

    # ── Stage 5: CLIP-embedding diversity selection ───────────────────────────
    # Greedily pick the `need` images most visually different from each other
    # AND from the already-existing images (so new images complement existing ones).
    if use_clip and len(validated) > need:
        try:
            # Encode existing images as "anchors" so new images diversify from them
            existing_embs = []
            for p in existing:
                try:
                    existing_embs.append(_enc_img(Image.open(p)))
                except Exception:
                    pass

            cand_embs = [_enc_img(img) for img, _, _, _ in validated]
            n_exist   = len(existing_embs)

            all_embs = np.vstack(existing_embs + cand_embs) if (existing_embs or cand_embs) \
                       else np.array(cand_embs)

            # selected_mask: True = already chosen (existing or newly picked)
            selected_mask    = [True]  * n_exist + [False] * len(cand_embs)
            chosen_cand_idxs = []

            for _ in range(min(need, len(cand_embs))):
                sel_idxs = [i for i, m in enumerate(selected_mask) if m]
                best_cand_idx, best_min_dist = None, -1.0

                for ci in range(len(cand_embs)):
                    ci_global = n_exist + ci
                    if selected_mask[ci_global]:
                        continue
                    if sel_idxs:
                        sel_embs = all_embs[sel_idxs]            # (k, D)
                        dists    = 1.0 - (sel_embs @ all_embs[ci_global])  # (k,) cosine distances
                        min_d    = float(np.min(dists))
                    else:
                        min_d = 1.0   # no anchors yet → all equally distant

                    if min_d > best_min_dist:
                        best_min_dist  = min_d
                        best_cand_idx  = ci

                if best_cand_idx is None:
                    break
                selected_mask[n_exist + best_cand_idx] = True
                chosen_cand_idxs.append(best_cand_idx)

            chosen = [validated[i] for i in chosen_cand_idxs]
            print(f"  {len(chosen)} diverse images selected (avg min-dist={best_min_dist:.3f})")

        except Exception as e:
            print(f"  Diversity selection failed ({e}) — using top-N by CLIP score")
            chosen = sorted(validated, key=lambda x: x[3], reverse=True)[:need]
    else:
        # No CLIP or fewer candidates than needed → just take what we have
        chosen = validated[:need]

    # ── Stage 6: save + compress ──────────────────────────────────────────────
    next_num = len(existing) + 1
    saved    = 0
    for img, url, title, score in chosen:
        out_path = bird_dir / f"{slug}_{next_num}.jpg"
        save_compressed(img, out_path)
        kb = out_path.stat().st_size / 1024
        label = f"clip={score:.3f}" if score > 0 else "no-clip"
        print(f"    ✓ {out_path.name}  {kb:.0f} KB  {label}  ← {Path(title).name[:45]}")
        next_num += 1
        saved += 1

    total = len(existing) + saved
    print(f"  → {total}/{target} images total for {en}")
    return total


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    from birds_200 import BIRDS_200

    parser = argparse.ArgumentParser(
        description="Fetch diverse, accurate bird images (5-10 per bird)"
    )
    parser.add_argument("bird",        nargs="?",  help="Bird slug or English name")
    parser.add_argument("--all",       action="store_true", help="Process all 200 birds")
    parser.add_argument("--level",     type=int,   help="Only birds of this difficulty level")
    parser.add_argument("--count",     type=int,   default=DEFAULT_TARGET,
                        help=f"Target images per bird (default: {DEFAULT_TARGET})")
    parser.add_argument("--skip-done", action="store_true",
                        help="Skip birds that already meet the target count")
    parser.add_argument("--no-clip",   action="store_true",
                        help="Disable CLIP (uses filename filter + phash only; much faster)")
    args = parser.parse_args()

    BIRDS_DIR.mkdir(parents=True, exist_ok=True)

    # ── Resolve bird list ──────────────────────────────────────────────────────
    if args.bird:
        q = args.bird.lower().strip()
        bird = next(
            (b for b in BIRDS_200 if b["name"] == q or b["en"].lower() == q), None
        )
        if not bird:   # partial match
            bird = next(
                (b for b in BIRDS_200 if q in b["name"] or q in b["en"].lower()), None
            )
        if not bird:
            print(f"Bird '{args.bird}' not found in BIRDS_200.")
            sys.exit(1)
        birds = [bird]
    elif args.all:
        birds = BIRDS_200
    elif args.level:
        birds = [b for b in BIRDS_200 if b["difficulty"] == args.level]
    else:
        parser.print_help()
        sys.exit(0)

    # ── CLIP initialisation ───────────────────────────────────────────────────
    use_clip = not args.no_clip
    if use_clip:
        use_clip = _load_clip(verbose=True)
        if not use_clip:
            print("  Falling back to filename filter + phash only.\n")

    print(f"\nTarget:  {args.count} images per bird")
    print(f"CLIP:    {'enabled' if use_clip else 'disabled'}")
    print(f"Birds:   {len(birds)}")
    print("=" * 55)

    for i, bird in enumerate(birds):
        bird_dir = BIRDS_DIR / bird["name"]
        existing = sorted(bird_dir.glob("*.jpg")) if bird_dir.exists() else []

        if args.skip_done and len(existing) >= args.count:
            print(f"[{i+1}/{len(birds)}] {bird['en']} — {len(existing)} images, skipped")
            continue

        print(f"\n[{i+1}/{len(birds)}] {bird['en']} ({bird['scientific']})")
        process_bird(bird, target=args.count, use_clip=use_clip)
        time.sleep(0.5)   # be polite to Wikimedia servers

    print("\n✓ All done.")


if __name__ == "__main__":
    main()
