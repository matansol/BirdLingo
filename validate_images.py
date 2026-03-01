"""
validate_images.py
==================
Uses OpenAI CLIP to verify that each downloaded bird image is actually
a photograph of the correct bird species.

For every image, CLIP compares it against two text prompts:
  ✓ "a photograph of a {English name}"
  ✗ "a drawing, illustration, skeleton, or map"

Images that score higher on the negative prompt (or below a confidence
threshold on the positive prompt) are flagged for replacement.

Usage:
  python validate_images.py                     # validate all birds
  python validate_images.py house_sparrow       # validate one bird
  python validate_images.py --level 1           # validate difficulty-1 birds
  python validate_images.py --threshold 0.6     # custom confidence threshold
  python validate_images.py --delete            # auto-delete bad images
  python validate_images.py --report            # save JSON report only

Requires:  pip install torch torchvision open-clip-torch pillow
"""

import sys, json, argparse, time
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "BirdLingo" / "assets"
BIRDS_DIR  = ASSETS_DIR / "birds"
REPORT_FILE = BASE_DIR / "image_validation_report.json"

# ── Lazy-load CLIP (heavy imports) ──────────────────────────────────────────
_model = None
_preprocess = None
_tokenize = None
_device = None

def _load_clip():
    """Load CLIP model once on first use."""
    global _model, _preprocess, _tokenize, _device
    if _model is not None:
        return

    print("Loading CLIP model (first time may download ~350MB)…")
    t0 = time.time()

    import torch
    import open_clip

    _device = "cuda" if torch.cuda.is_available() else "cpu"

    # ViT-B/32 is small, fast, and good enough for photo-vs-drawing detection
    _model, _, _preprocess = open_clip.create_model_and_transforms(
        "ViT-B-32", pretrained="laion2b_s34b_b79k"
    )
    _model = _model.to(_device).eval()
    _tokenize = open_clip.get_tokenizer("ViT-B-32")

    dt = time.time() - t0
    print(f"  CLIP loaded on {_device} in {dt:.1f}s\n")


def score_image(image_path: Path, bird_english_name: str) -> dict:
    """Score a single image: is it a photo of the named bird?

    Returns dict with:
      - photo_score:   probability it's a photo of this bird (0.0–1.0)
      - bad_score:     probability it's a drawing/skeleton/map (0.0–1.0)
      - verdict:       "good" | "bad" | "uncertain"
    """
    import torch
    from PIL import Image

    _load_clip()

    try:
        img = Image.open(image_path).convert("RGB")
    except Exception as e:
        return {"photo_score": 0.0, "bad_score": 1.0, "verdict": "bad", "error": str(e)}

    img_tensor = _preprocess(img).unsqueeze(0).to(_device)

    # Positive and negative text prompts
    texts = [
        f"a photograph of a {bird_english_name}",
        "a drawing, illustration, painting, sketch, or engraving of a bird",
        "a skeleton, skull, fossil, or taxidermy specimen",
        "a map, chart, diagram, stamp, or logo",
    ]
    text_tokens = _tokenize(texts).to(_device)

    with torch.no_grad():
        img_features = _model.encode_image(img_tensor)
        txt_features = _model.encode_text(text_tokens)

        # Normalize
        img_features = img_features / img_features.norm(dim=-1, keepdim=True)
        txt_features = txt_features / txt_features.norm(dim=-1, keepdim=True)

        # Cosine similarity → softmax probabilities
        similarity = (img_features @ txt_features.T).squeeze(0) * 100.0
        probs = similarity.softmax(dim=-1).cpu().numpy()

    photo_score = float(probs[0])
    bad_score   = float(probs[1] + probs[2] + probs[3])

    if photo_score >= 0.5:
        verdict = "good"
    elif photo_score >= 0.3:
        verdict = "uncertain"
    else:
        verdict = "bad"

    return {
        "photo_score": round(photo_score, 4),
        "bad_score": round(bad_score, 4),
        "verdict": verdict,
    }


