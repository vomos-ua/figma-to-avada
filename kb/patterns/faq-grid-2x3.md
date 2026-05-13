---
title: faq-grid-2x3
type: note
permalink: ai/figma-to-avada/kb/patterns/faq-grid-2x3
---

# Pattern: FAQ grid 2×3 (dark theme)

Always-visible FAQ cards in a 2-column × 3-row grid on dark navy background. No accordion — cards visible all at once for scannability.

## Figma signature

Generator detects this pattern when brief matches:

- Root frame `name` contains "FAQ"
- Root `fills` includes `#0D0D26` solid
- Root has decorative children (glow ellipses, chevron pattern)
- Header section: 3 TEXT nodes (eyebrow + headline + body) center-aligned
- 6 child frames named `FAQ 01`...`FAQ 06`, each with 3 TEXT nodes (number, question, answer)

## Avada shortcode template

```text
[fusion_builder_container type="flex" hundred_percent="no" hundred_percent_height="no" flex_align_items="flex-start" flex_justify_content="flex-start" hide_on_mobile="small-visibility,medium-visibility,large-visibility" background_color="#0D0D26" background_image="{{glow_bg_url}}" background_repeat="no-repeat" background_size="cover" padding_top="100px" padding_bottom="100px" padding_left="120px" padding_right="120px"]
  [fusion_builder_row]

    [fusion_builder_column type="1_1" type_small="1_1" layout="1_1" first="true" last="true" align_self="auto" padding_bottom="60px"]
      [fusion_title size="6" font_size="12px" line_height="auto" text_transform="uppercase" letter_spacing="0.12em" text_color="#2134EA" content_align="center" style_type="default" sep_color="" margin_bottom="16px"]{{EYEBROW}}[/fusion_title]
      [fusion_title size="2" font_size="48px" line_height="58px" text_color="#FFFFFF" content_align="center" style_type="default" sep_color="" margin_bottom="20px"]{{HEADLINE}}[/fusion_title]
      [fusion_text font_size="18px" line_height="28px" text_color="rgba(255,255,255,0.6)" content_alignment="center"]<p>{{SUB_HEADLINE}}</p>[/fusion_text]
    [/fusion_builder_column]

    {{#each FAQ_CARDS}}
    [fusion_builder_column type="1_2" type_small="1_1" layout="1_2" first="{{first}}" last="{{last}}" align_self="auto" background_color="rgba(255,255,255,0.04)" border_color="rgba(255,255,255,0.08)" border_style="solid" border_top="1px" border_right="1px" border_bottom="1px" border_left="1px" border_radius_top_left="16px" border_radius_top_right="16px" border_radius_bottom_left="16px" border_radius_bottom_right="16px" padding_top="32px" padding_right="32px" padding_bottom="32px" padding_left="32px" spacing_left="" spacing_right="16px" margin_bottom="24px"]
      [fusion_title size="6" font_size="14px" line_height="auto" letter_spacing="0.08em" text_color="#2134EA" content_align="left" style_type="default" sep_color="" margin_bottom="8px"]{{NUMBER}}[/fusion_title]
      [fusion_title size="3" font_size="20px" line_height="28px" text_color="#FFFFFF" content_align="left" style_type="default" sep_color="" margin_bottom="12px"]{{QUESTION}}[/fusion_title]
      [fusion_text font_size="14px" line_height="22px" text_color="rgba(255,255,255,0.6)" content_alignment="left"]<p>{{ANSWER}}</p>[/fusion_text]
    [/fusion_builder_column]
    {{/each}}

  [/fusion_builder_row]
[/fusion_builder_container]
```

## Variable substitution from brief

| Variable | Source in brief |
|---|---|
| `{{glow_bg_url}}` | Decorative children export combined as background image URL provided by Володимир after WP upload |
| `{{EYEBROW}}` | First TEXT child whose `text.textCase === 'ORIGINAL'` AND `fontSize <= 14` AND `letterSpacing.value >= 10` |
| `{{HEADLINE}}` | TEXT child with largest `fontSize` in the header region (y < 250) |
| `{{SUB_HEADLINE}}` | TEXT child below headline, font 16-18px, gray color |
| FAQ_CARDS | Each child frame named `FAQ NN` |
| `{{NUMBER}}` | First TEXT in card (small SemiBold, BLUE) |
| `{{QUESTION}}` | Second TEXT in card (20px SemiBold, WHITE) |
| `{{ANSWER}}` | Third TEXT in card (14px Regular, muted WHITE) |
| `first` / `last` | `"true"` for cards 1 and 6, `"false"` otherwise (but **NOT** based on row position — Avada flex rows handle wrapping. For 2-col layout, first/last per row would require splitting into 3 separate `fusion_builder_row` blocks.) |

## Important: 2-col grid in Avada

Avada doesn't auto-wrap columns. For a 2×3 grid you have two options:

**Option A — 3 separate rows (recommended for cards with different heights):**

```text
[fusion_builder_row]
  [column 1_2 first=true]Card 1[/column]
  [column 1_2 last=true]Card 2[/column]
[/fusion_builder_row]
[fusion_builder_row]
  [column 1_2 first=true]Card 3[/column]
  [column 1_2 last=true]Card 4[/column]
[/fusion_builder_row]
[fusion_builder_row]
  [column 1_2 first=true]Card 5[/column]
  [column 1_2 last=true]Card 6[/column]
[/fusion_builder_row]
```

But you need ONE container — that means 3 rows inside one container. **Avada allows multiple rows per container.**

**Option B — single row with 6 columns of `type="1_2"`:**

Avada will visually wrap them every 2 columns based on width. This works for equal-height cards. But explicit Option A is cleaner.

For our FAQ generator: use Option A — 3 rows inside one container.

## Decorative elements

Glow ellipses and chevron pattern from Figma → emit as `background_image` on the container. The brief includes them as `decorative: true` children. Generator:

1. If multiple decoratives, composite into single background PNG via image step
2. Otherwise emit single `background_image="https://..."` 
3. Володимир uploads the composite image, provides URL in `image-urls.json`

If decoratives are too complex to composite cleanly — fall back to plain solid `background_color` and add brand chevron via child theme CSS class.

## LP variants

- **Dark theme** (default): `background_color="#0D0D26"`, card `rgba(255,255,255,0.04)`, white text
- **Light theme** (alt): `background_color="#F5F6FA"`, card `#FFFFFF` with box-shadow, navy text

## Mobile (responsive)

`type_small="1_1"` on all FAQ cards → stack 1 per row on mobile. Padding reduces via `padding_*_small` if needed (default LP: keep card padding `32px`, container padding small `40px 20px`).