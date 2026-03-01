
import requests
import json

def get_wiki_image(scientific_name):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": scientific_name,
        "prop": "pageimages",
        "piprop": "original",
        "redirects": 1
    }
    
    try:
        response = requests.get(url, params=params, headers={"User-Agent": "BirdLingoBot/1.0"})
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        
        for page_id in pages:
            page = pages[page_id]
            if "original" in page:
                return page["original"]["source"]
    except Exception as e:
        print(f"Error: {e}")
    return None

test_birds = [
    {"name": "Bittern", "scientific": "Botaurus stellaris"},
    {"name": "Puffin", "scientific": "Fratercula arctica"}
]

print("Testing Wikipedia API fetch...")
for bird in test_birds:
    url = get_wiki_image(bird["scientific"])
    print(f"Bird: {bird['name']} ({bird['scientific']})")
    print(f"Image URL: {url}")
