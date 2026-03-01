"""
fix_bird_names.py
=================
Checks ALL names in birds_200.py against Wikipedia interlanguage links,
produces a corrections JSON file, and can apply fixes back to birds_200.py.

The scientific name is the universal, unambiguous key:
  scientific name → en.wikipedia → interlanguage links → he/es/fr titles

Special handling:
- Spanish Wikipedia often uses the scientific name as the article title.
  In that case we extract the common Spanish name from the article's first
  sentence (e.g. "El gorrión común (Passer domesticus) es un ave...").
- Same logic for French.
- If Wikipedia has no interlanguage link for a language, we keep our name.

Usage:
  python fix_bird_names.py                        # Check all, save report
  python fix_bird_names.py --sample 10            # Random sample of 10
  python fix_bird_names.py --bird waxwing         # Check one bird
  python fix_bird_names.py --apply                # Apply corrections to birds_200.py
  python fix_bird_names.py --apply --dry-run      # Show what would change, don't write
"""

import json, sys, os, time, re, argparse, random, io
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                  errors="replace", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8",
                                  errors="replace", line_buffering=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from birds_200 import BIRDS_200

try:
    import requests
except ImportError:
    print("ERROR: pip install requests")
    sys.exit(1)

# ── Config ───────────────────────────────────────────────────────────────────
HEADERS = {
    "User-Agent": "BirdLingoBot/1.0 (educational bird quiz) python-requests"
}
BIRDS_200_PATH = Path(__file__).parent / "birds_200.py"
CORRECTIONS_PATH = Path(__file__).parent / "name_corrections.json"
LANGS = ["he", "es", "fr"]


# ── Wikipedia API helpers ────────────────────────────────────────────────────

def wiki_resolve(title: str) -> dict | None:
    """Look up a title on en.wikipedia, follow redirects. Returns {title, pageid}."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query", "format": "json",
        "titles": title, "redirects": 1, "prop": "info",
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
    """Get interlanguage links {lang: localized_title} from en.wikipedia."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query", "format": "json",
        "titles": title, "prop": "langlinks",
        "lllimit": 100, "redirects": 1,
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


def wiki_extract_common_name(title: str, lang: str) -> str | None:
    """
    When a Wikipedia article title is the scientific name (e.g. "Bombycilla garrulus"),
    try to extract the local common name from the article's opening sentence.

    Patterns handled:
      es: "El gorrión común (Passer domesticus) es un ave..."
          → "gorrión común"
      es: "La golondrina común o ... (Hirundo rustica)..."
          → "golondrina común"
      fr: "Le Moineau domestique (Passer domesticus) est un oiseau..."
          → "Moineau domestique"
    """
    url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query", "format": "json",
        "titles": title, "prop": "extracts",
        "exintro": 1, "exsentences": 1, "explaintext": 1, "redirects": 1,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        pages = r.json().get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if pid == "-1":
                continue
            text = page.get("extract", "").strip()
            if not text:
                return None

            # Try to extract common name before the parenthetical scientific name
            # Pattern: "El/La/Le/Les/L' <common name> (<scientific name>)..."
            # Also: "<Common name> (<scientific name>)..."
            patterns = [
                # Spanish: "El gorrión común (Passer domesticus)..."
                r"^(?:El|La|Los|Las)\s+(.+?)\s*\(",
                # French: "Le Moineau domestique (Passer domesticus)..."
                r"^(?:Le|La|Les|L['']\s*)(.+?)\s*\(",
                # Generic: starts directly with name "(Scientific name)..."
                r"^(.+?)\s*\(",
            ]
            for pat in patterns:
                m = re.match(pat, text, re.IGNORECASE)
                if m:
                    name = m.group(1).strip().rstrip(",")
                    # Skip if the extracted "name" is just the scientific name again
                    if name.lower() == title.lower():
                        continue
                    # Skip if too long (probably grabbed a whole sentence)
                    if len(name) > 60:
                        continue
                    # Skip if it contains verbs/articles only
                    if len(name.split()) < 1:
                        continue
                    # Strip leading article for French/Spanish
                    name = re.sub(r"^(?:El|La|Los|Las|Le|La|Les|L['']\s*)\s+",
                                  "", name).strip()
                    # Take first alternative if "X o Y" or "X ou Y"
                    name = re.split(r'\s+(?:o|ou)\s+', name)[0].strip()
                    # Cut off trailing clauses: "también conocida como ..."
                    name = re.split(r'\s+(?:también|aussi|también conocid[ao])', name)[0].strip()
                    # Strip zero-width unicode
                    name = strip_unicode_junk(name)
                    # If still too long (>40 chars), probably grabbed junk
                    if len(name) > 40:
                        continue
                    # Capitalize first letter for display
                    if lang == "es":
                        name = name[0].upper() + name[1:] if name else name
                    elif lang == "fr":
                        name = name[0].upper() + name[1:] if name else name
                    return name
    except Exception as e:
        print(f"    [extract error {lang}] {e}")
    return None


