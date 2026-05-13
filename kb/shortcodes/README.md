---
title: README
type: note
permalink: ai/figma-to-avada/kb/shortcodes/readme-1
---

# kb/shortcodes

Generated catalog of Avada Fusion Builder + Fusion Core shortcodes.

## Files

| File | Purpose |
|---|---|
| `_catalog-generator.py` | Parses PHP source → catalog.json + catalog.md |
| `catalog.json` | Full machine-readable catalog (160 entries, ~240KB) |
| `catalog.md` | Human-readable index grouped by plugin |
| `core-reference.md` | Hand-curated reference for the 10 shortcodes used 95% of the time |

## How catalog was built

For each PHP file under `fusion-builder/shortcodes/`, `fusion-builder/inc/`, and `fusion-core/shortcodes/`:

1. Find `function get_element_defaults()` method
2. Extract the `return [ ... ]` array  
3. Parse PHP key-value pairs into JSON
4. Find shortcode name via `add_shortcode('fusion_...')` or `$shortcode = 'fusion_...'` constructor pattern

## Numbers

- 160 total entries
- 101 named shortcodes (have `add_shortcode()` or constructor `$shortcode`)
- 59 unnamed (mostly inner components: post-cards parts, woo blocks, base classes)
- Top 5 by param count:
  - `class-fusion-column-element.php` — 188 (inherited by `fusion_builder_column`)
  - `fusion_builder_container` — 185
  - `fusion_imageframe` — 108
  - `fusion_button` — 90
  - `fusion_title` — 82

## Important: inheritance

Some shortcodes inherit defaults from base classes:

| Shortcode | Own defaults | Inherited from |
|---|---|---|
| `fusion_builder_row` | 2 | `class-fusion-row-element.php` |
| `fusion_builder_column` | 0 | `class-fusion-column-element.php` (188 params!) |

When generating row/column shortcodes, **always check the base class defaults** in catalog.json under the `_unnamed` entries.

## Regenerate

```bash
cd kb/shortcodes
python _catalog-generator.py
```

Re-run anytime Avada plugins are updated. Diff catalog.json to spot breaking changes between versions.

## Known gaps

- `_dynamic` markers in defaults represent PHP function calls (`$fusion_settings->get(...)`) — actual default depends on theme settings, not extractable from source alone.
- `_unparsed` markers represent complex expressions our regex parser didn't handle. Rare. Review manually if needed.
- 56 component files (`components/*.php`) have defaults but no shortcode name — these are used internally by post-cards and woo elements, not standalone.