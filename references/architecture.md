> **Languages:** English | [简体中文](architecture.zh-CN.md)

# Architecture Reference

The complete technical specification of the single-file promo animation embodied by `assets/skeleton.html`. Consult section by section as you build.

## Contents

1. [File topology](#1-file-topology)
2. [Head & SEO metadata](#2-head--seo-metadata)
3. [Stage & aspect-ratio variable system](#3-stage--aspect-ratio-variable-system)
4. [Scene DOM contract](#4-scene-dom-contract)
5. [Stacked-mode responsive rules](#5-stacked-mode-responsive-rules)
6. [Color system](#6-color-system)
7. [SVG icon system](#7-svg-icon-system)
8. [Control bar](#8-control-bar)
9. [JavaScript infrastructure](#9-javascript-infrastructure)
10. [Animation engine & reusable snippets](#10-animation-engine--reusable-snippets)

---

## 1. File topology

```
<product>-promo.html      # The single-file deliverable (all CSS + JS inlined)
assets/<product>-logo.png # The only external asset besides GSAP
```

External dependencies (only these two):
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<img src="./assets/<product>-logo.png" alt="...">
```

Internal file order:
```
<head>  meta + JSON-LD + OG + <style> (all CSS)
<body>
  <div id="viewport"><div id="stage"> ...all scenes... </div></div>
  <div id="controls"> ...playback UI... </div>
  <svg id="svg-defs"><symbol>...</symbol>...</svg>   <!-- icon library -->
  <script> ...GSAP timeline + infrastructure... </script>
```

---

## 2. Head & SEO metadata

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{PRODUCT_NAME}} — {{TAGLINE}} | Product Promo</title>
<meta name="description" content="{{One action-oriented, keyword-rich product sentence}}">
<link rel="canonical" href="{{PAGE_URL}}">

<!-- JSON-LD: let search engines understand the page as a video -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "{{PRODUCT_NAME}} — {{TAGLINE}}",
  "description": "{{VIDEO_DESCRIPTION}}",
  "thumbnailUrl": "{{THUMBNAIL_URL}}",
  "uploadDate": "{{YYYY-MM-DD}}",
  "duration": "PT{{NN}}S",
  "contentUrl": "{{PAGE_URL}}",
  "publisher": { "@type": "Organization", "name": "{{ORG_NAME}}", "url": "{{ORG_URL}}" }
}
</script>

<!-- Open Graph -->
<meta property="og:type" content="video.other">
<meta property="og:title" content="{{PRODUCT_NAME}} — {{TAGLINE}}">
<meta property="og:description" content="{{OG_DESCRIPTION}}">
<meta property="og:image" content="{{OG_IMAGE_URL}}">
<meta property="og:url" content="{{PAGE_URL}}">
```

`duration` must be an ISO 8601 duration (`PT26S`) and agree with the JS `DURATION`.

---

## 3. Stage & aspect-ratio variable system

The animation runs on a **fixed-size virtual stage** scaled by `fitStage()` to fit any window. This guarantees pixel-identical layout across ratios.

```css
html, body {
  margin: 0; width: 100%; height: 100%;
  background: #070b18; overflow: hidden;
}
#viewport { position: fixed; inset: 0; overflow: hidden; }
#stage {
  position: absolute; left: 50%; top: 50%;
  width: 1920px; height: 1080px;              /* 16:9 default */
  background: var(--bg); overflow: hidden;
  transform: translate(-50%, -50%) scale(1);
  transform-origin: center center;
}
```

Aspect ratios write all layout variables onto `#stage`, so every scene reflows automatically:

```css
:root {
  --bg: #070b18;
  --brand: #165DFF;        /* harvested from the official site */
  --brand-light: #4080FF;
  --accent: #00C4B4;       /* teal */
  --accent-warm: #FF7D00;  /* warm orange */
  --text: #ffffff;
  --text-muted: #8b96b0;
}

/* 16:9 (default) — two columns: copy | graphic */
#stage {
  --sw: 1920px; --sh: 1080px;
  --pad-x: 110px; --col-left: 700px; --col-gap: 80px;
  --title-size: 76px; --stack-mode: 0;
}
/* 4:3 */
#stage[data-aspect="4:3"] {
  --sw: 1440px; --sh: 1080px;
  --pad-x: 80px; --col-left: 560px; --col-gap: 60px;
  --title-size: 68px; --stack-mode: 0;
}
/* 1:1 — stacked */
#stage[data-aspect="1:1"] {
  --sw: 1080px; --sh: 1080px;
  --pad-x: 70px; --col-left: 100%; --col-gap: 40px;
  --title-size: 62px; --stack-mode: 1;
}
/* 9:16 — stacked (portrait) */
#stage[data-aspect="9:16"] {
  --sw: 1080px; --sh: 1920px;
  --pad-x: 60px; --col-left: 100%; --col-gap: 36px;
  --title-size: 60px; --stack-mode: 1;
}
```

`fitStage()` (see §9) reads `data-aspect`, sets `#stage` width/height to `--sw`/`--sh`, and computes scale as `min(viewportW/stageW, viewportH/stageH)`.

---

## 4. Scene DOM contract

**Every scene must follow this structure**, or the two-column↔stacked responsive system breaks.

```html
<section class="scene" id="sN">
  <!-- ambient background: grid + glows -->
  <div class="grid-bg"></div>
  <div class="glow-orb orb-a"></div>
  <div class="glow-orb orb-b"></div>

  <!-- layout: exactly 2 direct children -->
  <div class="layout">
    <!-- child 1: copy (badge → title → sub → chips) -->
    <div class="left-copy">
      <div class="scene-badge"><svg class="ico"><use href="#ic-..."/></svg> Badge text</div>
      <h2 class="scene-title">Main title</h2>
      <p class="scene-sub">One descriptive subtitle sentence.</p>
      <div class="chip-row">
        <div class="chip"><svg class="ico"><use href="#ic-..."/></svg> Capability A</div>
        <div class="chip"><svg class="ico"><use href="#ic-..."/></svg> Capability B</div>
      </div>
    </div>

    <!-- child 2: the graphic visualization (any container class) -->
    <div class="my-stage"> ...div/SVG-built demo... </div>
  </div>
</section>
```

Layout CSS:

```css
.scene { position: absolute; inset: 0; opacity: 0; visibility: hidden; }
.scene.active { opacity: 1; visibility: visible; }

.layout {
  position: absolute; inset: 0;
  display: grid;
  grid-template-columns: var(--col-left) 1fr;   /* copy | graphic */
  align-items: center;
  gap: var(--col-gap);
  padding: 64px var(--pad-x);
}

.left-copy { display: flex; flex-direction: column; gap: 24px; max-width: var(--col-left); }
.scene-title { font-size: var(--title-size); font-weight: 800; line-height: 1.1; }
.scene-sub { font-size: 26px; color: var(--text-muted); line-height: 1.6; }
.chip-row { display: flex; flex-wrap: wrap; gap: 14px; }
```

**Contract rules:**
- `.layout` has exactly **2 children**: the copy block and the graphic block.
- The graphic block is a direct child of `.layout` (do NOT wrap it in a `.right` container — the stacked rules would then target the wrong element).
- Style graphics with selectors that match their class names; the validator flags any class selector that doesn't exist in the HTML.

Scene badge / title / sub / chips:

```css
.scene-badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 8px 16px; border-radius: 999px;
  background: rgba(22,93,255,.12); border: 1px solid rgba(22,93,255,.3);
  color: var(--brand-light); font-size: 16px; font-weight: 600;
}
.chip {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 18px; border-radius: 999px;
  background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.1);
  font-size: 17px; color: var(--text-muted);
}
```

---

## 5. Stacked-mode responsive rules

When `--stack-mode: 1` (1:1 and 9:16), the layout flips from two columns to a centered stacked column. **This is the most bug-prone part across ratios.**

```css
#stage[data-aspect="1:1"] .layout,
#stage[data-aspect="9:16"] .layout {
  grid-template-columns: 1fr;
  grid-template-rows: auto auto;    /* CRITICAL: never auto 1fr */
  align-content: center;            /* copy+graphic centered as one group */
  justify-items: stretch;           /* CRITICAL: not center, or width:100% graphics collapse */
  align-items: stretch;
  gap: 40px;
}
```

**Two non-negotiable stacked rules:**

1. **`grid-template-rows: auto auto` (NEVER `auto 1fr`).** With `1fr`, the second row (graphic) stretches to fill the remaining height, so the graphic centers inside an over-tall row and separates from the copy, leaving big empty space above and below. `auto auto` + `align-content: center` keeps both together as a compact centered group.

2. **`justify-items: stretch` (not `center`).** Graphic containers often use `width: 100%`; `center` collapses them to zero width. Use `stretch` so each child fills the column width and centers its own contents internally.

Copy is centered in stacked mode:

```css
#stage[data-aspect="1:1"] .left-copy,
#stage[data-aspect="9:16"] .left-copy {
  max-width: 100%; align-items: center; text-align: center;
}
#stage[data-aspect="1:1"] .left-copy .scene-title,
#stage[data-aspect="1:1"] .left-copy .scene-sub,
#stage[data-aspect="9:16"] .left-copy .scene-title,
#stage[data-aspect="9:16"] .left-copy .scene-sub { width: 100%; }
#stage[data-aspect="1:1"] .chip-row,
#stage[data-aspect="9:16"] .chip-row { justify-content: center; }
```

**Graphic heights (prevent overflow).** 9:16 has generous vertical space, so enlarge graphics; 1:1 must shrink them to avoid overflow:

```css
/* 9:16: enlarge graphics (vertical space is generous) */
#stage[data-aspect="9:16"] .my-stage { height: 700px; }
/* 1:1: tighten (space is limited) */
#stage[data-aspect="1:1"] .my-stage { height: 560px; }
```

Set an explicit height on **every** graphic container; otherwise its intrinsic height can overflow the stacked layout.

**Table graphics:** if you use a real `<table>` (semantic `th`/`td`), enlarge with element selectors, not class names:
```css
#stage[data-aspect="9:16"] .data-table th,
#stage[data-aspect="9:16"] .data-table td { padding: 16px 14px; }
```

---

## 6. Color system

Define brand colors as tokens on `:root` and reuse them everywhere. Never hardcode one-off hex values.

```css
:root {
  --brand: #165DFF;         /* primary — harvested from the official site */
  --brand-light: #4080FF;   /* lighter variant */
  --accent: #00C4B4;        /* teal accent */
  --accent-warm: #FF7D00;   /* warm orange (alerts/CTA) */
  --success: #00B42A;       /* green done-state */
  --gold: #FFB800;          /* gold highlight */
  --rose: #F53F3F;          /* rose emphasis */
  --bg: #070b18;            /* dark stage background */
  --surface: rgba(255,255,255,.04);
  --border: rgba(255,255,255,.09);
  --text: #ffffff;
  --text-muted: #8b96b0;
}
```

**Forbidden colors (unless the brand uses them):** `#722ED1`, `#EB2F96`, `#F472B6`, `#A855F7`, `#8B5CF6`, `#D946EF`, `#C026D3`. The validator scans for these.

Gradients should mix the brand color with a harmonious accent:
```css
background: linear-gradient(135deg, var(--brand), var(--accent));
```

---

## 7. SVG icon system

A single `<svg id="svg-defs">` at the bottom of the page holds all icons as `<symbol>`s. Reference them with `<use href="#ic-name">`.

```html
<svg id="svg-defs" aria-hidden="true"
     style="position:absolute;width:0;height:0;overflow:pointer">
  <symbol id="ic-database" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round">
    <ellipse cx="12" cy="5" rx="9" ry="3"/>
    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
    <path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"/>
  </symbol>
  <!-- more symbols... -->
</svg>
```

Usage (the `ico` class standardizes sizing and stroke):
```html
<svg class="ico"><use href="#ic-database"/></svg>
```
```css
.ico { width: 20px; height: 20px; stroke: currentColor; fill: none; }
```

**Rules:**
- 24×24 viewBox, `fill="none"`, `stroke="currentColor"`, `stroke-width="2"`, round caps/joins.
- Color inherits from the parent's `color`, so icons adapt to each scene's palette.
- **Never use emoji** — the validator flags common emoji plus `✓` and `→`.

---

## 8. Control bar

A bottom-fixed playback UI, sibling to `#stage` (a sibling, not a child).

```html
<div id="controls">
  <div class="progress-track" id="progress-track"><div class="progress-fill" id="progress-fill"></div></div>
  <button id="btn-play" class="ctrl-btn" title="Play/Pause (Space)">...</button>
  <button id="btn-replay" class="ctrl-btn" title="Replay (R)">...</button>
  <span class="time-label" id="time-label">0.0s / {{NN}}s</span>
  <div class="scene-nav" id="scene-nav"><!-- one .dot per scene --></div>
  <div class="aspect-switcher" id="aspect-switcher">
    <button data-aspect="16:9" class="on">16:9</button>
    <button data-aspect="4:3">4:3</button>
    <button data-aspect="1:1">1:1</button>
    <button data-aspect="9:16">9:16</button>
  </div>
</div>
```

Auto-hide (use `body:hover` because `#controls` is a sibling of `#viewport`):
```css
#controls { opacity: 0; transition: opacity .3s; }
body:hover #controls,
body.controls-force-show #controls { opacity: 1; }
```
A JS IIFE manages `controls-force-show` and an idle timer (hides after ~2.6s of mouse stillness). See the skeleton.

---

## 9. JavaScript infrastructure

The skeleton provides the parts below. Understand them before adding the timeline.

```js
const stage = document.getElementById('stage');
const scenes = Array.from(document.querySelectorAll('.scene'));
let currentAspect = '16:9';

// Scale the fixed stage to fit the window
function fitStage() {
  const w = window.innerWidth, h = window.innerHeight;
  const sw = parseFloat(getComputedStyle(stage).width);
  const sh = parseFloat(getComputedStyle(stage).height);
  const scale = Math.min(w / sw, h / sh);
  stage.style.transform = `translate(-50%, -50%) scale(${scale})`;
}

// Switch aspect ratio: set size variables + re-scale
function setAspect(ratio) {
  currentAspect = ratio;
  stage.setAttribute('data-aspect', ratio);
  // --sw/--sh are defined in CSS; fitStage reads the computed size
  fitStage();
}

// Scene visibility (used by timeline callbacks)
function showScene(id, t) {
  window.__tl.call(() => {
    scenes.forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    syncDots(id);
  }, null, t);
}
function hideScene(id, t) {
  window.__tl.call(() => document.getElementById(id).classList.remove('active'), null, t);
}

// Progress bar + time label
function updateProgress() {
  const t = window.__tl.time();
  progressFill.style.width = (t / DURATION * 100) + '%';
  timeLabel.textContent = t.toFixed(1) + 's / ' + DURATION.toFixed(1) + 's';
}
```

**Scene marks & duration** (drive everything):
```js
const DURATION = 26.2;                              // must equal the real timeline length
const MARKS = [0, 2.6, 6.0, 9.4, 12.8, 16.2, 19.4, 22.4];  // start of each scene
```

**Keyboard shortcuts:**
| Key | Action |
|-----|--------|
| `Space` | Play / pause |
| `R` | Replay |
| `1` `2` `3` `4` | Switch aspect 16:9 / 4:3 / 1:1 / 9:16 |
| `←` `→` | Prev/next scene mark |
| `C` | Toggle closing CTA |

---

## 10. Animation engine & reusable snippets

One master timeline, `paused: true`, exposed on `window.__tl` for debugging:

```js
window.__tl = gsap.timeline({ paused: true, onUpdate: updateProgress });
const tl = window.__tl;

// S1 (mark 0)
showScene('s1', 0);
tl.from('#s1 .brand-logo', { opacity: 0, scale: .8, duration: .8, ease: 'back.out(1.7)' }, 0.1)
  .from('#s1 .scene-title', { opacity: 0, y: 30, duration: .7 }, 0.5)
  .from('#s1 .scene-sub',   { opacity: 0, y: 20, duration: .6 }, 0.9);
hideScene('s1', 2.1);

// S2 (mark 2.6) ... and so on
```

### Reusable beat snippets

**Count-up:**
```js
function countUp(el, to, dur, at, prefix = '', suffix = '') {
  const obj = { v: 0 };
  tl.to(obj, { v: to, duration: dur, ease: 'power1.out',
    onUpdate: () => el.textContent = prefix + Math.round(obj.v).toLocaleString() + suffix
  }, at);
}
```

**Path stroke-draw (for connector lines / underlines):**
```js
tl.fromTo(path, { strokeDasharray: len, strokeDashoffset: len },
                { strokeDashoffset: 0, duration: .8, ease: 'power2.inOut' }, at);
```

**Donut fill:**
```js
tl.fromTo(circle, { strokeDashoffset: C }, { strokeDashoffset: C * (1 - pct), duration: 1 }, at);
```

**Typewriter:**
```js
function typeText(el, text, at, cps = 30) {
  tl.call(() => { el.textContent = ''; }, null, at);
  [...text].forEach((ch, i) =>
    tl.call(() => el.textContent += ch, null, at + i / cps));
}
```

**Drag cursor (move a card from A to B):**
```js
tl.to(cursor, { x: targetX, y: targetY, duration: .6, ease: 'power2.inOut' }, at)
  .to(card,   { x: targetX, y: targetY, duration: .5, ease: 'back.out(1.4)' }, at + .3);
```

**View switch (table → kanban → …):** stagger `.to()` on the tabs to toggle the active state, cross-fading container `opacity`/`scale`.

**Hub-and-spoke entrance:** the center logo scales in with a bounce, then nodes stagger in with `back.out` around the circle while connector lines stroke-draw.

**Logo breathing (closing):**
```js
tl.to(logo, { scale: 1.06, duration: 1.4, yoyo: true, repeat: 1, ease: 'sine.inOut' }, at);
```
> Caution: `yoyo`/`repeat` extend the real timeline. Compute the end point and sync `DURATION`.