def strip_unicode_junk(s: str) -> str:
    """Remove zero-width spaces, soft hyphens, and other invisible unicode."""
    return re.sub(r'[\u200b\u200c\u200d\u200e\u200f\ufeff\u00ad]', '', s).strip()


def looks_like_scientific_name(name: str) -> bool:
    """Check if a name looks like a Latin binomial (e.g. 'Bombycilla garrulus')
    or a genus-only name (e.g. 'Acanthis')."""
    name = strip_unicode_junk(name)
    # Genus-only (single capitalized Latin word)
    if re.match(r'^[A-Z][a-z]+$', name):
        return True
    # Also catch "Genus (genre)" pattern
    if re.match(r'^[A-Z][a-z]+\s*\(', name):
        return True
    parts = name.split()
    if len(parts) < 2:
        return False
    # Genus is capitalized, species is lowercase, both Latin-ish
    return (parts[0][0].isupper() and parts[1][0].islower()
            and all(c.isalpha() or c == '-' for c in name.replace(" ", "")))


# ── Main check logic ────────────────────────────────────────────────────────

def check_bird(bird: dict) -> dict:
    """
    Check one bird's names against Wikipedia.
    Returns a result dict with corrections if any.
    """
    slug = bird["name"]
    sci = bird["scientific"]
    en = bird["en"]

    result = {
        "slug": slug,
        "en": en,
        "scientific": sci,
        "corrections": {},   # {lang: {"old": ..., "new": ..., "source": ...}}
        "missing_wiki": [],  # langs with no Wikipedia interlanguage link
        "status": "ok",
        "en_wiki_title": "",
    }

    # Step 1: Resolve scientific name → English Wikipedia article
    page = wiki_resolve(sci)
    if not page:
        page = wiki_resolve(en)
        if not page:
            page = wiki_resolve(f"{en} (bird)")
    if not page:
        result["status"] = "not_found"
        return result

    result["en_wiki_title"] = page["title"]
    time.sleep(0.3)

    # Step 2: Check English name against Wikipedia article title
    en_wiki = strip_unicode_junk(page["title"])
    # Wikipedia titles may have disambiguation suffixes like " (bird)"
    en_wiki_clean = re.sub(r"\s*\(.*?\)\s*$", "", en_wiki).strip()
    if en_wiki_clean.lower() == en.lower():
        # Case-only difference (e.g. "Dalmatian pelican" vs "Dalmatian Pelican")
        # We keep our Title Case — standard in bird nomenclature
        pass
    elif en_wiki_clean != en:
        # Real word difference — use Wikipedia's name but in proper Title Case
        # Bird nomenclature: each significant word capitalized
        corrected = en_wiki_clean.title()
        # Fix common title() issues: 'S → 'S, -T → -t
        corrected = re.sub(r"(?<=')([A-Z])", lambda m: m.group(1).lower(), corrected)
        result["corrections"]["en"] = {
            "old": en,
            "new": corrected,
            "source": f"en.wikipedia article title for {sci}",
        }

    # Step 3: Get interlanguage links
    links = wiki_langlinks(page["title"], LANGS)
    time.sleep(0.3)

    # Step 4: Compare each non-English language
    for lang in LANGS:
        our_name = bird.get(lang, "")
        wiki_title = links.get(lang)

        if wiki_title is None:
            result["missing_wiki"].append(lang)
            continue

        # Strip invisible unicode from wiki title
        wiki_title = strip_unicode_junk(wiki_title)

        # Direct match — great!
        if wiki_title == our_name:
            continue

        # For Hebrew: Wikipedia title IS the common name
        if lang == "he":
            result["corrections"][lang] = {
                "old": our_name,
                "new": wiki_title,
                "source": "interlanguage link",
            }
            continue

        # For Spanish/French: wiki title might have article prefix "Le ", "El ", etc.
        # Strip those for comparison and for the correction
        clean_wiki = re.sub(r"^(?:El|La|Los|Las|Le|La|Les|L['']\s*)\s+", "", wiki_title).strip()
        clean_wiki = strip_unicode_junk(clean_wiki)
        if clean_wiki == our_name:
            continue

        # For Spanish/French: article title might be the scientific name
        # In that case, try to extract the common name from the article intro
        if looks_like_scientific_name(wiki_title) or looks_like_scientific_name(clean_wiki):
            common = wiki_extract_common_name(wiki_title, lang)
            time.sleep(0.3)
            if common:
                if common != our_name:
                    result["corrections"][lang] = {
                        "old": our_name,
                        "new": common,
                        "source": f"extracted from {lang}.wikipedia intro",
                        "wiki_title": wiki_title,
                    }
                # else: our name matches the extracted common name — OK!
            else:
                # Couldn't extract a common name; wiki uses scientific name.
                # Our common name is probably fine — just note it.
                result["corrections"][lang] = {
                    "old": our_name,
                    "new": wiki_title,
                    "source": "interlanguage link (scientific name as title)",
                    "note": "wiki uses scientific name; our common name may be fine",
                    "confidence": "low",
                }
        else:
            # Wiki title is a proper common name and it differs from ours
            # Use cleaned version (without article prefix)
            best_name = clean_wiki if clean_wiki != wiki_title else wiki_title
            result["corrections"][lang] = {
                "old": our_name,
                "new": best_name,
                "source": "interlanguage link",
            }

    if result["corrections"] or result["missing_wiki"]:
        result["status"] = "needs_correction"
    return result


