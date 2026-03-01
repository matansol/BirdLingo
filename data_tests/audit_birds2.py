import json
with open('BirdLingo/assets/birds_data.json', 'r', encoding='utf-8') as f:
    birds = json.load(f)

print('=== SUSPICIOUS LOCATION ISSUES ===')
suspects = {
    'bird_003': 'Blue Jay in Israel - native to North America only',
    'bird_133': 'Snowy Owl in Israel/Africa - Arctic bird',
    'bird_134': 'Great Horned Owl in Europe/Israel/Africa - Americas only',
    'bird_135': 'Screech Owl in Europe/Israel/Africa - Eastern N. America only',
    'bird_136': 'Burrowing Owl in Europe/Israel/Africa - Americas only',
    'bird_137': 'Tawny Owl in US/Africa - Europe/Asia only',
    'bird_159': 'Fairy Bluebird in US - Southeast Asia only',
}
for bid, issue in suspects.items():
    b = next(x for x in birds if x['id'] == bid)
    locs = b['locations']
    name = b['names']['en']
    print(f'  {bid} ({name}): locations={locs} -> {issue}')

print()
print('=== HEBREW NAMES - TRANSLITERATIONS ===')
translit = [
    ('bird_010', 'Cardinal'),
    ('bird_016', 'Flamingo'),
    ('bird_025', 'Toucan'),
    ('bird_035', 'Macaw (also means Macau city)'),
    ('bird_036', 'Puffin'),
    ('bird_037', 'Cormorant'),
    ('bird_043', 'Penguin'),
    ('bird_055', 'Cockatiel (also means cocktail)'),
    ('bird_057', 'Lorikeet'),
    ('bird_060', 'Ibis (also hotel chain)'),
    ('bird_062', 'Albatross'),
    ('bird_064', 'Condor'),
    ('bird_090', 'Thrasher'),
    ('bird_091', 'Myna'),
    ('bird_140', 'Francolin'),
    ('bird_144', 'Kiwi (also fruit)'),
    ('bird_145', 'Cassowary'),
    ('bird_147', 'Motmot'),
    ('bird_148', 'Trogon'),
    ('bird_150', 'Barbet'),
    ('bird_151', 'Aracari'),
    ('bird_152', 'Cotinga'),
    ('bird_153', 'Manakin'),
    ('bird_161', 'Drongo'),
    ('bird_175', 'Phalarope'),
]
for bid, note in translit:
    b = next(x for x in birds if x['id'] == bid)
    he_name = b['names']['he']
    en_name = b['names']['en']
    print(f'  {bid}: {en_name} -> he: {he_name} ({note})')

print()
print('=== QUESTIONABLE TAGS ===')
print('  bird_128 Sparrowhawk tagged Big - actually a SMALL raptor')
print('  bird_135 Screech Owl tagged Big - actually a SMALL owl')
print('  bird_136 Burrowing Owl tagged Big - actually a SMALL owl')

print()
cats = {}
for b in birds:
    c = b['category']
    cats[c] = cats.get(c, 0) + 1
print('=== CATEGORIES ===')
for c, n in sorted(cats.items()):
    print(f'  {c}: {n}')

print()
diffs = {}
for b in birds:
    d = b['difficulty']
    diffs[d] = diffs.get(d, 0) + 1
print('=== DIFFICULTIES ===')
for d, n in sorted(diffs.items()):
    print(f'  Level {d}: {n}')

print()
# Check for duplicate he names
he_names = {}
for b in birds:
    he = b['names']['he']
    if he in he_names:
        he_names[he].append(b['id'] + ' ' + b['names']['en'])
    else:
        he_names[he] = [b['id'] + ' ' + b['names']['en']]
print('=== DUPLICATE HEBREW NAMES ===')
for he, ids in he_names.items():
    if len(ids) > 1:
        print(f'  "{he}": {ids}')

# Check for duplicate es names
es_names = {}
for b in birds:
    es = b['names']['es']
    if es in es_names:
        es_names[es].append(b['id'] + ' ' + b['names']['en'])
    else:
        es_names[es] = [b['id'] + ' ' + b['names']['en']]
print()
print('=== DUPLICATE SPANISH NAMES ===')
for es, ids in es_names.items():
    if len(ids) > 1:
        print(f'  "{es}": {ids}')
