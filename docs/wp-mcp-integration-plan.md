---
title: wp-mcp-integration-plan
type: note
permalink: ai/figma-to-avada/docs/wp-mcp-integration-plan-1
---

# WP MCP Integration Plan — LP-Avada Abilities Plugin

**Date:** 2026-05-13
**Status:** Phase B blueprint (not yet implemented — current focus is Phase 0-3 manual pipeline)
**Replaces decision in:** `docs/wp-mcp-adapter-evaluation.md` (first-pass eval was too narrow)

## Reframe of prior recommendation

The first evaluation compared **empty mcp-adapter** vs **raw WP REST API**. Wrong comparison.

The right comparison is:

| Approach | Effort | Reuse value |
|---|---|---|
| Raw WP REST API + Application Password, per-project Claude skill | 1 hour per project | None — duplicated work each time |
| **LP-Avada Abilities plugin (one-time) + mcp-adapter transport** | **2-3 days once** | **Used on every LP-Avada client forever** |

LP works on Avada continuously. Custom plugin's PHP code lives **once** in our private repo, installs on each client WP, exposes the same MCP interface everywhere. Pays for itself by client #2.

## Architecture

```
Figma Desktop (Bridge plugin)
   ↓ figma-console MCP (no token)
extractor → brief.json + images/

KB (catalog, patterns, tokens) + brief
   ↓
generator (Claude skill) → shortcode.txt

   ↓ via @automattic/mcp-wordpress-remote (npm proxy)
WordPress + mcp-adapter
   ↓ exposes
LP-Avada Abilities Plugin:
   • lp-avada/create-page
   • lp-avada/update-page
   • lp-avada/upload-media
   • lp-avada/list-forms
   • lp-avada/create-form
   • lp-avada/get-page-shortcode
   • lp-avada/list-pages
   • lp-avada/validate-shortcode

   ↓ writes
WP database (posts + postmeta with Avada-specific keys)
   ↓
mcp-chrome (DevTools)
   ↓ verifies
Rendered page vs Figma reference
   ↓
LLM diff analysis → iteration (if needed)
```

This is the full **Figma → Avada autonomous loop** Володимир described two days ago. Concrete path.

## Abilities to implement (priority order)

### Tier 1 — Critical (MVP)

#### 1. `lp-avada/create-page`

Create a new Avada page with shortcode content and the correct Builder meta.

```php
[
  'input_schema' => [
    'type' => 'object',
    'properties' => [
      'title' => ['type' => 'string', 'required' => true],
      'slug' => ['type' => 'string'],
      'parent_id' => ['type' => 'integer'],
      'status' => ['type' => 'string', 'enum' => ['draft', 'publish'], 'default' => 'draft'],
      'shortcode' => ['type' => 'string', 'required' => true, 'description' => 'Avada Fusion Builder shortcode content'],
    ],
  ],
  'output_schema' => [
    'page_id' => 'integer',
    'page_url' => 'string',
    'edit_url' => 'string',
  ],
]
```

Implementation:
```php
$page_id = wp_insert_post([
  'post_type' => 'page',
  'post_status' => $status,
  'post_title' => $title,
  'post_name' => $slug,
  'post_parent' => $parent_id,
  'post_content' => $shortcode,
]);
update_post_meta($page_id, 'fusion_builder_status', 'active');
update_post_meta($page_id, '_fusion', serialize($default_fusion_settings));
```

`$default_fusion_settings` is the empty Avada page meta array — needs reverse-engineering from a fresh Avada page export. One-time research task.

#### 2. `lp-avada/update-page`

Replace existing page content. Idempotent.

```php
[
  'input_schema' => [
    'page_id' => 'integer',
    'shortcode' => 'string',
    'status' => 'string (optional)',
  ],
]
```

#### 3. `lp-avada/upload-media`

Upload image to WP Media Library, return URL + media_id (needed for `[fusion_imageframe image_id="NNN|full"]`).

```php
[
  'input_schema' => [
    'base64_content' => 'string',
    'filename' => 'string',
    'alt_text' => 'string',
    'mime_type' => 'string',
  ],
  'output_schema' => [
    'media_id' => 'integer',
    'url' => 'string',
    'webp_url' => 'string (if WebP generated)',
  ],
]
```

