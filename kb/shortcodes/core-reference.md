---
title: core-reference
type: note
permalink: ai/figma-to-avada/kb/shortcodes/core-reference
---

# Core 10 — practical Avada shortcode reference

Hand-curated reference for the 10 shortcodes used 95% of the time when generating LP landing pages. For full param lists see `catalog.json`.

## Quick syntax rules (CRITICAL — Avada parser is strict)

- **Single line per shortcode.** No newlines or blank lines between or inside tags.
- `[fusion_text]` content wrapped in `<p>` inline: `[fusion_text ...]<p>Body.</p>[/fusion_text]`
- `[fusion_title]` content inline without `<p>`: `[fusion_title ...]Headline[/fusion_title]`
- **No HTML comments** between shortcode tags — parser rejects them
- `animation_delay` in **seconds decimal**: `animation_delay="0.2"` = 200ms (NOT `"200"` = 200 seconds!)
- Empty attribute values omit the attribute entirely: not `type_medium=""`, just leave it out
- Column fractions: `1_1`, `1_2`, `1_3`, `2_3`, `1_4`, `3_4`, `1_5`, `2_5`, `3_5`, `1_6`, `5_6`
- Responsive: `type_small="1_1"` to stack on mobile

---

## 1. `[fusion_builder_container]` — page section wrapper

185 params total. The 12 you actually use:

```text
[fusion_builder_container
  type="flex"
  hundred_percent="no"
  hundred_percent_height="no"
  align_content="stretch"
  flex_align_items="flex-start"
  flex_justify_content="flex-start"
  hide_on_mobile="small-visibility,medium-visibility,large-visibility"
  background_color="#0D0D26"
  padding_top="80px"
  padding_bottom="80px"
  padding_left="120px"
  padding_right="120px"
]
  [fusion_builder_row]...[/fusion_builder_row]
[/fusion_builder_container]
```

- `type="flex"` — always (default since Avada 7+). Older `type="legacy"` exists but never use it for new builds.
- `hundred_percent="yes"` = full-width container ignoring page max-width.
- `background_color` = hex with `#`. Use brand tokens (LP NAVY `#0D0D26`).
- Padding always 4 sides explicit. Mobile via `padding_top_small`, etc.

---

## 2. `[fusion_builder_row]` — row inside container

2 own params + inherits. Just a wrapper, no styling. **Every container has exactly one row.**

```text
[fusion_builder_row]
  [fusion_builder_column ...]...[/fusion_builder_column]
[/fusion_builder_row]
```

---

## 3. `[fusion_builder_column]` — column inside row

188 params inherited from `class-fusion-column-element.php`. The 10 you actually use:

```text
[fusion_builder_column
  type="1_2"
  type_small="1_1"
  layout="1_2"
  align_self="auto"
  background_color="rgba(255,255,255,0.04)"
  border_color="rgba(255,255,255,0.08)"
  border_style="solid"
  border_width="1px"
  border_radius_top_left="16px"
  border_radius_top_right="16px"
  border_radius_bottom_left="16px"
  border_radius_bottom_right="16px"
  padding_top="32px"
  padding_right="32px"
  padding_bottom="32px"
  padding_left="32px"
  first="true"
  last="false"
]
  ...elements inside...
[/fusion_builder_column]
```

- `type` = fraction. `type_small="1_1"` = stack full-width on mobile.
- `first="true"` on first column of row, `last="true"` on last (`true` for single-column rows).
- Border radius is 4 separate corners — NOT a single `border_radius`.
- Background can be `rgba(...)` for transparency.

---

## 4. `[fusion_title]` — headings

82 params. Most relevant 10:

```text
[fusion_title
  hide_on_mobile="small-visibility,medium-visibility,large-visibility"
  title_type="text"
  rotation_effect="bounceIn"
  display_time="1200"
  loop_animation="once"
  content_align_medium=""
  content_align_small=""
  content_align="center"
  size="2"
  font_size="48px"
  line_height="58px"
  letter_spacing="0"
  text_color="#FFFFFF"
  text_transform="none"
  margin_top="0"
  margin_bottom="0"
  style_type="default"
  sep_color=""
  animation_delay="0"
]Що варто знати перед стартом[/fusion_title]
```

- `size="1"` to `"6"` = h1 to h6
- `content_align` = `left|center|right`
- For **eyebrow** style (small uppercase) — `size="6"`, `font_size="12px"`, `text_transform="uppercase"`, `letter_spacing="0.12em"`, color brand BLUE
- For **headline** — `size="2"`, big font, white/navy
- Default `style_type` adds a bottom border separator — set `style_type="default"` and `sep_color=""` to skip

