---
name: editable-ppt
description: >-
  Convert a flat visual (infographic, poster, or slide image) into an editable
  PowerPoint by separating content into independent objects. Use when the user
  wants an editable pptx from a picture, says a slide is not editable, or asks
  how to turn an infographic into layered slides.
---

# Editable PPT

## Goal

Turn a **flat picture** into a **layered PowerPoint** where people can edit the parts they actually need to change.

## Core idea

A finished visual is pixels.  
An editable slide is a stack of objects.

Do not treat “paste the whole image into PowerPoint” as an editable deliverable.

## Principles

1. **Decide what must be editable** before building.  
   Typical candidates: titles, body copy, colors, icons, photos, charts. Everything else can stay as imagery.

2. **Map each editable thing to a native object.**  
   - Words people will change → text boxes (or editable text frames)  
   - Colors / frames / dividers / badges people will restyle → shapes  
   - Photos / illustrations people will swap → separate image files  
   - Icons people will recolor or replace → prefer drawable strokes / glyphs separate from their background chrome  

3. **Keep structural chrome out of baked assets when it needs restyling.**  
   If a circle, card, or bar must change color later, make it a shape—not pixels inside a PNG.

4. **Split first, assemble second.**  
   Produce discrete parts, approve tricky parts (especially icons), then compose the slide. Don’t regenerate the whole deck to fix one asset.

5. **Stay brief-agnostic.**  
   Layout, palette, fonts, industry, and language come from the current request. This skill does not prescribe a brand look.

## Working loop

1. Deconstruct the source visual into object types.  
2. Agree the edit model with the user (what must stay editable).  
3. Produce assets for images/glyphs; use shapes for chrome.  
4. Preview ambiguous assets alone before full assembly.  
5. Assemble layers into `.pptx`.  
6. Deliver a file the user can open and edit.

## Acceptance

- The promised editable parts are real objects (not flattened into one image).  
- Swapping or editing one part does not require regenerating the whole visual.  
- Aspect ratio matches the brief.  
- The user can download/open the `.pptx` on their device.

## Anti-patterns

- Shipping one full-bleed image as “the editable slide”  
- Leaving placeholder “replace image” boxes in a final handoff  
- Baking restyleable chrome into icon/panel PNGs  
- Rebuilding the entire deck because one icon/asset is wrong  
- Encoding one project’s colors, layout, or industry into the method

## One-liner

**Separate what must change into objects, keep the rest as assets, then assemble — never confuse a pretty picture with an editable slide.**
