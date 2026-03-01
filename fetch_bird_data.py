"""
fetch_bird_data.py
==================
Fetches 3 regular images + 1 flying/aerial image for a bird from Wikimedia Commons,
saves them under BirdLingo/assets/birds/<bird_name>/, and updates birds_info.json.

Usage:
  python fetch_bird_data.py "House Sparrow"
  python fetch_bird_data.py house_sparrow
  python fetch_bird_data.py --all              # process all 200 birds
  python fetch_bird_data.py --all --skip-done  # skip fully complete birds
"""

import os, sys, json, time, re, argparse
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
from birds_200 import BIRDS_200

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "BirdLingo" / "assets"
BIRDS_DIR  = ASSETS_DIR / "birds"
INFO_FILE  = BASE_DIR / "birds_info.json"

HEADERS = {
    "User-Agent": "BirdWhoBot/1.0 (bird-quiz educational app; contact@birdwho.app) python-requests/2.31"
}
PEXELS_API_KEY = "BEq2brDnSXCuLYqSvzPlfGIAYqqlIQ0KYrEmOPWgv7P8DF28sd4s8aZE"

# ── Wikimedia Commons helpers ────────────────────────────────────────────────

def _commons_search(query: str, count: int = 6) -> list[dict]:
    """Search Wikimedia Commons for images matching query. Returns list of image info dicts."""
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrnamespace": 6,   # File namespace
        "gsrsearch": query,
        "gsrlimit": count * 3,
        "prop": "imageinfo",
        "iiprop": "url|mime|size",
        "iiurlwidth": 1200,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        results = []
        for page in pages.values():
            ii = page.get("imageinfo", [{}])[0]
            mime = ii.get("mime", "")
            if mime not in ("image/jpeg", "image/png", "image/webp"):
                continue
            url_val = ii.get("url") or ii.get("thumburl")
            if url_val:
                results.append({
                    "title": page.get("title", ""),
                    "url": url_val,
                    "width": ii.get("width", 0),
                    "height": ii.get("height", 0),
                })
        # Prefer larger images
        results.sort(key=lambda x: x["width"] * x["height"], reverse=True)
        return results[:count]
    except Exception as e:
        print(f"    [Commons search error] {e}")
        return []


