---
title: CLAUDE
type: note
permalink: ai/figma-to-avada/claude
---

# CLAUDE.md - figma-to-avada

Internal LP tool: Figma → Avada Fusion Builder shortcodes.

## Critical rules

1. **ONE container = ONE row.** Multiple `[fusion_builder_row]` inside one `[fusion_builder_container]` are silently FLATTENED into a single horizontal row by Avada. For multi-row sections, emit **multiple containers** stacked vertically. Split `padding_top`/`padding_bottom` across them so middle containers don't add double gaps. **This bug burned us once in Phase 3 — never again.**
2. **NO Figma Personal Access Token.** Use figma-console MCP exclusively. Bridge plugin must be active.
3. **NO automatic WordPress upload.** User uploads images manually, returns URLs, we substitute.
4. **NO em-dashes in generated shortcodes.** Avada Code View handles them poorly. Use `-` only.
5. **animation_delay in SECONDS DECIMAL.** `animation_delay="0.2"` = 200ms. NOT `"200"` (= 200 seconds!).
6. **NO HTML comments between shortcode tags.** Avada parser rejects them.
7. **`[fusion_text]` content wrapped in `<p>` inline.** `[fusion_title]` content inline without `<p>`. No newlines inside tags.
8. **Every column needs `first="true"` (leftmost) and `last="true"` (rightmost).** Missing flags break Avada flex layout. Single-column rows = both flags `true` on same column.
9. **NEVER use non-numeric placeholders for `form_post_id`.** Strings like `{{FORM_POST_ID}}` or `REPLACE_ME` cause Avada Builder to hang/freeze the editor. Use **`form_post_id="0"`** as the safe placeholder — Avada won't find form #0, won't render the form, but the page stays editable. Володимир replaces with real ID after creating the form in `Avada → Forms`. **Burned us in Phase 3 Light CTA test — never again.**

## Pipeline overview

```
Figma file (open in Desktop) → Bridge MCP → extractor/extract.js (run via figma_execute)
   → output/{site}/{page}/brief/sections/*.json  + images/*.png
User uploads images → returns URLs in output/{site}/{page}/image-urls.json
   → generator reads brief + image-urls + kb/ → output/{site}/{page}/shortcode/*.txt
User pastes into Avada Code View → polish → done.
```

## Knowledge base (kb/)

- `kb/shortcodes/` - reference catalog of [fusion_*] shortcodes extracted from plugin source
- `kb/patterns/` - LP-specific section patterns (hero, stats strip, cases, FAQ, CTA)
- `kb/tokens/` - LP design tokens → Avada Global Styles mapping

## When generating shortcodes

1. Read brief JSON for the section
2. Read `kb/patterns/` for matching pattern (or fallback to generic container/row/column)
3. Substitute image placeholders with URLs from `image-urls.json`
4. Apply LP design tokens (NAVY #0D0D26, BLUE #2134EA, WHITE #FFFFFF)
5. Validate: no em-dashes, animation_delay in seconds, content on single line

## Reference plugin source

Avada plugins are unpacked at `D:\AI\Linked Promo\docs\Avada\fusion-builder\` and `D:\AI\Linked Promo\docs\Avada\fusion-core\`. Use these as ground truth for shortcode parameters - documentation is incomplete.

Key paths:
- `fusion-builder/shortcodes/*.php` - 111 shortcode handlers with parameter defaults
- `fusion-builder/shortcodes/form/*.php` - Avada Forms field types
- `fusion-core/shortcodes/*.php` - legacy shortcodes (faq, portfolio, contact-form)