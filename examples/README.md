---
title: README
type: note
permalink: ai/figma-to-avada/examples/readme-1
---

# examples/

Per-section paste-ready Avada shortcodes for **PPC Landing v2** (`linked-promo.com`).

These files mirror the production-edited final at `D:\AI\Linked Promo\docs\Avada\ppc-landing-final-shortcode.txt` (Володимир's hand-corrected version, source of truth as of 2026-05-15).

## Files (16 sections, top → bottom on the page)

| # | File | Purpose |
|---|---|---|
| 01 | `01-hero.shortcode.txt` | Dark hero: H1 + CTA pair + dashboard image |
| 02 | `02-stats-strip.shortcode.txt` | White strip with 4 KPIs (5+ / 1.8% / $3.59 / 12-36h) |
| 03 | `03-advantages.shortcode.txt` | "Наші переваги" - 4 cards with FA icons |
| 04 | `04-b2b-targeting.shortcode.txt` | B2B targeting + match rate bars + audience upload buttons |
| 05 | `05-cross-channel.shortcode.txt` | Cross-channel remarketing - 4 user-path cards + impact stats |
| 06 | `06-segmented-marketing.shortcode.txt` | Segmented marketing: Cold / Warm / Hot segments + include/exclude logic |
| 07 | `07-ai-analytics.shortcode.txt` | AI analytics 4-step flow + diagram image |
| 08 | `08-platform-linkedin.shortcode.txt` | Platform 01/03 - LinkedIn Ads (3 ad-format cards) |
| 09 | `09-platform-meta.shortcode.txt` | Platform 02/03 - Meta Ads |
| 10 | `10-platform-google.shortcode.txt` | Platform 03/03 - Google Ads |
| 11 | `11-how-we-work.shortcode.txt` | "Як ми працюємо" - 6 process steps |
| 12 | `12-faq-header.shortcode.txt` | FAQ section header |
| 13 | `13-faq-pair-1.shortcode.txt` | FAQ Q&A pair (2 cards in row) |
| 14 | `14-faq-pair-2.shortcode.txt` | FAQ Q&A pair |
| 15 | `15-faq-pair-3.shortcode.txt` | FAQ Q&A pair |
| 16 | `16-final-cta.shortcode.txt` | Final CTA "Запуск за 14 днів" |

For paste-the-whole-page, use `output/ppc-landing-v2-all.shortcode.txt` (concatenation of all 16 in order).

## Brief / illustration helpers

- `*.brief.json` - extractor output for individual sections (kept for reference)
- `*.illustration-prompt.md` - ChatGPT-Image prompts for AI-generated section illustrations

## Sections that need image inserts (manual via Avada Builder)

Per Figma update 2026-05-15:
- `05-cross-channel`: Володимир will split single-column row into 1/2 + 1/2 in Builder, drop `cross-channel-illustration.webp` into the right column
- `06-segmented-marketing`: same — Володимир places `segmented-marketing-illustration.webp` to the right of the include/exclude block

## Paste workflow

1. Open WP → Pages → Add New → Avada Live Builder
2. Toggle **Code View** (`</>` icon)
3. Paste contents of one section file (or the full `ppc-landing-v2-all.shortcode.txt`)
4. Save → Preview

## Stale code archive

Pre-2026-05-15 examples (PR-quality but pre-final-edit) moved to `0===backup/old-examples-v1/`. Do not paste from there.
