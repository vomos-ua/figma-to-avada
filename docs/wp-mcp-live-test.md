# WP MCP live test — findings

**Date:** 2026-05-13
**Environment:** Production WordPress site `linked-promo.com`
**WP version:** 6.9.4 (updated from 6.2.9 specifically for this test)
**MCP Adapter version:** 0.5.0
**Avada versions:** Builder 3.15.3, Core 5.15.3

## What was tested

End-to-end MCP protocol communication with a real WordPress + Avada production install, from raw HTTP curl through to Claude Code MCP proxy registration. No custom abilities written for this test — only WP core defaults.

## Pipeline trace (each layer verified)

### 1. WordPress REST API base — ✅ works

```
GET https://linked-promo.com/wp-json/  →  200 OK
```

iThemes Security Pro does NOT block `/wp-json/` on this install.

### 2. Application Password authentication — ✅ works

```
GET /wp-json/wp/v2/users/me  (Basic auth: gclinked:xxxx...)
→ 200 OK with user JSON
```

App Password generated in `Users → Profile → Application Passwords` works as Basic auth credential against any WP REST endpoint.

### 3. WP Abilities API namespace registered — ✅ in core

Available namespaces on this install:

- `wp-abilities/v1` — Abilities API (CORE since WP 6.9)
- `mcp` — MCP Adapter plugin endpoint
- Plus standard WP REST: `wp/v2`, `oembed/1.0`, etc.
- Plus theme/plugin namespaces: `awb`, `yoast/v1`, `wp-rocket/v1`, `wpml/*`

### 4. Built-in abilities discovered — 2 found

```
GET /wp-json/wp-abilities/v1/abilities → [
  { name: "core/get-site-info", category: "site" },
  { name: "core/get-environment-info", category: "site" }
]
```

Both registered by WP core itself. Neither has `meta.mcp.public=true` flag.

### 5. REST execution of ability — ✅ works

```
GET /wp-json/wp-abilities/v1/abilities/core/get-site-info/run
→ {
    "name": "Linked Promo",
    "url": "https://linked-promo.com",
    "version": "6.9.4",
    "admin_email": "moskalyuk.v@linked-promo.com",
    ...
  }
```

Direct REST call bypasses MCP layer entirely. **No `meta.mcp.public` requirement** — abilities are callable via REST as long as `permission_callback` allows.

### 6. MCP endpoint handshake — ✅ works after fix

Initial mistake: sending `tools/list` without prior `initialize` returned empty tools array silently.

Correct sequence:

```
POST /wp-json/mcp/mcp-adapter-default-server
  {"method": "initialize", "params": {"protocolVersion": "2025-06-18", ...}}
→ Response header: Mcp-Session-Id: 7fd6f28b-95f2-4616-b152-6565693ae253
→ Response body: server capabilities

POST /wp-json/mcp/mcp-adapter-default-server
  Header: Mcp-Session-Id: 7fd6f28b-...
  {"method": "tools/list"}
→ 3 tools returned:
  - mcp-adapter-discover-abilities
  - mcp-adapter-get-ability-info
  - mcp-adapter-execute-ability
```

Without session ID header subsequent calls return `{"error":{"code":-32600,"message":"Invalid Request: Missing Mcp-Session-Id header"}}`.

### 7. MCP exposes only `meta.mcp.public=true` abilities — ⚠️ critical gate

```
tools/call → mcp-adapter-discover-abilities
→ result.abilities = []   (empty!)

tools/call → mcp-adapter-execute-ability {ability_name: "core/get-site-info"}
→ {"isError": true, "text": "Ability \"core/get-site-info\" is not exposed via MCP (mcp.public!=true)"}
```

The 2 core abilities exist (visible via REST) but are NOT exposed through MCP because they lack the `meta.mcp.public=true` flag. This is a deliberate security gate in the MCP Adapter.

To expose abilities via MCP, the registration must include:

```php
wp_register_ability('lp/example', [
  // ...standard fields...
  'meta' => ['mcp' => ['public' => true]],
]);
```

### 8. Claude Code MCP proxy registered — ✅ connected

```bash
claude mcp add wp-lp \
  -e WP_API_URL='https://linked-promo.com' \
  -e WP_API_USERNAME='gclinked' \
  -e WP_API_PASSWORD='xxxx xxxx ...' \
  -- npx -y @automattic/mcp-wordpress-remote
```

