import json

groups_meta = {
    "sparrow": {"en": "Sparrow", "he": "דרור", "es": "Gorrión", "fr": "Moineau"},
    "dove_pigeon": {"en": "Pigeon", "he": "יונה", "es": "Paloma", "fr": "Pigeon et Tourterelle"},
    "thrush": {"en": "Robin", "he": "קיכלי", "es": "Zorzal", "fr": "Grive et Merle"},
    "starling": {"en": "Starling", "he": "זרזיר", "es": "Estornino", "fr": "Étourneau et Martin"},
    "duck": {"en": "Duck", "he": "ברווז", "es": "Pato", "fr": "Canard"},
    "goose": {"en": "Goose", "he": "אווז", "es": "Ganso", "fr": "Oie"},
    "swan": {"en": "Swan", "he": "ברבור", "es": "Cisne", "fr": "Cygne"},
    "gull": {"en": "Gull", "he": "שחף", "es": "Gaviota", "fr": "Goéland et Sterne"},
    "pheasant": {"en": "Pheasant", "he": "פסיון", "es": "Faisán", "fr": "Faisan et Perdrix"},
    "bunting": {"en": "Bunting", "he": "גיבתון", "es": "Escribano", "fr": "Bruant"},
    "crow_jay": {"en": "Crow", "he": "עורב", "es": "Cuervo", "fr": "Corbeau et Geai"},
    "tit": {"en": "Tit", "he": "ירגזי", "es": "Carbonero", "fr": "Mésange"},
    "swallow": {"en": "Swallow", "he": "סנונית", "es": "Golondrina", "fr": "Hirondelle"},
    "finch": {"en": "Finch", "he": "פרוש", "es": "Pinzón", "fr": "Pinson"},
    "heron": {"en": "Heron", "he": "אנפה", "es": "Garza", "fr": "Héron"},
    "flamingo": {"en": "Flamingo", "he": "פלמינגו", "es": "Flamenco", "fr": "Flamant"},
    "hawk": {"en": "Hawk", "he": "נץ", "es": "Halcón", "fr": "Buse et Épervier"},
    "falcon": {"en": "Falcon", "he": "בז", "es": "Halcón", "fr": "Faucon"},
    "owl": {"en": "Owl", "he": "ינשוף", "es": "Búho", "fr": "Hibou et Chouette"},
    "swift": {"en": "Swift", "he": "סיס", "es": "Vencejo", "fr": "Martinet"},
    "pelican": {"en": "Pelican", "he": "שקנאי", "es": "Pelícano", "fr": "Pélican"},
    "stork": {"en": "Stork", "he": "חסידה", "es": "Cigüeña", "fr": "Cigogne"},
    "crane": {"en": "Crane", "he": "עגור", "es": "Grulla", "fr": "Grue"},
    "cormorant": {"en": "Cormorant", "he": "קורמורן", "es": "Cormorán", "fr": "Cormoran"},
    "hoopoe": {"en": "Hoopoe", "he": "דוכיפת", "es": "Abubilla", "fr": "Huppe"},
    "kingfisher": {"en": "Kingfisher", "he": "שלדג", "es": "Martín Pescador", "fr": "Martin-pêcheur"},
    "lark": {"en": "Lark", "he": "עפרוני", "es": "Alondra", "fr": "Alouette"},
    "eagle": {"en": "Eagle", "he": "עיט", "es": "Águila", "fr": "Aigle et Balbuzard"},
    "woodpecker": {"en": "Woodpecker", "he": "נקר", "es": "Pájaro Carpintero", "fr": "Pic"},
    "mockingbird": {"en": "Mockingbird", "he": "חקיין", "es": "Sinsonte", "fr": "Moqueur"},
    "waxwing": {"en": "Waxwing", "he": "אמבלרון", "es": "Ampelis", "fr": "Jaseur"},
    "oriole": {"en": "Oriole", "he": "פזאי", "es": "Oropéndola", "fr": "Loriot"},
    "tanager": {"en": "Tanager", "he": "טנאגר", "es": "Tángara", "fr": "Tangara"},
    "hummingbird": {"en": "Hummingbird", "he": "יונק דבש", "es": "Colibrí", "fr": "Colibri"},
    "wader": {"en": "Sandpiper", "he": "חופמאים", "es": "Limícolas", "fr": "Limicoles"},
    "rail": {"en": "Coot", "he": "רליתיים", "es": "Rálidos", "fr": "Râles et Foulques"},
    "grebe": {"en": "Grebe", "he": "טבלן", "es": "Somormujo", "fr": "Grèbe"},
    "seabird": {"en": "Albatross", "he": "אלבטרוס", "es": "Albatros", "fr": "Albatros et Pétrel"},
    "nuthatch": {"en": "Nuthatch", "he": "סיטה", "es": "Trepador", "fr": "Sittelle et Grimpereau"},
    "wren": {"en": "Wren", "he": "גדרון", "es": "Chochín", "fr": "Troglodyte"},
    "accentor": {"en": "Accentor", "he": "סתרי", "es": "Acentor", "fr": "Accenteur"},
    "warbler": {"en": "Warbler", "he": "סבכי ועלווית", "es": "Curruca", "fr": "Fauvette"},
    "bee_eater": {"en": "Bee-eater", "he": "שרקרק", "es": "Abejaruco", "fr": "Guêpier et Rollier"},
    "bustard": {"en": "Bustard", "he": "חובה", "es": "Avutarda", "fr": "Outarde"},
    "vulture": {"en": "Vulture", "he": "נשר", "es": "Buitre", "fr": "Vautour et Condor"},
    "ibis": {"en": "Ibis", "he": "מגלן", "es": "Ibis", "fr": "Ibis et Spatule"},
    "kinglet": {"en": "Kinglet", "he": "מלכילון", "es": "Reyezuelo", "fr": "Roitelet"},
    "dipper": {"en": "Dipper", "he": "אמודאי", "es": "Mirlo Acuático", "fr": "Cincle"},
    "parrot": {"en": "Parrot", "he": "תוכי", "es": "Loro", "fr": "Perroquet et Ara"},
    "honeyeater": {"en": "Honeyeater", "he": "דבשן", "es": "Melífago", "fr": "Méliphage"},
    "secretarybird": {"en": "Secretarybird", "he": "לבלר", "es": "Secretario", "fr": "Messager Sagittaire"},
    "shoebill": {"en": "Shoebill", "he": "מנעלן", "es": "Picozapato", "fr": "Bec-en-sabot"},
    "hornbill": {"en": "Hornbill", "he": "קלאו", "es": "Cálao", "fr": "Calao"},
    "quetzal": {"en": "Quetzal", "he": "קורוקו", "es": "Quetzal", "fr": "Quetzal"},
    "lyrebird": {"en": "Lyrebird", "he": "נבלי", "es": "Ave Lira", "fr": "Ménure"},
    "bird_of_paradise": {"en": "Bird of Paradise", "he": "עדניים", "es": "Ave del Paraíso", "fr": "Paradisier"},
    "kiwi": {"en": "Kiwi", "he": "קיווי", "es": "Kiwi", "fr": "Kiwi"},
    "flycatcher": {"en": "Flycatcher", "he": "חטפית", "es": "Papamoscas", "fr": "Gobemouche et Tarier"}
}

