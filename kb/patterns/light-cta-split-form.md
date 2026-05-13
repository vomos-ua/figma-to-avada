---
title: light-cta-split-form
type: note
permalink: ai/figma-to-avada/kb/patterns/light-cta-split-form-1
---

# Pattern: Light CTA — split layout with form card

Light-background CTA section. Left column = marketing text (eyebrow + headline + body + benefits list). Right column = white form card with shadow containing 4 form fields and submit button.

## Figma signature

Generator detects this pattern when brief matches:

- Root frame `name` contains "CTA" AND `fills[0].color === '#F5F6FA'`
- Two main content regions: left (x≈120, w≈580) and right (x≈740, w≈580)
- Left region: TEXT eyebrow + TEXT headline + TEXT body + 3 small frames each with VECTOR icon + TEXT
- Right region: white FRAME with corner radius 20 + DROP_SHADOW effect, containing form-like children (rectangles + placeholder texts)

## Avada shortcode template (single container, 2 columns)

```text
[fusion_builder_container type="flex" hundred_percent="no" hundred_percent_height="no" flex_align_items="center" flex_justify_content="flex-start" hide_on_mobile="small-visibility,medium-visibility,large-visibility" background_color="#F5F6FA" padding_top="80px" padding_bottom="80px" padding_left="120px" padding_right="120px" padding_top_small="60px" padding_bottom_small="60px" padding_left_small="20px" padding_right_small="20px"]
  [fusion_builder_row]

    [fusion_builder_column type="1_2" type_small="1_1" layout="1_2" first="true" last="false" align_self="center" spacing_right="40px" padding_top="0" padding_right="0" padding_bottom="0" padding_left="0"]
      EYEBROW + HEADLINE + BODY + CHECKLIST
    [/fusion_builder_column]

    [fusion_builder_column type="1_2" type_small="1_1" layout="1_2" first="false" last="true" align_self="center" background_color="#FFFFFF" border_radius_top_left="20px" border_radius_top_right="20px" border_radius_bottom_left="20px" border_radius_bottom_right="20px" box_shadow="yes" box_shadow_vertical="16px" box_shadow_blur="48px" box_shadow_color="rgba(13,17,38,0.08)" padding_top="40px" padding_right="40px" padding_bottom="40px" padding_left="40px"]
      FORM (Avada Forms)
    [/fusion_builder_column]

  [/fusion_builder_row]
[/fusion_builder_container]
```

## Left column content

```text
[fusion_title size="6" font_size="12px" text_transform="uppercase" letter_spacing="0.14em" text_color="#2134EA" content_align="left" style_type="default" sep_color="" margin_bottom="16px" fusion_font_family_title_font="Manrope" fusion_font_variant_title_font="600"]EYEBROW[/fusion_title]

[fusion_title size="2" font_size="48px" line_height="56px" text_color="#0D0D26" content_align="left" style_type="default" sep_color="" margin_bottom="20px" fusion_font_family_title_font="Manrope" fusion_font_variant_title_font="700"]HEADLINE LINE 1<br />HEADLINE LINE 2[/fusion_title]

[fusion_text font_size="17px" line_height="28px" text_color="#6C7080" content_alignment="left" fusion_font_family_text_font="Manrope" fusion_font_variant_text_font="400"]<p>BODY paragraph.</p>[/fusion_text]

[fusion_separator style_type="none" hide_on_mobile="small-visibility,medium-visibility,large-visibility" sep_color="" top_margin="32" bottom_margin="0" border_size="" icon="" alignment="center"][/fusion_separator]

[fusion_checklist iconcolor="#2134EA" circle="no" size="14" item_padding="0px 0px 12px 0px" hide_on_mobile="small-visibility,medium-visibility,large-visibility"]
  [fusion_li_item icon="fa-chevron-right fas"]BENEFIT 1[/fusion_li_item]
  [fusion_li_item icon="fa-chevron-right fas"]BENEFIT 2[/fusion_li_item]
  [fusion_li_item icon="fa-chevron-right fas"]BENEFIT 3[/fusion_li_item]
[/fusion_checklist]
```

Note on `[fusion_li_item icon="fa-chevron-right fas"]`: the `icon` param takes a FontAwesome class name. **LP brand uses chevron-right `›` as the bullet marker** (NOT a check-mark) — this matches the chevron pattern motif present in all dark sections, case eyebrows, and brand decoration. The wrapping `[fusion_checklist circle="no" iconcolor="#2134EA"]` renders the chevron in LP-blue, no surrounding circle.

Avoid `fa-check` with circle background — that's generic SaaS-app aesthetic, not LP brand.

## Right column content (Avada Form)

