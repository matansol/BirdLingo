"""
Sync JSON files with actual images on disk.
Scans assets/birds/ folders and updates the images arrays in both JSON files.
"""

from pathlib import Path
import json

BASE_DIR = Path(__file__).parent.parent
BIRDS_DIR = BASE_DIR / "assets" / "birds"
BIRDS_INFO = BASE_DIR / "../data/birds_info.json"
BIRDS_DATA = BASE_DIR / "assets" / "birds_data.json"

def scan_bird_images(bird_slug):
    """Scan a bird folder and return list of image filenames"""
    bird_dir = BIRDS_DIR / bird_slug
    if not bird_dir.exists():
        return []
    
    # Find all jpg/jpeg/png files
    images = []
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        images.extend([f.name for f in bird_dir.glob(ext)])
    
    # Sort by name
    return sorted(images)

def update_birds_info_json():
    """Update birds_info.json with actual images on disk"""
    with open(BIRDS_INFO, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updates = 0
    for bird_slug, bird_data in data.items():
        # Skip group entries — they aggregate images from member birds, no physical folder
        if bird_data.get('isGroup'):
            continue
        actual_images = scan_bird_images(bird_slug)
        old_images = bird_data.get('images', [])
        
        if actual_images != old_images:
            bird_data['images'] = actual_images
            updates += 1
            print(f"✓ {bird_slug}: {len(old_images)} → {len(actual_images)} images")
    
    # Save
    with open(BIRDS_INFO, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return updates

def update_birds_data_json():
    """Update assets/birds_data.json with actual images on disk"""
    with open(BIRDS_DATA, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updates = 0
    for bird in data:
        bird_slug = bird.get('image', '')
        if not bird_slug:
            continue
        
        actual_images = scan_bird_images(bird_slug)
        old_images = bird.get('images', [])
        
        if actual_images != old_images:
            bird['images'] = actual_images
            updates += 1
            print(f"✓ {bird_slug}: {len(old_images)} → {len(actual_images)} images")
    
    # Save
    with open(BIRDS_DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return updates

def regenerate_bird_images_js():
    """Regenerate assets/birdImages.js from actual images on disk"""
    output = []
    output.append("// Auto-generated file - do not edit manually")
    output.append("// Run sync_images.py to regenerate")
    output.append("")
    output.append("const birdImages = {")
    
    # Get all bird folders
    bird_folders = sorted([d.name for d in BIRDS_DIR.iterdir() if d.is_dir()])
    
    for bird_slug in bird_folders:
        images = scan_bird_images(bird_slug)
        if images:
            # JavaScript array format
            images_str = ', '.join([f'"{img}"' for img in images])
            output.append(f'  "{bird_slug}": [{images_str}],')
    
    output.append("};")
    output.append("")
    output.append("export default birdImages;")
    
    # Write to file
    js_file = BASE_DIR / "assets" / "birdImages.js"
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    return len(bird_folders)

def main():
    print("Syncing images with JSON files...\n")
    
    print("1. Updating birds_info.json...")
    count1 = update_birds_info_json()
    print(f"   Updated {count1} birds\n")
    
    print("2. Updating assets/birds_data.json...")
    count2 = update_birds_data_json()
    print(f"   Updated {count2} birds\n")
    
    print("3. Regenerating assets/birdImages.js...")
    count3 = regenerate_bird_images_js()
    print(f"   Generated for {count3} birds\n")
    
    print("✓ All files synced with actual images on disk!")

if __name__ == "__main__":
    main()
