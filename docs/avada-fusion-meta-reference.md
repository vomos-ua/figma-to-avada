---
title: avada-fusion-meta-reference
type: note
permalink: ai/figma-to-avada/docs/avada-fusion-meta-reference
---

# Avada `_fusion` post meta — reverse-engineered reference

**Date:** 2026-05-14
**Source:** Live extraction from `linked-promo.com` page #15658 ("PPC 2 Ads", draft) via `lp-meta-research` temp plugin REST endpoint.
**Avada Builder version:** 3.15.3 | **Avada Core:** 5.15.3 | **WP:** 6.9.4

## TL;DR

Creating a new Avada page via `wp_insert_post()` requires writing TWO post_meta keys for the Builder to recognize the page as editable:

```php
update_post_meta($page_id, 'fusion_builder_status', 'active');
update_post_meta($page_id, '_fusion', [
  // 21 keys below (defaults shown)
]);
```

No PHP serialization needed — WordPress's `update_post_meta()` auto-serializes arrays.

Optionally also track fonts used:

```php
update_post_meta($page_id, '_fusion_google_fonts', [
  'Manrope' => ['variants' => ['400', '600', '700']],
]);
```

## Full `_fusion` schema (21 keys)

All keys are **flat strings** except `main_padding` which is a 2-key dict. No nested complex structures.

| Key | Type | Real value on test page | Notes |
|---|---|---|---|
| `bg_full` | string | `"no"` | Background image full-screen? |
| `bg_repeat` | string | `"default"` | BG repeat behavior |
| `container_hundred_percent_animation` | string | `""` | Empty by default |
| `content_bg_full` | string | `"no"` | Content area BG full-screen? |
| `content_bg_repeat` | string | `"default"` | |
| `display_header` | string | `"yes"` | Show theme header? |
| `displayed_menu` | string | `"default"` | Which menu to show |
| `header_bg_full` | string | `"no"` | Header BG full-screen? |
| `header_bg_repeat` | string | `"repeat"` | |
| `main_padding` | dict | `{"top": "", "bottom": ""}` | Empty = use theme default |
| `page_title_bar` | string | `"no"` | Show breadcrumb bar? |
| `page_title_custom_text` | string | `"Реклама в соцмережах\r\n"` | Title for title bar (CRLF noise from textarea) |
| `pages_sidebar` | string | `"default_sidebar"` | Sidebar 1 widget area |
| `pages_sidebar_2` | string | `"default_sidebar"` | Sidebar 2 widget area |
| `seo_follow` | string | `"auto"` | Robots meta follow |
| `seo_index` | string | `"auto"` | Robots meta index |
| `show_first_featured_image` | string | `"yes"` | Show featured image at top |
| `sidebar_sticky` | string | `"default"` | Sticky sidebar behavior |
| `slider_type` | string | `"no"` | Header slider type (no = none) |
| `slider_visibility` | string | `"small-visibility,medium-visibility,large-visibility"` | Slider on which screen sizes |
| `wooslider` | string | `"0"` | WooCommerce slider ID (0 = none) |

## Safe defaults for `_fusion` when creating a new LP landing page

For typical LP landing pages (no header, no breadcrumb, no sidebars, full-width content):

```php
$default_fusion = [
  'bg_full' => 'no',
  'bg_repeat' => 'default',
  'container_hundred_percent_animation' => '',
  'content_bg_full' => 'no',
  'content_bg_repeat' => 'default',
  'display_header' => 'no',         // hide for landing pages
  'displayed_menu' => 'default',
  'header_bg_full' => 'no',
  'header_bg_repeat' => 'repeat',
  'main_padding' => ['top' => '0', 'bottom' => '0'],   // landing = flush edges
  'page_title_bar' => 'no',          // no breadcrumbs
  'page_title_custom_text' => '',
  'pages_sidebar' => 'default_sidebar',
  'pages_sidebar_2' => 'default_sidebar',
  'seo_follow' => 'auto',
  'seo_index' => 'auto',
  'show_first_featured_image' => 'no',
  'sidebar_sticky' => 'default',
  'slider_type' => 'no',
  'slider_visibility' => 'small-visibility,medium-visibility,large-visibility',
  'wooslider' => '0',
];
```