```text
[fusion_title size="3" font_size="26px" line_height="32px" text_color="#0D0D26" content_align="left" style_type="default" sep_color="" margin_bottom="6px" fusion_font_family_title_font="Manrope" fusion_font_variant_title_font="700"]Залиште заявку[/fusion_title]

[fusion_text font_size="14px" line_height="20px" text_color="#6C7080" content_alignment="left" margin_bottom="24px" fusion_font_family_text_font="Manrope" fusion_font_variant_text_font="400"]<p>Відповімо протягом 2 годин у робочий час</p>[/fusion_text]

[fusion_form form_post_id="0" margin_bottom="0"]
  [fusion_form_text name="full_name" label="" placeholder="Ваше імʼя" required="yes" input_field_icon="fa-user" /]
  [fusion_form_email name="email" label="" placeholder="Робочий email" required="yes" input_field_icon="fa-envelope" /]
  [fusion_form_phone_number name="phone" label="" placeholder="Телефон (необовʼязково)" required="no" input_field_icon="fa-phone" /]
  [fusion_form_textarea name="message" label="" placeholder="Коротко про задачу" required="no" rows="3" /]
  [fusion_form_submit margin_top="16px" /]
[/fusion_form]

[fusion_text font_size="12px" line_height="16px" text_color="#6C7080" content_alignment="center" margin_top="16px" margin_bottom="0" fusion_font_family_text_font="Manrope" fusion_font_variant_text_font="400"]<p>Без спаму. Один дзвінок і конкретний план.</p>[/fusion_text]
```

## ⚠️ Critical: form_post_id placeholder rule (learned in Phase 3 Light CTA test)

**NEVER use string placeholders like `{{FORM_POST_ID}}` for the `form_post_id` attribute.** Avada Builder tries to parse it as integer and **hangs the editor**. The whole page becomes unresponsive — Володимир had to recover via browser refresh.

**Safe approach:** generate with `form_post_id="0"`. Avada won't find form ID 0 → renders nothing where the form would be, but the page stays fully editable. Replace `0` with the real form ID **after creating the form** (see steps below).

## Form setup steps for Володимир (manual, one-time per page)

Avada Forms require a separate form post to exist before the shortcode can reference it:

1. WP Admin → **Avada → Forms → Add New**
2. Form name: "Linked Promo - PPC Landing CTA"
3. Add fields (just create blank Avada Form, the actual fields go inline via shortcode)
4. Form settings:
   - **Email Recipient:** moskalyuk.v@linked-promo.com
   - **Email Subject:** "Нова заявка з PPC лендінгу"
   - **Success message:** "Дякуємо! Звʼяжемося протягом 2 годин."
   - **Email content:** include all field names via `{full_name}`, `{email}`, `{phone}`, `{message}` placeholders
   - **Submit button text:** override "Submit" → "Отримати стратегію →" (or via shortcode `[fusion_form_submit text="..." /]`)
5. Publish → copy the form post ID from URL (`post.php?post=NNN`)
6. Open `final-cta-light.shortcode.txt`, **replace `{{FORM_POST_ID}}`** with the actual ID
7. Paste shortcode into Avada Builder Code View on the page

If we skip Avada Forms and use static visual instead (faster but no submission), the right column becomes 4 styled `[fusion_text]` blocks + a `[fusion_button]` — but then form submissions don't work, defeating the CTA purpose.

## Variable substitution from brief

| Variable | Source in brief |
|---|---|
| `EYEBROW` | TEXT child in left region with `font_size: 12px` AND `letterSpacing.value >= 14` |
| `HEADLINE LINE 1`, `LINE 2` | The largest TEXT (font_size: 48px) in left region. Split on `\n` |
| `BODY` | TEXT below headline, font 17px, color `#6C7080` |
| `BENEFIT 1/2/3` | The 3 TEXT children adjacent to check-icon frames (color `#0D0D26`, font 16px Medium) |
| `Form title` | TEXT inside Form Card with font_size: 26px |
| `Form sub` | TEXT inside Form Card with font_size: 14px and color `#6C7080` |
| Form field placeholders | TEXT children in Form Card with color `#9CA0B0` (the LP placeholder color) — in order: name, email, phone, message |
| `Submit button text` | TEXT inside the button rectangle (font_size: 16px SemiBold WHITE) |
| `Disclaimer` | Last TEXT in Form Card with font_size: 12px |

## Equal-height columns

`flex_align_items="center"` on container vertically centers the columns within the container. If left content is shorter than right (which is our case — form card is 520px tall, left content ~450px), Avada flex handles spacing automatically.

For **identical column heights** (matching backgrounds), use `flex_align_items="stretch"` instead. We don't need that here because the form card has its own white background; the left side is transparent against `#F5F6FA` container.

## Anti-patterns (do NOT generate)

❌ Generating form as static `[fusion_text]` blocks just because Figma shows visual inputs. The form must be a real `[fusion_form]` — Володимир needs to capture leads.

❌ Hardcoding `form_post_id`. Always use `{{FORM_POST_ID}}` placeholder — every WP install has different IDs.

❌ Using `[fusion_button]` standalone for the submit. Avada Forms have their own `[fusion_form_submit]` that handles AJAX, validation, success state. Standalone button doesn't submit.

❌ Nested rows. Same rule as FAQ pattern — one container, one row.

## Mobile (responsive)

`type_small="1_1"` on both columns → form card drops below the marketing text on mobile. Container side padding reduces via `padding_left_small="20px"`.

The white form card with shadow on mobile is the same width as the screen minus padding. Box shadow stays visible.