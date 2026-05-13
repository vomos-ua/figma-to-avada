---
title: faq-grid-2x3
type: note
permalink: ai/figma-to-avada/kb/patterns/faq-grid-2x3
---

# Pattern: FAQ grid 2×3 (dark theme)

Always-visible FAQ cards in a 2-column × 3-row grid on dark navy background. No accordion — cards visible all at once for scannability.

## ⚠️ Critical Avada rule (learned from Phase 3 test)

**ONE container = ONE row. Multiple `fusion_builder_row` inside one container are FLATTENED into a single visual row.**

For our 2×3 grid this means **4 separate containers**, not 1 container with 4 rows:

```
Container 1 (header)        ← row of 1 column (1/1)
Container 2 (row 1 of cards) ← row of 2 columns (1/2 + 1/2)
Container 3 (row 2 of cards) ← row of 2 columns (1/2 + 1/2)
Container 4 (row 3 of cards) ← row of 2 columns (1/2 + 1/2)
```

All 4 containers share the same `background_color="#0D0D26"` and side padding, but vertical padding is split:

| Container | `padding_top` | `padding_bottom` |
|---|---|---|
| 1 (header) | `100px` | `40px` |
| 2 (cards 1-2) | `0` | `24px` |
| 3 (cards 3-4) | `0` | `24px` |
| 4 (cards 5-6) | `0` | `100px` |

Otherwise stacked containers create visible gaps between them.

## Figma signature

Generator detects this pattern when brief matches:

- Root frame `name` contains "FAQ"
- Root `fills` includes `#0D0D26` solid
- Root has decorative children (glow ellipses, chevron pattern)
- Header section: 3 TEXT nodes (eyebrow + headline + body) center-aligned
- 6 child frames named `FAQ 01`...`FAQ 06`, each with 3 TEXT nodes (number, question, answer)

## Avada shortcode template

See `examples/faq-block.shortcode.txt` for the complete working version. Structural skeleton:

```text
[fusion_builder_container background_color="#0D0D26" padding_top="100px" padding_bottom="40px" padding_left="120px" padding_right="120px"]
  [fusion_builder_row]
    [fusion_builder_column type="1_1" first="true" last="true"]
      EYEBROW + HEADLINE + SUB
    [/fusion_builder_column]
  [/fusion_builder_row]
[/fusion_builder_container]

[fusion_builder_container background_color="#0D0D26" padding_top="0" padding_bottom="24px" padding_left="120px" padding_right="120px" flex_align_items="stretch"]
  [fusion_builder_row]
    [fusion_builder_column type="1_2" first="true" last="false" spacing_right="16px"]
      CARD 01 (number + question + answer)
    [/fusion_builder_column]
    [fusion_builder_column type="1_2" first="false" last="true"]
      CARD 02
    [/fusion_builder_column]
  [/fusion_builder_row]
[/fusion_builder_container]

... (containers 3 + 4 same shape, with cards 03/04 and 05/06)

Final container has padding_bottom="100px" to close the section.
```

Key details:

- **`flex_align_items="stretch"`** on card containers → both cards in a row equal height when their content lengths differ
- **`spacing_right="16px"`** on first column of each card row → 16px gap between the two cards
- **`type_small="1_1"`** on every card column → stack 1 per row on mobile

## Variable substitution from brief

| Variable | Source in brief |
|---|---|
| `{{glow_bg_url}}` | Decorative children export combined as background image URL provided by Володимир after WP upload |
| `{{EYEBROW}}` | First TEXT child whose `text.textCase === 'ORIGINAL'` AND `fontSize <= 14` AND `letterSpacing.value >= 10` |
| `{{HEADLINE}}` | TEXT child with largest `fontSize` in the header region (y < 250) |
| `{{SUB_HEADLINE}}` | TEXT child below headline, font 16-18px, gray color |
| FAQ_CARDS[0..5] | Each child frame named `FAQ NN`, in order |
| `{{NUMBER}}` | First TEXT in card (small SemiBold, BLUE) |
| `{{QUESTION}}` | Second TEXT in card (20px SemiBold, WHITE) |
| `{{ANSWER}}` | Third TEXT in card (14px Regular, muted WHITE) |

## Decorative elements

Glow ellipses and chevron pattern from Figma → emit as `background_image` on container 1 (header). The brief includes them as `decorative: true` children. Generator:

1. If multiple decoratives, composite into single background PNG via image step
2. Add `background_image="https://..."` + `background_repeat="no-repeat"` + `background_size="cover"` to container 1
3. Володимир uploads the composite image, provides URL in `image-urls.json`

For repeating decorative across all 4 containers: cleaner to use `background_position` math per container, or fall back to a child theme CSS class that paints the decorative across the whole section.

For our PPC Landing FAQ specifically: chevron pattern spans the FULL block (1040px height). To preserve this look across 4 containers, the cleanest is a `.lp-faq-decorative` body class set via Avada page settings + child theme CSS that paints the SVG pattern as `body.page-id-NNN .lp-faq` background. Outside of MVP scope — leave plain navy for v1.

## LP variants

- **Dark theme** (default): `background_color="#0D0D26"`, card `rgba(255,255,255,0.04)`, white text
- **Light theme** (alt): `background_color="#F5F6FA"`, card `#FFFFFF` with box-shadow, navy text

## Mobile (responsive)

`type_small="1_1"` on all FAQ cards → stack 1 per row on mobile. Containers padding `_small` variants:

```
padding_top_small="60px"      # first container
padding_bottom_small="60px"   # last container
padding_left_small="20px"
padding_right_small="20px"
```

## Anti-patterns (do NOT generate)

❌ Multiple `[fusion_builder_row]` inside one `[fusion_builder_container]` — Avada flattens them. This was the bug in v1.

❌ Using `[fusion_accordion]` + `[fusion_toggle]` for FAQ when source design has always-visible cards. Toggle is collapse-by-default — different UX.

❌ Hardcoded inline styles via `style=""` attribute. Use Avada-native params or child theme CSS classes.