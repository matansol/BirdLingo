import json
import os
from google import genai
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.genai import types

# Load the bird data
with open('birds_info.json', 'r', encoding='utf-8') as f:
    birds_data = json.load(f)

# Collect all species to classify
species_list = []
for key, data in birds_data.items():
    if "isGroup" not in data or not data["isGroup"]:
        species_list.append({
            "key": key,
            "name": data["names"]["en"],
            "he": data["names"]["he"],
            "es": data["names"]["es"],
            "fr": data["names"]["fr"],
            "category": data.get("category", "")
        })

print(f"Total birds to group: {len(species_list)}")

client = genai.Client()

def classify_birds(birds_batch):
    prompt = f"""
    I have a list of specific bird species. I want to assign each one to a general high-level "group" or "family". 
    For example: "Rock Dove" -> "Dove", "Mallard" -> "Duck", "Golden Eagle" -> "Eagle", "American Crow" -> "Crow".
    I also need the group name translated appropriately into Hebrew (he), Spanish (es), and French (fr). 
    Capitalize the group names appropriately in English. 
    
    Here is the list of birds in JSON format:
    {json.dumps(birds_batch, indent=2, ensure_ascii=False)}
    
    Return a valid JSON array of objects. **ONLY output the raw JSON array**, no markdown block, no extra text formatting.
    Each object must have exactly these keys:
    - "key": The original bird key
    - "group_en": The high-level group name in English (e.g., "Dove")
    - "group_he": The high-level group name in Hebrew
    - "group_es": The high-level group name in Spanish
    - "group_fr": The high-level group name in French
    - "groupId": A snake_case unique ID for the group (e.g., "dove", "duck", "eagle")
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        text = response.text.strip()
        if text.startswith('```json'): text = text[7:]
        if text.endswith('```'): text = text[:-3]
        return json.loads(text.strip())
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return []

# Process in batches
batch_size = 30
batches = [species_list[i:i + batch_size] for i in range(0, len(species_list), batch_size)]

all_results = []
for i, batch in enumerate(batches):
    print(f"Processing batch {i+1}/{len(batches)}...")
    res = classify_birds(batch)
    if res:
        all_results.extend(res)
    time.sleep(2) # rate limiting

# Now update the JSON and create groups
groups_dict = {}

# First, add the group information to each bird
for result in all_results:
    bird_key = result["key"]
    if bird_key in birds_data:
        birds_data[bird_key]["groupId"] = result["groupId"]
        birds_data[bird_key]["isGroup"] = False
        
        # Track the group
        g_id = result["groupId"]
        if g_id not in groups_dict:
            groups_dict[g_id] = {
                "name": g_id,
                "names": {
                    "en": result["group_en"],
                    "he": result["group_he"],
                    "es": result["group_es"],
                    "fr": result["group_fr"]
                },
                "isGroup": True,
                "scientificName": "Various",
                "difficulty": birds_data[bird_key].get("difficulty", 1), # take min difficulty later
                "category": birds_data[bird_key].get("category", "Unknown"), # assume same category
                "locations": set(birds_data[bird_key].get("locations", [])),
                "images": [],
                "flyingImage": None,
                "description": {
                    "en": f"A group representing {result['group_en']} species.",
                    "he": f"קבוצה המייצגת מיני {result['group_he']}.",
                    "es": f"Un grupo que representa especies de {result['group_es']}.",
                    "fr": f"Un groupe représentant les espèces de {result['group_fr']}."
                }
            }
        else:
            # aggregate locations
            groups_dict[g_id]["locations"].update(birds_data[bird_key].get("locations", []))
            # take minimum difficulty (so if a group has a common bird, the group itself is common)
            groups_dict[g_id]["difficulty"] = min(groups_dict[g_id]["difficulty"], birds_data[bird_key].get("difficulty", 5))

# Second pass: aggregate images for groups
for bird_key, data in birds_data.items():
    if not data.get("isGroup", False) and "groupId" in data:
        g_id = data["groupId"]
        if g_id in groups_dict:
            # add the first 2 images from each species to the group
            if "images" in data:
                groups_dict[g_id]["images"].extend(data["images"][:2])
            # assign flying image if group doesn't have one
            if "flyingImage" in data and not groups_dict[g_id].get("flyingImage"):
                groups_dict[g_id]["flyingImage"] = data["flyingImage"]

# convert locations back to lists and add groups to the main dict
for g_id, g_data in groups_dict.items():
    g_data["locations"] = list(g_data["locations"])
    # ensure no more than ~6 images per group so we don't bloat the app
    if len(g_data["images"]) > 6:
        import random
        random.shuffle(g_data["images"])
        g_data["images"] = g_data["images"][:6]
    
    birds_data[f"group_{g_id}"] = g_data

# Save back to JSON
with open('birds_info.json', 'w', encoding='utf-8') as f:
    json.dump(birds_data, f, ensure_ascii=False, indent=2)

print(f"Added {len(groups_dict)} generic groups to birds_info.json!")

# Generate the birds_data.json for the app
import shutil
shutil.copyfile('birds_info.json', 'fetch_output.json')
import sys
import subprocess
try:
    subprocess.run([sys.executable, 'fix_bird_data.py'], check=True)
    print("Successfully ran fix_bird_data.py to create src/assets/birds_data.json")
except Exception as e:
    print(f"Failed to copy data to app: {e}")
