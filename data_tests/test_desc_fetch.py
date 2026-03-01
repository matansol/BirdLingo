
import requests
import json
import re

def clean_description(text):
    if not text: return None
    # Remove text in parentheses (often scientific names or pronunciation)
    text = re.sub(r'\s*\([^)]*\)', '', text)
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_bird_description(scientific_name):
    # Using 'extracts' to get a summary
    # exintro=1: Return only content before the first section.
    # exsentences=3: Return first 3 sentences.
    # explaintext=1: Return plain text instead of HTML.
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": scientific_name,
        "exintro": 1,
        "exsentences": 3,
        "explaintext": 1,
        "redirects": 1
    }
    
    try:
        response = requests.get(url, params=params, headers={"User-Agent": "BirdLingoBot/1.0"})
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        
        for page_id in pages:
            if page_id == "-1": continue
            page = pages[page_id]
            if "extract" in page:
                return clean_description(page["extract"])
    except Exception as e:
        print(f"Error: {e}")
    return None

test_birds = [
    {"name": "Bittern", "scientific": "Botaurus stellaris"},
    {"name": "Puffin", "scientific": "Fratercula arctica"}
]

print("Testing Wikipedia Description API...")
for bird in test_birds:
    print(f"\n--- {bird['name']} ---")
    desc = get_bird_description(bird["scientific"])
    print(desc)
