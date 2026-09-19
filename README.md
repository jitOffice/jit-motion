> **Languages:** English | [简体中文](README.zh-CN.md)

<div align="center">

<img src="assets/preview.png" alt="jit-motion — multi-scene storyboard, four aspect ratios & playback controls" width="860">

# jit-motion

**Ship a polished product promo video as one self-contained HTML file.**
No video editor, no render farm — just a product brief and your AI coding agent.

<p>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Codex%20%7C%20Cursor%20%7C%20Qoder-blue" alt="Works with">
  <img src="https://img.shields.io/badge/GSAP-3.12-88ce02" alt="GSAP">
  <img src="https://img.shields.io/badge/runtime-none-brightgreen" alt="No runtime deps">
  <img src="https://img.shields.io/badge/emoji-0-brightgreen" alt="Zero emoji">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="PRs welcome">
</p>

</div>

A **tool-agnostic** Agent Skill that turns a product brief into a single-file, self-contained HTML product promo animation — 15-30s, multi-scene GSAP timeline, four aspect ratios, zero emoji. It's pure **Markdown + one HTML skeleton + one Python validator**, so any AI coding tool that can *read files, write files, and run a shell* can use it.

> **Naming:** `jit-motion` is the project / repo name. The skill's internal identifier (folder + frontmatter `name`) is `product-promo-animation`.

## Features

- 🎞️ **One file, plays anywhere** — all CSS/JS inlined; only GSAP (CDN) and your logo are external.
- 🧭 **Four aspect ratios** — 16:9 / 4:3 / 1:1 / 9:16 with automatic layout reflow, no per-size hand-tuning.
- 🎨 **Brand-faithful** — harvests primary colors + logo from the product's official site.
- 🧩 **Zero emoji** — a 24×24 stroke-SVG icon system that stays crisp at any scale.
- ✅ **Deterministic validator** — `validate.py` catches dead CSS selectors, emoji leaks, timing drift and forbidden colors.
- 🤖 **Works with every major agent** — Claude Code, Codex, Cursor, Qoder, or any web LLM.

## Quick start

Give your agent this one line (works for any file-capable agent):

> "Read `SKILL.md` and follow it strictly. Generate a single-file HTML promo animation for **&lt;product&gt;**; brief below: **&lt;…&gt;**. Then run `scripts/validate.py` until it prints `OK`."

