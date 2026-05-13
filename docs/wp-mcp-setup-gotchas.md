---
title: wp-mcp-setup-gotchas
type: note
permalink: ai/figma-to-avada/docs/wp-mcp-setup-gotchas-1
---

# WP MCP setup gotchas (lessons from the 3-reload misery)

Real-world friction encountered while setting up `wp-lp` MCP server in Claude Code for the first time. None of these are documented prominently — saving the next person ~30 min of debugging.

## Gotcha 1: `WP_API_URL` must be the FULL MCP endpoint URL

**Wrong:**
```
WP_API_URL=https://linked-promo.com
```

**Right:**
```
WP_API_URL=https://linked-promo.com/wp-json/mcp/mcp-adapter-default-server
```

**Why this matters:** the proxy `@automattic/mcp-wordpress-remote` has backwards-compat behavior — a bare-domain URL resolves to the **legacy `wordpress-mcp` plugin** endpoint (`/wp-json/wp/v2/wpmcp`), which doesn't exist on a fresh `mcp-adapter` install. Result: silent "Connection Failed" with no clear error.

Buried in the README:
> for backwards compatibility, a bare-domain `WP_API_URL` (e.g. `https://your-wordpress-site.com`) still resolves to the `wordpress-mcp` endpoint. **New setups should install `mcp-adapter` and use the full URL shown above.**

**How to debug:** run the proxy manually via stdio with a `tools/list` request. If the response `instructions` field says `"MCP WordPress Remote Proxy Server (Connection Failed)"` instead of `"Default MCP server for WordPress abilities discovery and execution"`, your URL is wrong.

## Gotcha 2: Claude Code `~/.claude.json` has case-sensitive project paths on Windows

`claude mcp add wp-lp ...` writes the server config into the project section of `~/.claude.json`. On Windows, the JSON can have BOTH `D:/AI/Linked Promo` and `d:/AI/Linked Promo` as separate project entries due to how different tools normalize paths.

If Claude Code's current session reads from the `d:` entry but you added the config to the `D:` entry → server invisible.

**Fix:** use `--scope user` so the config goes to the user-level `mcpServers` key, which is read regardless of project path case:

```bash
claude mcp add --scope user wp-lp \
  -e WP_API_URL='https://your-site.com/wp-json/mcp/mcp-adapter-default-server' \
  -e WP_API_USERNAME='your-user' \
  -e WP_API_PASSWORD='xxxx xxxx xxxx xxxx xxxx xxxx' \
  -- npx -y @automattic/mcp-wordpress-remote
```

## Gotcha 3: Each MCP config change needs a Claude Code reload

`claude mcp list` showing "✓ Connected" reflects whether the binary can be spawned and a handshake succeeds — but the **active Claude Code session loaded its MCP servers at session start**. Adding or modifying a server via `claude mcp add` / `claude mcp remove` does NOT hot-reload into the running session.

After any `claude mcp` operation: **VS Code → Command Palette → "Developer: Reload Window"**.

Tools surface as deferred (loadable via `ToolSearch select:...`). If you only see `ListMcpResourcesTool` and `ReadMcpResourceTool` (the generic MCP tools) but no server-specific tools — the server is connected but its tools haven't been catalogued. Try ToolSearch with the server name as keyword.

## Gotcha 4: `tools/list` via raw HTTP returns empty without session ID

MCP protocol requires:

1. POST `initialize` → server returns `Mcp-Session-Id` in response **headers**
2. (Optional) POST `notifications/initialized` (no response body, just signals client is ready)
3. POST `tools/list` with `Mcp-Session-Id` header → returns actual tools

Without session header, you get `{"jsonrpc":"2.0","id":N,"error":{"code":-32600,"message":"Invalid Request: Missing Mcp-Session-Id header"}}`.

The proxy `@automattic/mcp-wordpress-remote` handles this transparently — only matters when debugging via raw curl.

## Gotcha 5: Built-in WP core abilities are NOT exposed via MCP

After installing `mcp-adapter` + activating, calling `mcp-adapter-discover-abilities` returns an EMPTY abilities array — even though WP core registers 2 abilities (`core/get-site-info`, `core/get-environment-info`) visible via the REST endpoint `/wp-json/wp-abilities/v1/abilities`.

**Why:** the MCP server gates abilities by the `meta.mcp.public=true` flag in the ability registration. WP core registers without this flag.

**Implication for our LP-Avada plugin:** every ability we register MUST include:

```php
'meta' => ['mcp' => ['public' => true]],
```

Otherwise the abilities are callable via REST but invisible via MCP. Both paths from the same ability registration — just MCP needs the explicit flag.

## Recommended setup sequence (clean install)

For LP team members setting up a new WP+MCP environment:

```bash
# 1. Install MCP Adapter plugin on the WP site (manual via wp-admin → Plugins → Add New → Upload)

# 2. Generate Application Password (WP admin → Users → Profile → Application Passwords)

# 3. Add MCP server to Claude Code at user scope, with full endpoint URL
claude mcp add --scope user wp-CLIENT \
  -e WP_API_URL='https://CLIENT-SITE.com/wp-json/mcp/mcp-adapter-default-server' \
  -e WP_API_USERNAME='YOUR-USER' \
  -e WP_API_PASSWORD='xxxx xxxx xxxx xxxx xxxx xxxx' \
  -- npx -y @automattic/mcp-wordpress-remote

# 4. Verify connection (should show ✓ Connected)
claude mcp list | grep wp-CLIENT

# 5. Reload VS Code window
# Ctrl+Shift+P → Developer: Reload Window

# 6. In the new session, ToolSearch for the tools
# query: "mcp-adapter discover abilities"

# 7. Call mcp__wp-CLIENT__mcp-adapter-discover-abilities to verify pipeline
```

If discover-abilities returns empty `[]` AND you haven't installed any custom plugins registering MCP-public abilities — that's expected. Install our `linked-promo-avada-mcp` plugin (when built) to get the LP-specific abilities.

## TL;DR for the impatient

1. Full URL: `/wp-json/mcp/mcp-adapter-default-server`
2. `--scope user` always
3. Reload after every config change
4. Empty abilities array ≠ broken — it's the `mcp.public` gate doing its job