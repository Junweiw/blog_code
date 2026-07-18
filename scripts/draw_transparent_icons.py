#!/usr/bin/env python3
"""Draw clean transparent circular icons for the AI industry-chain PPT."""

from pathlib import Path
import math

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
DEST_ICONS = ROOT / "assets" / "ppt-parts" / "icons"
DEST_METRICS = ROOT / "assets" / "ppt-parts" / "metrics"

BLUE = (59, 130, 246, 255)
WHITE = (255, 255, 255, 255)
SIZE = 256


def blank():
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def draw_ring(draw, cx, cy, r_outer, thickness=14):
    bbox = [cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer]
    draw.ellipse(bbox, outline=BLUE, width=thickness)


def icon_compute(path):
    img = blank()
    d = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    draw_ring(d, cx, cy, 110, 14)
    body = [cx - 36, cy - 36, cx + 36, cy + 36]
    d.rounded_rectangle(body, radius=8, outline=WHITE, width=6)
    for i in range(-2, 3):
        off = i * 12
        d.rectangle([cx + off - 3, cy - 50, cx + off + 3, cy - 36], fill=WHITE)
        d.rectangle([cx + off - 3, cy + 36, cx + off + 3, cy + 50], fill=WHITE)
        d.rectangle([cx - 50, cy + off - 3, cx - 36, cy + off + 3], fill=WHITE)
        d.rectangle([cx + 36, cy + off - 3, cx + 50, cy + off + 3], fill=WHITE)
    d.rectangle([cx - 14, cy - 14, cx + 14, cy + 14], outline=WHITE, width=3)
    img.save(path)


def icon_infra(path):
    img = blank()
    d = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    draw_ring(d, cx, cy, 110, 14)
    d.ellipse([cx - 50, cy - 20, cx + 10, cy + 30], fill=WHITE)
    d.ellipse([cx - 20, cy - 40, cx + 40, cy + 20], fill=WHITE)
    d.ellipse([cx + 5, cy - 15, cx + 55, cy + 30], fill=WHITE)
    d.rectangle([cx - 45, cy, cx + 50, cy + 28], fill=WHITE)
    for y in (cy + 38, cy + 50):
        d.rounded_rectangle([cx - 28, y, cx + 28, y + 10], radius=2, outline=BLUE, width=2)
    img.save(path)


def icon_model(path):
    img = blank()
    d = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    draw_ring(d, cx, cy, 110, 14)
    d.ellipse([cx - 48, cy - 40, cx + 5, cy + 42], outline=WHITE, width=5)
    d.ellipse([cx - 5, cy - 40, cx + 48, cy + 42], outline=WHITE, width=5)
    nodes = [(cx - 20, cy - 10), (cx + 18, cy - 8), (cx, cy + 12), (cx - 10, cy + 28), (cx + 15, cy + 25)]
    for i in range(len(nodes) - 1):
        d.line([nodes[i], nodes[i + 1]], fill=WHITE, width=2)
    d.line([nodes[0], nodes[2]], fill=WHITE, width=2)
    for x, y in nodes:
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=WHITE)
    img.save(path)


def icon_agent(path):
    img = blank()
    d = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    draw_ring(d, cx, cy, 110, 14)
    pts = [
        (cx, cy - 35),
        (cx - 40, cy + 10),
        (cx + 40, cy + 10),
        (cx - 15, cy + 40),
        (cx + 15, cy + 40),
        (cx, cy),
    ]
    edges = [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (1, 3), (2, 4), (0, 1), (0, 2)]
    for a, b in edges:
        d.line([pts[a], pts[b]], fill=WHITE, width=3)
    for x, y in pts:
        d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=WHITE)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=BLUE)
    img.save(path)


def icon_app(path):
    img = blank()
    d = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    draw_ring(d, cx, cy, 110, 14)
    d.ellipse([cx - 28, cy - 48, cx + 28, cy + 8], outline=WHITE, width=5)
    d.rectangle([cx - 14, cy + 8, cx + 14, cy + 22], outline=WHITE, width=4)
    d.line([cx - 10, cy + 28, cx + 10, cy + 28], fill=WHITE, width=4)
    d.line([cx - 8, cy + 34, cx + 8, cy + 34], fill=WHITE, width=3)
    for ang in (-50, -25, 25, 50):
        rad = math.radians(ang - 90)
        x1 = cx + 38 * math.cos(rad)
        y1 = cy - 10 + 38 * math.sin(rad)
        x2 = cx + 52 * math.cos(rad)
        y2 = cy - 10 + 52 * math.sin(rad)
        d.line([(x1, y1), (x2, y2)], fill=WHITE, width=3)
    img.save(path)


def metric_capex(path):
    img = blank()
    d = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    draw_ring(d, cx, cy, 110, 12)
    base = cy + 35
    heights = [25, 40, 55, 75]
    x0 = cx - 40
    for i, h in enumerate(heights):
        x = x0 + i * 22
        d.rectangle([x, base - h, x + 14, base], fill=WHITE)
    d.line([(cx - 35, cy + 20), (cx + 35, cy - 35)], fill=WHITE, width=4)
    d.polygon([(cx + 35, cy - 35), (cx + 18, cy - 32), (cx + 32, cy - 18)], fill=WHITE)
    img.save(path)


def metric_latency(path):
    img = blank()
    d = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    draw_ring(d, cx, cy, 110, 12)
    bbox = [cx - 45, cy - 40, cx + 45, cy + 50]
    d.arc(bbox, start=200, end=340, fill=WHITE, width=6)
    d.line([(cx, cy + 10), (cx + 28, cy - 25)], fill=WHITE, width=5)
    d.ellipse([cx - 6, cy + 4, cx + 6, cy + 16], fill=WHITE)
    img.save(path)


def metric_unit(path):
    img = blank()
    d = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    draw_ring(d, cx, cy, 110, 12)
    d.rounded_rectangle([cx - 36, cy - 48, cx + 36, cy + 48], radius=6, outline=WHITE, width=5)
    d.rectangle([cx - 24, cy - 36, cx + 24, cy - 18], outline=WHITE, width=3)
    for row in range(3):
        for col in range(3):
            x = cx - 22 + col * 16
            y = cy - 6 + row * 16
            d.rectangle([x, y, x + 10, y + 10], fill=WHITE)
    img.save(path)


def metric_pmf(path):
    img = blank()
    d = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    draw_ring(d, cx, cy, 110, 12)
    for r, w in [(48, 5), (30, 5), (14, 5)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=w)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=WHITE)
    img.save(path)


def main():
    DEST_ICONS.mkdir(parents=True, exist_ok=True)
    DEST_METRICS.mkdir(parents=True, exist_ok=True)
    icon_compute(DEST_ICONS / "01-compute.png")
    icon_infra(DEST_ICONS / "02-infra.png")
    icon_model(DEST_ICONS / "03-model.png")
    icon_agent(DEST_ICONS / "04-agent.png")
    icon_app(DEST_ICONS / "05-app.png")
    metric_capex(DEST_METRICS / "01-capex.png")
    metric_latency(DEST_METRICS / "02-latency.png")
    metric_unit(DEST_METRICS / "03-unit.png")
    metric_pmf(DEST_METRICS / "04-pmf.png")
    print(f"Wrote icons to {DEST_ICONS} and {DEST_METRICS}")


if __name__ == "__main__":
    main()
