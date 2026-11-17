import sys, pathlib
from PIL import Image, ImageDraw
d = pathlib.Path(sys.argv[1]); out = sys.argv[2]
fs = sorted(d.glob("t*.png")); cols = 3; w, h = 640, 360
sheet = Image.new("RGB", (cols * w, ((len(fs) + cols - 1) // cols) * h), "black")
for i, f in enumerate(fs):
    im = Image.open(f).convert("RGB").resize((w, h)); ImageDraw.Draw(im).text((8, 8), f"{i+1}: {f.stem}", fill=(255, 255, 0))
    sheet.paste(im, ((i % cols) * w, (i // cols) * h))
sheet.save(out)
