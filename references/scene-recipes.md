> **Languages:** English | [简体中文](scene-recipes.zh-CN.md)

# Scene Recipes

Eight proven scene archetypes that make up the ~26s product-promo narrative. Each recipe gives the purpose, graphic structure, key elements, and animation beats. Pick per product capability, then rename and recolor to the brand.

> All graphics are HTML `<div>` / inline SVG using the color tokens defined in §6. No external images (except the logo), no emoji.

---

## S1 — Brand opening (~2.6s)

**Purpose:** Establish brand identity instantly. Logo + product name + tagline.

**Graphic:** A centered logo with orbiting particles and a gradient-text tagline under the product name.

**Elements:**
- `.brand-logo` — the logo image (120–160px) with a glow
- `.orbit` — 2–3 concentric rings with small dots running on `motionPath` or simple rotation
- `.brand-name` — large gradient text (brand → accent)
- `.brand-tagline` — a soft subtitle
- `.hero-chips` — 3–4 capability chips (optional)

**Animation beats:**
1. `t=0.1` logo bounces in (`back.out(1.7)`, scale .8→1)
2. `t=0.4` orbit rings fade in + continuous rotation (`repeat: -1`, but **time-boxed**)
3. `t=0.5` brand name reveals line by line (`y: 30→0`)
4. `t=0.9` tagline fades in
5. `t=1.4` chips stagger in
6. `t=2.1` `hideScene('s1')`

---

## S2 — Core editor / capability (~3.4s)

**Purpose:** Show the product's primary feature — "what it does".

**Graphic:** A mock interface (editor canvas, table, or document) actively filling with content.

**Elements:**
- `.editor-frame` — a window chrome with `.titlebar` (red/yellow/green dots) + `.toolbar` (icon buttons)
- `.editor-canvas` — the content area: text lines, a `<table class="data-table">`, or cards
- `.typing-line` — a line filled character by character by the typewriter
- `.cursor-blink` — a blinking caret

**Animation beats:**
1. Frame slides in + toolbar icons stagger
2. Typewriter fills the title line (`typeText`)
3. Table rows stagger in; cell numbers count up
4. A toolbar icon "gets clicked" (scale pulse) and triggers a highlight
5. Subtitle chips light up as each capability appears