---

## 5. `[fusion_text]` — body text

51 params. Most relevant 8:

```text
[fusion_text
  hide_on_mobile="small-visibility,medium-visibility,large-visibility"
  columns="1"
  font_size="14px"
  line_height="22px"
  text_color="rgba(255,255,255,0.6)"
  content_alignment="left"
  margin_top="0"
  margin_bottom="0"
  animation_delay="0"
]<p>3 етапи: підготовка $50-200...</p>[/fusion_text]
```

- Content must be wrapped in `<p>` inline. Multi-paragraph = multiple `<p>` tags, no newlines between.
- `text_color` accepts hex or rgba.
- For small note text — use small `font_size` and `text_color` with low alpha.

---

## 6. `[fusion_button]` — CTA buttons

90 params. Most relevant 12:

```text
[fusion_button
  link="https://linked-promo.com/ppc"
  text_transform="none"
  target="_self"
  hide_on_mobile="small-visibility,medium-visibility,large-visibility"
  type="flat"
  size="large"
  stretch="default"
  border_radius="12px"
  color="custom"
  button_gradient_top_color="#2134EA"
  button_gradient_bottom_color="#2134EA"
  button_gradient_top_color_hover="#1A2BC0"
  button_gradient_bottom_color_hover="#1A2BC0"
  accent_color="#FFFFFF"
  accent_hover_color="#FFFFFF"
  bevel_color=""
  border_top="0"
  border_right="0"
  border_bottom="0"
  border_left="0"
]Отримати стратегію →[/fusion_button]
```

- `type="flat"` = solid color (recommended). `type="3d"` deprecated.
- `color="custom"` enables `button_gradient_*` overrides. Otherwise pulls from theme.
- `size` = `small|medium|large|xlarge`
- For LP brand button: solid `#2134EA`, white text, no border, 12px corner radius.

---

## 7. `[fusion_imageframe]` — images

108 params. Most relevant 10:

```text
[fusion_imageframe
  image_id="123|full"
  max_width=""
  sticky_max_width=""
  skip_lazy_load=""
  hide_on_mobile="small-visibility,medium-visibility,large-visibility"
  style_type="none"
  blur=""
  stylecolor=""
  hover_type="none"
  bordersize="0"
  borderradius="0"
  align_medium="none"
  align_small="none"
  align="none"
  margin_top=""
  margin_bottom=""
  lightbox="no"
  alt="Hero illustration"
  link=""
]https://linked-promo.com/wp-content/uploads/2026/05/hero.webp[/fusion_imageframe]
```

- `image_id="NNN|full"` — the `NNN` is the WP media library ID, `|full` is the size. For our pipeline, Володимир uploads and gives us URL + ID.
- Image URL goes between the tags, NOT in an `src=` attribute.
- `alt` is required for accessibility.

---

## 8. `[fusion_separator]` — divider

24 params. Most relevant 6:

```text
[fusion_separator
  style_type="single solid"
  hide_on_mobile="small-visibility,medium-visibility,large-visibility"
  sep_color="rgba(255,255,255,0.1)"
  border_size="1"
  width=""
  alignment="center"
  bottom_margin="40px"
]
[/fusion_separator]
```

- `style_type` options: `none|single solid|single dashed|single dotted|double solid|double dashed|double dotted|shadow`
- Empty `width` = 100% of column.

---

## 9. `[fusion_form]` + form fields — forms

`fusion_form.php` (78 params) wraps any form. Fields live inside `form/` directory:

- `email.php` → `[fusion_email]`
- `phone-number.php` → `[fusion_phone_number]`
- `text.php` → `[fusion_text]` *(NB: collides with body text shortcode — Avada uses context to disambiguate)*
- `textarea.php` → `[fusion_textarea]`
- `submit.php` → `[fusion_submit]`
- `checkbox.php` → `[fusion_checkbox]`
- `select.php` → `[fusion_select]`
- `consent.php` → `[fusion_consent]` (GDPR)
- `recaptcha.php` → `[fusion_recaptcha]`
- `honeypot.php` → `[fusion_honeypot]` (spam protection)

