#!/usr/bin/env python3
"""Single-slide 16:9 PPT with full infographic embedded."""

from pathlib import Path
import shutil

from pptx import Presentation
from pptx.util import Inches

ASSETS = Path(__file__).resolve().parent.parent / "assets"
# 1920x1080 PNG — true 16:9, no stretch on widescreen slide
INFOGRAPHIC_16x9 = ASSETS / "ai-industry-chain-infographic-zh-16x9.png"
SOURCE = Path("/opt/cursor/artifacts/assets/ai-industry-chain-infographic-zh.png")

# Standard PowerPoint widescreen 16:9 (13.333" × 7.5")
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def ensure_16x9_png():
    ASSETS.mkdir(parents=True, exist_ok=True)
    if INFOGRAPHIC_16x9.exists():
        return INFOGRAPHIC_16x9

    from PIL import Image

    src = ASSETS / "ai-industry-chain-infographic-zh.png"
    if not src.exists() and SOURCE.exists():
        shutil.copy2(SOURCE, src)
    if not src.exists():
        raise FileNotFoundError("Source infographic PNG missing")

    img = Image.open(src)
    tw, th = 1920, 1080
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    out = resized.crop((left, top, left + tw, top + th))
    out.save(INFOGRAPHIC_16x9)
    return INFOGRAPHIC_16x9


def main():
    png = ensure_16x9_png()

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.shapes.add_picture(str(png), 0, 0, width=SLIDE_W, height=SLIDE_H)

    outputs = [
        Path("/workspace/AI-industry-chain-infographic-16x9.pptx"),
        Path("/workspace/output/AI产业链信息图-16x9.pptx"),
    ]
    for out in outputs:
        prs.save(str(out))
        print(f"Saved: {out} ({out.stat().st_size} bytes) — slide 16:9, image 1920×1080")


if __name__ == "__main__":
    main()
