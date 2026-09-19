> **语言：** [English](README.md) | 简体中文

<div align="center">

<img src="assets/preview.png" alt="jit-motion —— 多场景分镜、四种画幅比例与播放控件" width="860">

# jit-motion

**把产品宣传片，做成一个自包含的单文件 HTML。**
无需剪辑软件、无需渲染农场——只要一份产品简报和你的 AI 编程助手。

<p>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Codex%20%7C%20Cursor%20%7C%20Qoder-blue" alt="Works with">
  <img src="https://img.shields.io/badge/GSAP-3.12-88ce02" alt="GSAP">
  <img src="https://img.shields.io/badge/runtime-none-brightgreen" alt="No runtime deps">
  <img src="https://img.shields.io/badge/emoji-0-brightgreen" alt="Zero emoji">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="PRs welcome">
</p>

</div>

一个**工具无关**的 Agent Skill：把产品需求简介，生成为单文件、自包含的 HTML 产品宣传动画——15-30 秒、多场景 GSAP 时间轴、四画幅比例、零 emoji。它全部由 **Markdown + 一个 HTML 骨架 + 一个 Python 校验器**构成，不依赖任何特定 AI 平台，凡是能「读文件 + 写文件 + 跑 shell」的 AI 编码工具都能用它。

> **命名说明：** `jit-motion` 是项目 / 仓库名；技能的内部标识（目录名 + frontmatter `name`）为 `product-promo-animation`。

## 特性

- 🎞️ **单文件，随处可播** — 全部 CSS/JS 内联；仅 GSAP（CDN）与你的 logo 为外部引用。
- 🧭 **四种画幅比例** — 16:9 / 4:3 / 1:1 / 9:16 自动重排布局，无需逐尺寸手工微调。
- 🎨 **品牌保真** — 从产品官网抓取主色与 logo。
- 🧩 **零 emoji** — 24×24 描边 SVG 图标系统，任意缩放都清晰。
- ✅ **确定性校验器** — `validate.py` 捕获死 CSS 选择器、emoji 泄漏、时长漂移与禁用色。
- 🤖 **适配主流 Agent** — Claude Code、Codex、Cursor、Qoder，或任意网页大模型。

## 快速开始

把下面这句话交给你的 Agent（任何能读文件的 Agent 都适用）：

> 「读取 `SKILL.md` 并严格遵循它，为 **<产品>** 生成单文件 HTML 宣传动画；简报如下：**<…>**。完成后用 `scripts/validate.py` 校验到『OK』。」

