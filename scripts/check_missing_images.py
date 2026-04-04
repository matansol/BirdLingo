"""Check which image files referenced in birdImages.js don't exist on disk."""
import re
import os

JS_PATH = os.path.join("BirdLingo", "assets", "birdImages.js")
BASE_DIR = os.path.join("BirdLingo", "assets")

with open(JS_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Extract all paths from require('./birds/...')
paths = re.findall(r"require\(['\"](\./[^'\"]+)['\"]\)", content)
print(f"Total require() references: {len(paths)}")

missing = []
for p in paths:
    rel = p.replace("./", "", 1)  # strip leading ./
    full = os.path.join(BASE_DIR, rel)
    if not os.path.exists(full):
        missing.append(full.replace("\\", "/"))

print(f"Missing files: {len(missing)}\n")
for m in missing:
    print(m)

if not missing:
    print("All referenced files exist!")
