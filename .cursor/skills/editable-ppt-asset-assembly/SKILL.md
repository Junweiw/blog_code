---
name: editable-ppt-asset-assembly
description: >-
  Build editable 16:9 PowerPoint slides by splitting visuals into discrete
  assets (heroes, white-line icons) and composing them with native PPT shapes
  and text boxes. Use when the user wants an editable PPT/infographic (not a
  flat image), Chinese/English consulting-style slides, or complains that icons
  look embedded / not editable.
---

# Editable PPT: Asset Split + Native Assembly

## Goal

Deliver a **16:9 `.pptx`** where every meaningful element is separately editable:

- Text → text boxes
- Cards / bars / circles → native shapes
- Photos → individual PNGs
- Icons → **white-line PNGs on transparent bg** + **PPT circle shapes** (filled or hollow), then **grouped**

Never deliver “one AI PNG pasted full-bleed” as the editable solution.

## Workflow (do this in order)

### 1. Lock structure with the user (1 message)

Confirm before generating:

- Slide size: **16:9** (13.333" × 7.5")
- Layout: e.g. header + N columns + footer
- Icon style: filled blue circle + white glyph **vs** white glyph + hollow ring
- Language / copy

Do **not** assemble the final PPT until icon style is approved.

### 2. Generate discrete assets

| Asset type | Spec | Notes |
|---|---|---|
| Column heroes | Separate images, consistent crop (e.g. 800×600) | One scene per column |
| Icons / metrics | **White lines only**, RGBA, transparent background | No navy square, no checkerboard, no baked blue circle |
| Background / cards | **Not images** | Use PPT rectangles / rounded rects |

Store under something like:

```
assets/ppt-parts/
  heroes/
  icons-white/
  metrics-white/
```

### 3. Preview icons alone (mandatory gate)

Before PPT assembly, export preview sheets:

1. White glyphs on dark bg
2. White glyphs composited on a blue circle (final look mock)
3. White glyphs on light bg (proves transparency)

Show the user. **Wait for OK.**

### 4. Assemble with python-pptx (native layers)

Bottom → top:

1. Background shape
2. Header / footer bars (shapes)
3. Title / subtitle / labels (text boxes)
4. Column cards (rounded rects)
5. Per column: title + tagline text → **icon group** → hero picture
6. Footer slogan text → **metric icon groups** + labels

**Column icon group (filled style):**

1. `OVAL` shape, solid fill `#3B82F6`, no line
2. White-line PNG centered on top (~65–70% of circle diameter)
3. Group oval + picture

**Metric icon group (outline style):**

1. White-line PNG
2. `OVAL` with **no fill**, blue line ~1.5–2 pt
3. Group ring + picture

### 5. Deliver

- Save `.pptx` at repo root with English filename for easy download
- Push branch + give **GitHub raw download URL** (not `127.0.0.1`)
- Mention: ungroup icon groups to recolor circles / replace glyphs

## Icon extraction recipe

From a filled-circle AI icon (or similar):

1. Keep only near-white, low-chroma pixels → pure white RGB + alpha
2. Crop to glyph bbox, pad to square (~1.35×), resize 256×256
3. **Do not** bake the blue circle into the PNG
4. Blue circle is always a PPT shape

If AI icon has checkerboard “fake transparency”, discard bg entirely; do not try to salvage the square.

## Do's

- **Do** split 素材 first, assemble second
- **Do** use native shapes for circles, cards, bars
- **Do** use white-only transparent glyphs for icons
- **Do** group circle + glyph so users can move them together
- **Do** preview icons on light + dark before PPT rebuild
- **Do** keep slide true 16:9; resize/crop assets to match
- **Do** provide a GitHub / artifact download link for cloud/mobile users
- **Do** put regeneratable scripts next to assets (`create_*_ppt*.py`, `draw_*_icons.py`)

## Don'ts

- **Don't** paste one full AI infographic as the “editable” slide
- **Don't** leave “← 可替换图片” placeholders in a deliverable
- **Don't** ship AI icons with opaque navy / checkerboard backgrounds
- **Don't** bake blue circles into icon PNGs if the circle should be editable
- **Don't** iterate the whole PPT for icon tweaks — fix assets, then reassemble
- **Don't** send `http://127.0.0.1:...` links to mobile / Cursor Cloud clients
- **Don't** claim pixel-perfect AI art + fully editable text in one layer — use two layers of intent (visual assets + editable chrome)

## Minimal acceptance checklist

- [ ] Slide ratio = 16:9
- [ ] Titles / body copy are text boxes (click-to-edit)
- [ ] Column icons = shape circle + white PNG, grouped
- [ ] Metric icons = white PNG + hollow ring (if requested), grouped
- [ ] No checkerboard / dark square around icons
- [ ] Heroes are separate pictures
- [ ] Downloadable via public raw URL

## Reference implementation (this repo)

- Assemble: `scripts/create_ai_chain_ppt_editable.py`
- White icons: `assets/ppt-parts/icons-white/`, `metrics-white/`
- Heroes: `assets/ppt-parts/heroes/`
- Output: `AI-industry-chain-editable-16x9.pptx`
