---
title: README
type: note
permalink: ai/figma-to-avada/extractor/readme-2
---

# extractor/

Bridge MCP-based Figma extractor. No Personal Access Token needed.

## How it works

`extract.js` is **not run standalone**. It's a JavaScript payload sent to Figma's plugin context via `mcp__figma-console__figma_execute`.

## Run via Claude Code

```text
1. Open target Figma file in Figma Desktop
2. Activate Bridge plugin (Plugins → Development → Figma Desktop Bridge)
3. In Claude Code: substitute NODE_ID placeholder in extract.js
4. Call mcp__figma-console__figma_execute with the substituted code
5. Save returned JSON to output/{site}/{page}/brief/sections/{n}-{name}.json
```

## Returned JSON shape

```json
{
  "meta": { "extractedAt": "...", "figmaFile": "...", "rootNodeId": "...", "rootNodeName": "..." },
  "tree": {
    "id": "62:2",
    "name": "FAQ",
    "type": "FRAME",
    "bounds": { "x": 0, "y": 10528, "w": 1440, "h": 1040 },
    "fills": [{ "type": "SOLID", "color": "#0D0D26", "opacity": 1 }],
    "layout": { "mode": "NONE" },
    "children": [...]
  }
}
```

## Image export (separate step)

Images are exported via `mcp__figma-console__figma_capture_screenshot` per node. Save to `output/{site}/{page}/images/`. Reference by node `id` in the brief.