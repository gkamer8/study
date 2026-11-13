"""Render every SVG in figures/ to PNG for visual checking (not deployed)."""
import os, sys, glob, cairosvg
from figlib import OUT
dst = sys.argv[1] if len(sys.argv) > 1 else "/workspace/figrender"
os.makedirs(dst, exist_ok=True)
pat = sys.argv[2] if len(sys.argv) > 2 else "*"
for f in sorted(glob.glob(os.path.join(OUT, pat + ".svg"))):
    out = os.path.join(dst, os.path.basename(f)[:-4] + ".png")
    cairosvg.svg2png(url=f, write_to=out, output_width=900)
    print(out)
