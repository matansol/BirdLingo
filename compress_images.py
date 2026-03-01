import os
from PIL import Image
from pathlib import Path

# Configuration
BIRDS_DIR = Path(r'c:\Users\matan\Documents\BirdWho_ag\BirdLingo\assets\birds')
MAX_WIDTH = 800  # Max width in pixels
MAX_HEIGHT = 800  # Max height in pixels
JPEG_QUALITY = 70  # JPEG quality (1-100, lower = smaller file)

def compress_image(image_path):
    """Compress a single image file."""
    try:
        with Image.open(image_path) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Get original size
            original_size = os.path.getsize(image_path)
            width, height = img.size
            
            # Resize if needed
            if width > MAX_WIDTH or height > MAX_HEIGHT:
                img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
                width, height = img.size
            
            # Save with compression
            img.save(image_path, 'JPEG', quality=JPEG_QUALITY, optimize=True, progressive=True)
            
            new_size = os.path.getsize(image_path)
            reduction = ((original_size - new_size) / original_size) * 100
            
            return original_size, new_size, reduction, width, height
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None, None, None, None, None

def main():
    total_original = 0
    total_new = 0
    count = 0
    
    print(f"Compressing images in: {BIRDS_DIR}")
    print(f"Max dimensions: {MAX_WIDTH}x{MAX_HEIGHT}px")
    print(f"JPEG quality: {JPEG_QUALITY}\n")
    
    # Find all image files
    for bird_folder in BIRDS_DIR.iterdir():
        if bird_folder.is_dir():
            for image_file in bird_folder.glob('*.jpg'):
                orig, new, reduction, w, h = compress_image(image_file)
                if orig is not None:
                    total_original += orig
                    total_new += new
                    count += 1
                    print(f"✓ {image_file.name}: {orig/1024:.0f}KB → {new/1024:.0f}KB ({reduction:.1f}% reduction, {w}x{h}px)")
    
    print(f"\n{'='*60}")
    print(f"Processed: {count} images")
    print(f"Total size: {total_original/1024/1024:.1f}MB → {total_new/1024/1024:.1f}MB")
    print(f"Total reduction: {((total_original - total_new) / total_original) * 100:.1f}%")
    print(f"Space saved: {(total_original - total_new)/1024/1024:.1f}MB")

if __name__ == '__main__':
    input("This will modify all bird images. Press Enter to continue or Ctrl+C to cancel...")
    main()
