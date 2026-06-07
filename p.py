import os
import random
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# --- CONFIGURATION ---
FONT_FILES = ["Jigmo.ttf", "Jigmo2.ttf", "Jigmo3.ttf"]
OUTPUT_DIR = Path("jigmo_dataset")
IMAGE_SIZE = (64, 64)

# Dataset volume requirements
IMAGES_PER_CHAR_TRAIN = 10
IMAGES_PER_CHAR_TEST = 10

# All 11 CJK Unicode Blocks (100,000+ characters)
CJK_RANGES = [
    (0x4E00, 0x9FFF),   (0x3400, 0x4DBF),   (0x20000, 0x2A6DF),
    (0x2A700, 0x2B73F), (0x2B740, 0x2B81F), (0x2B820, 0x2CEAF),
    (0x2CEB0, 0x2EBEF), (0x30000, 0x3134F), (0x31350, 0x323AF),
    (0x2EBF0, 0x2EE5F), (0x323B0, 0x3347F)
]

# Process-local cache to prevent repeated disk I/O
_FONT_CACHE = {}

def get_cached_font(font_path, size):
    key = (font_path, size)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = ImageFont.truetype(font_path, size)
    return _FONT_CACHE[key]

def apply_pipeline_variances(char, active_fonts):
    """
    Implements the 5 core variance types: 
    Size, Rotation, Translation, Weight, and Blur.
    """
    # 1. Variance: Font Size (28pt to 48pt, step 4)
    font_size = random.choice([28, 32, 36, 40, 44, 48])
    
    # Render on oversized canvas (96x96) to prevent clipping during rotation/shift
    pad = int(IMAGE_SIZE[0] * 1.5)
    img_large = Image.new("L", (pad, pad), color=255)
    draw = ImageDraw.Draw(img_large)
    
    rendered = False
    for f_path in active_fonts:
        font = get_cached_font(f_path, font_size)
        # Check if glyph exists in this font slice
        if font.getmask(char).getbbox() is not None:
            bbox = draw.textbbox((0, 0), char, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            # Center it
            x = (pad - w) // 2 - bbox[0]
            y = (pad - h) // 2 - bbox[1]
            draw.text((x, y), char, fill=0, font=font)
            rendered = True
            break
            
    if not rendered:
        return None

    # 2. Variance: Stroke Weight (30% Bold, 30% Thin, 40% Regular)
    weight_roll = random.random()
    if weight_roll < 0.30:
        img_large = img_large.filter(ImageFilter.MinFilter(3)) # Bold
    elif weight_roll < 0.60:
        img_large = img_large.filter(ImageFilter.MaxFilter(3)) # Thin

    # 3. Variance: Rotation (±8°)
    angle = random.uniform(-8, 8)
    img_rotated = img_large.rotate(angle, resample=Image.BICUBIC, fillcolor=255)
    
    # 4. Variance: Translation (±3 pixels X/Y jitter)
    shift_x = random.randint(-3, 3)
    shift_y = random.randint(-3, 3)
    
    # Crop 96x96 down to 64x64 using the jittered center
    start_x = (pad - IMAGE_SIZE[0]) // 2 + shift_x
    start_y = (pad - IMAGE_SIZE[1]) // 2 + shift_y
    final_img = img_rotated.crop((start_x, start_y, start_x + IMAGE_SIZE[0], start_y + IMAGE_SIZE[1]))
    
    # 5. Variance: Blur (Gaussian 0-0.6, 20% chance)
    if random.random() < 0.20:
        radius = random.uniform(0.1, 0.6)
        final_img = final_img.filter(ImageFilter.GaussianBlur(radius))
        
    return final_img

def worker_task(payload):
    """Execution unit for a single character class."""
    char, active_fonts, train_root, test_root = payload
    
    # Check if any font supports the glyph before creating folders
    supported = False
    for f in active_fonts:
        if get_cached_font(f, 24).getmask(char).getbbox() is not None:
            supported = True
            break
    if not supported:
        return False

    hex_id = f"U_{ord(char):05X}"
    t_dir = train_root / hex_id
    v_dir = test_root / hex_id
    
    t_dir.mkdir(exist_ok=True)
    v_dir.mkdir(exist_ok=True)
    
    # Generate Train Set (10 images)
    for i in range(IMAGES_PER_CHAR_TRAIN):
        img = apply_pipeline_variances(char, active_fonts)
        if img: img.save(t_dir / f"train_{i}.png")
            
    # Generate Test Set (10 images)
    for i in range(IMAGES_PER_CHAR_TEST):
        img = apply_pipeline_variances(char, active_fonts)
        if img: img.save(v_dir / f"test_{i}.png")
            
    return True

def main():
    # Detect available Jigmo parts
    active_fonts = [f for f in FONT_FILES if os.path.exists(f)]
    if not active_fonts:
        print("Error: No Jigmo .ttf files found. Place Jigmo.ttf, Jigmo2.ttf, and Jigmo3.ttf in this folder.")
        return

    # Expand ranges into a flat list of characters
    print("Expanding 100k+ Unicode targets...")
    all_chars = [chr(cp) for start, end in CJK_RANGES for cp in range(start, end + 1)]
    
    # Build directory structure
    train_root, test_root = OUTPUT_DIR / "train", OUTPUT_DIR / "test"
    train_root.mkdir(parents=True, exist_ok=True)
    test_root.mkdir(parents=True, exist_ok=True)

    print(f"Starting extremely fast parallel generation on {len(all_chars)} characters...")
    
    # Prepare task payloads
    tasks = [(c, active_fonts, train_root, test_root) for c in all_chars]
    
    success_count = 0
    with ProcessPoolExecutor() as executor:
        # chunksize=200 balances communication overhead and core utilization
        results = executor.map(worker_task, tasks, chunksize=200)
        
        for idx, result in enumerate(results):
            if result:
                success_count += 1
            if idx % 1000 == 0 and idx > 0:
                print(f"Progress: {idx}/{len(all_chars)} characters checked. Valid classes: {success_count}")

    print(f"\nFinished! Dataset ready in ./{OUTPUT_DIR}")
    print(f"Total Character Classes: {success_count}")
    print(f"Total Images Generated: {success_count * 20}")

if __name__ == "__main__":
    main()