def _get_wiki_page_images(scientific_name: str, count: int = 6) -> list[dict]:
    """Get images from the Wikipedia article for a species."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": scientific_name,
        "prop": "images",
        "imlimit": 20,
        "redirects": 1,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        image_titles = []
        for page in pages.values():
            for img in page.get("images", []):
                t = img.get("title", "")
                if t.lower().endswith((".jpg", ".jpeg", ".png")):
                    image_titles.append(t)
        if not image_titles:
            return []
        # Now get actual URLs for these images
        return _get_commons_image_urls(image_titles[:count])
    except Exception as e:
        print(f"    [Wiki page images error] {e}")
        return []


def _get_commons_image_urls(titles: list[str]) -> list[dict]:
    """Get direct URLs for a list of File: titles from Commons."""
    if not titles:
        return []
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": "|".join(titles),
        "prop": "imageinfo",
        "iiprop": "url|mime|size",
        "iiurlwidth": 1200,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        results = []
        for page in pages.values():
            ii = page.get("imageinfo", [{}])[0]
            mime = ii.get("mime", "")
            if mime not in ("image/jpeg", "image/png", "image/webp"):
                continue
            url_val = ii.get("url") or ii.get("thumburl")
            if url_val:
                results.append({
                    "title": page.get("title", ""),
                    "url": url_val,
                    "width": ii.get("width", 0),
                    "height": ii.get("height", 0),
                })
        results.sort(key=lambda x: x["width"] * x["height"], reverse=True)
        return results
    except Exception as e:
        print(f"    [Commons URL fetch error] {e}")
        return []


# ── Layer 1: Filename-based bad-image filter ────────────────────────────────

_BAD_TITLE_KEYWORDS = [
    "illustration", "drawing", "sketch", "painting", "lithograph", "plate",
    "engraving", "diagram", "chart", "map", "range",
    "skeleton", "skull", "bone", "fossil", "taxidermy", "specimen",
    "egg", "nest", "feather",
    "stamp", "coin", "logo", "icon", "emblem", "flag", "coat_of_arms",
    "museum", "mount", "stuffed",
    "distribution", "habitat_map", "locator",
    "phylogeny", "cladogram", "taxonomy",
    "captive", "cage",
]

_BAD_TITLE_PATTERNS = re.compile(
    r"|".join(re.escape(k) for k in _BAD_TITLE_KEYWORDS), re.IGNORECASE
)

# Minimum dimensions — real photos are typically > 400px
_MIN_WIDTH  = 400
_MIN_HEIGHT = 300


def _is_bad_image(img: dict) -> bool:
    """Return True if the image looks like a drawing, skeleton, map, etc."""
    title = img.get("title", "")
    if _BAD_TITLE_PATTERNS.search(title):
        return True
    w = img.get("width", 0)
    h = img.get("height", 0)
    if w < _MIN_WIDTH or h < _MIN_HEIGHT:
        return True
    return False


def _is_good_photo(img: dict) -> bool:
    """Return True if image passes all quality filters."""
    return not _is_bad_image(img)


# ── Layer 2: Wikimedia Commons category-based fetching ──────────────────────

def _commons_category_images(scientific_name: str, count: int = 10) -> list[dict]:
    """Fetch images from the curated Commons category for a species.
    Categories like 'Category:Passer domesticus' contain hand-curated photos."""
    url = "https://commons.wikimedia.org/w/api.php"
    # Try the scientific name as a category (most species have one)
    cat_title = scientific_name.replace(" ", "_")
    params = {
        "action": "query",
        "format": "json",
        "generator": "categorymembers",
        "gcmtitle": f"Category:{cat_title}",
        "gcmtype": "file",
        "gcmlimit": count * 4,  # Get more to filter from
        "prop": "imageinfo",
        "iiprop": "url|mime|size",
        "iiurlwidth": 1200,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        if not pages:
            return []
        results = []
        for page in pages.values():
            ii = page.get("imageinfo", [{}])[0]
            mime = ii.get("mime", "")
            if mime not in ("image/jpeg", "image/png", "image/webp"):
                continue
            url_val = ii.get("url") or ii.get("thumburl")
            title = page.get("title", "")
            if url_val:
                results.append({
                    "title": title,
                    "url": url_val,
                    "width": ii.get("width", 0),
                    "height": ii.get("height", 0),
                })
        
        # Score images by quality indicators
        def _score_category_image(img: dict) -> float:
            """Higher score = better for quiz. Range 0-100."""
            score = 50.0
            title_lower = img["title"].lower()
            w, h = img["width"], img["height"]
            
            # +30: Bird name or scientific name in title
            sci_words = scientific_name.lower().split()
            if any(word in title_lower for word in sci_words):
                score += 30
            
            # -20: Generic camera filenames (DSC, IMG, DSCN, etc.)
            if re.search(r'\b(dsc|img|dscn|_mg_|p\d{7})\b', title_lower):
                score -= 20
            
            # +10: Aspect ratio close to 4:3 or 3:2 (good for quiz)
            if w and h:
                aspect = w / h
                if 1.2 <= aspect <= 1.8:  # Between 5:4 and 16:9
                    score += 10
                elif aspect < 1.0 or aspect > 2.5:  # Too tall or too wide
                    score -= 10
            
            # +5: Larger resolution (but not too much weight)
            if w and h:
                megapixels = (w * h) / 1_000_000
                score += min(megapixels * 2, 15)  # Cap at +15
            
            return score
        
        # Sort by score descending
        results.sort(key=_score_category_image, reverse=True)
        
        # Diversify selection: avoid picking images with similar names (same photo session)
        selected = []
        used_patterns = set()
        
        for img in results:
            if len(selected) >= count:
                break
            
            # Extract base pattern from filename (without sequential numbers at the end)
            title = img["title"].lower()
            # Remove "file:" prefix and extension
            basename = re.sub(r'file:', '', title)
            basename = re.sub(r'\.(jpg|jpeg|png|webp)$', '', basename)
            # Remove trailing numbers like "_01", "_02", " 01", " 1", etc.
            base_pattern = re.sub(r'[\s_-]*\d+$', '', basename)
            
            # Skip if this looks like it's from the same photo series
            if base_pattern in used_patterns:
                continue
            
            selected.append(img)
            used_patterns.add(base_pattern)
        
        # If we couldn't get enough diverse images, fill with remaining ones
        if len(selected) < count:
            for img in results:
                if img not in selected:
                    selected.append(img)
                    if len(selected) >= count:
                        break
        
        return selected
    except Exception as e:
        print(f"    [Commons category error] {e}")
        return []


# ── Image fetching strategies (combined) ─────────────────────────────────────

def _dedup_add(results: list[dict], more: list[dict]) -> list[dict]:
    """Append images from 'more' that aren't already in 'results' (by URL)."""
    seen = {r["url"] for r in results}
    for img in more:
        if img["url"] not in seen:
            results.append(img)
            seen.add(img["url"])
    return results


