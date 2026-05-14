---
title: stats-strip-light
type: note
permalink: ai/figma-to-avada/kb/patterns/stats-strip-light-1
---

# Pattern: Stats Strip (light, 4 columns)

Thin horizontal strip with 4 statistics. Light theme: white background, navy numbers with blue accent units, gray labels. Vertical dividers between columns.

## Figma signature

Generator detects when brief matches:

- Root frame `name` includes "Stats" or "Strip"
- Root `bounds.h` < 150 (thin strip)
- Root `fills` = `#FFFFFF` solid
- Root has 4 child frames with `text` containing a number (regex `^[\d.,$-]+$`) + sibling TEXT label
- Optionally: chevron BrandPattern decorative frame (skip)

## Avada shortcode template

**Single container + single row + 4 columns.** Each column has `border_right="1px"` except the last. Numbers use inline `<span>` for accent unit color split.

```text
[fusion_builder_container type="flex" hundred_percent="no" hundred_percent_height="no" flex_align_items="center" flex_justify_content="space-between" background_color="#FFFFFF" border_color="#E0E0E5" border_style="solid" border_top="1px" border_right="1px" border_bottom="1px" border_left="1px" padding_top="13px" padding_bottom="13px" padding_left="120px" padding_right="120px" padding_top_small="20px" padding_bottom_small="20px" padding_left_small="20px" padding_right_small="20px" hide_on_mobile="small-visibility,medium-visibility,large-visibility"]
[fusion_builder_row]

[fusion_builder_column type="1_4" type_small="1_2" layout="1_4" first="true" last="false" align_self="center" border_right="1px" border_color="#E0E0E5" border_style="solid" padding_top="0" padding_right="20px" padding_bottom="0" padding_left="0"]
[fusion_title size="2" font_size="44px" line_height="60px" text_color="#14141F" content_align="left" style_type="default" sep_color="" margin_bottom="6px" fusion_font_family_title_font="Manrope" fusion_font_variant_title_font="800"]{{NUMBER_1}}<span style="color:#2134EA;">{{ACCENT_1}}</span>[/fusion_title]
[fusion_text font_size="13px" line_height="18px" text_color="#737385" content_alignment="left" fusion_font_family_text_font="Manrope" fusion_font_variant_text_font="400"]<p>{{LABEL_1}}</p>[/fusion_text]
[/fusion_builder_column]

[fusion_builder_column type="1_4" type_small="1_2" layout="1_4" first="false" last="false" align_self="center" border_right="1px" border_color="#E0E0E5" border_style="solid" padding_top="0" padding_right="20px" padding_bottom="0" padding_left="20px"]
[fusion_title size="2" font_size="44px" line_height="60px" text_color="#14141F" content_align="left" style_type="default" sep_color="" margin_bottom="6px" fusion_font_family_title_font="Manrope" fusion_font_variant_title_font="800"]{{NUMBER_2}}<span style="color:#2134EA;">{{ACCENT_2}}</span>[/fusion_title]
[fusion_text font_size="13px" line_height="18px" text_color="#737385" content_alignment="left" fusion_font_family_text_font="Manrope" fusion_font_variant_text_font="400"]<p>{{LABEL_2}}</p>[/fusion_text]
[/fusion_builder_column]

[fusion_builder_column type="1_4" type_small="1_2" layout="1_4" first="false" last="false" align_self="center" border_right="1px" border_color="#E0E0E5" border_style="solid" padding_top="0" padding_right="20px" padding_bottom="0" padding_left="20px"]
[fusion_title size="2" font_size="44px" line_height="60px" text_color="#14141F" content_align="left" style_type="default" sep_color="" margin_bottom="6px" fusion_font_family_title_font="Manrope" fusion_font_variant_title_font="800"]{{NUMBER_3}}<span style="color:#2134EA;">{{ACCENT_3}}</span>[/fusion_title]
[fusion_text font_size="13px" line_height="18px" text_color="#737385" content_alignment="left" fusion_font_family_text_font="Manrope" fusion_font_variant_text_font="400"]<p>{{LABEL_3}}</p>[/fusion_text]
[/fusion_builder_column]

[fusion_builder_column type="1_4" type_small="1_2" layout="1_4" first="false" last="true" align_self="center" padding_top="0" padding_right="0" padding_bottom="0" padding_left="20px"]
[fusion_title size="2" font_size="44px" line_height="60px" text_color="#14141F" content_align="left" style_type="default" sep_color="" margin_bottom="6px" fusion_font_family_title_font="Manrope" fusion_font_variant_title_font="800"]{{NUMBER_4}}<span style="color:#2134EA;">{{ACCENT_4}}</span>[/fusion_title]
[fusion_text font_size="13px" line_height="18px" text_color="#737385" content_alignment="left" fusion_font_family_text_font="Manrope" fusion_font_variant_text_font="400"]<p>{{LABEL_4}}</p>[/fusion_text]
[/fusion_builder_column]

[/fusion_builder_row]
[/fusion_builder_container]
```

## Variable substitution

| Variable | Source in brief |
|---|---|
| `{{NUMBER_N}}` | Stat N's main number (e.g. "5", "1.8", "$3.59", "12-36") |
| `{{ACCENT_N}}` | Stat N's accent unit (e.g. "+", "%", "", "h"). **Empty if no accent unit (like $3.59).** |
| `{{LABEL_N}}` | Stat N's label below the number |

If accent is empty, the `<span>` still renders nothing — no harm. Generator can also conditionally omit the span tag when accent is empty for cleaner output.

## Mobile (responsive)

`type_small="1_2"` on all columns → stacks 2x2 on mobile (4 stats in a 2x2 grid).
For very small screens, `type_xsmall="1_1"` could be added but Avada default is 2-column on small.

Container padding reduces: `padding_top_small="20px"`, etc.

## Anti-patterns

❌ Using `[fusion_separator]` between columns — separators are HORIZONTAL only. Vertical dividers via `border_right` on columns.

❌ Wrapping number+accent in nested `[fusion_title]` calls — Avada doesn't compose inline elements that way. Use `<span style="color:...">` inside ONE title.

❌ Skipping `align_self="center"` — column content vertically misaligns with neighbors having different content height.

❌ Forgetting `border_right="0"` (or omitting `border_right`) on the LAST column — creates extra divider after the 4th stat.

## Decorative elements (not rendered in v1)

- Chevron `BrandPattern` overlay (decorative, marked skip in extractor)
- Bottom-right blue `AccentLine` 200×2 at 10% opacity (decorative)

To render these accurately, Володимир would need to export `BrandPattern` frame as PNG → upload to Media Library → set as `background_image` on container with `background_position="center"` and `background_repeat="no-repeat"`. Skipped for v1, can add later for visual fidelity.

## LP variants

- **Dark theme** (alternative): `background_color="#0D0D26"`, numbers `#FFFFFF`, accents `#2134EA`, labels `rgba(255,255,255,0.6)`, dividers `rgba(255,255,255,0.08)`. Same structure, just inverted colors.