Uses `wp_handle_upload` + `wp_insert_attachment` + `wp_update_attachment_metadata`.

### Tier 2 — Forms support

#### 4. `lp-avada/list-forms`

Returns existing Avada Form posts. Needed to find `form_post_id` for `[fusion_form]`.

```php
[
  'output_schema' => [
    'forms' => [
      ['id' => 'integer', 'title' => 'string', 'created_at' => 'string'],
    ],
  ],
]
```

Query: `get_posts(['post_type' => 'fusion_form', 'numberposts' => -1])`.

#### 5. `lp-avada/create-form`

Create new Avada Form. Generator can auto-create on first use instead of asking user.

```php
[
  'input_schema' => [
    'name' => 'string',
    'email_to' => 'string',
    'subject' => 'string',
    'success_message' => 'string',
    'submit_button_text' => 'string',
  ],
  'output_schema' => [
    'form_id' => 'integer',
  ],
]
```

### Tier 3 — Read + diagnostics

#### 6. `lp-avada/get-page-shortcode`

Read existing page's shortcode. Useful for diff against generated version.

#### 7. `lp-avada/list-pages`

List pages with title/slug/status filter.

#### 8. `lp-avada/validate-shortcode`

Server-side shortcode parse check. Avada has `FusionBuilder::set_shortcode_defaults` we can call to catch malformed tags before they're pasted.

Returns `{ valid: bool, errors: [{line, column, message}] }`.

## Resources (MCP component, not tools)

Beyond tools, expose **read-only LP knowledge** as MCP resources Claude can pull on-demand:

#### `lp-avada://catalog/shortcodes`

Returns `kb/shortcodes/catalog.json` — all 160 shortcode definitions. Claude reads this to know valid params.

#### `lp-avada://kb/patterns`

Returns list of LP patterns (`kb/patterns/*.md`). Each pattern is a resource Claude can fetch.

#### `lp-avada://kb/tokens`

LP design tokens (`kb/tokens/lp-design-tokens.md`).

Resources are cached by Claude → no repeat fetches per session.

## Prompts (third MCP component)

Pre-built prompt templates exposed to Claude. User-facing trigger: "Generate Avada page from Figma frame".

#### `lp-avada/generate-page-from-figma`

```yaml
arguments:
  - figma_node_id (string, required)
  - target_page_slug (string, required)
  - parent_page_id (integer, optional)
template: |
  You are generating an Avada Fusion Builder page from Figma node {figma_node_id}.

  Steps:
  1. Call mcp__figma-console__figma_execute with the LP extractor (path: extractor/extract.js, substitute NODE_ID={figma_node_id})
  2. Read the returned brief JSON
  3. Fetch lp-avada://catalog/shortcodes and lp-avada://kb/patterns for context
  4. Match the brief to a known pattern, or fall back to generic container/row/column
  5. Apply LP design tokens (lp-avada://kb/tokens)
  6. Call lp-avada/upload-media for each image asset in the brief
  7. Call lp-avada/create-page with the generated shortcode + uploaded image URLs

  Critical Avada rules:
  - ONE container = ONE row (multiple rows in one container are flattened)
  - animation_delay in SECONDS DECIMAL ("0.2" = 200ms)
  - No HTML comments between shortcode tags
  - All form fields require a real form_post_id (call lp-avada/list-forms or lp-avada/create-form)
```

This is HUGE: Володимир (or any LP team member) can trigger the full pipeline from a slash command in Claude without explaining the procedure each time.

## File layout

```
linked-promo-avada-mcp/                       (separate GitHub repo)
├── linked-promo-avada-mcp.php                # Main plugin file (bootstrap)
├── composer.json                              # Requires wordpress/mcp-adapter
├── README.md
├── includes/
│   ├── class-lp-abilities-registrar.php      # Hooks into mcp_adapter_init, registers all abilities
│   ├── abilities/
│   │   ├── class-create-page-ability.php
│   │   ├── class-update-page-ability.php
│   │   ├── class-upload-media-ability.php
│   │   ├── class-list-forms-ability.php
│   │   ├── class-create-form-ability.php
│   │   └── ...
│   ├── resources/
│   │   ├── class-catalog-resource.php        # exposes kb/shortcodes/catalog.json
│   │   ├── class-patterns-resource.php
│   │   └── class-tokens-resource.php
│   └── prompts/
│       └── class-generate-page-prompt.php
├── vendor/                                    # composer install
└── languages/
```

