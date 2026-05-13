---
title: wp-mcp-adapter-evaluation
type: note
permalink: ai/figma-to-avada/docs/wp-mcp-adapter-evaluation
---

# WordPress/mcp-adapter — evaluation

**Date:** 2026-05-13
**Decision:** **NOT adopting** for current pipeline. Use raw WP REST API + Application Passwords instead.

## Repository

- https://github.com/WordPress/mcp-adapter
- v0.5.0, 1,065 stars, 123 forks, actively developed (last push 2026-05-13)
- Owner: WordPress org (official), GPL-2.0
- Created: 2025-07-10

## What it is

PHP Composer package / WordPress plugin. Runs **inside** WordPress as an adapter for the WordPress Abilities API (`wp_register_ability()`, core since WP 6.9).

**It is not** a standalone Node server. **It is not** a generic WP REST wrapper.

## Critical finding: it has no built-in WP tools

Only 3 built-in abilities — all introspection:

- `mcp-adapter/discover-abilities`
- `mcp-adapter/get-ability-info`
- `mcp-adapter/execute-ability`

**Zero built-in tools for** create/update pages, upload media, set post_content, set post_meta, inspect existing content.

Verified by GitHub code search: `wp_insert_post`, `update_post_meta`, `wp_handle_upload` appear **0 times in PHP source**.

> **"It is plumbing, not a product"** — research agent verdict.

## Avada compatibility

**Zero Avada awareness.** Search for `avada`, `fusion_builder`, `fusion_builder_status` in repos `WordPress/mcp-adapter` and `Automattic/mcp-wordpress-remote` returns 0 results.

Critical Avada concerns:

- `_fusion` meta is a **serialized PHP array**. Any tool that writes Avada page meta must serialize correctly or Builder won't open the page in visual edit mode.
- `fusion_builder_status="active"` post_meta required for shortcode rendering.
- Unverified whether shortcode-only (without `_fusion`) gives editable page in Avada Builder or just front-end render.

## Realistic integration effort (if we adopted it)

~1-2 days of PHP work to write custom abilities:

- `lp/create-avada-page` → `wp_insert_post` + Avada meta
- `lp/upload-media` → `media_handle_sideload` (helper not built-in)
- `lp/set-fusion-meta` → `update_post_meta` with serialized `_fusion` array

Plus reverse-engineering Avada Builder's internal state model. None of this is shortened by mcp-adapter — it only saves the MCP transport layer.

## Pre-1.0 risk

- v0.3, v0.5 both had breaking changes (migration guides exist)
- Abilities API is core only in WP 6.9 (Nov 2025); older WP needs separate `wordpress/abilities-api` plugin which was **archived Feb 2026**
- More breaking changes likely before v1.0

## Better alternatives, ranked

### 1. Raw WP REST API + Application Passwords (RECOMMENDED)

```bash
POST /wp-json/wp/v2/pages
Authorization: Basic <base64(user:app_password)>
Content-Type: application/json

{
  "title": "PPC Landing",
  "slug": "ppc",
  "status": "publish",
  "content": "[fusion_builder_container]...",
  "meta": { "fusion_builder_status": "active" }
}
```

Pre-requisites for Avada meta in REST:

```php
// in child theme functions.php (one-time setup)
register_post_meta('page', 'fusion_builder_status', [
  'show_in_rest' => true,
  'single' => true,
  'type' => 'string',
]);
```

This is what `andreata/figma-to-avada` already uses. Zero plugins, 30-line Claude skill.

**Effort to adopt:** 1 hour. We already have App Password capability in WP admin.

### 2. wp-cli over SSH

```bash
wp post create \
  --post_type=page \
  --post_title="PPC Landing" \
  --post_status=publish \
  --post_content="$(cat shortcode.txt)" \
  --meta_input='{"fusion_builder_status":"active"}'
```

Most direct, requires SSH access to WP host. We have that on Hostinger.

### 3. mcp-adapter — only if scope expands

If LP later wants to expose **many** WP capabilities to Claude beyond Avada page creation (CRM-style reads, analytics queries, user management, etc.) — then mcp-adapter's abstraction starts paying off. For just "paste shortcode → create page", it's overkill.

## Decision

Phase B of original plan (automated WP integration) will use **raw WP REST API + Application Passwords**. Implementation:

1. One-time: register Avada meta keys in REST via child theme `functions.php`
2. Add `output/{site}/{page}/deploy.js` script: reads `shortcode.txt`, POSTs to WP REST API, returns page URL
3. Володимир sets `.env.local` with WP_URL + WP_USER + WP_APP_PASSWORD
4. Pipeline: extract → generate → deploy (one command)

Estimated effort: **half a day** vs 1-2 days for mcp-adapter integration with same end result.

## Phase B prerequisites (when we get there)

- [ ] WP App Password for Володимир
- [ ] Child theme already deployed (for `register_post_meta` snippet)
- [ ] Verify Avada Forms `form_post_id` can be read via REST (`/wp-json/wp/v2/avada_form` or custom endpoint)
- [ ] Media upload endpoint test (file size limits, MIME types)

For now (Phase 0-3 still in progress) — manual paste flow continues. No need to integrate WP automation until we have at least 3-4 working patterns.