bird_to_group = {
    "house_sparrow": "sparrow",
    "rock_pigeon": "dove_pigeon",
    "common_blackbird": "thrush",
    "european_starling": "starling",
    "mallard": "duck",
    "canada_goose": "goose",
    "mute_swan": "swan",
    "herring_gull": "gull",
    "peacock": "pheasant",
    "american_robin": "thrush",
    "northern_cardinal": "bunting",
    "blue_jay": "crow_jay",
    "american_crow": "crow_jay",
    "eurasian_magpie": "crow_jay",
    "great_tit": "tit",
    "blue_tit": "tit",
    "barn_swallow": "swallow",
    "eurasian_collared_dove": "dove_pigeon",
    "common_wood_pigeon": "dove_pigeon",
    "house_finch": "finch",
    "mourning_dove": "dove_pigeon",
    "common_myna": "starling",
    "house_crow": "crow_jay",
    "european_robin": "flycatcher",
    "goldfinch": "finch",
    "great_egret": "heron",
    "flamingo": "flamingo",
    "common_buzzard": "hawk",
    "kestrel": "falcon",
    "barn_owl": "owl",
    "common_swift": "swift",
    "song_thrush": "thrush",
    "pelican": "pelican",
    "white_stork": "stork",
    "common_crane": "crane",
    "grey_heron": "heron",
    "little_egret": "heron",
    "cormorant": "cormorant",
    "hoopoe": "hoopoe",
    "sparrowhawk": "hawk",
    "black_headed_gull": "gull",
    "common_kingfisher": "kingfisher",
    "nightingale": "flycatcher",
    "skylark": "lark",
    "chaffinch": "finch",
    "greenfinch": "finch",
    "red_tailed_hawk": "hawk",
    "bald_eagle": "eagle",
    "osprey": "eagle",
    "peregrine_falcon": "falcon",
    "great_horned_owl": "owl",
    "snowy_owl": "owl",
    "golden_eagle": "eagle",
    "black_kite": "hawk",
    "red_kite": "hawk",
    "downy_woodpecker": "woodpecker",
    "great_spotted_woodpecker": "woodpecker",
    "green_woodpecker": "woodpecker",
    "northern_mockingbird": "mockingbird",
    "american_goldfinch": "finch",
    "black_capped_chickadee": "tit",
    "tufted_titmouse": "tit",
    "cedar_waxwing": "waxwing",
    "baltimore_oriole": "oriole",
    "scarlet_tanager": "tanager",
    "eastern_bluebird": "thrush",
    "ruby_throated_hummingbird": "hummingbird",
    "wood_duck": "duck",
    "great_blue_heron": "heron",
    "canada_jay": "crow_jay",
    "eurasian_jay": "crow_jay",
    "common_sandpiper": "wader",
    "lapwing": "wader",
    "little_owl": "owl",
    "tawny_owl": "owl",
    "long_eared_owl": "owl",
    "black_redstart": "flycatcher",
    "wheatear": "flycatcher",
    "stonechat": "flycatcher",
    "waxwing": "waxwing",
    "puffin": "seabird",
    "gannet": "seabird",
    "avocet": "wader",
    "curlew": "wader",
    "oystercatcher": "wader",
    "snipe": "wader",
    "common_tern": "gull",
    "common_coot": "rail",
    "moorhen": "rail",
    "bittern": "heron",
    "grebe": "grebe",
    "shearwater": "seabird",
    "common_swift_apus": "swift",
    "house_martin": "swallow",
    "sand_martin": "swallow",
    "wryneck": "woodpecker",
    "nuthatch": "nuthatch",
    "treecreeper": "nuthatch",
    "wren": "wren",
    "dunnock": "accentor",
    "blackcap": "warbler",
    "garden_warbler": "warbler",
    "chiffchaff": "warbler",
    "willow_warbler": "warbler",
    "reed_warbler": "warbler",
    "sedge_warbler": "warbler",
    "long_tailed_tit": "tit",
    "coal_tit": "tit",
    "marsh_tit": "tit",
    "bullfinch": "finch",
    "siskin": "finch",
    "linnet": "finch",
    "yellowhammer": "bunting",
    "corn_bunting": "bunting",
    "booted_eagle": "eagle",
    "short_toed_eagle": "eagle",
    "levant_sparrowhawk": "hawk",
    "white_tailed_eagle": "eagle",
    "marsh_harrier": "hawk",
    "montagu_harrier": "hawk",
    "hobby": "falcon",
    "merlin": "falcon",
    "lanner_falcon": "falcon",
    "scops_owl": "owl",
    "bee_eater": "bee_eater",
    "roller": "bee_eater",
    "little_bustard": "bustard",
    "common_quail": "pheasant",
    "pheasant": "pheasant",
    "red_legged_partridge": "pheasant",
    "kinglet": "kinglet",
    "great_bustard": "bustard",
    "black_grouse": "pheasant",
    "capercaillie": "pheasant",
    "grey_partridge": "pheasant",
    "water_rail": "rail",
    "purple_heron": "heron",
    "night_heron": "heron",
    "squacco_heron": "heron",
    "glossy_ibis": "ibis",
    "spoonbill": "ibis",
    "ferruginous_duck": "duck",
    "garganey": "duck",
    "black_stork": "stork",
    "saker_falcon": "falcon",
    "bonelli_eagle": "eagle",
    "imperial_eagle": "eagle",
    "steppe_eagle": "eagle",
    "griffon_vulture": "vulture",
    "egyptian_vulture": "vulture",
    "black_vulture": "vulture",
    "eagle_owl": "owl",
    "ural_owl": "owl",
    "pygmy_owl": "owl",
    "tengmalm_owl": "owl",
    "ortolan_bunting": "bunting",
    "hawfinch": "finch",
    "crossbill": "finch",
    "redpoll": "finch",
    "twite": "finch",
    "snow_bunting": "bunting",
    "lapland_bunting": "bunting",
    "brambling": "finch",
    "firecrest": "kinglet",
    "bearded_tit": "tit",
    "penduline_tit": "tit",
    "wallcreeper": "nuthatch",
    "dipper": "dipper",
    "ring_ouzel": "thrush",
    "bluethroat": "flycatcher",
    "wryneck_eur": "woodpecker",
    "kakapo": "parrot",
    "california_condor": "vulture",
    "philippine_eagle": "eagle",
    "whooping_crane": "crane",
    "california_clapper_rail": "rail",
    "spixs_macaw": "parrot",
    "blue_throated_macaw": "parrot",
    "regent_honeyeater": "honeyeater",
    "forest_owlet": "owl",
    "stellers_sea_eagle": "eagle",
    "harpy_eagle": "eagle",
    "martial_eagle": "eagle",
    "secretary_bird": "secretarybird",
    "shoebill": "shoebill",
    "african_spoonbill": "ibis",
    "javan_rhino_hornbill": "hornbill",
    "resplendent_quetzal": "quetzal",
    "superb_lyrebird": "lyrebird",
    "bird_of_paradise": "bird_of_paradise",
    "kiwi": "kiwi",
    "bali_myna": "starling",
    "palawan_peacock_pheasant": "pheasant",
    "blue_crowned_laughingthrush": "babbler",
    "amsterdam_albatross": "seabird",
    "cahow": "seabird",
    "ivory_billed_woodpecker": "woodpecker",
    "po_ouli": "honeyeater",
    "giant_ibis": "ibis",
    "new_caledonian_lorikeet": "parrot",
    "swift_parrot": "parrot",
}

