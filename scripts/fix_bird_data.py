"""
fix_bird_data.py
================
Fixes BirdLingo/assets/birds_data.json by:
1. Using each bird's scientific name to find the CORRECT English Wikipedia article
2. Following Wikipedia's INTERLANGUAGE LINKS to get proper Hebrew & Spanish names
3. Fetching correct descriptions from each language's Wikipedia article
4. Flagging and replacing garbage descriptions (disambiguation, wrong topic)
5. Validating locations

Strategy: Scientific names are unambiguous. "Passer domesticus" always resolves
to the House Sparrow article, which links to "דרור הבית" (Hebrew) and
"Passer domesticus" (Spanish). This avoids the disambiguation trap that caused
"חנקן" (Shrike) → Nitrogen, "קרנף" (Hornbill) → Rhinoceros, etc.

Usage:
  python fix_bird_data.py                  # Dry-run: report issues only
  python fix_bird_data.py --fix            # Fix all issues and write output
  python fix_bird_data.py --fix --bird 42  # Fix only bird_042
  python fix_bird_data.py --report         # Generate detailed report
"""

import json, re, sys, time, argparse, io
from pathlib import Path

# Fix Windows console encoding for Hebrew/Spanish output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True)

try:
    import requests
except ImportError:
    print("ERROR: 'requests' not installed. Run: pip install requests")
    sys.exit(1)

try:
    from birds_200 import BIRDS_200
    _BIRDS_BY_SCI = {b["scientific"]: b for b in BIRDS_200}
except ImportError:
    print("WARNING: birds_200.py not found – location sync from catalog disabled")
    _BIRDS_BY_SCI = {}

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
APP_DATA   = BASE_DIR / "BirdLingo" / "assets" / "birds_data.json"
OUTPUT     = BASE_DIR / "BirdLingo" / "assets" / "birds_data_fixed.json"
REPORT     = BASE_DIR / "data_fix_report.txt"

HEADERS = {
    "User-Agent": "BirdLingoBot/1.0 (educational bird quiz app) python-requests"
}

# ── Garbage detection patterns ───────────────────────────────────────────────
HE_GARBAGE = [
    "האם התכוונתם ל",     # "Did you mean..." (disambiguation)
    "פירושונים",           # "Disambiguations"
    "הפניה ל",             # "Redirect to"
]

ES_GARBAGE = [
    "puede referirse a",
    "puede hacer referencia",
    "puede designar",
    "término puede referirse",
    "se puede referir",
]

EN_GARBAGE = [
    "may refer to",
    "can refer to",
    "disambiguation",
]

# Known wrong-topic indicators (description clearly not about a bird)
WRONG_TOPIC_HE = [
    "יסוד כימי",       # chemical element
    "משקה",             # drink (cocktail)
    "מלון",             # hotel (Ibis)
    "עיר",              # city (Macau)
    "כנסייה",           # church
    "תפילה",            # prayer
    "מונרכיה",          # monarchy
    "רשת מלונות",       # hotel chain
    "צלילה",            # scuba diving
    "כלי נגינה",        # musical instrument
    "קרינת",            # radiation
    "אלכוהול",          # alcohol
]

WRONG_TOPIC_ES = [
    "género musical",   # music genre (flamenco)
    "utensilio",        # utensil (spatula)
    "aeronave",         # aircraft
    "profesión",        # profession
    "tipo de barco",    # ship type
    "fruta",            # fruit
    "bebida",           # drink
    "aguja de coser",   # sewing needle
    "monarquía",        # monarchy
]


def is_garbage(text: str, lang: str) -> bool:
    """Check if a description is a disambiguation page or wrong topic."""
    if not text or len(text.strip()) < 30:
        return True
    t = text.lower()
    
    patterns = {
        "he": HE_GARBAGE + WRONG_TOPIC_HE,
        "es": ES_GARBAGE + WRONG_TOPIC_ES,
        "en": EN_GARBAGE,
    }
    for p in patterns.get(lang, []):
        if p.lower() in t:
            return True
    return False


def has_bird_keywords(text: str, lang: str) -> bool:
    """Check if description likely talks about a bird (not a homonym)."""
    t = text.lower()
    keywords = {
        "en": ["bird", "species", "plumage", "feather", "wing", "nest", "breed",
               "passerine", "raptor", "waterfowl", "avian", "migrate", "songbird",
               "family", "order", "genus", "egg", "habitat"],
        "he": ["ציפור", "מין", "נוצות", "כנף", "קן", "מטיל", "נודד",
               "שיר", "משפחת", "סדרת", "דגירה", "ביצ", "מקור"],
        "es": ["ave", "pájaro", "especie", "plumaje", "pluma", "nido", "migra",
               "familia", "orden", "género", "huevo", "hábitat", "vuelo"],
    }
    for kw in keywords.get(lang, keywords["en"]):
        if kw in t:
            return True
    return False


