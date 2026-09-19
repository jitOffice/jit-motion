---
name: product-promo-animation
description: Generate a single-file, self-contained HTML product promotional animation video (15-30s) from a product brief/PRD. Produces a multi-scene GSAP timeline storyboard, a four aspect-ratio switcher (16:9/4:3/1:1/9:16), a zero-emoji SVG icon system, brand colors harvested from the official site, playback controls, and SEO video metadata. Use when the user asks for a product promo animation, marketing/ad video, animated HTML demo, or product launch video, or mentions building a product video with GSAP/motion/SVG. 基于产品需求文档/PRD/简介生成单文件、自包含的 HTML 产品宣传动画视频；当用户要求制作产品宣传动画、营销/广告视频、HTML 动画演示或产品发布视频时使用。
---

> **Languages:** English | [简体中文](SKILL.zh-CN.md)

# Product Promo Animation

Turn a product brief into a broadcast-quality, single-file HTML animated promo video. This skill distills a pattern proven across multiple product launches (multi-dimensional tables, AI knowledge bases, collaborative document tools).

## What this skill produces

A single self-contained `.html` file with:
- A 15-30s animation telling the product story scene-by-scene, driven by one GSAP timeline
- A four-aspect-ratio switcher (16:9 landscape, 4:3, 1:1, 9:16 portrait) with automatic layout reflow
- Polished SVG-only icons (zero emoji) + brand colors harvested from the product's official site
- Full playback controls (play/pause, replay, scrub, scene nav, aspect switcher, keyboard shortcuts)
- SEO video metadata (JSON-LD `VideoObject`, Open Graph, canonical)

## When to use

Trigger when the user wants a **product promo animation/video as HTML**, typically supplying:
- A brief / PRD / markdown spec describing the product and the capabilities to highlight
- The product name and official website (for brand harvesting)
- Constraints: duration, visual style, reference videos, forbidden elements

## Hard rules (non-negotiable)

These come from recurring user feedback; violating any one is a defect.

1. **Zero emoji.** Every icon must be an inline SVG `<symbol>`/`<use>` (24×24 viewBox, `stroke="currentColor"`, `fill="none"`, stroke-width 2, round caps/joins). Emoji render inconsistently and look unprofessional.
2. **No purple/magenta gradients** (unless the brand itself uses them). Default forbidden hexes: `#722ED1`, `#EB2F96`, `#F472B6`, `#A855F7`, `#8B5CF6`, `#D946EF`, `#C026D3`. Use brand-harmonious accents instead (teal `#00C4B4`, warm orange `#FF7D00`, success green `#00B42A`, gold `#FFB800`, rose `#F53F3F`).
3. **Brand fidelity.** Primary colors and logo must be harvested from the product's official site — never invented. The logo must appear (at least in the opening + closing scenes).
4. **Single file.** All CSS and JS inlined; only the animation library (GSAP) and the logo image are external.
5. **Selectors must match real class names.** A CSS rule targeting a class that doesn't exist silently does nothing. The validator catches this — never skip validation.
6. **Timing consistency.** The `DURATION` constant, the UI time label, the JSON-LD `duration`, and the timeline's real length must all agree.

## Workflow

Copy this checklist into your working notes and track progress:

```
- [ ] Phase 1: Digest the brief
- [ ] Phase 2: Harvest brand identity
- [ ] Phase 3: Design the storyboard
- [ ] Phase 4: Start from the skeleton
- [ ] Phase 5: Build the scenes
- [ ] Phase 6: Choreograph the timeline
- [ ] Phase 7: Validate and deliver
```

### Phase 1: Digest the brief

Read the user's requirement doc in full and extract a working sheet:
- **Product**: name, tagline, official URL
- **Capabilities to highlight**: the explicit feature list (these become the middle scenes)
- **Duration target**: e.g. "15-30s" → plan ~26s
- **Hard constraints**: forbidden colors, icon style, reference videos, output path
- **Tone**: from the requested marketing angle (e.g. "product marketing expert")

If the brief doesn't specify an output location, ask, or default to the brief's directory.

### Phase 2: Harvest brand identity

Visit the product's official site to extract ground truth — do not guess:
- **Primary color** and gradient stops (inspect CSS / theme)
- **Logo URL** (download it beside the output file, e.g. `./assets/<product>-logo.png`)
- **Accent colors** used in the design system
- **Visual language**: card styling, corner radius, shadows, typography

Record these as a "brand token" sheet and reuse it throughout. See [references/architecture.md](references/architecture.md) §Color System for the token structure.

### Phase 3: Design the storyboard

Map capabilities onto a scene sequence. The proven structure is **8 scenes / ~26s** (scale to 6-8 for shorter durations):

