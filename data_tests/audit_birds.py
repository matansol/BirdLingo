import json
import re

with open('BirdLingo/assets/birds_data.json', 'r', encoding='utf-8') as f:
    birds = json.load(f)

print(f"Total birds: {len(birds)}")
print(f"ID range: {birds[0]['id']} to {birds[-1]['id']}")
print()

# 1. Check structure completeness
required_top = ['id','names','scientificName','category','difficulty','image','description','locations']
required_names = ['en','he','es']

print("=== MISSING TOP-LEVEL FIELDS ===")
for b in birds:
    missing = [k for k in required_top if k not in b]
    if missing:
        print(f"  {b['id']} ({b['names']['en']}): missing {missing}")

print()
print("=== MISSING NAME FIELDS ===")
for b in birds:
    missing = [k for k in required_names if k not in b.get('names',{})]
    if missing:
        print(f"  {b['id']} ({b['names'].get('en','?')}): missing names.{missing}")

print()
print("=== MISSING DESCRIPTION.he ===")
missing_he = []
for b in birds:
    if 'he' not in b.get('description',{}):
        missing_he.append(b)
print(f"Count: {len(missing_he)}")
for b in missing_he:
    print(f"  {b['id']} ({b['names']['en']})")

print()
print("=== MISSING DESCRIPTION.es ===")
missing_es = []
for b in birds:
    if 'es' not in b.get('description',{}):
        missing_es.append(b)
print(f"Count: {len(missing_es)}")
for b in missing_es:
    print(f"  {b['id']} ({b['names']['en']})")

print()
print("=== HEBREW DESC = 'האם התכוונתם ל...' ===")
did_you_mean = []
for b in birds:
    he_desc = b.get('description',{}).get('he','')
    if he_desc.startswith('האם התכוונתם ל'):
        did_you_mean.append(b)
print(f"Count: {len(did_you_mean)}")
for b in did_you_mean:
    print(f"  {b['id']} ({b['names']['en']}) - he name: {b['names']['he']}")

print()
print("=== HEBREW DESC - CLEARLY WRONG (not about bird) ===")
# Manual list based on reading
wrong_he_desc = {
    'bird_010': 'About Catholic cardinal (church rank)',
    'bird_035': 'About Macau (Chinese city)',
    'bird_055': 'About cocktail drinks',
    'bird_060': 'About Ibis hotel chain',
    'bird_077': 'About Givaton (Israeli settlement)',
    'bird_080': 'About Nitrogen (chemical element)',
    'bird_088': 'About Gold (chemical element)',
    'bird_097': 'About Rhinoceros (animal)',
    'bird_106': 'About human diver (scuba)',
    'bird_112': 'About reed plant',
    'bird_116': 'About Gladiolus/iris plant',
    'bird_117': 'About Shacharit (Jewish morning prayer)',
    'bird_120': 'About Chronozone (geological term)',
    'bird_150': 'About Barbat (Wallachian ruler)',
    'bird_163': 'About Monarchy (political system)',
    'bird_165': 'About Violin (musical instrument)',
    'bird_172': 'About Scone (baked food)',
    'bird_204': 'About human diver (scuba)',
}
print(f"Count: {len(wrong_he_desc)}")
for bid, reason in wrong_he_desc.items():
    b = next(x for x in birds if x['id'] == bid)
    print(f"  {bid} ({b['names']['en']}) -> {reason}")

print()
print("=== SPANISH DESC - WRONG TOPIC (not about bird) ===")
wrong_es_desc = {
    'bird_010': 'About Catholic cardinal (church rank)',
    'bird_016': 'About Flamenco music',
    'bird_061': 'About spatula tool',
    'bird_073': 'About airplane',
    'bird_077': 'About notary/scribe profession',
    'bird_089': "About cat's meow sound",
    'bird_108': 'About pikemen soldiers',
    'bird_109': 'About warship (frigate)',
    'bird_129': 'About secretary profession',
    'bird_144': 'About kiwi fruit',
    'bird_154': 'About ant colony/anthill',
    'bird_156': 'About Mexican anise liquor',
    'bird_160': 'About the name Philemon (mythology)',
    'bird_162': 'About a hand fan',
    'bird_163': 'About political monarchy',
    'bird_168': 'About a sewing needle',
    'bird_172': 'About soldiers/combatants',
    'bird_208': 'About myths/legends',
}
print(f"Count: {len(wrong_es_desc)}")
for bid, reason in wrong_es_desc.items():
    b = next(x for x in birds if x['id'] == bid)
    print(f"  {bid} ({b['names']['en']} / {b['names']['es']}) -> {reason}")

print()
print("=== SPANISH DESC - DISAMBIGUATION PAGES ===")
disambig_patterns = [
    'puede referirse', 'puede hacer referencia', 'puede estar referido',
    'puede estar vinculado', 'puede tener varios significados',
    'puede aludir', 'hace referencia a varios', 'puede designar',
    'puede ser:'
]
es_disambig = []
for b in birds:
    es_desc = b.get('description',{}).get('es','')
    for pat in disambig_patterns:
        if pat in es_desc.lower():
            es_disambig.append(b)
            break
print(f"Count: {len(es_disambig)}")
for b in es_disambig:
    en = b['names']['en']
    es = b['names']['es']
    snippet = b['description']['es'][:80]
    print(f"  {b['id']} ({en} / {es}): {snippet}...")

print()
print("=== ENGLISH DESC ISSUES ===")
for b in birds:
    en_desc = b.get('description',{}).get('en','')
    if 'may refer to' in en_desc or 'can refer to' in en_desc:
        print(f"  {b['id']} ({b['names']['en']}): {en_desc[:80]}...")

print()
print("=== UNIQUE IMAGE KEYS ===")
images = sorted(set(b['image'] for b in birds))
print(f"Count: {len(images)}")
for img in images:
    print(f"  {img}")

print()
print("=== TAGS ANALYSIS ===")
with_tags = [b for b in birds if b.get('tags') and len(b['tags']) > 0]
all_tags = set()
for b in birds:
    for t in b.get('tags',[]):
        all_tags.add(t)
print(f"Birds with non-empty tags: {len(with_tags)}")
print(f"Unique tags: {all_tags}")
for b in with_tags:
    print(f"  {b['id']} ({b['names']['en']}): {b['tags']}")

print()
print("=== EMPTY LOCATIONS ===")
empty_loc = [b for b in birds if not b.get('locations')]
print(f"Count: {len(empty_loc)}")
for b in empty_loc:
    print(f"  {b['id']} ({b['names']['en']})")
