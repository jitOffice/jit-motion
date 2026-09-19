> **Languages:** English | [简体中文](quality-checklist.zh-CN.md)

# Quality Gate & Checklist

Two gates, run in order. **Do not deliver until both pass.**

---

## Gate 1 — Static validation (automated)

```bash
python3 scripts/validate.py <output.html>
```

Exit code: `0` = OK (warnings possible), `1` = errors found, `2` = usage/file error. Fix **all** errors; review each warning to confirm it's harmless. Add `--lang zh` / `--lang en` to choose the diagnostic language (otherwise it auto-detects your locale).

The validator covers:

- [ ] **No leftover placeholders** (every `{{TOKEN}}` must be replaced)
- [ ] **Structure balance** (tags balanced; sensible `<script>`/`<style>` counts)
- [ ] **Zero emoji** (scans content after stripping comments, for emoji, `✓`, `→`)
- [ ] **No forbidden colors** (`#722ED1`/`#EB2F96`/`#F472B6`/`#A855F7`/`#8B5CF6`/`#D946EF`/`#C026D3`, unless the brand uses them)
- [ ] **No dead CSS selectors** (every class selector matches a real class in the HTML/JS)
- [ ] **Timing consistency** (`DURATION` == time label == JSON-LD `PT..S`)
- [ ] **GSAP present** (script tag + `gsap.timeline`)
- [ ] **JSON-LD present** (`VideoObject`)
- [ ] **Logo present** (a logo asset is referenced)
- [ ] **Scenes match marks** (scene count == `MARKS` entries)

> The dead-selector check is the highest-value gate — it catches responsive rules that target the wrong class name and therefore **silently do nothing** (historically the hardest bug class to find).

---

## Gate 2 — Browser pass (manual)

Open the file in a browser (use a local server so `./assets/` resolves):

```bash
python3 -m http.server 8000
# visit http://localhost:8000/<output.html>
```

- [ ] **Console clean** (open DevTools Console; zero red errors)
- [ ] **Play/pause** works (button + Space key)
- [ ] **Replay** resets to the start
- [ ] **Scrub** seeks to any moment
- [ ] **All scenes activate in order** (S1→S8, no skips, no stuck frames)
- [ ] **Scene nav dots** jump to their scenes
- [ ] **Every aspect ratio reflows correctly:**
  - [ ] 16:9 — two columns, copy | graphic
  - [ ] 4:3 — two columns, narrowed
  - [ ] 1:1 — stacked, grouped & centered (copy hugs the graphic)
  - [ ] 9:16 — stacked, grouped & centered; **copy and graphic never split**; no overflow
- [ ] **No scrollbars**, content never overflows the stage at any ratio
- [ ] **CTA toggle** shows/hides the button/URL (+ `C` key)
- [ ] **Keyboard shortcuts** all work (`Space` `R` `1-4` `←` `→` `C`)
- [ ] **Controls auto-hide** fades out after ~2.6s idle and reappears on mouse move

### Browser probe (optional)

Paste into the DevTools Console to assert state programmatically:

```js
// Timeline is exposed and its duration matches
console.assert(window.__tl, '__tl missing');
console.log('duration:', window.__tl.duration());

// Seek to and activate each scene, confirm .active applies
const marks = [0, 2.6, 6.0, 9.4, 12.8, 16.2, 19.4, 22.4];
marks.forEach((t, i) => {
  window.__tl.pause(t + 0.05);
  const active = document.querySelector('.scene.active');
  console.log(`scene ${i + 1} @${t}:`, active ? active.id : 'none');
});

// Each ratio sets data-aspect
['16:9','4:3','1:1','9:16'].forEach(r => {
  setAspect(r);
  console.assert(document.getElementById('stage').dataset.aspect === r, `ratio ${r} failed`);
});
```

---

## Common defects table

| Symptom | Root cause | Fix |
|---------|-----------|-----|
| Copy/graphic split in 9:16 | stacked grid used `auto 1fr` | `auto auto` + `align-content: center` |
| Graphic zero-width in stacked | `justify-items: center` | use `stretch` |
| Responsive rule does nothing | dead selector (class mismatch, e.g. `.copy` vs `.left-copy`) | match real class names; run the validator |
| Table enlargement not working | targeting `.tc`/`.tr` but it's a `<table>` | use `.data-table th/td` |
| Emoji in copy | used `✓`/`→` or pictographs | replace with an SVG icon |
| Time label mismatch | `DURATION` ≠ real timeline length | recompute the end point; sync all four |
| Empty-tween warning | GSAP selector typo (`#id .x` doesn't exist) | verify the target exists |
| Controls never show | `#viewport:hover #controls` (they're siblings) | `body:hover #controls` + JS idle-hide |
| Content overflows at a ratio | graphic has no explicit height | set `height` on every graphic container |
| Purple/magenta appears | used a default forbidden color | swap to a harmonious brand accent |

---

## Delivery summary template

After the pass, report to the user:

```
Delivered <product>-promo.html (single file, self-contained)
  • Duration: <NN>s, <K> scenes
  • Aspects: 16:9 / 4:3 / 1:1 / 9:16 (all pass the browser check)
  • Brand: <primary color> harvested from <official site>
  • Icons: <M> SVG symbols, zero emoji
  • Validation: validate.py = OK (exit 0)
  • Browser: console clean, all scenes + aspects + shortcuts verified
```
