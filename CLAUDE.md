---
title: CLAUDE
type: note
permalink: ai/figma-to-avada/claude
---

# CLAUDE.md - figma-to-avada

Internal LP tool: Figma → Avada Fusion Builder shortcodes.

## Critical rules

1. **NO Figma Personal Access Token.** Use figma-console MCP exclusively. Bridge plugin must be active.
2. **NO automatic WordPress upload.** User uploads images manually, returns URLs, we substitute.
3. **NO em-dashes in generated shortcodes.** Avada Code View handles them poorly. Use `-` only.
4. **animation_delay in SECONDS DECIMAL.** `animation_delay="0.2"` = 200ms. NOT `"200"` (= 200 seconds!).
5. **NO HTML comments between shortcode tags.** Avada parser rejects them.
6. **`[fusion_text]` content wrapped in `<p>` inline.** `[fusion_title]` content inline without `<p>`. No newlines inside tags.

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