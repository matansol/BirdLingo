"""Regenerate birdImages.js from actual files on disk."""
from pathlib import Path
import os

BASE = Path(__file__).parent
BIRDS_DIR = BASE / "BirdLingo" / "assets" / "birds"
OUT = BASE / "BirdLingo" / "assets" / "birdImages.js"

os.chdir(BASE)

lines = [
    "// Bird image imports - generated from actual files on disk",
    "// Each bird has multiple images in subdirectories",
    "",
    "const birdImages = {",
]

bird_dirs = sorted([d for d in BIRDS_DIR.iterdir() if d.is_dir() and d.name != "backup_images"])

total = 0
for bd in bird_dirs:
    slug = bd.name
    imgs = sorted(bd.glob("*.jpg"))
    if not imgs:
        continue
    parts = []
    for img in imgs:
        parts.append(f"require('./birds/{slug}/{img.name}')")
    requires = ", ".join(parts)
    lines.append(f"  {slug}: [{requires}],")
    total += len(imgs)

lines.append("};")
lines.append("")
lines.append("export default birdImages;")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"Generated birdImages.js: {len(bird_dirs)} birds, {total} images")