with open('birds_info.json', 'r', encoding='utf-8') as f:
    birds_data = json.load(f)

# Optional: Clear existing groups if any to avoid duplication
keys_to_delete = [k for k in birds_data.keys() if birds_data[k].get('isGroup')]
for k in keys_to_delete:
    del birds_data[k]

groups_dict = {}

for bird_key, data in birds_data.items():
    if bird_key in bird_to_group:
        g_id = bird_to_group[bird_key]
        data["groupId"] = g_id
        data["isGroup"] = False
        
        if g_id not in groups_dict:
            groups_dict[g_id] = {
                "name": g_id,
                "names": groups_meta[g_id],
                "isGroup": True,
                "scientificName": "Various",
                "difficulty": data.get("difficulty", 1),
                "category": data.get("category", "Unknown"),
                "locations": set(data.get("locations", [])),
                "tags": set(data.get("tags", [])),
                "images": [],
                "flyingImage": None,
                "description": {
                    "en": f"A group representing {groups_meta[g_id]['en']} species.",
                    "he": f"קבוצה המייצגת מיני {groups_meta[g_id]['he']}.",
                    "es": f"Un grupo que representa especies de {groups_meta[g_id]['es']}.",
                    "fr": f"Un groupe représentant les espèces de {groups_meta[g_id]['fr']}."
                }
            }
        else:
            groups_dict[g_id]["locations"].update(data.get("locations", []))
            groups_dict[g_id]["tags"].update(data.get("tags", []))
            # take min difficulty so the group is accessible if any common bird is in it
            groups_dict[g_id]["difficulty"] = min(groups_dict[g_id]["difficulty"], data.get("difficulty", 5))

