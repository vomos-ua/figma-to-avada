---
title: README
type: note
permalink: ai/figma-to-avada/readme
---

# figma-to-avada

LP internal tool — convert Figma designs to Avada Fusion Builder shortcodes.

**Status:** Phase 0 (smoke test) — under active development. Not stable.

## Approach

```
Figma Desktop (Bridge MCP)
        ↓ figma_execute walks node tree (no Figma token needed)
extractor/ → brief.json + images/*.png
        ↓
Володимир uploads images to WordPress manually
        ↓ returns image URLs to generator
generator/ (Claude skill) reads brief + KB + image URLs
        ↓
output/{site}/{page}/shortcode.txt
        ↓
Володимир pastes into Avada Code View → polish → done
```

## Why not andreata/figma-to-avada directly

We forked the idea, not the code:

- They use Figma REST API + Personal Access Token → we use figma-console MCP (no token)
- They use WordPress REST API → we keep image upload manual (simpler, no plumbing)
- Their knowledge base is Italian generic → ours is LP-specific from day 1

## Directory layout

```
figma-to-avada/
├── extractor/        Node.js + Claude skill: walks Figma via Bridge → JSON brief
├── kb/               LP-specific knowledge base
│   ├── shortcodes/   Catalog of Avada [fusion_*] shortcodes with params
│   ├── patterns/     LP-spec patterns (hero, stats strip, cases, FAQ, CTA)
│   └── tokens/       LP design tokens → Avada Global Styles mapping
├── generator/        Claude skill: brief + KB + image URLs → shortcodes
├── output/           Generated artifacts (gitignored)
└── examples/         Sample briefs + resulting shortcodes
```

## Phase plan

See `D:\AI\Linked Promo\docs\Avada\00-pipeline-plan.md` for full plan.

- [x] Phase 0: Smoke test infrastructure (this commit)
- [ ] Phase 0: Minimal extractor + test on PPC Landing FAQ block
- [ ] Phase 1: Catalog all 111 fusion_* shortcodes from PHP source
- [ ] Phase 2: LP knowledge base
- [ ] Phase 3: Test run on full PPC Landing
- [ ] Phase 4: Stabilization (CLI, cache, validation)
- [ ] Phase 5: Team handoff documentation

## License

Internal — not for redistribution.