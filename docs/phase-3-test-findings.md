---
title: phase-3-test-findings
type: note
permalink: ai/figma-to-avada/docs/phase-3-test-findings-1
---

# Phase 3 — First Avada paste test findings

**Date:** 2026-05-13
**Tested by:** Володимир Москалюк
**File:** `examples/faq-block.shortcode.txt` v1 → v2

## Critical bug found in v1

### Symptom

Pasted into Avada Live Builder Code View. Expected: 2×3 grid of FAQ cards with header above. Got: **all 7 columns (1 header + 6 cards) flattened into a single horizontal row**, cards extremely narrow with text wrapping to ~30 lines vertically.

### Root cause

I generated **4 `[fusion_builder_row]` blocks inside ONE `[fusion_builder_container]`** thinking Avada would render them as 4 sequential rows. Avada does NOT support multiple rows per container — it silently flattens them into one row.

I had this rule documented in `CLAUDE.md` ("Every container has ONE fusion_builder_row") but ignored it during generation. The pattern doc `kb/patterns/faq-grid-2x3.md` incorrectly recommended this approach.

### Fix (v2)

**One container per visual row of content.** For our FAQ 2×3 grid:

- Container 1: header (eyebrow + headline + sub) — 1 row, 1 column 1/1
- Container 2: cards 01 + 02 — 1 row, 2 columns 1/2
- Container 3: cards 03 + 04 — 1 row, 2 columns 1/2
- Container 4: cards 05 + 06 — 1 row, 2 columns 1/2

All containers share same `background_color="#0D0D26"`, `padding_left="120px"`, etc. Vertical padding split: top container gets `padding_top="100px"`, bottom container gets `padding_bottom="100px"`, middle ones use `padding_top="0"` to avoid gaps.

## Lessons learned

| # | Lesson | Applied to |
|---|---|---|
| 1 | **HARD RULE: 1 container = 1 row.** Multiple `fusion_builder_row` per container → flattening | CLAUDE.md, core-reference.md, faq-grid-2x3.md |
| 2 | For multi-row layouts, use **multiple containers stacked vertically**, NOT multiple rows in one container | faq-grid-2x3.md pattern updated |
| 3 | When stacking containers, **split vertical padding**: first gets full `padding_top`, last gets full `padding_bottom`, middle ones use `padding_top="0"` to avoid double gaps | core-reference.md |
| 4 | **`flex_align_items="stretch"`** on card containers so both cards in a row equal height even when content differs | faq-grid-2x3.md |
| 5 | Avada Live Builder edit view shows ACTUAL rendered output (with editor overlay). What you see in editor = what visitors see. Not a preview-only quirk. | n/a |

## Cost of this bug

If I had pasted andreata's repo's own pattern (which DOES follow "1 container 1 row" everywhere), the layout would have worked first try. Cost = ~30 min of generation rework + 5 min Володимир test cycle.

**Process change:** Before generating new patterns, **read andreata's CLAUDE.md hard rules section + my own CLAUDE.md once more**. Don't trust ad-hoc layout logic.

## What still works after the fix

- LP brand tokens correctly applied (NAVY background, BLUE eyebrow, white text, rgba muted bodies)
- Manrope font enforced via `fusion_font_family_*_font` on every text node
- Animation fade-up with stagger
- Card styling (border, radius, padding, fill)
- Mobile responsive via `type_small="1_1"`

## Still missing (intentionally — Phase 4 work)

- **Decorative background**: chevron pattern + 2 glow ellipses not rendered. Need Володимир to composite + upload as single PNG, add `background_image=` to first container.
- **Equal heights**: Cards 01, 03, 05 (left column) might differ in height from 02, 04, 06 (right column). `flex_align_items="stretch"` should handle this but verify visually.