For PPC landings the key overrides vs test page:
- `display_header` → `"no"` (no nav for conversion-focused landing)
- `main_padding` → `0/0` (full bleed)
- `page_title_bar` → `"no"`
- `show_first_featured_image` → `"no"`

## `_wp_page_template` (separate meta, not part of _fusion)

The test page also has `_wp_page_template` = `100-width.php`. This is Avada's full-width page template — no sidebar, content stretches to viewport edges. For landing pages we want this:

```php
update_post_meta($page_id, '_wp_page_template', '100-width.php');
```

Other Avada templates available (from theme files): `default.php`, `blank.php`, `100-width.php`, `side-navigation.php`. For LP landings ALWAYS use `100-width.php` or `blank.php`.

## `_fusion_google_fonts` schema

Tracks which Google Fonts the page uses so Avada can preload them on render. Built from the `fusion_font_family_*_font` attributes parsed across the shortcode content:

```json
{
  "Manrope": {
    "variants": ["400", "600", "700"]
  }
}
```

Our generator already emits `fusion_font_family_title_font="Manrope"` + `fusion_font_variant_title_font="700"` on every title element. The plugin should:

1. Parse the generated shortcode for `fusion_font_variant_*` values
2. Group by font family
3. Deduplicate variants
4. Write the resulting map to `_fusion_google_fonts`

If we forget this meta key, Avada will still render — fonts load lazily on first reference. But explicit preload via this meta = better LCP score on Lighthouse.

## Other meta keys on the test page (informational, NOT required)

| Key | Purpose | Required for our plugin? |
|---|---|---|
| `_alp_processed` | Avada Layout Pack tracker | No (used by add-on, not core) |
| `_dp_original` | Duplicate Post plugin's original-post tracking | No (artefact of Володимир duplicating from page #15396) |
| `_edit_last` | User ID who last edited | No (WP auto) |
| `_edit_lock` | Edit lock timestamp + user | No (WP auto) |
| `_wpml_media_duplicate` | WPML media duplication flag | Only if multilingual page |
| `_wpml_media_featured` | WPML featured image flag | Only if multilingual page |
| `_wpml_word_count` | WPML translation cost estimator | Auto-populated by WPML |
| `_yoast_wpseo_*` | Yoast SEO meta (focus keyword, reading time, etc.) | Optional — populate if we generate SEO meta |
| `pages_sidebar` (top-level, NOT in _fusion) | Sidebar widget area mapping | Avada legacy, may be redundant with _fusion's pages_sidebar |
| `pages_sidebar_2` (top-level) | Sidebar 2 widget area mapping | Same as above |

## Minimum to create a working Avada page

```php
$page_id = wp_insert_post([
  'post_type' => 'page',
  'post_status' => 'draft',          // or 'publish'
  'post_title' => 'My PPC Landing',
  'post_name' => 'my-ppc-landing',   // slug
  'post_content' => $shortcode_text, // generated by our pipeline
]);

update_post_meta($page_id, 'fusion_builder_status', 'active');
update_post_meta($page_id, '_fusion', $default_fusion);
update_post_meta($page_id, '_wp_page_template', '100-width.php');
update_post_meta($page_id, '_fusion_google_fonts', $font_map);
```

4 meta keys + the `wp_insert_post` call. ~15 lines of PHP for the `lp-avada/create-page` ability. Much simpler than I feared.

## Anti-patterns

- **Don't** PHP-serialize values manually before passing to `update_post_meta()`. WP serializes automatically and DOUBLE-serializes if you do it manually → meta unreadable.
- **Don't** skip `fusion_builder_status="active"` — without it, the Avada Builder thinks the page wasn't built with it and falls back to native WP editor.
- **Don't** copy meta keys like `_alp_processed`, `_dp_original`, `_edit_*`, `_yoast_wpseo_*` blindly from other pages. Either set them appropriately or omit.

## Next step

Phase B unblocked. Write `linked-promo-avada-mcp` plugin with `lp-avada/create-page` ability using this schema. Estimated 1 day of PHP work for Tier 1 abilities (create-page, update-page, upload-media).

## Cleanup

`lp-meta-research` temp plugin can now be deactivated and deleted from `linked-promo.com`. All useful data extracted.