---
title: lp-design-tokens
type: note
permalink: ai/figma-to-avada/kb/tokens/lp-design-tokens
---

# LP design tokens → Avada mapping

Single source of truth for LP brand values when generating Avada shortcodes. Generator MUST resolve Figma colors/fonts to these tokens, never hardcode arbitrary values.

## Colors

### Primary palette

| Token | Hex | rgba (when used) | Figma source | Avada usage |
|---|---|---|---|---|
| `--lp-navy` | `#0D0D26` | — | FAQ background, dark sections | `background_color="#0D0D26"` on container |
| `--lp-blue` | `#2134EA` | — | Primary CTA, eyebrow text, accent fills | `button_gradient_top/bottom`, `text_color` on titles |
| `--lp-blue-hover` | `#1A2BC0` | — | Button hover state | `button_gradient_top/bottom_color_hover` |
| `--lp-white` | `#FFFFFF` | — | Text on dark, light card bg | `text_color`, `background_color` |
| `--lp-light-bg` | `#F5F6FA` | — | Light section bg (Final CTA) | `background_color` on container |
| `--lp-gray-text` | `#6C7080` | — | Body text on light bg | `text_color` |
| `--lp-placeholder` | `#9CA0B0` | — | Form field placeholders | input `placeholder_color` |
| `--lp-input-bg` | `#F5F6FA` | — | Form input fill | input field background |

### Functional alphas (on dark bg)

| Token | Value | Usage |
|---|---|---|
| `--lp-text-muted` | `rgba(255,255,255,0.6)` | Body text, secondary labels |
| `--lp-text-faint` | `rgba(255,255,255,0.4)` | Disclaimers, fine print |
| `--lp-border-soft` | `rgba(255,255,255,0.08)` | Card borders on dark |
| `--lp-fill-soft` | `rgba(255,255,255,0.04)` | Card backgrounds on dark |

## Typography

### Font family

**Manrope** (Google Fonts) — ONLY font used in LP system. No fallbacks beyond `sans-serif`.

```text
fusion_font_family_*_font="Manrope"
fusion_font_variant_*_font="500"  // or 700, etc.
```

### Type scale (matched to Figma builds)

| Element | Figma | Avada `font_size` | `line_height` | `font_style` | Letter spacing |
|---|---|---|---|---|---|
| **Eyebrow** (uppercase label) | SemiBold 12px | `12px` | auto | `600` | `0.12em` (`letter_spacing="0.12"`) |
| **H1 Hero** | Bold 56-64px | `56px` | `64px` | `700` | `0` |
| **H2 Section** | Bold 48px | `48px` | `58px` | `700` | `0` |
| **H3 Card title** | SemiBold 20px | `20px` | `28px` | `600` | `0` |
| **Body L** | Regular 18px | `18px` | `28px` | `400` | `0` |
| **Body M** (default) | Regular 16px | `16px` | `24px` | `400` | `0` |
| **Body S** (cards) | Regular 14px | `14px` | `22px` | `400` | `0` |
| **Caption** (disclaimers) | Regular 12px | `12px` | `16px` | `400` | `0` |
| **Button** | SemiBold 16px | `16px` | `24px` | `600` | `0` |

## Spacing rhythm

LP grid uses 8px increments. Common values:

| Avada `padding_*` / `margin_*` | Figma equivalent |
|---|---|
| `8px` | xs gap inside small components |
| `16px` | small gap between text blocks |
| `24px` | inside card padding |
| `32px` | medium gap, card padding wide |
| `40px` | between major elements in card |
| `60px` | between sections within block |
| `80px` | block top/bottom padding (default) |
| `120px` | block side padding (default for content width 1200) |

### Container content width

Standard LP block: 1440px outer, 120px side padding → 1200px content. `flex_align_items="center"` keeps content centered.

## Corner radius

| Element | Radius |
|---|---|
| Buttons | `12px` |
| Cards | `16px` |
| Form input fields | `10px` |
| Form card (outer) | `20px` |
| Icon badge / circle | `50%` (full circle) |

In Avada use 4 separate corner params (NOT a single `border_radius`):

```text
border_radius_top_left="16px"
border_radius_top_right="16px"
border_radius_bottom_left="16px"
border_radius_bottom_right="16px"
```

## Shadow / effects

LP uses subtle shadows mainly on **white cards on light backgrounds** (CTA form card on `#F5F6FA`).

| Element | Avada shadow approach |
|---|---|
| Form card on light | `box_shadow="yes" box_shadow_blur="48" box_shadow_color="rgba(13,17,38,0.08)" box_shadow_vertical="16"` |
| Card on dark | No shadow — use `border_color="rgba(255,255,255,0.08)"` instead |

Glow effects (gradient radial) and chevron patterns are **NOT Avada-native**. Generator emits them as:
- Background-image on the container (when whole block has glow)
- Custom CSS in `style` attribute or child theme (for complex layered glows)

## Animation defaults

LP landing has subtle fade-up animations on scroll for key elements:

```text
animation_type="fade"
animation_direction="up"
animation_speed="0.3"
animation_delay="0"
animation_offset="top-into-view"
```

Stagger via `animation_delay`: `"0"`, `"0.1"`, `"0.2"`, `"0.3"` on sequential cards.

## Resolution rules (Figma color → token)

When the extractor emits a color, the generator must match it to a token:

1. Exact hex match → use the token directly
2. Hex with slight variance (rounding errors from gradient stops) → snap to nearest token if within ΔE < 3
3. `rgba()` with `--lp-white` base → use the `--lp-text-*` family by alpha
4. Unknown color → emit raw hex AND warn in build log: "Color #XYZABC not in LP palette, manual review required"

## Font resolution rules

1. Figma uses `Manrope` → emit `fusion_font_family_*_font="Manrope"`
2. Figma uses other Google font → emit as-is + warn (off-brand)
3. Figma uses non-Google font → fail loudly. LP only uses web-safe Google fonts.

Figma `fontStyle` → Avada `font_variant`:

| Figma | Variant |
|---|---|
| `Light` | `300` |
| `Regular` | `400` |
| `Medium` | `500` |
| `SemiBold` | `600` |
| `Bold` | `700` |
| `ExtraBold` | `800` |
| `Black` | `900` |