def fetch_regular_images(bird: dict, count: int = 3) -> list[dict]:
    """Try multiple strategies to get good regular (perched/standing) bird photos."""
    sci = bird["scientific"]
    en  = bird["en"]
    results = []

    # Strategy 1 (Layer 2): Commons category — curated, best quality
    cat_imgs = _commons_category_images(sci, count=count*3)
    filtered = [r for r in cat_imgs if _is_good_photo(r)]
    for img in filtered:
        img["_source"] = "Commons category"
    results = filtered
    if results:
        print(f"    [Strategy 1: Commons category → {len(results)} images]")

    # Strategy 2: Wikipedia article images
    if len(results) < count:
        wiki_imgs = _get_wiki_page_images(sci, count=count*2)
        filtered = [r for r in wiki_imgs if _is_good_photo(r)]
        for img in filtered:
            img["_source"] = "Wikipedia article"
        old_len = len(results)
        results = _dedup_add(results, filtered)
        if len(results) > old_len:
            print(f"    [Strategy 2: Wikipedia article → +{len(results) - old_len} images]")

    # Strategy 3: Commons direct search by scientific name
    if len(results) < count:
        more = _commons_search(sci, count=count*2)
        filtered = [r for r in more if _is_good_photo(r)]
        for img in filtered:
            img["_source"] = f"Commons search: {sci}"
        old_len = len(results)
        results = _dedup_add(results, filtered)
        if len(results) > old_len:
            print(f"    [Strategy 3: Commons search '{sci}' → +{len(results) - old_len} images]")

    # Strategy 4: Commons search by English name
    if len(results) < count:
        more = _commons_search(f"{en} bird photo", count=count*2)
        filtered = [r for r in more if _is_good_photo(r)]
        for img in filtered:
            img["_source"] = f"Commons search: {en} bird photo"
        old_len = len(results)
        results = _dedup_add(results, filtered)
        if len(results) > old_len:
            print(f"    [Strategy 4: Commons search '{en} bird photo' → +{len(results) - old_len} images]")

    return results[:count]


# ── Image download & save ────────────────────────────────────────────────────

