#!/usr/bin/env python3
"""Generate AI industry chain PPT with embedded infographic images."""

from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

NAVY = RGBColor(10, 22, 40)
NAVY_LIGHT = RGBColor(18, 35, 60)
GOLD = RGBColor(245, 197, 24)
WHITE = RGBColor(255, 255, 255)
BLUE_ICON = RGBColor(59, 130, 246)
GRAY = RGBColor(180, 190, 210)
FONT = "Microsoft YaHei"

ASSETS = Path(__file__).resolve().parent.parent / "assets"
INFOGRAPHIC = ASSETS / "ai-industry-chain-infographic-zh.png"
COLUMNS_DIR = ASSETS / "column-crops"

COLUMNS = [
    {"title": "算力层", "tagline": "生于硅片，GPU 与 HBM\n驱动一切。", "icon": "芯"},
    {"title": "基础设施层", "tagline": "电力、液冷与万卡\n集群规模化。", "icon": "云"},
    {"title": "模型层", "tagline": "数据训练，算力炼成\n认知能力。", "icon": "脑"},
    {"title": "智能体层", "tagline": "工具编排，自主规划\n与闭环执行。", "icon": "链"},
    {"title": "应用层", "tagline": "落地千行百业，\n嵌入日常工作。", "icon": "用"},
]
METRICS = ["资本开支", "推理延迟", "单位经济", "产品契合"]

# Crop boxes tuned for 1536x1024 generated infographic (left, top, right, bottom) as fractions
COLUMN_CROP_FRAC = [
    (0.025, 0.50, 0.195, 0.88),
    (0.210, 0.50, 0.385, 0.88),
    (0.400, 0.50, 0.575, 0.88),
    (0.590, 0.50, 0.765, 0.88),
    (0.780, 0.50, 0.975, 0.88),
]


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


def ensure_assets(source: Path):
    ASSETS.mkdir(parents=True, exist_ok=True)
    COLUMNS_DIR.mkdir(parents=True, exist_ok=True)

    if not INFOGRAPHIC.exists():
        if source.exists():
            import shutil
            shutil.copy2(source, INFOGRAPHIC)
        else:
            raise FileNotFoundError(f"Infographic not found: {source}")

    img = Image.open(INFOGRAPHIC)
    w, h = img.size
    crops = []
    for i, (l, t, r, b) in enumerate(COLUMN_CROP_FRAC):
        box = (int(l * w), int(t * h), int(r * w), int(b * h))
        out = COLUMNS_DIR / f"col-{i + 1}.png"
        img.crop(box).save(out)
        crops.append(out)
    return crops


def build_exact_slide(prs, image_path: Path):
    """Slide 1: full infographic — pixel-accurate to generated image."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.shapes.add_picture(str(image_path), 0, 0, width=prs.slide_width, height=prs.slide_height)


def build_editable_slide(prs, column_images: list[Path]):
    """Slide 2: editable text + embedded column images from infographic."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_w = prs.slide_width
    slide_h = prs.slide_height

    bg = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, slide_w, slide_h)
    set_fill(bg, NAVY)
    bg.line.fill.background()

    header_h = Inches(1.55)
    header = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, slide_w, header_h)
    set_fill(header, NAVY_LIGHT)
    header.line.fill.background()

    add_textbox(slide, Inches(0.45), Inches(0.28), Inches(12.0), Inches(0.65),
                "做 AI 投资？最大的差异不是模型，而是产业链。", size=28, bold=True)
    add_textbox(slide, Inches(0.45), Inches(0.95), Inches(12.0), Inches(0.4),
                "五层结构，一条链条，价值从芯片流向应用。", size=16, color=GRAY)

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

        add_textbox(slide, left + Inches(0.12), col_top + Inches(0.15), col_w - Inches(0.24), Inches(0.45),
                    col["title"], size=20, bold=True, align=PP_ALIGN.CENTER)
        add_textbox(slide, left + Inches(0.1), col_top + Inches(0.62), col_w - Inches(0.2), Inches(0.75),
                    col["tagline"], size=12, color=GRAY, align=PP_ALIGN.CENTER)

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

        img_top = col_top + Inches(2.45)
        img_h = Inches(1.65)
        img_left = left + Inches(0.15)
        img_w = col_w - Inches(0.3)
        if i < len(column_images) and column_images[i].exists():
            slide.shapes.add_picture(str(column_images[i]), img_left, img_top, width=img_w, height=img_h)

    footer_top = Inches(6.35)
    footer_h = Inches(1.05)
    footer = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, footer_top, slide_w, footer_h)
    set_fill(footer, NAVY_LIGHT)
    footer.line.fill.background()

    msg_box = slide.shapes.add_textbox(Inches(0.45), footer_top + Inches(0.28), Inches(7.2), Inches(0.55))
    tf = msg_box.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    r1 = p.add_run()
    r1.text = "同一技术，不同层级。"
    r1.font.name = FONT
    r1.font.size = Pt(15)
    r1.font.color.rgb = WHITE
    r2 = p.add_run()
    r2.text = "看懂产业链，才能抓住价值。"
    r2.font.name = FONT
    r2.font.size = Pt(15)
    r2.font.bold = True
    r2.font.color.rgb = GOLD

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


def main():
    source = Path("/opt/cursor/artifacts/assets/ai-industry-chain-infographic-zh.png")
    column_images = ensure_assets(source)

    out_dir = Path("/workspace/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "AI产业链信息图-可编辑.pptx"
    root_copy = Path("/workspace/AI-industry-chain-editable.pptx")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    build_exact_slide(prs, INFOGRAPHIC)
    build_editable_slide(prs, column_images)

    prs.save(str(out_path))
    import shutil
    shutil.copy2(out_path, root_copy)
    print(f"Saved: {out_path}")
    print(f"Slide 1: full infographic embedded")
    print(f"Slide 2: editable + {len(column_images)} column images")


if __name__ == "__main__":
    main()