# ── Wikipedia API helpers ────────────────────────────────────────────────────

def wiki_search_by_scientific_name(scientific_name: str) -> dict | None:
    """
    Search English Wikipedia for a scientific name.
    Returns the page title and pageid if found.
    """
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": scientific_name,
        "redirects": 1,
        "prop": "info",
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if pid != "-1" and "missing" not in page:
                return {"title": page["title"], "pageid": int(pid)}
    except Exception as e:
        print(f"    [Wiki search error] {e}")
    return None


def wiki_get_langlinks(title: str, langs: list[str] = ["he", "es"]) -> dict:
    """
    Get interlanguage links from an English Wikipedia article.
    Returns {lang_code: localized_title} for each requested language.
    """
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "langlinks",
        "lllimit": 50,
        "redirects": 1,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        result = {}
        for page in pages.values():
            for ll in page.get("langlinks", []):
                if ll["lang"] in langs:
                    result[ll["lang"]] = ll["*"]
        return result
    except Exception as e:
        print(f"    [Langlinks error] {e}")
        return {}


def wiki_get_extract(title: str, lang: str = "en", sentences: int = 3) -> str | None:
    """
    Get the intro extract from a Wikipedia article in the given language.
    Uses the title in that language (e.g. Hebrew title for he.wikipedia).
    """
    url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "exintro": 1,
        "exsentences": sentences,
        "explaintext": 1,
        "redirects": 1,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if pid == "-1":
                continue
            extract = page.get("extract", "").strip()
            if extract and len(extract) > 30:
                # Clean up parenthetical latin names, excess whitespace
                extract = re.sub(r"\s+", " ", extract).strip()
                return extract
    except Exception as e:
        print(f"    [Extract error {lang}] {e}")
    return None