Prefer auto-discovery? Install it into your tool → [Install by tool](#install-by-tool).

## Table of contents

- [Features](#features)
- [Quick start](#quick-start)
- [Bilingual docs](#bilingual-docs)
- [Directory structure](#directory-structure)
- [Install by tool](#install-by-tool)
- [Prerequisites](#prerequisites)
- [Validator](#validator)
- [Contributing](#contributing)
- [License](#license)

## Bilingual docs

Every document ships in English and Simplified Chinese:

| English | 简体中文 |
|---------|----------|
| [`SKILL.md`](SKILL.md) | [`SKILL.zh-CN.md`](SKILL.zh-CN.md) |
| [`README.md`](README.md) | [`README.zh-CN.md`](README.zh-CN.md) |
| [`references/architecture.md`](references/architecture.md) | [`references/architecture.zh-CN.md`](references/architecture.zh-CN.md) |
| [`references/scene-recipes.md`](references/scene-recipes.md) | [`references/scene-recipes.zh-CN.md`](references/scene-recipes.zh-CN.md) |
| [`references/quality-checklist.md`](references/quality-checklist.md) | [`references/quality-checklist.zh-CN.md`](references/quality-checklist.zh-CN.md) |

`assets/skeleton.html` and `scripts/validate.py` are **shared** by both languages (code is language-neutral); the validator prints bilingual diagnostics. Each file's top has an `English | 简体中文` switcher.

> **On `SKILL.md`:** AI tools auto-load the file named exactly `SKILL.md`, so the English one is the canonical entry. Its `description` carries both English and Chinese trigger terms, so it is discovered for queries in either language. To feed Chinese instructions, point your agent at [`SKILL.zh-CN.md`](SKILL.zh-CN.md).

## Directory structure

```
jit-motion/
├── SKILL.md                    # Main entry: hard rules + 7-phase workflow (EN, canonical)
├── SKILL.zh-CN.md              # 简体中文
├── README.md / README.zh-CN.md # This file (EN / ZH)
├── LICENSE                     # MIT
├── references/
│   ├── architecture.md         # HTML/CSS/JS spec, color system, DOM contract, animation snippets
│   ├── scene-recipes.md        # Visual recipes + beats for the 8 scene archetypes
│   ├── quality-checklist.md    # Static + browser validation gates
│   └── *.zh-CN.md              # 简体中文 versions
├── assets/
│   ├── skeleton.html           # Copy-to-start template (with {{TOKEN}} placeholders)
│   └── preview.png             # This hero image
└── scripts/
    └── validate.py             # Deterministic static validator (python3, stdlib only)
```

The `SKILL.md` frontmatter (`name` / `description`) follows the **Anthropic Agent Skills** spec — Claude Code and Qoder auto-discover it and trigger on demand; other tools load it manually (below).

---

## Install by tool

| Tool | Mechanism | Auto-discovery |
|------|-----------|:--------------:|
| **Qoder** | copy into `.qoder/skills/` | ✅ |
| **Claude Code** | copy into `.claude/skills/` | ✅ |
| **Codex CLI** | `AGENTS.md` or `~/.codex/prompts/` | ➖ (manual) |
| **Cursor** | `.cursor/rules/*.mdc` | ➖ (rule) |
| **Web LLMs** | paste `SKILL.md` as context | ➖ (manual) |

### Qoder

```bash
# Project-level (shared with the team via the repo)
mkdir -p .qoder/skills
cp -r <jit-motion> .qoder/skills/

# Or personal-level (available across all projects)
mkdir -p ~/.qoder/skills
cp -r <jit-motion> ~/.qoder/skills/
```
Then simply say "make a promo animation for product X" — the skill is matched automatically.

### Claude Code (Anthropic)

```bash
# Project-level
mkdir -p .claude/skills
cp -r <jit-motion> .claude/skills/

# Or personal-level
mkdir -p ~/.claude/skills
cp -r <jit-motion> ~/.claude/skills/
```
Claude Code loads `SKILL.md` on relevant tasks based on `description`, and reads `references/` on demand.

### Codex (OpenAI Codex CLI)

Codex has no skill-directory auto-discovery. It reads project instructions from **`AGENTS.md`** and custom slash commands from **`~/.codex/prompts/`**.

**Option A — register in `AGENTS.md` (recommended, team-shared).** Append to the repo-root `AGENTS.md`:

```markdown
## Available skill: jit-motion (product promo animation)

When asked to "generate a product promo animation / marketing video / animated HTML demo":
1. Read `<jit-motion>/SKILL.md` in full and follow its hard rules and 7-phase workflow.
2. Read `references/architecture.md`, `references/scene-recipes.md`, `references/quality-checklist.md` as needed.
3. Start by copying `assets/skeleton.html`; replace every {{TOKEN}}.
4. Before delivering, run `python3 <jit-motion>/scripts/validate.py <output>` until it prints `OK`.
```

**Option B — a custom slash command (personal use).** Create `~/.codex/prompts/promo-animation.md`:

```markdown
Read and strictly follow <jit-motion>/SKILL.md (plus its references/ and assets/skeleton.html).
Generate a single-file HTML promo animation for the product below, then validate with scripts/validate.py until it prints `OK`.

Product brief:
$ARGUMENTS
```
Then run `/promo-animation <paste brief or path to brief>` in Codex. (`$ARGUMENTS` is Codex's argument placeholder; if unsupported, put the brief at the end of the file or in chat.)

### Cursor

Cursor uses **Project Rules** (`.cursor/rules/*.mdc`) or `AGENTS.md`. Since the skill is long, point a rule at `SKILL.md` rather than inlining it. Create `.cursor/rules/jit-motion.mdc`:

```markdown
---
description: Generate a single-file HTML product promo animation (GSAP multi-scene, four aspect ratios, zero emoji)
globs:
alwaysApply: false
---

When the task involves a "product promo animation / marketing video / animated HTML demo",
first read and strictly follow `<jit-motion>/SKILL.md`,
read its `references/` as needed, start from `assets/skeleton.html`,
and run `scripts/validate.py` until it prints `OK` before delivering.
```
Cursor injects the rule as context on relevant tasks; the agent then reads `SKILL.md` itself.

### Generic (any AI / web ChatGPT, Claude, Gemini, etc.)

For tools without a filesystem, use the "paste context" method:

1. Send the full [`SKILL.md`](SKILL.md) as the **first message / system prompt**;
2. Attach (or paste) [`references/architecture.md`](references/architecture.md), [`references/scene-recipes.md`](references/scene-recipes.md), and [`assets/skeleton.html`](assets/skeleton.html);
3. Provide the product brief: name, official site, capabilities to highlight, duration, forbidden elements, output requirements;
4. Have the model replace the `{{TOKEN}}`s in the skeleton and output the full HTML;
5. Save the HTML locally and run the validator once (web versions can't run it for you).

---

## Prerequisites

- **python3** — to run `scripts/validate.py` (pure standard library, no pip installs).
- **Network** — the produced HTML references GSAP via CDN; harvesting brand colors/logo requires reaching the product's official site.
- **Local server** (optional, for the browser pass with relative asset paths):
  ```bash
  python3 -m http.server 8000   # open http://localhost:8000/<output>.html
  ```

## Validator

```bash
python3 scripts/validate.py <output>.html            # auto-detects locale
python3 scripts/validate.py <output>.html --lang zh  # force Chinese diagnostics
python3 scripts/validate.py <output>.html --lang en  # force English diagnostics
# Exit code: 0 = OK (warnings possible) | 1 = errors present | 2 = usage/file error
```

Checks: placeholders, structure balance, zero emoji, forbidden colors, **dead CSS selectors**, timing consistency, GSAP, JSON-LD, logo, scene/marks count. **Never deliver without running it.**

## Contributing

Issues and PRs are welcome — new scene archetypes, more language versions, and validator checks especially. Please run `scripts/validate.py` on any example you add and keep the EN / `zh-CN` docs in sync.

## License

Released under the [MIT License](LICENSE). © 2026 JitWord 即时文档团队.
