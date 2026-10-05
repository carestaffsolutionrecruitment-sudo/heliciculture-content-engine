# Commercial Heliculture Masterclass: Course Visual Specs (Master Reference)

**Snail World (snailworld.org) · ProductDyno Product ID 44288**

This is the master visual reference for the course. The source files sit beside it in this folder; this page records what each one is and exactly where it is used in ProductDyno.

| File | What it is |
|---|---|
| [README.md](README.md) | Layout specs: brand tokens, banner, KPI grid and trench schematic |
| [image-prompts.md](image-prompts.md) | Nano Banana and Midjourney prompts, one hero image per module, plus the pre-publishing checklist |
| [hero-banner.svg](hero-banner.svg) / [hero-banner-mobile.svg](hero-banner-mobile.svg) | Course hero banner, 1200 × 400 and stacked 750 × 500 |
| [module-3-7-kpi-grid.html](module-3-7-kpi-grid.html) | Production economics KPI grid |
| [module-2-trench-pen-cross-section.svg](module-2-trench-pen-cross-section.svg) | Trench pen drainage and airflow schematic |

## ProductDyno Placement Map

All visuals sit inside each page's existing Code element, wrapped in `<!-- sw-visual:… -->` and `<!-- /sw-visual:… -->` markers. The original lesson HTML is unchanged between the markers.

| Page (section ID) | Visual added | Position |
|---|---|---|
| Course Overview (657839) | Course hero banner (spec SVGs, unchanged) | Top |
| Module 1 (657767) | Module banner + image slot, Module 1 | Top |
| Module 2 (657776) | Module banner | Top |
| Lesson 2.1 System Typologies (657777) | Trench pen schematic + caption | After the pen typology table |
| Lesson 2.3 Controlled Micro-Climate (657779) | Image slot, Module 2 | Top |
| Deliverable: Pen Specification Checklist (657781) | Trench pen schematic + caption | Top |
| Module 3 (657785) | Module banner + image slot, Module 3 | Top |
| Lesson 3.2 Feed Formulation (657787) | KPI grid | End |
| Module 4 (657794) | Module banner | Top |
| Lesson 4.2 Quarantine and Biosecurity Protocols (657796) | Image slot, Module 4 | Top |
| Module 5 (657803) | Module banner + image slot, Module 5 | Top |
| Module 6 (657812) | Module banner + image slot, Module 6 | Top |
| Module 7 (657821) | Module banner + image slot, Module 7 | Top |
| Lesson 7.2 Capital and Operating Cost Modelling (657823) | KPI grid | End |
| Module 8 (657830) | Module banner + image slot, Module 8 | Top |
| Bonus: Resource Library and SOPs (657850) | Bonus banner | Top |

## Module Banners

Built from `hero-banner.svg` and `hero-banner-mobile.svg`: the same background, rack grid, line-art snail, gold rule and brand tokens. The changes are:

- an eyebrow line (`MODULE 1` … `MODULE 8`, `BONUS`) in warm white at 85 % opacity;
- the module title in gold, auto-sized to fit (desktop: up to 2 lines, 34–50 px, within 760 px; mobile: up to 3 lines, 36–56 px, within 650 px);
- subtitle: "Commercial Heliculture Masterclass · Snail World" (desktop), "Snail World professional course" (mobile).

The desktop and mobile SVGs are both inline. A small `<style>` block swaps them at 640 px, the same breakpoint as the `<picture>` example in the README.

## Image Slots (Nano Banana)

Each slot is a hidden `<figure data-sw-slot="module-N" style="display:none">` with an empty `<img>`, plus a `<template data-sw-design-note>` holding that module's Nano Banana and Midjourney prompts. Students see nothing until an image is added. To publish one:

1. Generate the image from the prompt and run the checklist at the end of `image-prompts.md`.
2. Upload it, put its URL in the `src` and a scene description in `alt`.
3. Delete `style="display:none"` from the figure, and optionally the design-note template.

Module 1's slot is on the module page as a mood image only. The Species Comparison Matrix and the species lessons need specialist-checked real photographs (see rule 4 in `image-prompts.md`).

## Adjustments Made for the ProductDyno Theme

- **KPI grid:**
  - the dark-mode rules were removed, because the course theme is always light;
  - the design tokens were scoped to `.sw-kpi-section` instead of `:root`;
  - the card basis was lowered from 280 px to 240 px so three cards fit the 870 px lesson column;
  - `rem` values were converted to `px`, because the theme sets a 10 px root font;
  - `#pdDraggableArea`-scoped overrides cancel the theme's list indent and its paragraph and code styles.
- **Trench schematic:** inline with `width:100%; height:auto`, and a caption that repeats the key dimensions as text. On phones it scales to the screen width, so its small labels are hard to read there. The caption carries the figures.

## Not Covered by This Spec

- No prompt or visual exists for a Kenya YEDF/WEF funding section. This course has no such lesson; that bonus lives in the Button Mushroom Masterclass.
- Micro-climate monitoring grids and workflow schematics have not been designed yet. The trench pen cross-section is the only technical schematic.