| # | Scene archetype | Duration | Purpose |
|---|-----------------|----------|---------|
| S1 | Brand opening | ~2.6s | Logo entrance + particles + product name + tagline |
| S2 | Core editor/capability | ~3.4s | Show the primary feature concretely |
| S3 | Build/create | ~3.4s | The signature "wow" workflow (e.g. drag-to-build) |
| S4 | Multi-view/flexibility | ~3.4s | Tabbed switch between multiple modes |
| S5 | Ecosystem/integrations | ~3.4s | Hub-and-spoke connections |
| S6 | AI intelligence | ~3.2s | Query → result → smart suggestions |
| S7 | Real-time collaboration | ~3.0s | Multi-user cursors, comments, presence |
| S8 | Brand close | ~3.8s | Logo breathing + tagline + capability chips + CTA |

Produce a **timing table** with fixed scene marks (e.g. `0, 2.6, 6.0, 9.4, 12.8, 16.2, 19.4, 22.4`) and, per scene, an element + animation-beat list. Pick only the archetypes that match the brief's capabilities; rename and reposition freely. See [references/scene-recipes.md](references/scene-recipes.md) for each archetype's visual recipe and animation beats.

### Phase 4: Start from the skeleton

Copy [assets/skeleton.html](assets/skeleton.html) to the output path. It contains the full infrastructure with `{{PLACEHOLDER}}` tokens:
- `<head>`: meta, JSON-LD `VideoObject`, OG tags, GSAP script tag
- CSS: stage + four-aspect variable system + scene/layout/control styles
- SVG symbol icon-library scaffold
- Two example scenes (S1 brand, S2 capability) demonstrating the DOM pattern
- Control bar HTML
- JS: `fitStage`, `setAspect`, timeline init, `showScene`/`hideScene`, `updateProgress`, scene nav, keyboard, controls auto-hide

Replace every `{{TOKEN}}`; no placeholder may remain. Understand the infrastructure before editing — see [references/architecture.md](references/architecture.md).

### Phase 5: Build the scenes

For each scene in the storyboard:
1. Define the SVG `<symbol>`s it needs in the icon library (reuse across scenes).
2. Write the scene DOM: `.scene#sN > .grid-bg + .glow-orb* + .layout > (.left-copy + <graphic>)`.
3. `.left-copy` carries badge + title + subtitle + chip-row (the copy); the graphic container carries the visual demo.
4. Build all graphics from styled HTML/SVG divs — no external images except the logo.

Follow the DOM contract exactly so the responsive system works. See [references/architecture.md](references/architecture.md) §Scene DOM Contract.

### Phase 6: Choreograph the timeline

Build the single `gsap.timeline({ paused: true })`. For each scene at mark `TN`:
- `showScene('sN', TN)`, then a staggered `.from()` entrance: badge → title → subtitle → chips → graphic
- Graphic-specific beats (typing, dragging, count-up, path draw, tab switch, cursor move)
- `hideScene('sN', TN + sceneDuration - 0.5)` for the cross-fade

Set `DURATION` to the last scene's end. Wire `updateProgress` with the scene-marks array. See [references/architecture.md](references/architecture.md) §Animation Engine for reusable beat snippets (count-up, stroke-draw, typewriter, drag cursor, view switch).

### Phase 7: Validate and deliver

**Never deliver without running the validator.**

```bash
python3 scripts/validate.py <output.html>
```

It checks: structure balance, zero emoji, forbidden colors, **dead CSS selectors** (rules targeting classes absent from the HTML), timing consistency, GSAP presence, JSON-LD presence. Fix everything it reports and re-run until it prints `OK`. (Diagnostics are bilingual — pass `--lang zh` for Chinese, or let it auto-detect your locale.)

Then do the browser pass per [references/quality-checklist.md](references/quality-checklist.md): console clean, all scenes activate in order, aspect switches reflow correctly (especially 9:16 — copy and graphic must stay grouped, never split), no overflow scrollbars.

## Reference files

- [references/architecture.md](references/architecture.md) — full HTML/CSS/JS technical spec, color system, DOM contract, animation-engine snippets
- [references/scene-recipes.md](references/scene-recipes.md) — visual recipes and animation beats for the 8 scene archetypes
- [references/quality-checklist.md](references/quality-checklist.md) — static + browser validation gates and common defects
- [assets/skeleton.html](assets/skeleton.html) — copy-to-start template with the full infrastructure
- [scripts/validate.py](scripts/validate.py) — deterministic static validator
- [README.md](README.md) — installation & usage across Codex / Claude Code / Cursor / Qoder

## Anti-patterns learned in production

- **Dead selector**: writing `.copy` when the HTML class is `.left-copy` → the rule is silently ignored. Always cross-check class names; the validator enforces it.
- **9:16 layout split**: using `grid-template-rows: auto 1fr` in stacked mode makes the graphic float in an over-tall row, separating it from the copy. Use `auto auto` + `align-content: center`.
- **Timing drift**: a `yoyo`/`repeat` tween pushes the timeline past `DURATION`. Compute the real end and sync all four duration references.
- **Emoji leak**: a stray `✓` or `→` in copy. Scan and replace with SVG.
- **GSAP selector typo**: writing `#id .child` when the element uses `class="child"` → empty-tween warning. Verify targets exist.
