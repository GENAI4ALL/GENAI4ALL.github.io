# Generate 64x64 PNG favicon from images/logo.png
# Usage (PowerShell):
#   python tools/make_favicon.py
# Requires: pip install pillow

from PIL import Image
from pathlib import Path

"""
Generate a single 64x64 PNG favicon from images/logo.png

Usage (PowerShell):
    python tools/make_favicon.py

Output:
        /favicon-64x64.png

Notes:
    - Auto-crops transparent margins to maximize visible area
    - Adds ~8% padding around the logo to avoid edge clipping
    - Uses high-quality LANCZOS resampling
"""

ROOT = Path(__file__).resolve().parents[1]
logo_png = ROOT / 'images' / 'logo.png'
output_png = ROOT / 'favicon-64x64.png'

if not logo_png.exists():
        raise SystemExit(f"Logo not found: {logo_png}")

img = Image.open(logo_png).convert('RGBA')

# 1) Auto-crop transparent margins to maximize visible area
alpha = img.split()[-1]
bbox = alpha.getbbox()
if bbox:
        img = img.crop(bbox)

# 2) Fit into a square canvas with small padding
max_side = max(img.width, img.height)
pad = int(0.08 * max_side)  # 8% padding
canvas_size = max_side + pad * 2
canvas = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
offset = ((canvas_size - img.width) // 2, (canvas_size - img.height) // 2)
canvas.paste(img, offset, img)

# 3) Resize to exactly 64x64 and save
favicon_64 = canvas.resize((64, 64), Image.LANCZOS)
favicon_64.save(output_png, format='PNG')
print(f"Wrote {output_png}")
