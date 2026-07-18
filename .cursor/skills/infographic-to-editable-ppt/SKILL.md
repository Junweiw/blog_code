---
name: infographic-to-editable-ppt
description: >-
  Turn an infographic or visual slide concept into an editable PowerPoint by
  splitting it into discrete assets and reassembling with native PPT shapes and
  text. Use when the user wants an editable PPT/pptx from an infographic,
  poster, or AI-generated image; complains that a slide is not editable; or asks
  how to convert a flat visual into PowerPoint layers.
---

# Infographic → Editable PPT

## Core idea

A finished infographic is a **flat picture**. An editable PPT is a **stack of objects**.

```
Infographic (pixels)  →  split into 素材  →  reassemble as PPT objects
```

| Layer in the visual | Becomes in PPT |
|---|---|
| Headlines, labels, captions | Text boxes |
| Cards, bars, dividers, colored circles | Native shapes |
| Photos / illustrations | Separate image files |
| Icon glyphs | Transparent glyph PNGs (usually monochrome) |
| Icon backgrounds / rings | Native shape circles (filled or outline), grouped with glyphs |

**Rule:** Never treat “paste the whole infographic as one picture” as the editable deliverable.

## Where this skill should live

| Location | Use when |
|---|---|
| **User / personal skills** (recommended for this topic) | You want the method in *every* project, any deck |
| **Project `.cursor/skills/`** | Only this repo needs the workflow, or the project has a fixed template |

This skill is **method-level**, not brand-level. Prefer **personal skills** so it applies across repos. Keep project-specific colors, fonts, and layouts out of the skill; ask or follow the brief for each job.

## Workflow

### 1. Deconstruct the infographic

Before making files, list every object type:

1. Text blocks (title, subtitles, column labels, footnotes)
2. Structural shapes (background, cards, dividers, footer bar)
3. Imagery (one asset per visual cell / panel)
4. Icons (glyph vs circular backing — treat separately)

Also note: aspect ratio (usually **16:9**), number of columns/sections, language.

### 2. Agree the edit model with the user

Ask only what changes the build:

- One slide or multiple?
- Which parts must stay editable text vs can stay as images?
- Icon treatment: glyph-only + shape circle, or full precomposed icon?
- Match an existing brand/theme, or invent a clean default?

Do **not** hardcode a palette in the method. Colors come from the brief or reference.

### 3. Produce discrete assets

- Export or generate **one image per visual panel**
- For icons: prefer **glyph-only transparent PNGs** (e.g. white or black lines). Do **not** bake the circular backing into the PNG if that circle should be recolorable in PPT
- Keep backgrounds / cards as shapes, not flattened into photos
- Normalize sizes/crops so assembly is consistent

Suggested folder pattern (adapt names freely):

```text
assets/ppt-parts/
  panels/          # or heroes/, photos/
  icons-glyph/     # transparent monochrome glyphs
```

### 4. Preview glyphs before assembly (gate)

Show glyph previews alone:

- On a dark background
- On a light background (proves true transparency)
- Optionally mocked on a circle shape (final look)

**Wait for approval** before building the `.pptx`. Fixing icons after full assembly wastes cycles.

### 5. Assemble with native PPT objects

Typical bottom → top:

1. Slide background shape
2. Section bars / cards (shapes)
3. Text boxes
4. Icon groups (shape circle + glyph image)
5. Panel images

**Filled-circle icon group:** circle shape (solid fill, no line) + glyph image centered on top → group  
**Outline-circle icon group:** glyph image + circle shape (no fill, stroke only) → group  

Use `python-pptx` (or equivalent) so rebuilds are repeatable. Keep a small assemble script in the project when the deck will be regenerated.

### 6. Deliver

- True target aspect ratio (usually 16:9)
- English-friendly filename for download when useful
- Share a **real download URL** (repo raw / artifact), not machine-local `127.0.0.1`, if the user is on Cloud/mobile
- Tell the user they can ungroup icon groups to recolor rings/circles or swap glyphs

## Do's

- Split the infographic into objects first; assemble second
- Put copy in text boxes whenever the user may edit wording
- Put structural chrome in shapes whenever the user may recolor/resize
- Keep icon glyphs transparent; put circular backings in PPT shapes when editability matters
- Preview icon assets before PPT rebuild
- Regenerate from scripts when the same template will be reused

## Don'ts

- Don't ship a single flattened infographic PNG as the “editable” slide
- Don't leave empty “replace image” placeholders in a final deliverable
- Don't bake opaque square backgrounds (or fake checkerboard transparency) into icons
- Don't bake editable chrome (colored circles, cards) into icon PNGs
- Don't rebuild the whole deck to tweak one icon — fix the asset, then reassemble
- Don't couple the method to one brand color, one industry, or one layout

## Acceptance checklist

- [ ] Target aspect ratio correct (usually 16:9)
- [ ] User-facing copy is editable text (where promised)
- [ ] Cards / bars / circles that should recolor are shapes
- [ ] Icons are glyph + shape (if that model was chosen), grouped
- [ ] No opaque junk around icon glyphs
- [ ] Panel images are separate, replaceable pictures
- [ ] User has a working download path

## One-line summary

**Deconstruct the infographic into text / shapes / images / glyphs, approve glyphs, then reassemble as layered PPT — never as one flat picture.**