def validate_bird(bird: dict, threshold: float = 0.5, delete: bool = False) -> dict:
    """Validate all images for a single bird. Returns summary dict."""
    slug = bird["name"]
    en   = bird["en"]
    bird_dir = BIRDS_DIR / slug

    if not bird_dir.exists():
        return {"slug": slug, "en": en, "status": "no_dir", "images": []}

    # Find all jpg images in the bird's directory
    image_files = sorted(bird_dir.glob("*.jpg"))
    if not image_files:
        return {"slug": slug, "en": en, "status": "no_images", "images": []}

    results = []
    good = bad = uncertain = 0

    for img_path in image_files:
        score = score_image(img_path, en)
        score["file"] = img_path.name

        if score["verdict"] == "good":
            good += 1
            icon = "✓"
        elif score["verdict"] == "uncertain":
            uncertain += 1
            icon = "?"
        else:
            bad += 1
            icon = "✗"

        print(f"    {icon} {img_path.name:30s}  photo={score['photo_score']:.2f}  bad={score['bad_score']:.2f}  → {score['verdict']}")

        if delete and score["verdict"] == "bad":
            img_path.unlink()
            print(f"      🗑  DELETED {img_path.name}")
            score["deleted"] = True

        results.append(score)

    status = "ok" if bad == 0 else "has_bad"
    return {
        "slug": slug,
        "en": en,
        "status": status,
        "good": good,
        "bad": bad,
        "uncertain": uncertain,
        "images": results,
    }


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    from birds_200 import BIRDS_200

    parser = argparse.ArgumentParser(
        description="Validate bird images using CLIP (is this a photo of the bird?)"
    )
    parser.add_argument("bird", nargs="?", help="Bird slug to validate")
    parser.add_argument("--level", type=int, help="Only validate birds of given difficulty level")
    parser.add_argument("--threshold", type=float, default=0.5,
                        help="Minimum photo_score to consider 'good' (default: 0.5)")
    parser.add_argument("--delete", action="store_true",
                        help="Auto-delete images classified as 'bad'")
    parser.add_argument("--report", action="store_true",
                        help="Save detailed JSON report to image_validation_report.json")
    args = parser.parse_args()

    if args.bird:
        # Single bird
        bird = None
        for b in BIRDS_200:
            if b["name"] == args.bird.lower().strip() or b["en"].lower() == args.bird.lower().strip():
                bird = b
                break
        if not bird:
            print(f"Bird '{args.bird}' not found.")
            sys.exit(1)
        birds = [bird]
    elif args.level:
        birds = [b for b in BIRDS_200 if b["difficulty"] == args.level]
    else:
        birds = BIRDS_200

    print(f"Validating {len(birds)} bird(s) with CLIP…\n")

    all_results = []
    total_good = total_bad = total_uncertain = total_images = 0

    for i, bird in enumerate(birds):
        print(f"[{i+1}/{len(birds)}] {bird['en']} ({bird['scientific']})")
        result = validate_bird(bird, threshold=args.threshold, delete=args.delete)
        all_results.append(result)

        total_good += result.get("good", 0)
        total_bad += result.get("bad", 0)
        total_uncertain += result.get("uncertain", 0)
        total_images += result.get("good", 0) + result.get("bad", 0) + result.get("uncertain", 0)

    # ── Summary ──
    print(f"\n{'='*55}")
    print(f"VALIDATION SUMMARY")
    print(f"{'='*55}")
    print(f"  Birds checked:     {len(birds)}")
    print(f"  Total images:      {total_images}")
    print(f"  ✓ Good:            {total_good}")
    print(f"  ? Uncertain:       {total_uncertain}")
    print(f"  ✗ Bad:             {total_bad}")
    if total_images > 0:
        print(f"  Bad rate:          {total_bad/total_images*100:.1f}%")

    # List all bad images
    bad_list = []
    for r in all_results:
        for img in r.get("images", []):
            if img["verdict"] == "bad":
                bad_list.append(f"  {r['slug']}/{img['file']}  (photo={img['photo_score']:.2f})")
    if bad_list:
        print(f"\n{'─'*55}")
        print(f"BAD IMAGES ({len(bad_list)}):")
        for b in bad_list:
            print(b)

    # Save report
    if args.report or len(birds) > 1:
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "total_birds": len(birds),
                "total_images": total_images,
                "good": total_good,
                "bad": total_bad,
                "uncertain": total_uncertain,
                "birds": all_results,
            }, f, ensure_ascii=False, indent=2)
        print(f"\nReport saved to {REPORT_FILE}")


if __name__ == "__main__":
    main()
