#!/usr/bin/env python3
"""
Assemble editable 16:9 AI industry-chain PPT from discrete assets.

Layer order (bottom → top):
  background → header bar → title/subtitle text →
  5 column cards → per column: title, tagline, icon image, hero image →
  footer bar → slogan text → metric icons + labels
"""

from pathlib import Path
import shutil

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
PARTS = ROOT / "assets" / "ppt-parts"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

NAVY = RGBColor(10, 22, 40)
NAVY_CARD = RGBColor(14, 28, 50)
NAVY_BAR = RGBColor(18, 35, 60)
GOLD = RGBColor(245, 197, 24)
WHITE = RGBColor(255, 255, 255)
GRAY = RGBColor(180, 190, 210)
CARD_LINE = RGBColor(30, 55, 90)
FONT = "Microsoft YaHei"

COLUMNS = [
    {
        "title": "算力层",
        "tagline": "生于硅片，GPU 与 HBM\n驱动一切。",
        "icon": PARTS / "icons" / "01-compute.png",
        "hero": PARTS / "heroes" / "01-compute.png",
    },
    {
        "title": "基础设施层",
        "tagline": "电力、液冷与万卡\n集群规模化。",
        "icon": PARTS / "icons" / "02-infra.png",
        "hero": PARTS / "heroes" / "02-infra.png",
    },
    {
        "title": "模型层",
        "tagline": "数据训练，算力炼成\n认知能力。",
        "icon": PARTS / "icons" / "03-model.png",
        "hero": PARTS / "heroes" / "03-model.png",
    },
    {
        "title": "智能体层",
        "tagline": "工具编排，自主规划\n与闭环执行。",
        "icon": PARTS / "icons" / "04-agent.png",
        "hero": PARTS / "heroes" / "04-agent.png",
    },
    {
        "title": "应用层",
        "tagline": "落地千行百业，\n嵌入日常工作。",
        "icon": PARTS / "icons" / "05-app.png",
        "hero": PARTS / "heroes" / "05-app.png",
    },
]

METRICS = [
    {"label": "资本开支", "icon": PARTS / "metrics" / "01-capex.png"},
    {"label": "推理延迟", "icon": PARTS / "metrics" / "02-latency.png"},
    {"label": "单位经济", "icon": PARTS / "metrics" / "03-unit.png"},
    {"label": "产品契合", "icon": PARTS / "metrics" / "04-pmf.png"},
]


def set_fill(shape, color):
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(
    slide,
    left,
    top,
    width,
    height,
    text,
    size=14,
    bold=False,
    color=WHITE,
    align=PP_ALIGN.LEFT,
    anchor=MSO_ANCHOR.TOP,
):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    # Clear default empty run and write multi-line text
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = align
        p.font.name = FONT
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.space_after = Pt(2)
    return box


def require_assets():
    missing = []
    for col in COLUMNS:
        for key in ("icon", "hero"):
            if not col[key].exists():
                missing.append(str(col[key]))
    for m in METRICS:
        if not m["icon"].exists():
            missing.append(str(m["icon"]))
    if missing:
        raise FileNotFoundError("Missing assets:\n" + "\n".join(missing))