def wiki_get_categories(title: str) -> list[str]:
    """Get categories from English Wikipedia to verify it's about a bird."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "categories",
        "cllimit": 30,
        "redirects": 1,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        cats = []
        for page in pages.values():
            for c in page.get("categories", []):
                cats.append(c.get("title", ""))
        return cats
    except Exception:
        return []


def is_bird_article(title: str) -> bool:
    """Verify the Wikipedia article is actually about a bird species."""
    cats = wiki_get_categories(title)
    bird_indicators = ["bird", "aves", "passerine", "raptor", "waterfowl",
                       "falcon", "owl", "parrot", "penguin", "species"]
    cats_lower = " ".join(cats).lower()
    return any(ind in cats_lower for ind in bird_indicators)


# ── Location & tag helpers (merged from add_locations.py) ────────────────────

LOCATION_MAPPING = {
    "Israel": [
        "Sparrow", "Pigeon", "Starling", "Dove", "Great Tit", "Myna", "Swallow",
        "Robin", "Thrush", "Goldfinch", "Mallard", "Egret", "Hoopoe", "Stork",
        "Blackbird", "Magpie", "Crow", "Wood Pigeon", "Swan", "Falcon", "Owl",
        "Osprey", "Bee-eater", "Ibis", "Kingfisher", "Kestrel", "Swift", "Martin",
        "Warbler", "Wagtail", "Bulbul", "Sunbird", "Heron", "Cormorant", "Gull",
        "Tern", "Plover", "Sandpiper", "Lapwing", "Wheatear", "Shrike",
        "Flycatcher", "Pipit", "Lark", "Eagle", "Vulture", "Buzzard", "Kite",
        "Harrier", "Hawk", "Crane", "Pelican", "Flamingo", "Griffon Vulture",
        "Chukar", "Jay", "Raven", "Stonechat", "White-throated Kingfisher",
    ],
    "Africa": [
        "Hoopoe", "Shoebill", "Secretary Bird", "Flamingo", "Roller", "Swallow",
        "Egret", "Osprey", "Falcon", "Owl", "Bee-eater", "Myna", "Sparrow",
        "Pigeon", "Cattle Egret", "Ostrich", "Guinea Fowl", "Hornbill", "Weaver",
        "Sunbird", "Vulture", "Eagle", "Stork", "Pelican", "Crane", "Ibis",
        "Parrot", "Lovebird", "Grey Parrot", "Turaco", "Barbet", "Honeyguide",
        "Drongo", "Shrike", "Fiscal", "Boubou", "Cisticola", "Cormorant",
        "Darter", "Mousebird",
    ],
    "US": [
        "Sparrow", "Pigeon", "Starling", "Finch", "Robin", "Dove", "Crow",
        "Blue Jay", "Cardinal", "Goldfinch", "Woodpecker", "Hawk", "Mallard",
        "Goose", "Heron", "Eagle", "Vulture", "Chickadee", "Nuthatch", "Bluebird",
        "Hummingbird", "Kingfisher", "Blackbird", "Grackle", "Junco", "Wren",
        "Titmouse", "Mockingbird", "Cowbird", "Warbler", "Phoebe", "Duck",
        "Turkey", "Owl", "Flicker", "Waxwing", "Killdeer", "Kestrel", "Swallow",
        "Falcon", "Osprey", "Egret", "Pelican", "Crane", "Spoonbill", "Avocet",
        "Bunting", "Flycatcher", "Tanager", "Grosbeak", "Oriole", "Meadowlark",
        "Thrasher", "Vireo", "Catbird", "Sapsucker", "Roadrunner", "Condor",
        "Quail", "Grouse", "Ptarmigan", "Tern", "Skimmer", "Puffin",
    ],
    "Europe": [
        "Sparrow", "Pigeon", "Starling", "Blackbird", "Great Tit", "Blue Tit",
        "Magpie", "Robin", "Goldfinch", "Swan", "Mallard", "Wood Pigeon", "Dove",
        "Swallow", "Swift", "Martin", "Gull", "Buzzard", "Kestrel", "Heron",
        "Woodpecker", "Wren", "Dunnock", "Thrush", "Nuthatch", "Treecreeper",
        "Crow", "Rook", "Jackdaw", "Pheasant", "Partridge", "Owl", "Falcon",
        "Osprey", "Bee-eater", "Puffin", "Egret", "Hoopoe", "Stork", "Crane",
        "Cormorant", "Grebe", "Loon", "Shearwater", "Petrel", "Gannet", "Skua",
        "Tern", "Auk", "Guillemot", "Razorbill", "Cuckoo", "Nightjar",
        "Kingfisher", "Roller", "Oriole",
    ],
    "Asia": [
        "Sparrow", "Pigeon", "Myna", "Crow", "Magpie", "Bulbul", "Dove",
        "Kingfisher", "Drongo", "Koel", "Coucal", "Kite", "Eagle", "Parakeet",
        "Munia", "Sunbird", "Minivet", "Peafowl", "Duck", "Pheasant", "Hornbill",
        "Barbet", "Broadbill", "Pitta", "Leafbird", "Flowerpecker", "White-eye",
        "Babbler", "Laughingthrush", "Tailorbird", "Prinia", "Cisticola",
        "Warbler", "Flycatcher", "Robin", "Thrush", "Redstart", "Forktail",
        "Chat", "Accentor", "Pipit", "Wagtail", "Bunting", "Rosefinch",
        "Grosbeak", "Crane", "Stork", "Ibis", "Spoonbill", "Heron", "Egret",
        "Bittern", "Pelican", "Cormorant", "Darter", "Grebe", "Loon",
    ],
}

BIG_BIRDS_KEYWORDS = [
    "Ostrich", "Emu", "Rhea", "Cassowary", "Pelican", "Flamingo", "Swan",
    "Eagle", "Vulture", "Condor", "Stork", "Crane", "Turkey", "Peacock",
    "Albatross", "Heron", "Goose", "Cormorant", "Hawk", "Owl", "Penguin",
    "Bustard", "Capercaillie", "Grouse", "Shoebill", "Hornbill", "Spoonbill",
]


def fix_locations_and_tags(bird: dict) -> list[str]:
    """
    Update a bird's locations and tags.
    Priority: birds_200.py catalog > keyword matching fallback.
    Also adds 'Big' tag for large bird species.
    Returns list of changes made.
    """
    changes = []
    en_name = bird["names"]["en"]
    sci_name = bird.get("scientificName", "")

    # ── Locations ──
    catalog_entry = _BIRDS_BY_SCI.get(sci_name)
    if catalog_entry and catalog_entry.get("locations"):
        # Use authoritative locations from birds_200.py
        new_locs = sorted(set(catalog_entry["locations"]))
        old_locs = sorted(set(bird.get("locations", [])))
        if new_locs != old_locs:
            bird["locations"] = catalog_entry["locations"]
            changes.append(f"  ✓ Locations (catalog): {old_locs} → {catalog_entry['locations']}")
    else:
        # Keyword fallback from LOCATION_MAPPING
        new_locs = []
        for location, keywords in LOCATION_MAPPING.items():
            for kw in keywords:
                if kw.lower() in en_name.lower():
                    new_locs.append(location)
                    break
        new_locs = sorted(set(new_locs))
        old_locs = sorted(set(bird.get("locations", [])))
        if new_locs and new_locs != old_locs:
            bird["locations"] = new_locs
            changes.append(f"  ✓ Locations (keyword): {old_locs} → {new_locs}")

    # ── Tags ──
    tags = bird.get("tags", [])
    if not isinstance(tags, list):
        tags = []
    for kw in BIG_BIRDS_KEYWORDS:
        if kw.lower() in en_name.lower() and "Big" not in tags:
            tags.append("Big")
            changes.append(f"  ✓ Added tag: Big")
            break
    bird["tags"] = tags

    return changes


# ── Main fix logic ───────────────────────────────────────────────────────────

def analyze_bird(bird: dict) -> dict:
    """
    Analyze a single bird entry and return a report + fixes.
    """
    bird_id = bird["id"]
    en_name = bird["names"]["en"]
    he_name = bird["names"]["he"]
    es_name = bird["names"]["es"]
    sci_name = bird["scientificName"]
    desc = bird.get("description", {})
    
    issues = []
    fixes = {}
    
    # Check descriptions
    for lang, text in [("en", desc.get("en", "")), 
                        ("he", desc.get("he", "")),
                        ("es", desc.get("es", ""))]:
        if not text:
            issues.append(f"  MISSING {lang} description")
        elif is_garbage(text, lang):
            issues.append(f"  GARBAGE {lang} description: {text[:80]}...")
        elif not has_bird_keywords(text, lang):
            issues.append(f"  SUSPECT {lang} description (no bird keywords): {text[:80]}...")
    
    # Check locations
    if not bird.get("locations") or len(bird["locations"]) == 0:
        issues.append(f"  EMPTY locations")
    
    # Check tags
    if not bird.get("tags"):
        for kw in BIG_BIRDS_KEYWORDS:
            if kw.lower() in en_name.lower():
                issues.append(f"  MISSING 'Big' tag (matches '{kw}')")
                break
    
    return {"id": bird_id, "en": en_name, "sci": sci_name, "issues": issues}


def fix_bird(bird: dict, force: bool = False) -> tuple[dict, list[str]]:
    """
    Fix a single bird's names, descriptions using Wikipedia interlanguage links.
    Returns (updated_bird, list_of_changes_made).
    """
    bird = {**bird}  # shallow copy
    bird["names"] = {**bird["names"]}
    bird["description"] = {**bird.get("description", {})}
    
    changes = []
    sci_name = bird["scientificName"]
    en_name = bird["names"]["en"]
    desc = bird["description"]
    
    # Step 1: Find the correct English Wikipedia article via scientific name
    print(f"  Looking up: {sci_name} ({en_name})")
    page = wiki_search_by_scientific_name(sci_name)
    
    if not page:
        # Fallback: try English common name + " (bird)"
        page = wiki_search_by_scientific_name(en_name)
        if not page:
            page = wiki_search_by_scientific_name(f"{en_name} (bird)")
    
    if not page:
        changes.append(f"  ✗ Could not find Wikipedia article for {sci_name}")
        return bird, changes
    
    en_title = page["title"]
    time.sleep(0.3)
    
    # Step 2: Get interlanguage links (Hebrew, Spanish)
    langlinks = wiki_get_langlinks(en_title, ["he", "es"])
    time.sleep(0.3)
    
    # Step 3: Fix Hebrew name if langlink exists
    if "he" in langlinks:
        he_wiki_name = langlinks["he"]
        old_he = bird["names"]["he"]
        if old_he != he_wiki_name:
            bird["names"]["he"] = he_wiki_name
            changes.append(f"  ✓ Hebrew name: \"{old_he}\" → \"{he_wiki_name}\"")
    
    # Step 4: Fix descriptions
    # English
    en_desc = desc.get("en", "")
    if force or not en_desc or is_garbage(en_desc, "en") or not has_bird_keywords(en_desc, "en"):
        new_desc = wiki_get_extract(en_title, "en", 3)
        if new_desc and has_bird_keywords(new_desc, "en"):
            old_preview = (en_desc[:60] + "...") if en_desc else "(empty)"
            bird["description"]["en"] = new_desc
            changes.append(f"  ✓ English desc fixed: {old_preview}")
        time.sleep(0.3)
    
    # Hebrew
    he_desc = desc.get("he", "")
    if force or not he_desc or is_garbage(he_desc, "he") or not has_bird_keywords(he_desc, "he"):
        he_title = langlinks.get("he")
        if he_title:
            new_desc = wiki_get_extract(he_title, "he", 3)
            if new_desc and not is_garbage(new_desc, "he"):
                old_preview = (he_desc[:60] + "...") if he_desc else "(empty)"
                bird["description"]["he"] = new_desc
                changes.append(f"  ✓ Hebrew desc fixed: {old_preview}")
            time.sleep(0.3)
    
    # Spanish
    es_desc = desc.get("es", "")
    if force or not es_desc or is_garbage(es_desc, "es") or not has_bird_keywords(es_desc, "es"):
        es_title = langlinks.get("es", sci_name)  # Many Spanish articles use scientific name
        new_desc = wiki_get_extract(es_title, "es", 3)
        if new_desc and not is_garbage(new_desc, "es"):
            old_preview = (es_desc[:60] + "...") if es_desc else "(empty)"
            bird["description"]["es"] = new_desc
            changes.append(f"  ✓ Spanish desc fixed: {old_preview}")
        time.sleep(0.3)
    
    # Step 5: Fix locations & tags (merged from add_locations.py)
    loc_changes = fix_locations_and_tags(bird)
    changes.extend(loc_changes)
    
    return bird, changes


def main():
    parser = argparse.ArgumentParser(description="Fix BirdLingo bird data")
    parser.add_argument("--fix", action="store_true", help="Apply fixes (otherwise dry-run)")
    parser.add_argument("--force", action="store_true", help="Re-fetch all descriptions, even good ones")
    parser.add_argument("--bird", type=int, help="Fix only bird_NNN (e.g. --bird 42)")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")
    parser.add_argument("--limit", type=int, default=0, help="Process only first N birds")
    args = parser.parse_args()
    
    # Load current data
    with open(APP_DATA, "r", encoding="utf-8") as f:
        birds = json.load(f)
    
    print(f"Loaded {len(birds)} birds from {APP_DATA}")
    print(f"Mode: {'FIX' if args.fix else 'DRY-RUN (use --fix to apply)'}\n")
    
    # ── Analyze ──
    if args.report or not args.fix:
        print("=" * 60)
        print("ANALYSIS REPORT")
        print("=" * 60)
        
        total_issues = 0
        issue_birds = 0
        report_lines = []
        
        for bird in birds:
            if args.bird and bird["id"] != f"bird_{args.bird:03d}":
                continue
            result = analyze_bird(bird)
            if result["issues"]:
                issue_birds += 1
                total_issues += len(result["issues"])
                line = f"\n{result['id']} | {result['en']} ({result['sci']})"
                print(line)
                report_lines.append(line)
                for issue in result["issues"]:
                    print(issue)
                    report_lines.append(issue)
        
        print(f"\n{'=' * 60}")
        print(f"Total: {issue_birds} birds with issues, {total_issues} issues total")
        print(f"{'=' * 60}\n")
        
        if args.report:
            with open(REPORT, "w", encoding="utf-8") as f:
                f.write("\n".join(report_lines))
            print(f"Report saved to {REPORT}")
        
        if not args.fix:
            print("Run with --fix to apply corrections.")
            return
    
    # ── Fix ──
    print("=" * 60)
    print("FIXING DATA")
    print("=" * 60)
    
    fixed_birds = []
    total_changes = 0
    processed = 0
    
    for i, bird in enumerate(birds):
        if args.bird and bird["id"] != f"bird_{args.bird:03d}":
            fixed_birds.append(bird)
            continue
        
        if args.limit and processed >= args.limit:
            fixed_birds.append(bird)
            continue
        
        # Check if this bird needs fixing
        result = analyze_bird(bird)
        needs_fix = len(result["issues"]) > 0 or args.force
        
        if needs_fix:
            print(f"\n[{i+1}/{len(birds)}] {bird['id']} | {bird['names']['en']}")
            fixed_bird, changes = fix_bird(bird, force=args.force)
            fixed_birds.append(fixed_bird)
            total_changes += len(changes)
            for c in changes:
                print(c)
            processed += 1
            time.sleep(0.5)  # Be nice to Wikipedia API
        else:
            fixed_birds.append(bird)
    
    # Save
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(fixed_birds, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'=' * 60}")
    print(f"Done! {total_changes} changes across {processed} birds")
    print(f"Fixed data saved to: {OUTPUT}")
    print(f"\nTo apply: copy {OUTPUT.name} → {APP_DATA.name}")
    print(f"  copy BirdLingo\\assets\\birds_data_fixed.json BirdLingo\\assets\\birds_data.json")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
