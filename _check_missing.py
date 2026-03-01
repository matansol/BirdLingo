"""Find missing image references in birdImages.js."""
import re
from pathlib import Path

BASE = Path(__file__).parent
f = (BASE / "BirdLingo" / "assets" / "birdImages.js").read_text(encoding="utf-8")
paths = re.findall(r"require\('\./birds/([^']+)'\)", f)
base = BASE / "BirdLingo" / "assets"
missing = [p for p in paths if not (base / "birds" / p).exists()]
print(f"Total requires: {len(paths)}")
print(f"Missing: {len(missing)}")
for m in missing:
    print(f"  {m}")
