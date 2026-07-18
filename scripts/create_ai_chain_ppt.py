#!/usr/bin/env python3
"""Generate editable AI industry chain infographic PPT (Chinese)."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

# Colors
NAVY = RGBColor(10, 22, 40)
NAVY_LIGHT = RGBColor(18, 35, 60)
GOLD = RGBColor(245, 197, 24)
WHITE = RGBColor(255, 255, 255)
BLUE_ICON = RGBColor(59, 130, 246)
GRAY = RGBColor(180, 190, 210)

FONT = "Microsoft YaHei"

COLUMNS = [
    {
        "title": "算力层",
        "tagline": "生于硅片，GPU 与 HBM\n驱动一切。",
        "icon": "芯",
    },
    {
        "title": "基础设施层",
        "tagline": "电力、液冷与万卡\n集群规模化。",
        "icon": "云",
    },
    {
        "title": "模型层",
        "tagline": "数据训练，算力炼成\n认知能力。",
        "icon": "脑",
    },
    {
        "title": "智能体层",
        "tagline": "工具编排，自主规划\n与闭环执行。",
        "icon": "链",
    },
    {
        "title": "应用层",
        "tagline": "落地千行百业，\n嵌入日常工作。",
        "icon": "用",
    },
]

METRICS = ["资本开支", "推理延迟", "单位经济", "产品契合"]


def set_fill(shape, color):
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, left, top, width, height, text, size=14, bold=False, color=WHITE, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    p.font.name = FONT
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    return box


def add_rich_textbox(slide, left, top, width, height, parts, size=14, align=PP_ALIGN.LEFT):
    """parts: list of (text, color, bold)"""
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = align
    for i, (text, color, bold) in enumerate(parts):
        run = p.add_run() if i else p.runs[0] if p.runs else p.add_run()
        if i == 0 and not p.runs:
            run = p.add_run()
        elif i > 0:
            run = p.add_run()
        elif p.runs:
            run = p.runs[0]
        else:
            run = p.add_run()
        run.text = text
        run.font.name = FONT
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
    return box


def build_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    slide_w = prs.slide_width
    slide_h = prs.slide_height

    # Full slide background
    bg = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, slide_w, slide_h)
    set_fill(bg, NAVY)
    bg.line.fill.background()

    # Header band
    header_h = Inches(1.55)
    header = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, slide_w, header_h)
    set_fill(header, NAVY_LIGHT)
    header.line.fill.background()

    add_textbox(
        slide,
        Inches(0.45),
        Inches(0.28),
        Inches(12.0),
        Inches(0.65),
        "做 AI 投资？最大的差异不是模型，而是产业链。",
        size=28,
        bold=True,
    )
    add_textbox(
        slide,
        Inches(0.45),
        Inches(0.95),
        Inches(12.0),
        Inches(0.4),
        "五层结构，一条链条，价值从芯片流向应用。",
        size=16,
        color=GRAY,
    )

    # Column layout
    col_top = Inches(1.75)
    col_h = Inches(4.35)
    margin_x = Inches(0.35)
    gap = Inches(0.18)
    total_w = slide_w - 2 * margin_x
    col_w = (total_w - 4 * gap) // 5

    for i, col in enumerate(COLUMNS):
        left = margin_x + i * (col_w + gap)

        card = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, left, col_top, col_w, col_h)
        set_fill(card, RGBColor(14, 28, 50))
        card.line.color.rgb = RGBColor(30, 55, 90)
        card.line.width = Pt(1)

        add_textbox(
            slide,
            left + Inches(0.12),
            col_top + Inches(0.15),
            col_w - Inches(0.24),
            Inches(0.45),
            col["title"],
            size=20,
            bold=True,
            align=PP_ALIGN.CENTER,
        )

        add_textbox(
            slide,
            left + Inches(0.1),
            col_top + Inches(0.62),
            col_w - Inches(0.2),
            Inches(0.75),
            col["tagline"],
            size=12,
            color=GRAY,
            align=PP_ALIGN.CENTER,
        )

        icon_size = Inches(0.72)
        icon_left = left + (col_w - icon_size) // 2
        icon_top = col_top + Inches(1.55)
        circle = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, icon_left, icon_top, icon_size, icon_size)
        set_fill(circle, BLUE_ICON)
        circle.line.fill.background()

        icon_box = slide.shapes.add_textbox(icon_left, icon_top + Inches(0.12), icon_size, icon_size - Inches(0.24))
        tf = icon_box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = col["icon"]
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = WHITE

        # Placeholder image area (editable rectangle)
        img_top = col_top + Inches(2.45)
        img_h = Inches(1.65)
        img_area = slide.shapes.add_shape(
            MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
            left + Inches(0.15),
            img_top,
            col_w - Inches(0.3),
            img_h,
        )
        set_fill(img_area, RGBColor(22, 40, 68))
        img_area.line.color.rgb = RGBColor(45, 75, 120)
        img_area.line.width = Pt(0.75)

        add_textbox(
            slide,
            left + Inches(0.15),
            img_top + Inches(0.55),
            col_w - Inches(0.3),
            Inches(0.5),
            "← 可替换图片",
            size=10,
            color=RGBColor(100, 130, 170),
            align=PP_ALIGN.CENTER,
        )

    # Footer band
    footer_top = Inches(6.35)
    footer_h = Inches(1.05)
    footer = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, footer_top, slide_w, footer_h)
    set_fill(footer, NAVY_LIGHT)
    footer.line.fill.background()

    # Footer left message
    msg_box = slide.shapes.add_textbox(Inches(0.45), footer_top + Inches(0.28), Inches(7.2), Inches(0.55))
    tf = msg_box.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    run1 = p.add_run()
    run1.text = "同一技术，不同层级。"
    run1.font.name = FONT
    run1.font.size = Pt(15)
    run1.font.color.rgb = WHITE
    run2 = p.add_run()
    run2.text = "看懂产业链，才能抓住价值。"
    run2.font.name = FONT
    run2.font.size = Pt(15)
    run2.font.bold = True
    run2.font.color.rgb = GOLD

    # Footer metrics
    metric_w = Inches(1.35)
    metric_start = Inches(8.1)
    metric_gap = Inches(0.25)
    for j, label in enumerate(METRICS):
        mx = metric_start + j * (metric_w + metric_gap)
        my = footer_top + Inches(0.18)

        m_circle = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, mx, my, Inches(0.42), Inches(0.42))
        set_fill(m_circle, RGBColor(30, 55, 90))
        m_circle.line.color.rgb = BLUE_ICON
        m_circle.line.width = Pt(1)

        add_textbox(slide, mx - Inches(0.05), my + Inches(0.48), metric_w, Inches(0.35), label, size=11, align=PP_ALIGN.CENTER)


def build_reference_slide(prs, image_path: Path):
    """Second slide with the generated PNG for visual reference."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    set_fill(bg, NAVY)
    bg.line.fill.background()

    add_textbox(
        slide,
        Inches(0.4),
        Inches(0.2),
        Inches(10),
        Inches(0.4),
        "参考图（第 1 页为可编辑版本）",
        size=14,
        color=GRAY,
    )

    if image_path.exists():
        slide.shapes.add_picture(str(image_path), Inches(0.2), Inches(0.55), width=Inches(12.9))


def main():
    out_dir = Path("/workspace/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "AI产业链信息图-可编辑.pptx"
    image_path = Path("/opt/cursor/artifacts/assets/ai-industry-chain-infographic-zh.png")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    build_slide(prs)
    build_reference_slide(prs, image_path)

    prs.save(str(out_path))
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