## Deployment process

1. Володимир creates Application Password in WP admin
2. SSH or wp-cli: `wp plugin install <github_release_url>` or upload zip
3. Activate plugin → adapter auto-registers default server
4. Verify: `wp mcp-adapter list` shows `mcp-adapter-default-server`
5. Verify: `wp mcp-adapter serve --user=admin --server=mcp-adapter-default-server` accepts STDIO
6. Claude Code `.mcp.json` adds:

```json
{
  "mcpServers": {
    "lp-wp": {
      "command": "npx",
      "args": ["-y", "@automattic/mcp-wordpress-remote"],
      "env": {
        "WP_API_URL": "https://client-site.com/wp-json/mcp/mcp-adapter-default-server",
        "WP_API_USERNAME": "vomos",
        "WP_API_PASSWORD": "xxxx xxxx xxxx xxxx"
      }
    }
  }
}
```

7. Claude can now call `mcp__lp-wp__execute-ability` with `{ability_name: 'lp-avada/create-page', ...}`.

## Effort estimate

| Task | Time |
|---|---|
| Plugin bootstrap + Composer + Jetpack autoloader | 0.5 day |
| `_fusion` meta reverse-engineering (export fresh Avada page, document the array structure) | 0.5 day |
| Implement 5 Tier 1 abilities + tests | 1 day |
| Implement Tier 2 form abilities | 0.5 day |
| Implement Resources + Prompts | 0.5 day |
| End-to-end test (Figma → generator → adapter → WP page created) | 1 day |
| Documentation + handoff guide for LP team | 0.5 day |
| **TOTAL** | **~4.5 days** |

vs. raw WP REST API: 1 hour to wire up, BUT no reuse → 1 hour per future project. Adapter pays off after ~5 projects.

## Risks

| Risk | Mitigation |
|---|---|
| mcp-adapter pre-1.0 breaking changes | Pin version in composer.json, test before bumping |
| `_fusion` meta structure changes between Avada versions | Diff exports between versions, parameterize schema |
| Client WP host blocks long-running PHP (composer install) | Pre-build plugin zip with vendor/ included |
| Application Password disabled by host (some managed WP block this) | Fallback to JWT or OAuth (mcp-adapter supports both) |
| Multiple plugins using mcp-adapter version conflicts | Use Jetpack Autoloader as recommended in README |

## Prerequisites before starting Phase B

- [ ] Phase 0-3 fully validated (currently in progress)
- [ ] **At least 5 working patterns** in `kb/patterns/` (currently 2: FAQ + Light CTA)
- [ ] **Reverse-engineered `_fusion` meta** structure documented in `docs/avada-fusion-meta-reference.md`
- [ ] Володимир has dev WP env for testing (Hostinger sandbox)
- [ ] Володимир decides: separate repo `vomos-ua/linked-promo-avada-mcp` or monorepo with `figma-to-avada`?

## Decision

**Adopt mcp-adapter for Phase B.** Update prior eval doc with this reframe.

**Do not start Phase B yet** — current focus must be:
1. Validate Light CTA in WP (current pending step for Володимир)
2. Build 3 more patterns: Stats Strip, Cases Slider, Hero (with dashboard as image)
3. Complete PPC Landing end-to-end via manual paste flow
4. Document lessons → grow KB

After PPC Landing is done, we have data on real friction. Then Phase B kicks off with clarity on what abilities ACTUALLY matter.

**Soft deadline for Phase B start:** when KB has 6+ patterns + we've manually shipped 1 full Avada landing.

## Open questions for Володимир

1. **Repo strategy:** separate `vomos-ua/linked-promo-avada-mcp` (cleaner) or fold into `figma-to-avada` (faster start)?
2. **Plugin scope:** LP-private (only for LP-owned client Avada sites) or open-source as a community contribution?
3. **WP version target:** require 6.9+ (clean, Abilities API in core) or support 6.8 with `wordpress/abilities-api` plugin (archived Feb 2026 — risky)?
4. **Hosting model:** every client's WP gets the plugin installed, or LP runs a central proxy WP that talks to client WPs via REST?