`claude mcp list` shows `wp-lp: npx -y @automattic/mcp-wordpress-remote - ✓ Connected`.

Proxy handles the session handshake automatically (stdio → HTTPS bridge). Restart Claude Code session to get its tools surfaced into the active tool list.

## Strategic implications

This test compresses 2 weeks of theory-mode planning into concrete reality. Key takeaways:

### REST API is the simpler path for execution

Every WP ability is callable via 1 HTTP GET/POST with Basic Auth. No session, no protocol negotiation, no `meta.mcp.public` requirement. For straight "run this command on WP" workflows, raw REST wins on simplicity:

```bash
# Single curl call - works against any registered ability
curl -u user:app_password https://site.com/wp-json/wp-abilities/v1/abilities/lp/create-page/run \
  -X POST -H "Content-Type: application/json" \
  -d '{"title": "...", "shortcode": "..."}'
```

vs MCP (~3-4 round trips, session state, protocol versioning, public-flag gating).

### MCP wins on discovery + structured Resources/Prompts

What MCP gives that raw REST does not:

- **Auto-discovery** — Claude can list available abilities without prior knowledge
- **Schema introspection** — input/output schemas exposed through MCP tools/list response
- **Resources** — read-only URIs (e.g. expose our knowledge base as `lp-avada://catalog`)
- **Prompts** — structured templates (e.g. "generate-page-from-figma" with pre-filled instructions)

For an internal LP team workflow where Claude already knows the tools (because we wrote them), discovery matters less. The Resources + Prompts components are the real differentiator for AI-native UX.

### Pragmatic recommendation for LP-Avada plugin

Write our abilities in PHP using `wp_register_ability()` (standard Abilities API). Mark them `meta.mcp.public=true`. This gives us **both pathways** with zero extra work:

- Direct REST calls → fast and simple for scripted pipelines
- MCP exposure → discoverable by Claude Code natively when team uses it interactively

The cost is the same (write the ability once in PHP). The benefit is dual access.

### Avada-specific abilities to write (revised list)

Based on what we now know works:

| Ability | Method | Public via MCP? |
|---|---|---|
| `lp-avada/create-page` | POST | yes |
| `lp-avada/update-page` | POST | yes |
| `lp-avada/upload-media` | POST | yes |
| `lp-avada/list-pages` | GET | yes |
| `lp-avada/get-page-shortcode` | GET | yes |
| `lp-avada/list-forms` | GET | yes |
| `lp-avada/create-form` | POST | yes |
| `lp-avada/validate-shortcode` | GET | yes |

All Tier 1 + Tier 2 from prior plan, simplified — no Resources/Prompts in MVP (those come later).

## Open questions for production

1. **iThemes Security Pro**: it didn't block `/wp-json/` on this install, but on different LP-client installs with stricter iThemes config, REST might be blocked. Mitigation: our plugin can document the required iThemes whitelist rules.

2. **WP Rocket caching**: `/wp-json/` should bypass page cache automatically, but worth verifying on a high-traffic site. Mitigation: explicit cache-control headers in our ability response.

3. **WPML compatibility**: WPML is active. If our pages need to support multilingual, ability needs to handle language taxonomy. Out of scope for v1 — single-language pages only.

4. **`_fusion` meta structure**: still unresearched. Next step is dump a working Avada page's `_fusion` meta from this WP install via `get_post_meta($id, '_fusion', true)` to see the serialized structure. THIS is the gating research item before we can write `lp-avada/create-page`.

## Security cleanup

The Application Password used for this test (`W19Y 7jSm wNX3 lpyA Elbo Jl2R`) was shared in chat context for testing. After test completion, Володимир MUST:

1. WP Admin → Users → Profile → Application Passwords
2. Find row "Claude Code"
3. Click **Revoke**

The new LP-Avada plugin (when built) will use its own App Password generated per-environment, not this test password.

## Decision

**Build LP-Avada Abilities Plugin** as originally planned in `wp-mcp-integration-plan.md`, with revisions:

- ALL abilities marked `meta.mcp.public=true` from the start
- Test BOTH access paths (REST + MCP) in CI
- Phase B can now start once we have the `_fusion` meta structure documented
