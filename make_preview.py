"""Generate social preview image (1200x630) from screenshot with title overlay."""
from PIL import Image, ImageDraw, ImageFont
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(SCRIPT_DIR, "Screenshot 2026-04-15 194728.png")
OUT = os.path.join(SCRIPT_DIR, "preview.png")

OG_W, OG_H = 1200, 630
TITLE = "How Much of Earth Have You Covered?"
SUBTITLE = "Visualize your travel footprint with a geographic bounding box"
BG_COLOR = (15, 20, 35)       # dark navy matching site bg
OVERLAY_COLOR = (0, 0, 0, 170)  # semi-transparent black strip

img = Image.new("RGB", (OG_W, OG_H), BG_COLOR)

# Load and fit screenshot into the upper portion
src = Image.open(SRC).convert("RGB")
src_w, src_h = src.size

# We'll reserve ~110px at bottom for text, fit screenshot into rest
text_strip_h = 120
map_h = OG_H - text_strip_h
scale = min(OG_W / src_w, map_h / src_h)
new_w = int(src_w * scale)
new_h = int(src_h * scale)
src_resized = src.resize((new_w, new_h), Image.LANCZOS)

# Center horizontally, align to top
x_off = (OG_W - new_w) // 2
img.paste(src_resized, (x_off, 0))

# Dark gradient strip at bottom
draw = ImageDraw.Draw(img)
# Gradient: fade the bottom edge of the screenshot into the bg color
for i in range(60):
    alpha = int(255 * (i / 60) ** 1.5)
    y = new_h - 60 + i
    if 0 <= y < OG_H:
        draw.rectangle([(0, y), (OG_W, y)], fill=(*BG_COLOR, alpha))

# Solid text area
draw.rectangle([(0, OG_H - text_strip_h), (OG_W, OG_H)], fill=BG_COLOR)

# --- Fonts ---
# Try to load a nice font, fall back to default
def load_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/times.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

font_title = load_font(38, bold=True)
font_sub   = load_font(22, bold=False)

GOLD  = (212, 175, 100)
LIGHT = (200, 200, 210)

# Draw title
title_bbox = draw.textbbox((0, 0), TITLE, font=font_title)
title_w = title_bbox[2] - title_bbox[0]
tx = (OG_W - title_w) // 2
ty = OG_H - text_strip_h + 16
draw.text((tx, ty), TITLE, font=font_title, fill=GOLD)

# Draw subtitle
sub_bbox = draw.textbbox((0, 0), SUBTITLE, font=font_sub)
sub_w = sub_bbox[2] - sub_bbox[0]
sx = (OG_W - sub_w) // 2
sy = ty + (title_bbox[3] - title_bbox[1]) + 10
draw.text((sx, sy), SUBTITLE, font=font_sub, fill=LIGHT)

img.save(OUT, "PNG", optimize=True)
print(f"Saved {OUT}  ({OG_W}x{OG_H})")