想用自动发现？安装进你的工具 → [按工具安装](#按工具安装)。

## 目录

- [特性](#特性)
- [快速开始](#快速开始)
- [双语文档](#双语文档)
- [目录结构](#目录结构)
- [按工具安装](#按工具安装)
- [前置条件](#前置条件)
- [校验器](#校验器)
- [参与贡献](#参与贡献)
- [许可证](#许可证)

## 双语文档

每份文档都提供中英双语：

| 英文 | 简体中文 |
|------|----------|
| [`SKILL.md`](SKILL.md) | [`SKILL.zh-CN.md`](SKILL.zh-CN.md) |
| [`README.md`](README.md) | [`README.zh-CN.md`](README.zh-CN.md) |
| [`references/architecture.md`](references/architecture.md) | [`references/architecture.zh-CN.md`](references/architecture.zh-CN.md) |
| [`references/scene-recipes.md`](references/scene-recipes.md) | [`references/scene-recipes.zh-CN.md`](references/scene-recipes.zh-CN.md) |
| [`references/quality-checklist.md`](references/quality-checklist.md) | [`references/quality-checklist.zh-CN.md`](references/quality-checklist.zh-CN.md) |

`assets/skeleton.html` 与 `scripts/validate.py` 为两种语言**共享**（代码语言中立），校验器输出双语诊断。每个文档顶部都有 `English | 简体中文` 切换链接。

> **关于 `SKILL.md`：** AI 工具只自动加载文件名恰好为 `SKILL.md` 的文件，故英文那份是规范入口。它的 `description` 同时含中英文触发词，两种语言的提问都能命中。若想喂中文指令，请把 Agent 指向 [`SKILL.zh-CN.md`](SKILL.zh-CN.md)。

## 目录结构

```
jit-motion/
├── SKILL.md                    # 主入口：硬性规则 + 7 阶段工作流（英文·规范）
├── SKILL.zh-CN.md              # 简体中文
├── README.md / README.zh-CN.md # 本文件（英 / 中）
├── LICENSE                     # MIT
├── references/
│   ├── architecture.md         # HTML/CSS/JS 技术规格、配色、DOM 契约、动画片段
│   ├── scene-recipes.md        # 8 种场景原型的视觉配方与动画节拍
│   ├── quality-checklist.md    # 静态 + 浏览器双重校验门禁
│   └── *.zh-CN.md              # 简体中文版本
├── assets/
│   ├── skeleton.html           # 开箱即用的启动模板（含 {{TOKEN}} 占位符）
│   └── preview.png             # 顶部英雄图
└── scripts/
    └── validate.py             # 确定性静态校验器（python3，纯标准库）
```

`SKILL.md` 顶部的 YAML frontmatter（`name` / `description`）遵循 **Anthropic Agent Skills** 规范——Claude Code 与 Qoder 可据此自动发现并按需触发；其他工具则手动加载（见下）。

---

## 按工具安装

| 工具 | 接入方式 | 自动发现 |
|------|----------|:--------:|
| **Qoder** | 拷入 `.qoder/skills/` | ✅ |
| **Claude Code** | 拷入 `.claude/skills/` | ✅ |
| **Codex CLI** | `AGENTS.md` 或 `~/.codex/prompts/` | ➖（手动） |
| **Cursor** | `.cursor/rules/*.mdc` | ➖（规则） |
| **网页大模型** | 把 `SKILL.md` 作为上下文粘贴 | ➖（手动） |

### Qoder

```bash
# 项目级（随仓库共享给团队）
mkdir -p .qoder/skills
cp -r <jit-motion> .qoder/skills/

# 或个人级（所有项目可用）
mkdir -p ~/.qoder/skills
cp -r <jit-motion> ~/.qoder/skills/
```
之后直接说「帮我为 XX 产品做一个宣传动画」，Skill 会被自动匹配调用。

### Claude Code（Anthropic）

```bash
# 项目级
mkdir -p .claude/skills
cp -r <jit-motion> .claude/skills/

# 或个人级
mkdir -p ~/.claude/skills
cp -r <jit-motion> ~/.claude/skills/
```
Claude Code 会依据 `description` 在相关任务时自动加载 `SKILL.md`，并按需读取 `references/`。

### Codex（OpenAI Codex CLI）

Codex 没有「技能目录自动发现」机制，它通过 **`AGENTS.md`** 读取项目指令、通过 **`~/.codex/prompts/`** 提供自定义斜杠命令。

**方式 A — 在 `AGENTS.md` 中登记（推荐，团队共享）。** 在仓库根 `AGENTS.md` 追加：

```markdown
## 可用技能：jit-motion（产品宣传动画）

当需要「生成产品宣传动画 / 营销视频 / HTML 动画演示」时：
1. 先完整阅读 `<jit-motion>/SKILL.md` 并严格遵循其硬性规则与 7 阶段工作流；
2. 按需读取 references/architecture.md、references/scene-recipes.md、references/quality-checklist.md；
3. 从 assets/skeleton.html 复制起步，替换全部 {{TOKEN}}；
4. 交付前必须运行 `python3 <jit-motion>/scripts/validate.py <输出文件>`，直到打印「OK」。
```

**方式 B — 做成自定义斜杠命令（个人常用）。** 新建 `~/.codex/prompts/promo-animation.md`：

```markdown
阅读并严格遵循 <jit-motion>/SKILL.md（及其 references/、assets/skeleton.html），
为下面这个产品生成单文件 HTML 宣传动画，完成后用 scripts/validate.py 校验到「OK」。

产品简报：
$ARGUMENTS
```
之后在 Codex 里输入 `/promo-animation <粘贴简报或简报文件路径>` 即可。（`$ARGUMENTS` 为 Codex 参数占位；若不支持，把简报写在文件末尾或对话里。）

### Cursor

Cursor 用 **Project Rules**（`.cursor/rules/*.mdc`）或 `AGENTS.md`。因为 Skill 较长，最佳做法是**建一条规则指向 SKILL.md**，而非把全文塞进规则。新建 `.cursor/rules/jit-motion.mdc`：

```markdown
---
description: 生成单文件 HTML 产品宣传动画（GSAP 多场景、四画幅比例、零 emoji）
globs:
alwaysApply: false
---

当任务涉及「产品宣传动画 / 营销视频 / HTML 动画演示」时，
先阅读并严格遵循 `<jit-motion>/SKILL.md`，
按需读取其 references/，从 assets/skeleton.html 起步，
交付前运行 scripts/validate.py 校验到「OK」。
```
Cursor 会在相关任务时把该规则作为上下文注入，Agent 随后自行去读 SKILL.md。

### 通用方式（任意 AI / 网页版 ChatGPT、Claude、Gemini 等）

没有文件系统的工具，用「贴上下文」法：

1. 把 [`SKILL.md`](SKILL.md) 全文作为**首条消息 / 系统提示**发给模型；
2. 附上（或粘贴）[`references/architecture.md`](references/architecture.md)、[`references/scene-recipes.md`](references/scene-recipes.md) 与 [`assets/skeleton.html`](assets/skeleton.html)；
3. 给出产品简报：产品名、官网、待突出能力、时长、禁用元素、输出要求；
4. 让模型替换骨架里的 `{{TOKEN}}` 并输出完整 HTML；
5. 把产出的 HTML 存盘后本地跑一次校验（网页版无法自动运行）。

---

## 前置条件

- **python3** — 运行 `scripts/validate.py`（纯标准库，无需 pip 安装）。
- **联网** — 产出的 HTML 通过 CDN 引用 GSAP；抓品牌配色/logo 需访问产品官网。
- **本地服务器**（可选，用于浏览器走查相对路径资源）：
  ```bash
  python3 -m http.server 8000   # 访问 http://localhost:8000/<输出文件>.html
  ```

## 校验器

```bash
python3 scripts/validate.py <输出文件>.html            # 按 locale 自动检测语言
python3 scripts/validate.py <输出文件>.html --lang zh  # 强制中文诊断
python3 scripts/validate.py <输出文件>.html --lang en  # 强制英文诊断
# 退出码：0 = 通过（可能有警告）｜1 = 有错误｜2 = 用法/文件错误
```

检查：占位符、结构平衡、零 emoji、禁用色、**死 CSS 选择器**、时长一致、GSAP、JSON-LD、logo、场景/标记数匹配。**未跑校验不要交付。**

## 参与贡献

欢迎 Issue 与 PR——尤其是新的场景原型、更多语言版本、以及校验器新检查项。请为你添加的示例运行 `scripts/validate.py`，并保持中英两份文档同步。

## 许可证

基于 [MIT License](LICENSE) 发布。© 2026 JitWord 即时文档团队。
