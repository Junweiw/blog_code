---
name: editable-ppt
description: >-
  Turn an infographic, poster, or flat slide image into an editable PowerPoint
  (.pptx) by splitting it into text boxes, shapes, panel images, and transparent
  icon glyphs. Use when the user wants an editable PPT/pptx from a picture,
  complains a slide is not editable, or asks how to convert an infographic into
  layered PowerPoint objects.
---

# Editable PPT

Rebuild a flat visual (infographic / poster / AI slide image) into a **layered, editable `.pptx`**.

## Goal

Ship a PowerPoint where the parts people actually change are **independent objects**, not one baked image.

## Core principles

1. **A picture is pixels. An editable PPT is an object stack.** Split first, assemble second. Never treat “paste the whole image” as the editable deliverable.
2. **Map objects deliberately:**
   - Copy → text boxes
   - Cards / bars / circles / dividers → native shapes
   - Photos / illustrations → separate pictures (one asset per panel)
   - Icon drawings → transparent monochrome glyph PNGs
   - Icon circular backings / rings → PPT oval shapes, then **group** with the glyph
3. **Do not bake editable chrome into icon PNGs** (no filled brand circle inside the file if that circle should be recolorable).
4. **Preview glyphs before assembling the deck.** Approve icons, then build.
5. **Keep brand specifics out of this skill.** Colors, fonts, industry copy come from the brief.

## Workflow

### 1. Lock “done”

Confirm: aspect ratio (usually 16:9), what must stay editable, icon style (filled circle vs outline ring), language.

### 2. Deconstruct

List every object: text blocks, structural shapes, panel images, icon glyphs vs circular backings.

### 3. Produce discrete assets

- One image per visual panel
- Glyph-only transparent PNGs for icons
- Structural chrome as shapes, not flattened into photos

### 4. Icon preview gate (mandatory)

Show:

- Glyphs on dark background
- Glyphs on light background (proves true transparency)
- Optional mock: glyph on a circle shape (final look)

Wait for OK before building `.pptx`.

### 5. Assemble with native layers

Typical bottom → top: background → cards/bars → text → icon groups → panel photos.

- **Filled icon group:** solid oval + centered glyph → group  
- **Outline icon group:** glyph + hollow stroked oval → group  

Prefer a regeneratable script (e.g. `python-pptx`) when the deck will be rebuilt.

### 6. Deliver

- Correct aspect ratio
- Real download URL when the user is on Cloud/mobile (not `127.0.0.1`)
- Note that icon groups can be ungrouped to recolor circles or swap glyphs

## Acceptance checklist

- [ ] Target aspect ratio correct (usually 16:9)
- [ ] Editable copy is in text boxes
- [ ] Recolorable chrome is shapes
- [ ] Replaceable panels are separate pictures
- [ ] Icons are glyph + shape when that model was chosen, grouped
- [ ] No opaque square / fake checkerboard around glyphs
- [ ] User has a working download path

## Known traps

| Trap | Fix |
|------|-----|
| Whole image pasted as “editable” | Rebuild as layered objects; flat image at most as a reference slide |
| Icons with navy squares or baked checkerboard | Extract glyph-only; circles as shapes |
| Recolorable circles baked into PNGs | Split glyph vs circle, then group |
| Regenerating the whole deck to fix one icon | Fix the asset → re-preview → reassemble |
| Localhost links for Cloud/mobile users | Push and share raw/artifact download URLs |

## Boundaries

- Not a brand system (no fixed palette in this skill)
- Not a substitute for “full-bleed AI-rendered deck” workflows when editability is not required
- Does not promise pixel-identical AI art and full editability in one layer

## One-liner

**Split into text / shapes / images / glyphs → approve glyphs → assemble layered PPT — never ship one flat picture as editable.**