```text
[fusion_form form_post_id="123" margin_bottom="20px"]
  [fusion_text name="full_name" label="Ваше імʼя" placeholder="" required="yes"][/fusion_text]
  [fusion_email name="email" label="Робочий email" required="yes"][/fusion_email]
  [fusion_phone_number name="phone" label="Телефон" required="no"][/fusion_phone_number]
  [fusion_textarea name="message" label="Коротко про задачу" required="no"][/fusion_textarea]
  [fusion_honeypot][/fusion_honeypot]
  [fusion_submit text="Отримати стратегію →"][/fusion_submit]
[/fusion_form]
```

- `form_post_id` — Avada Forms are stored as separate posts. Володимир creates form in `Avada → Forms` admin, gets ID, we paste it.
- Each field has `name` (DB key), `label` (visible), `placeholder`, `required`.

---

## 10. `[fusion_toggle]` — accordion (FAQ alternative)

For FAQ blocks where collapse/expand is wanted instead of always-visible cards:

```text
[fusion_accordion type="" boxed_mode="" border_size="1" border_color="" background_color="" hover_color="" divider_line="" title_font_size="" icon_size="" icon_color="" icon_boxed_mode="" icon_box_color="" icon_alignment="left" toggle_hover_accent_color="" hide_on_mobile="small-visibility,medium-visibility,large-visibility"]
  [fusion_toggle title="Скільки коштує?" open="no"]<p>3 етапи: підготовка $50-200...</p>[/fusion_toggle]
  [fusion_toggle title="Через скільки буде перший лід?" open="no"]<p>Підготовчий етап - до 2 тижнів...</p>[/fusion_toggle]
[/fusion_accordion]
```

For our PPC Landing FAQ block we built **grid 2x3 of always-visible cards** — that maps to `fusion_builder_column` 2-wide with text inside, NOT to fusion_toggle. Use toggle only if user wants click-to-expand UX.

---

## Common patterns

### Eyebrow + Headline + Body stack (centered)

```text
[fusion_title size="6" font_size="12px" text_transform="uppercase" letter_spacing="0.12em" text_color="#2134EA" content_align="center" style_type="default" sep_color=""]ЧАСТІ ПИТАННЯ[/fusion_title]
[fusion_title size="2" font_size="48px" line_height="58px" text_color="#FFFFFF" content_align="center" style_type="default" sep_color=""]Що варто знати перед стартом[/fusion_title]
[fusion_text font_size="18px" line_height="28px" text_color="rgba(255,255,255,0.6)" content_alignment="center"]<p>Відповіді на типові питання - без юридичної води.</p>[/fusion_text]
```

### 3-column row of cards (responsive)

```text
[fusion_builder_row]
  [fusion_builder_column type="1_3" type_small="1_1" first="true" last="false" padding_top="32px" padding_right="32px" padding_bottom="32px" padding_left="32px" background_color="rgba(255,255,255,0.04)" border_radius_top_left="16px" border_radius_top_right="16px" border_radius_bottom_left="16px" border_radius_bottom_right="16px"]
    ...card 1 content...
  [/fusion_builder_column]
  [fusion_builder_column type="1_3" type_small="1_1" first="false" last="false" ...]
    ...card 2 content...
  [/fusion_builder_column]
  [fusion_builder_column type="1_3" type_small="1_1" first="false" last="true" ...]
    ...card 3 content...
  [/fusion_builder_column]
[/fusion_builder_row]
```

---

## Where defaults come from

Every shortcode has a `get_element_defaults()` method in its PHP file. Values like `_dynamic` in our catalog represent calls to `$fusion_settings->get('setting_name')` — these depend on user's theme options. When generating, **always set explicit values** for typography, colors, spacing — don't rely on theme defaults, which vary per install.

## LP-specific brand tokens

| Token | Value | Use |
|---|---|---|
| `--lp-navy` | `#0D0D26` | Dark backgrounds (FAQ, hero) |
| `--lp-blue` | `#2134EA` | Primary CTA, accents, eyebrow |
| `--lp-blue-hover` | `#1A2BC0` | Button hover |
| `--lp-light` | `#F5F6FA` | Light backgrounds (Final CTA) |
| `--lp-white` | `#FFFFFF` | Text on dark, form card bg |
| `--lp-text-muted` | `rgba(255,255,255,0.6)` | Body text on dark |
| `--lp-text-gray` | `#6C7080` | Body text on light |
| `--lp-border-soft` | `rgba(255,255,255,0.08)` | Card borders on dark |

Font: **Manrope** (Google Fonts) — Regular, Medium, SemiBold, Bold, ExtraBold.