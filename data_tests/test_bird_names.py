"""
test_bird_names.py
==================
Verifies bird names in birds_200.py against Wikipedia interlanguage links.

The scientific name is the universal key:
  scientific name → en.wikipedia → interlanguage links → he/es article titles

Usage:
  python tests/test_bird_names.py                   # Check all 200 birds
  python tests/test_bird_names.py --sample 10       # Random sample of 10
  python tests/test_bird_names.py --bird house_sparrow  # Check one bird by slug
  python tests/test_bird_names.py --lang he         # Check only Hebrew
  python tests/test_bird_names.py --lang es         # Check only Spanish
"""

import sys, os, time, argparse, random, io

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                  errors="replace", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8",
                                  errors="replace", line_buffering=True)

# Add parent dir so we can import birds_200
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from birds_200 import BIRDS_200

try:
    import requests
except ImportError:
    print("ERROR: pip install requests")
    sys.exit(1)

HEADERS = {
    "User-Agent": "BirdLingoBot/1.0 (educational bird quiz) python-requests"
}


def wiki_resolve(scientific_name: str) -> dict | None:
    """Look up scientific name on en.wikipedia and return page info."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query", "format": "json",
        "titles": scientific_name, "redirects": 1, "prop": "info",
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        pages = r.json().get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if pid != "-1" and "missing" not in page:
                return {"title": page["title"], "pageid": int(pid)}
    except Exception as e:
        print(f"    [resolve error] {e}")
    return None


def wiki_langlinks(title: str, langs: list[str]) -> dict:
    """Get interlanguage links from an English Wikipedia article."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query", "format": "json",
        "titles": title, "prop": "langlinks",
        "lllimit": 50, "redirects": 1,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        pages = r.json().get("query", {}).get("pages", {})
        result = {}
        for page in pages.values():
            for ll in page.get("langlinks", []):
                if ll["lang"] in langs:
                    result[ll["lang"]] = ll["*"]
        return result
    except Exception as e:
        print(f"    [langlinks error] {e}")
        return {}


def check_bird(bird: dict, langs: list[str]) -> dict:
    """
    Check one bird against Wikipedia.
    Returns {slug, status, mismatches: [{lang, ours, wiki}], missing_links: [lang]}
    """
    slug = bird["name"]
    sci = bird["scientific"]
    result = {"slug": slug, "en": bird["en"], "sci": sci,
              "status": "ok", "mismatches": [], "missing_links": []}

    page = wiki_resolve(sci)
    if not page:
        # Fallback: try English name
        page = wiki_resolve(bird["en"])
        if not page:
            result["status"] = "not_found"
            return result

    time.sleep(0.3)
    links = wiki_langlinks(page["title"], langs)
    time.sleep(0.3)

    lang_key_map = {"he": "he", "es": "es", "fr": "fr"}
    for lang in langs:
        key = lang_key_map.get(lang, lang)
        our_name = bird.get(key, "")
        wiki_name = links.get(lang)
        if wiki_name is None:
            result["missing_links"].append(lang)
        elif wiki_name != our_name:
            result["mismatches"].append({"lang": lang, "ours": our_name, "wiki": wiki_name})

    if result["mismatches"] or result["missing_links"]:
        result["status"] = "mismatch"
    return result


def main():
    parser = argparse.ArgumentParser(description="Verify birds_200.py names vs Wikipedia")
    parser.add_argument("--sample", type=int, default=0,
                        help="Check a random sample of N birds (0 = all)")
    parser.add_argument("--bird", type=str, default="",
                        help="Check one bird by slug (e.g. house_sparrow)")
    parser.add_argument("--lang", type=str, default="he,es",
                        help="Comma-separated langs to check (default: he,es)")
    args = parser.parse_args()

    langs = [l.strip() for l in args.lang.split(",")]
    birds = BIRDS_200

    if args.bird:
        birds = [b for b in birds if b["name"] == args.bird]
        if not birds:
            print(f"Bird '{args.bird}' not found in BIRDS_200")
            sys.exit(1)
    elif args.sample > 0:
        birds = random.sample(birds, min(args.sample, len(birds)))

    print(f"Checking {len(birds)} birds against Wikipedia  (langs: {', '.join(langs)})")
    print("=" * 70)

    ok = 0
    mismatches = []
    not_found = []

    for i, bird in enumerate(birds):
        label = f"[{i+1}/{len(birds)}] {bird['name']} ({bird['scientific']})"
        print(f"{label} ... ", end="", flush=True)

        result = check_bird(bird, langs)

        if result["status"] == "ok":
            print("✓")
            ok += 1
        elif result["status"] == "not_found":
            print("✗ NOT FOUND on Wikipedia")
            not_found.append(result)
        else:
            parts = []
            for m in result["mismatches"]:
                parts.append(f'{m["lang"]}: "{m["ours"]}" → "{m["wiki"]}"')
            for lang in result["missing_links"]:
                parts.append(f"{lang}: no wiki link")
            print("⚠  " + " | ".join(parts))
            mismatches.append(result)

        time.sleep(0.5)  # Be nice to Wikipedia

    # ── Summary ──
    print("\n" + "=" * 70)
    print(f"RESULTS:  {ok} OK  |  {len(mismatches)} mismatches  |  {len(not_found)} not found")
    print("=" * 70)

    if mismatches:
        print("\n── MISMATCHES ──")
        for r in mismatches:
            print(f"\n  {r['slug']}  ({r['sci']})")
            for m in r["mismatches"]:
                print(f"    {m['lang']}: ours=\"{m['ours']}\"  wiki=\"{m['wiki']}\"")
            for lang in r["missing_links"]:
                print(f"    {lang}: no interlanguage link on Wikipedia")

    if not_found:
        print("\n── NOT FOUND ──")
        for r in not_found:
            print(f"  {r['slug']}  ({r['sci']})")


if __name__ == "__main__":
    main()