> **Table tip:** use a semantic `<table class="data-table">` with `th`/`td`. In stacked mode, enlarge with `.data-table th/td`, **not** `.tc`/`.tr` classes (those don't exist → dead selector).

---

## S3 — Build / create (~3.4s)

**Purpose:** The signature "wow" workflow — how the user creates/builds. Common for drag-and-drop builders.

**Graphic:** A component palette + a canvas; a card is dragged in and snaps into place.

**Elements:**
- `.palette` — a left rail of draggable components (each with an icon)
- `.canvas` — the drop area with a dashed `.drop-zone`
- `.drag-card` — the card moved by the cursor
- `.cursor` — a pointer SVG that moves along a path

**Animation beats:**
1. Palette items stagger in
2. The cursor moves to a palette item and presses down (scale pulse)
3. The cursor drags `.drag-card` to the `.drop-zone` (`x/y` tween)
4. The drop zone highlights → the card snaps with `back.out`
5. The built structure accumulates piece by piece

---

## S4 — Multi-view / flexibility (~3.4s)

**Purpose:** Show the same data in multiple presentations (table / kanban / calendar / chart).

**Graphic:** A tabbed view switcher that cross-fades between visualizations.

**Elements:**
- `.view-tabs` — tab buttons (Table / Kanban / Calendar / Chart)
- `.view-panel` — one per view, stacked, only the active one visible
- `.kanban-col`, `.cal-cell`, `.bar`, etc., per view

**Animation beats:**
1. The tab bar slides in; the first view activates
2. A tab "gets clicked" → the current view fades out (`opacity/scale`), the next fades in
3. Each view shows its signature motion (kanban cards into columns, bars growing, calendar cells filling)
4. Cycle or walk through the views in turn

---

## S5 — Ecosystem / integrations (~3.4s)

**Purpose:** Show how the product connects to a wider ecosystem (hub-and-spoke).

**Graphic:** A central logo/hub with satellite nodes joined by stroke-drawn lines.

**Elements:**
- `.hub` — the central logo or main node
- `.spoke-node` — 6–8 integration points around it (icon + label)
- `.spoke-line` — SVG `<line>`/`<path>` from hub to each node

**Animation beats:**
1. The hub scales in with a bounce
2. Lines stroke-draw outward from the center (`strokeDashoffset`)
3. Satellite nodes stagger in with `back.out` as each line arrives
4. A soft continuous float (time-boxed)
5. Data "pulses" run along a few lines (small dot translation)

---

## S6 — AI intelligence (~3.2s)

**Purpose:** Present AI/automation capabilities — a query goes in, insights come out.

**Graphic:** A prompt input, then generated answer/suggestion cards.

**Elements:**
- `.ai-prompt` — an input box filled by the typewriter with a question
- `.ai-thinking` — blinking dots or a spinning ring
- `.ai-result` — generated cards/summary/chart
- `.ai-suggest` — follow-up suggestion chips

**Animation beats:**
1. The prompt types out character by character
2. The "thinking" indicator pulses (~0.6s)
3. Result cards reveal with a stagger; key numbers count up
4. Suggestion chips bounce in
5. A "confidence" donut fills

---

## S7 — Real-time collaboration (~3.0s)

**Purpose:** Show multi-user real-time collaboration.

**Graphic:** Multiple named cursors, comment bubbles, and presence avatars on a shared canvas.

**Elements:**
- `.collab-cursor` — colored pointers with name tags (one brand color per user)
- `.comment-bubble` — a pop-in comment bubble
- `.avatar-stack` — online user avatars (overlapping circles)
- `.presence-ring` — a green dot on avatars

**Animation beats:**
1. The avatar stack bounces in, presence indicators light up
2. 2–3 colored cursors move independently across the canvas
3. A comment bubble pops at one cursor
4. A piece of text is "selected" by a user (highlight)
5. A reaction/like briefly appears

---

## S8 — Brand close (~3.8s)

**Purpose:** End on a strong brand impression + CTA.

**Graphic:** A centered logo (breathing), tagline, a capability chip row, a CTA button and URL.

**Elements:**
- `.outro-logo` — the logo with a soft `scale` breathe
- `.outro-tagline` — large tagline
- `.outro-chips` — a chip row summarizing capabilities
- `.cta-btn` — a "Try it now" button (controlled by the CTA toggle)
- `.cta-url` — the product URL

**Animation beats:**
1. The logo scales in, then breathes (`yoyo`, `sine.inOut`)
2. The tagline reveals line by line
3. Chips stagger in
4. The CTA button pulses with a glow; the URL fades in
5. The glow softly converges; **compute the real end point → set `DURATION`**

> **CTA toggle:** the `#cta-toggle` in the top-right (`role="switch"`) toggles visibility of `.cta-btn` and `.cta-url`, shortcut `C`. The preference is stored in localStorage.

---

## Adapting across product types

These archetypes were distilled for a multi-dimensional table product, but they transfer:

- **Docs / editors** (collaborative docs, writing tools): S2 = writing canvas; S3 = template/block building; S4 = outline/page/PDF views; S6 = AI continuation; S7 = live co-editing.
- **Knowledge base / wiki**: S2 = search + article; S3 = building a knowledge graph with AI; S5 = interlinked pages; S6 = Q&A retrieval.
- **Dashboards / BI**: S2 = chart builder; S4 = chart-type switching; S6 = automated insights.
- **Non-product (campaigns/ideas)**: swap "capabilities" for "messages"; S2–S7 become argument/story beats; keep S1 opening and S8 CTA close.

Always: match scenes to the brief's capabilities first, then order them by narrative logic (problem → capability → ecosystem → intelligence → collaboration → brand).
