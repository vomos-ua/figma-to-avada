---
title: README
type: note
permalink: ai/figma-to-avada/examples/readme-1
---

# examples/

End-to-end pipeline outputs from the FAQ block of PPC Landing v2 (`linked-promo.com` Figma).

## Files

| File | What it is |
|---|---|
| `faq-block.brief.json` | Extractor output (abbreviated). Real one is 14k chars, this is a readable subset. |
| `faq-block.shortcode.txt` | Generator output. **Paste-ready** Avada Code View. No fixtures, no fake URLs. |

## What this proves

Hand-traced the full pipeline:

```
Figma FAQ (node 62:2)
  → extractor (via Bridge MCP) → brief JSON (14k chars, no decorative noise)
  → KB: core-reference + lp-design-tokens + faq-grid-2x3 pattern
  → generator → shortcode.txt (above)
```

The shortcode in `faq-block.shortcode.txt` corresponds exactly to what we built in Figma:

- Container 1440px wide, NAVY `#0D0D26` background, 100px vertical + 120px side padding
- Header row: BLUE eyebrow + WHITE 48px headline + 60%-white 18px body, all centered
- 3 rows × 2 columns of FAQ cards (Avada doesn't auto-wrap, so 3 separate rows)
- Each card: 16px radius, 1px soft-white border, 4%-white fill, 32px padding
- Inside card: BLUE number badge → WHITE 20px question → 60%-white 14px answer
- Manrope font family enforced via `fusion_font_family_*_font="Manrope"`
- Subtle fade-up animation on header + staggered animation_delay on cards

## What's missing (vs Figma)

- **Decorative glow + chevron pattern**: not rendered. Generator emits container without background_image. To match Figma exactly, Володимир would composite the 2 glow ellipses + chevron pattern into a single PNG via Figma export, upload to WP, then we'd add `background_image="https://..."` to the container.
- **Exact glow positioning**: Avada `background_position` is limited. Real-pixel placement requires custom CSS in child theme.

## Sanity check before paste

Володимир should verify:

1. Open `faq-block.shortcode.txt` in any text editor
2. Confirm: no newlines INSIDE individual shortcode tags (multi-line params are killed by Avada parser)
3. Confirm: all `animation_delay` values look like `"0.1"`, `"0.2"` — never `"100"` or `"200"`
4. Paste into WP → Pages → Add New → Avada Live Builder → Toggle Code View → paste → Save → Preview

If layout breaks: most likely cause is missing `first="true"` / `last="true"` on column ends. Each row must have exactly one `first="true"` (the leftmost column) and one `last="true"` (the rightmost). For single-column rows both flags on same column.

## Phase 3 next step

Generate the same way for other PPC Landing blocks: Stats Strip, How We Work, Final CTA. Add patterns to `kb/patterns/` as new templates emerge.