def download_image(url: str, save_path: Path) -> bool:
    max_retries = 3
    for attempt in range(max_retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 429:
                wait = 15 * (attempt + 1)
                print(f"    Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            if r.status_code != 200:
                print(f"    HTTP {r.status_code} for {url}")
                return False
            img = Image.open(BytesIO(r.content))
            if img.mode in ("RGBA", "P", "L"):
                img = img.convert("RGB")
            # Resize if very large (keep aspect ratio, max 1600px wide)
            if img.width > 1600:
                ratio = 1600 / img.width
                img = img.resize((1600, int(img.height * ratio)), Image.LANCZOS)
            img.save(save_path, "JPEG", quality=85, optimize=True)
            return True
        except Exception as e:
            print(f"    Download error (attempt {attempt+1}): {e}")
            time.sleep(2)
    return False


# ── Wikipedia description fetching ──────────────────────────────────────────

def _wiki_extract(search_term: str, lang: str = "en", sentences: int = 2) -> str | None:
    url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": search_term,
        "exintro": 1,
        "exsentences": sentences,
        "explaintext": 1,
        "redirects": 1,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if pid == "-1":
                continue
            extract = page.get("extract", "").strip()
            if extract and len(extract) > 30:
                # Clean up
                extract = re.sub(r"\s*\([^)]{1,60}\)", "", extract)
                extract = re.sub(r"\s+", " ", extract).strip()
                # Keep only first 2 sentences
                sentences_list = re.split(r'(?<=[.!?])\s+', extract)
                return " ".join(sentences_list[:sentences]).strip()
    except Exception as e:
        print(f"    [Wiki extract error {lang}] {e}")
    return None


def fetch_descriptions(bird: dict) -> dict:
    sci  = bird["scientific"]
    he   = bird["he"]
    es   = bird["es"]
    desc = {}
    en_desc = _wiki_extract(sci, "en", 2)
    if en_desc:
        desc["en"] = en_desc
    time.sleep(0.3)
    he_desc = _wiki_extract(he, "he", 2)
    if he_desc:
        desc["he"] = he_desc
    time.sleep(0.3)
    es_desc = _wiki_extract(es, "es", 2)
    if es_desc:
        desc["es"] = es_desc
    time.sleep(0.3)
    fr_desc = _wiki_extract(bird["fr"], "fr", 2)
    if fr_desc:
        desc["fr"] = fr_desc
    time.sleep(0.3)
    return desc


def fetch_habitat(scientific_name: str) -> str | None:
    """Try to extract habitat info from Wikipedia intro."""
    text = _wiki_extract(scientific_name, "en", 4)
    if not text:
        return None
    # Look for habitat keywords
    for kw in ("found in", "lives in", "inhabits", "habitat", "native to",
                "distributed", "range", "breeds in", "occurs in"):
        idx = text.lower().find(kw)
        if idx != -1:
            snippet = text[idx:idx + 120].split(".")[0]
            return snippet.strip().capitalize()
    return None


# ── Main per-bird processor ──────────────────────────────────────────────────

def process_bird(bird: dict, skip_done: bool = False, force: bool = False, image_count: int = 3) -> bool:
    slug      = bird["name"]
    en        = bird["en"]
    bird_dir  = BIRDS_DIR / slug
    bird_dir.mkdir(parents=True, exist_ok=True)

    img_names = [f"{slug}_{i+1}.jpg" for i in range(image_count)]

    img_paths = [bird_dir / n for n in img_names]

    # Load existing info
    info = load_info()

    already_done = (
        all(p.exists() for p in img_paths) and
        slug in info and
        info[slug].get("description", {}).get("en")
    )
    if skip_done and already_done and not force:
        print(f"  ✓ {en} — already complete, skipping")
        return True

    print(f"\n{'─'*55}")
    print(f"  🐦 {en} ({bird['scientific']})  [Difficulty {bird['difficulty']}]")

    # ── Download regular images ──
    saved_imgs = []
    # If force mode, re-download all images; otherwise only download missing
    missing_regular = list(range(image_count)) if force else [i for i, p in enumerate(img_paths) if not p.exists()]
    if missing_regular or not skip_done:
        print(f"  Fetching regular images…")
        candidates = fetch_regular_images(bird, count=image_count)
        for i, idx in enumerate(missing_regular):
            if i >= len(candidates):
                print(f"    ✗ Not enough images found (got {len(candidates)})")
                break
            img_info = candidates[i]
            url = img_info["url"]
            path = img_paths[idx]
            source = img_info.get("_source", "Unknown")
            title = img_info.get('title', 'untitled')
            print(f"    [{source}] {title[:70]}")
            print(f"      → {url[:100]}")
            ok = download_image(url, path)
            print(f"    {'✓' if ok else '✗'} {img_names[idx]}")
            if ok:
                saved_imgs.append(img_names[idx])
            time.sleep(1.0)
    else:
        print(f"  ✓ Regular images already present")
        saved_imgs = img_names[:]

    # ── Update birds_info.json ──
    entry = info.get(slug, {})
    if not entry.get("description", {}).get("en"):
        print(f"  Fetching descriptions…")
        desc = fetch_descriptions(bird)
        if desc:
            entry["description"] = {**entry.get("description", {}), **desc}
    if not entry.get("habitat"):
        hab = fetch_habitat(bird["scientific"])
        if hab:
            entry["habitat"] = hab

    all_imgs = [n for n in img_names if (bird_dir / n).exists()]
    entry.update({
        "name": slug,
        "names": {"en": bird["en"], "he": bird["he"], "es": bird["es"], "fr": bird["fr"]},
        "scientificName": bird["scientific"],
        "difficulty": bird["difficulty"],
        "category": bird["category"],
        "locations": bird["locations"],
        "images": all_imgs,
    })
    info[slug] = entry
    save_info(info)
    print(f"  ✓ birds_info.json updated")
    return True


# ── JSON helpers ─────────────────────────────────────────────────────────────

def load_info() -> dict:
    if INFO_FILE.exists():
        with open(INFO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_info(data: dict):
    with open(INFO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── CLI ───────────────────────────────────────────────────────────────────────

def find_bird(query: str) -> dict | None:
    q = query.lower().strip()
    for b in BIRDS_200:
        if b["name"] == q or b["en"].lower() == q:
            return b
    # Partial match
    for b in BIRDS_200:
        if q in b["name"] or q in b["en"].lower():
            return b
    return None


def main():
    parser = argparse.ArgumentParser(description="Fetch bird images and info")
    parser.add_argument("bird", nargs="?", help="Bird name or slug")
    parser.add_argument("--all", action="store_true", help="Process all 200 birds")
    parser.add_argument("--skip-done", action="store_true", help="Skip fully complete birds")
    parser.add_argument("--force", action="store_true", help="Re-download images even if they exist")
    parser.add_argument("--count", type=int, default=3, help="Number of images to download per bird (default: 3)")
    parser.add_argument("--level", type=int, help="Only process birds of given difficulty level")
    args = parser.parse_args()

    BIRDS_DIR.mkdir(parents=True, exist_ok=True)

    if args.all or args.level:
        birds = BIRDS_200
        if args.level:
            birds = [b for b in birds if b["difficulty"] == args.level]
        print(f"Processing {len(birds)} birds…")
        ok = fail = 0
        for bird in birds:
            try:
                if process_bird(bird, skip_done=args.skip_done, force=args.force, image_count=args.count):
                    ok += 1
                else:
                    fail += 1
            except KeyboardInterrupt:
                print("\n\nStopped by user.")
                break
            except Exception as e:
                print(f"  ERROR processing {bird['en']}: {e}")
                fail += 1
            time.sleep(2.0)
        print(f"\n{'='*40}")
        print(f"Done. Success: {ok}, Failed: {fail}")

    elif args.bird:
        bird = find_bird(args.bird)
        if not bird:
            print(f"Bird '{args.bird}' not found in BIRDS_200 list.")
            print("Tip: use the English name (e.g. 'House Sparrow') or slug (e.g. 'house_sparrow')")
            sys.exit(1)
        process_bird(bird, skip_done=args.skip_done, force=args.force, image_count=args.count)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
