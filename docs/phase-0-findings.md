---
title: phase-0-findings
type: note
permalink: ai/figma-to-avada/docs/phase-0-findings
---

# Phase 0 — Smoke test findings

**Date:** 2026-05-13
**Test target:** FAQ block (node id `62:2`) from PPC Landing v2 in `linked-promo.com` Figma file.

## TL;DR

- ✅ Bridge MCP-based extraction works without Figma Personal Access Token
- ✅ JSON brief structure is clean and complete for the generator
- ⚠️ **Critical finding:** decorative SVG patterns (chevron tiles, gradient glows) inflate brief 10x. Mandatory skip logic implemented in v0.1.0.
- ✅ Result: 124k chars → 14k chars (-89%) without losing any meaningful content.

## What worked

- `figma_execute` returns full JSON in one call. No pagination, no rate limits.
- All key node properties extracted in one pass: fills, strokes, text, layout, effects, bounds, opacity, corner radius.
- Decorative skip via name regex (`/chevron|glow|pattern|texture|noise/i`) + ELLIPSE+GRADIENT_RADIAL heuristic catches all noise in PPC Landing.

## What broke / lessons

### 1. Decorative patterns flood the tree

First raw extraction returned 607 nodes:
- 296 FRAME (mostly Chevron Pattern wrappers)
- 288 VECTOR (individual chevron paths)
- 21 TEXT (the only real content)
- 2 ELLIPSE (glow gradients)

97% noise. Generator would have choked trying to translate each chevron to a shortcode.

**Fix in extractor:** stop walking inside frames named `chevron|glow|pattern|texture|noise|particles|grid bg|decoration` and mark them as `{ decorative: true, exportHint: 'background-image' }`. Generator emits these as CSS background-image or skips entirely.

### 2. Gradient-radial ellipses = glow effects

Pure ELLIPSE with single GRADIENT_RADIAL fill is always a glow in LP designs. Heuristic catches them even when names like "Ellipse" are generic.

### 3. Mixed Auto Layout + absolute positioning

FAQ block uses `layout.mode: NONE` at root with all children absolutely positioned. Generator must reconstruct layout from `bounds.x/y` + container width, not rely on Figma Auto Layout for everything. This is fine - Avada containers/columns position children via flexbox anyway.

## What's left to verify

- Image export pipeline (figma_capture_screenshot per node → save PNG → sharp convert to WebP)
- Component instances (we have none in this test - need to test on a section with INSTANCE nodes)
- Vector shapes that AREN'T decorative (custom icons, illustrations)
- Multi-page Figma files (we tested one page only)

## Decision gate result

**GO.** Brief structure is generator-ready. Moving to Phase 1: shortcode catalog from Avada plugin PHP source.

## Sample brief

See `examples/faq-block.brief.json` (heavily abbreviated for readability).

Full live extraction output: 14,127 chars covering FAQ root + 3 decorative markers + 3 header texts + 6 FAQ cards with 18 inner texts. Ready to feed into generator.