def build_editable_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    sw, sh = prs.slide_width, prs.slide_height

    # 1) Background
    bg = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, sw, sh)
    set_fill(bg, NAVY)
    bg.line.fill.background()

    # 2) Header bar + title / subtitle text boxes
    header_h = Inches(1.45)
    header = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, sw, header_h)
    set_fill(header, NAVY_BAR)
    header.line.fill.background()

    add_textbox(
        slide,
        Inches(0.4),
        Inches(0.25),
        Inches(12.4),
        Inches(0.6),
        "做 AI 投资？最大的差异不是模型，而是产业链。",
        size=28,
        bold=True,
    )
    add_textbox(
        slide,
        Inches(0.4),
        Inches(0.9),
        Inches(12.4),
        Inches(0.4),
        "五层结构，一条链条，价值从芯片流向应用。",
        size=15,
        color=GRAY,
    )

    # 3) Five column cards
    col_top = Inches(1.65)
    col_h = Inches(4.5)
    margin_x = Inches(0.3)
    gap = Inches(0.16)
    col_w = (sw - 2 * margin_x - 4 * gap) / 5

    for i, col in enumerate(COLUMNS):
        left = margin_x + i * (col_w + gap)

        # Card shape
        card = slide.shapes.add_shape(
            MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, left, col_top, col_w, col_h
        )
        set_fill(card, NAVY_CARD)
        card.line.color.rgb = CARD_LINE
        card.line.width = Pt(1)
        try:
            card.adjustments[0] = 0.08
        except Exception:
            pass

        # Title (editable text)
        add_textbox(
            slide,
            left + Inches(0.08),
            col_top + Inches(0.12),
            col_w - Inches(0.16),
            Inches(0.4),
            col["title"],
            size=18,
            bold=True,
            align=PP_ALIGN.CENTER,
        )

        # Tagline (editable text)
        add_textbox(
            slide,
            left + Inches(0.08),
            col_top + Inches(0.52),
            col_w - Inches(0.16),
            Inches(0.7),
            col["tagline"],
            size=11,
            color=GRAY,
            align=PP_ALIGN.CENTER,
        )

        # Icon image (replaceable)
        icon_size = Inches(0.72)
        icon_left = left + (col_w - icon_size) / 2
        icon_top = col_top + Inches(1.3)
        slide.shapes.add_picture(
            str(col["icon"]), icon_left, icon_top, width=icon_size, height=icon_size
        )

        # Hero image (replaceable)
        hero_left = left + Inches(0.12)
        hero_top = col_top + Inches(2.2)
        hero_w = col_w - Inches(0.24)
        hero_h = Inches(2.05)
        slide.shapes.add_picture(
            str(col["hero"]), hero_left, hero_top, width=hero_w, height=hero_h
        )

    # 4) Footer bar
    footer_top = Inches(6.35)
    footer_h = Inches(1.05)
    footer = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, footer_top, sw, footer_h
    )
    set_fill(footer, NAVY_BAR)
    footer.line.fill.background()

    # Slogan (two-run text: white + gold)
    slogan_box = slide.shapes.add_textbox(
        Inches(0.4), footer_top + Inches(0.28), Inches(6.8), Inches(0.55)
    )
    tf = slogan_box.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    r1 = p.add_run()
    r1.text = "同一技术，不同层级。"
    r1.font.name = FONT
    r1.font.size = Pt(14)
    r1.font.color.rgb = WHITE
    r2 = p.add_run()
    r2.text = "看懂产业链，才能抓住价值。"
    r2.font.name = FONT
    r2.font.size = Pt(14)
    r2.font.bold = True
    r2.font.color.rgb = GOLD

    # Metric icons + labels
    metric_start = Inches(7.6)
    metric_w = Inches(1.3)
    metric_gap = Inches(0.15)
    icon_sz = Inches(0.4)
    for j, m in enumerate(METRICS):
        x = metric_start + j * (metric_w + metric_gap)
        y = footer_top + Inches(0.12)
        slide.shapes.add_picture(str(m["icon"]), x + Inches(0.4), y, width=icon_sz, height=icon_sz)
        add_textbox(
            slide,
            x,
            y + Inches(0.45),
            metric_w,
            Inches(0.35),
            m["label"],
            size=11,
            align=PP_ALIGN.CENTER,
            color=GRAY,
        )


def main():
    require_assets()

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    build_editable_slide(prs)

    out_root = ROOT / "AI-industry-chain-editable-16x9.pptx"
    out_dir = ROOT / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_cn = out_dir / "AI产业链信息图-可编辑-16x9.pptx"

    prs.save(str(out_root))
    shutil.copy2(out_root, out_cn)

    # Sanity check
    check = Presentation(str(out_root))
    slide = check.slides[0]
    pics = sum(1 for s in slide.shapes if s.shape_type == 13)
    texts = sum(1 for s in slide.shapes if s.has_text_frame and s.text.strip())
    shapes = len(slide.shapes)
    print(f"Saved: {out_root} ({out_root.stat().st_size} bytes)")
    print(f"  16:9 ratio = {check.slide_width / check.slide_height:.4f}")
    print(f"  shapes={shapes}, pictures={pics}, text_boxes={texts}")
    print(f"  Expected pictures: 5 icons + 5 heroes + 4 metrics = 14")


if __name__ == "__main__":
    main()