# ── Apply corrections to birds_200.py ────────────────────────────────────────

def apply_corrections(corrections: list[dict], dry_run: bool = False) -> int:
    """
    Read birds_200.py, find each bird's _b() line, and replace old names
    with corrected ones. Only applies high-confidence corrections.
    Returns number of changes applied.
    """
    source = BIRDS_200_PATH.read_text(encoding="utf-8")
    changes = 0

    for entry in corrections:
        slug = entry["slug"]
        for lang, fix in entry["corrections"].items():
            # Skip low-confidence corrections (scientific-name-as-title with no extracted common)
            if fix.get("confidence") == "low":
                continue

            old_name = fix["old"]
            new_name = fix["new"]

            # Find the _b("slug",...) line and replace the old name
            # We search for the exact old string in the context of this slug's line
            # The _b() call has: slug, en, he, es, fr, sci, ...
            # We need to replace the specific language field

            # Escape for regex
            old_escaped = re.escape(old_name)

            # Pattern: find a _b( line containing this slug and the old name
            # We replace old_name with new_name only on lines containing the slug
            pattern = re.compile(
                r'(^_b\("' + re.escape(slug) + r'".*?)' + old_escaped + r'(.*$)',
                re.MULTILINE
            )

            new_source = pattern.sub(r'\g<1>' + new_name.replace('\\', '\\\\') + r'\2', source, count=1)
            if new_source != source:
                changes += 1
                if dry_run:
                    print(f"  WOULD FIX: {slug} [{lang}] \"{old_name}\" → \"{new_name}\"")
                else:
                    print(f"  FIXED: {slug} [{lang}] \"{old_name}\" → \"{new_name}\"")
                source = new_source
            else:
                print(f"  SKIP (not found in source): {slug} [{lang}] \"{old_name}\"")

    if not dry_run and changes > 0:
        BIRDS_200_PATH.write_text(source, encoding="utf-8")
        print(f"\n✓ Wrote {changes} corrections to {BIRDS_200_PATH}")

    return changes


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Check & fix bird names in birds_200.py against Wikipedia")
    parser.add_argument("--sample", type=int, default=0,
                        help="Check random sample of N birds")
    parser.add_argument("--bird", type=str, default="",
                        help="Check one bird by slug")
    parser.add_argument("--apply", action="store_true",
                        help="Apply corrections to birds_200.py")
    parser.add_argument("--dry-run", action="store_true",
                        help="With --apply: show changes but don't write")
    parser.add_argument("--lang", type=str, default="",
                        help="Override langs to check (comma-separated)")
    args = parser.parse_args()

    global LANGS
    if args.lang:
        LANGS = [l.strip() for l in args.lang.split(",")]

    birds = BIRDS_200

    if args.bird:
        birds = [b for b in birds if b["name"] == args.bird]
        if not birds:
            print(f"Bird '{args.bird}' not found in BIRDS_200")
            sys.exit(1)
    elif args.sample > 0:
        birds = random.sample(birds, min(args.sample, len(birds)))

    # ── If --apply with existing corrections file, apply and exit ──
    if args.apply and CORRECTIONS_PATH.exists() and not args.bird and not args.sample:
        print(f"Applying corrections from {CORRECTIONS_PATH}")
        with open(CORRECTIONS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        count = apply_corrections(data["corrections"], dry_run=args.dry_run)
        print(f"\n{'Would apply' if args.dry_run else 'Applied'} {count} corrections.")
        return

    # ── Check birds ──
    print(f"Checking {len(birds)} birds against Wikipedia  (langs: {', '.join(LANGS)})")
    print("=" * 72)

    all_results = []
    corrections = []
    not_found = []
    ok_count = 0

    for i, bird in enumerate(birds):
        label = f"[{i+1}/{len(birds)}] {bird['name']} ({bird['scientific']})"
        print(f"{label} ... ", end="", flush=True)

        result = check_bird(bird)
        all_results.append(result)

        if result["status"] == "ok":
            print("✓")
            ok_count += 1
        elif result["status"] == "not_found":
            print("✗ NOT FOUND")
            not_found.append(result)
        else:
            parts = []
            for lang, fix in result["corrections"].items():
                conf = fix.get("confidence", "high")
                marker = "?" if conf == "low" else "→"
                parts.append(f'{lang}: "{fix["old"]}" {marker} "{fix["new"]}"')
            for lang in result["missing_wiki"]:
                parts.append(f"{lang}: no wiki link")
            print("⚠  " + " | ".join(parts))
            if result["corrections"]:
                corrections.append(result)

        time.sleep(0.5)

    # ── Summary ──
    high_conf = sum(
        1 for c in corrections
        for fix in c["corrections"].values()
        if fix.get("confidence", "high") == "high"
    )
    low_conf = sum(
        1 for c in corrections
        for fix in c["corrections"].values()
        if fix.get("confidence") == "low"
    )

    print(f"\n{'=' * 72}")
    print(f"SUMMARY")
    print(f"{'=' * 72}")
    print(f"  Checked:              {len(birds)} birds")
    print(f"  OK (no changes):      {ok_count}")
    print(f"  Need correction:      {len(corrections)} birds")
    print(f"    High confidence:    {high_conf} name fixes")
    print(f"    Low confidence:     {low_conf} (wiki uses scientific name, ours may be fine)")
    print(f"  Not found on Wiki:    {len(not_found)}")
    print(f"  Missing wiki links:   {sum(len(r['missing_wiki']) for r in all_results)}")

    # ── Detailed corrections ──
    if corrections:
        print(f"\n{'─' * 72}")
        print("HIGH-CONFIDENCE CORRECTIONS (will be applied with --apply):")
        print(f"{'─' * 72}")
        for c in corrections:
            for lang, fix in c["corrections"].items():
                if fix.get("confidence") == "low":
                    continue
                print(f"  {c['slug']:30s} [{lang}]  \"{fix['old']}\"  →  \"{fix['new']}\"")
                if fix.get("wiki_title"):
                    print(f"  {'':30s}        (wiki title: {fix['wiki_title']})")

        low_entries = [(c, lang, fix) for c in corrections
                       for lang, fix in c["corrections"].items()
                       if fix.get("confidence") == "low"]
        if low_entries:
            print(f"\n{'─' * 72}")
            print("LOW-CONFIDENCE (wiki uses scientific name — review manually):")
            print(f"{'─' * 72}")
            for c, lang, fix in low_entries:
                print(f"  {c['slug']:30s} [{lang}]  ours: \"{fix['old']}\"  wiki: \"{fix['new']}\"")

    # ── Save corrections file ──
    output = {
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_checked": len(birds),
        "total_ok": ok_count,
        "total_corrections": len(corrections),
        "high_confidence_fixes": high_conf,
        "low_confidence_fixes": low_conf,
        "corrections": corrections,
        "not_found": not_found,
    }
    with open(CORRECTIONS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Corrections saved to: {CORRECTIONS_PATH}")
    print(f"  Run 'python fix_bird_names.py --apply --dry-run' to preview changes")
    print(f"  Run 'python fix_bird_names.py --apply' to apply to birds_200.py")


if __name__ == "__main__":
    main()