for bird_key, data in birds_data.items():
    if not data.get("isGroup", False) and "groupId" in data:
        g_id = data["groupId"]
        if g_id in groups_dict:
            if "images" in data:
                groups_dict[g_id]["images"].extend(data["images"][:2])
            if "flyingImage" in data and not groups_dict[g_id].get("flyingImage"):
                groups_dict[g_id]["flyingImage"] = data["flyingImage"]

for g_id, g_data in groups_dict.items():
    g_data["locations"] = list(g_data["locations"])
    g_data["tags"] = list(g_data["tags"])
    # shuffle and cap images so group doesn't have 40 images
    import random
    random.seed(42)  # for consistency
    random.shuffle(g_data["images"])
    g_data["images"] = g_data["images"][:6]
    
    birds_data[f"group_{g_id}"] = g_data

with open('birds_info.json', 'w', encoding='utf-8') as f:
    json.dump(birds_data, f, ensure_ascii=False, indent=2)

print(f"Added {len(groups_dict)} generic groups to birds_info.json!")

import subprocess
import sys
import shutil

shutil.copyfile('birds_info.json', 'fetch_output.json')
subprocess.run([sys.executable, 'fix_bird_data.py'], check=True)
print("Successfully ran fix_bird_data.py to create src/assets/birds_data.json")
