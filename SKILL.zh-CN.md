---
name: product-promo-animation
description: 基于产品需求文档/PRD/简介，生成单文件、自包含的 HTML 产品宣传动画视频（15-30 秒）。产出包含多场景 GSAP 时间轴分镜、四比例切换（16:9/4:3/1:1/9:16）、零 emoji 的 SVG 图标系统、抓取自官网的品牌配色、播放控件与 SEO 视频元数据。当用户要求制作产品宣传动画、营销/广告视频、HTML 动画演示、产品发布视频，或提到用 GSAP/motion/SVG 动画做产品视频时使用。Generate a self-contained animated HTML product promotional video (15-30s) from a product brief; use when the user asks for a product promo animation, marketing video, animated HTML demo, or product showcase built with GSAP/motion/SVG.
---

> **语言：** [English](SKILL.md) | 简体中文

# 产品宣传动画（Product Promo Animation）

把一份产品需求简介，转化为广播级、单文件的 HTML 动画宣传视频。本 Skill 沉淀了已在多个产品发布中验证成功的通用模式（多维表格、AI 知识库、协同文档工具）。

## 本 Skill 产出什么

一个自包含的 `.html` 文件，具备：
- 由 GSAP 时间轴驱动、逐场景讲述产品故事的 15-30 秒动画
- 四种画幅比例切换（16:9 横屏、4:3、1:1、9:16 竖屏），并自动重排布局
- 仅使用精致 SVG 图标（零 emoji）+ 抓取自品牌官网的配色
- 完整播放控件（播放/暂停、重播、进度拖拽、场景导航、比例切换、键盘快捷键）
- SEO 视频元数据（JSON-LD `VideoObject`、Open Graph、canonical）

## 何时使用

当用户需要**以 HTML 形式制作产品宣传动画/视频**时触发，通常会提供：
- 描述产品与待突出能力的需求简介 / PRD / markdown 规格
- 产品名称与官网地址（用于抓取品牌）
- 时长、视觉风格、参考视频、禁用元素等约束

## 硬性规则（不可协商）

以下均来自反复出现的用户反馈，违反任意一条即为缺陷。

1. **零 emoji。** 每个图标都必须是内联 SVG `<symbol>`/`<use>`（24×24 viewBox、`stroke="currentColor"`、`fill="none"`、stroke-width 2、圆角端点/连接）。emoji 渲染不一致且显得不专业。
2. **禁用紫色/洋红渐变**（除非品牌本身使用）。默认禁用色值：`#722ED1`、`#EB2F96`、`#F472B6`、`#A855F7`、`#8B5CF6`、`#D946EF`、`#C026D3`。改用与品牌协调的辅助色（青绿 `#00C4B4`、暖橙 `#FF7D00`、成功绿 `#00B42A`、金黄 `#FFB800`、玫红 `#F53F3F`）。
3. **品牌保真。** 主色与 logo 必须抓取自产品官网，不可凭空臆造配色。logo 必须出现（至少开场 + 收尾两个场景）。
4. **单文件。** 所有 CSS 与 JS 内联；仅动画库（GSAP）与 logo 图片为外部引用。
5. **选择器必须匹配真实类名。** targeting 不存在类名的 CSS 规则会静默失效。校验器会捕获此问题——绝不可跳过校验。
6. **时长一致。** `DURATION` 常量、界面时间标签、JSON-LD `duration`、以及时间轴真实长度，四者必须一致。

## 工作流

将以下清单复制到工作笔记中并跟踪进度：

```
- [ ] 阶段 1：消化需求简介
- [ ] 阶段 2：抓取品牌标识
- [ ] 阶段 3：设计分镜脚本
- [ ] 阶段 4：从骨架起步
- [ ] 阶段 5：搭建各场景
- [ ] 阶段 6：编排时间轴动画
- [ ] 阶段 7：校验并交付
```

### 阶段 1：消化需求简介

完整阅读用户的需求文档，提取为一张工作表：
- **产品**：名称、标语、官网 URL
- **待突出能力**：明确的功能清单（它们将成为中间各场景）
- **时长目标**：如"15-30 秒" → 规划约 26 秒
- **硬性约束**：禁用色、图标风格、参考视频、输出路径
- **调性**：来自所要求的营销视角（如"产品营销专家"）

若简介未指明输出位置，先询问，或默认与简介同目录。

### 阶段 2：抓取品牌标识

访问产品官网提取事实依据——不要臆测：
- **主色**与渐变止点（检查 CSS / 主题）
- **Logo URL**（下载到输出文件旁，如 `./assets/<product>-logo.png`）
- 设计系统中使用的**辅助色**
- **视觉语言**：卡片样式、圆角、阴影、字体排印

把这些记录为一份"品牌 token"清单，全程复用。token 结构见 [references/architecture.zh-CN.md](references/architecture.zh-CN.md) §配色系统。

### 阶段 3：设计分镜脚本

将能力映射为场景序列。经验证的结构是 **8 场景 / 约 26 秒**（更短时长可缩至 6-8 场景）：

| # | 场景原型 | 时长 | 目的 |
|---|---------|------|------|
| S1 | 品牌开场 | ~2.6s | Logo 入场 + 粒子 + 产品名 + 标语 |
| S2 | 核心编辑器/能力 | ~3.4s | 具体呈现首要功能 |
| S3 | 搭建/创造 | ~3.4s | 招牌"惊艳"工作流（如拖拽搭建） |
| S4 | 多维视图/灵活性 | ~3.4s | 多模式标签切换 |
| S5 | 生态/集成 | ~3.4s | 中心辐射式连接 |
| S6 | AI 智能 | ~3.2s | 查询 → 结果 → 智能建议 |
| S7 | 实时协同 | ~3.0s | 多用户光标、评论、在线状态 |
| S8 | 品牌收尾 | ~3.8s | Logo 呼吸 + 标语 + 能力 chip + CTA |

产出一张**时间表**，含固定场景标记（如 `0, 2.6, 6.0, 9.4, 12.8, 16.2, 19.4, 22.4`），以及每场景的元素 + 动画节拍清单。只挑选与简介能力匹配的原型，可自由重命名与再定位。每种原型的视觉配方与动画节拍见 [references/scene-recipes.zh-CN.md](references/scene-recipes.zh-CN.md)。

### 阶段 4：从骨架起步

将 [assets/skeleton.html](assets/skeleton.html) 复制到输出路径。它含完整基础设施与 `{{PLACEHOLDER}}` 占位 token：
- `<head>`：meta、JSON-LD `VideoObject`、OG 标签、GSAP script 标签
- CSS：舞台 + 四比例变量系统 + 场景/布局/控件样式
- SVG symbol 图标库脚手架
- 两个示例场景（S1 品牌、S2 能力），演示 DOM 模式
- 控件条 HTML
- JS：`fitStage`、`setAspect`、时间轴初始化、`showScene`/`hideScene`、`updateProgress`、场景导航、键盘、控件自动隐藏

替换每一个 `{{TOKEN}}`，不可遗留占位符。动手前先理解基础设施——见 [references/architecture.zh-CN.md](references/architecture.zh-CN.md)。

### 阶段 5：搭建各场景

对分镜中的每个场景：
1. 在图标库中定义它需要的 SVG `<symbol>`（跨场景复用）。
2. 编写场景 DOM：`.scene#sN > .grid-bg + .glow-orb* + .layout > (.left-copy + <图形>)`。
3. `.left-copy` 承载 badge + 标题 + 副标题 + chip-row（文案）；图形容器承载可视化演示。
4. 所有图形都用带样式的 HTML/SVG div 实现——除 logo 外不用外部图片。

严格遵循 DOM 契约，响应式系统才能生效。见 [references/architecture.zh-CN.md](references/architecture.zh-CN.md) §场景 DOM 契约。

### 阶段 6：编排时间轴动画

构建唯一的 `gsap.timeline({ paused: true })`。对标记 `TN` 处的每个场景：
- `showScene('sN', TN)`，随后 badge → 标题 → 副标题 → chips → 图形的错峰 `.from()` 入场
- 图形专属节拍（打字、拖拽、数字滚动、路径描边、标签切换、光标移动）
- `hideScene('sN', TN + 场景时长 - 0.5)` 做交叉淡出

将 `DURATION` 设为最后一个场景的结束点。用场景标记数组接通 `updateProgress`。可复用的节拍片段（数字滚动、描边绘制、打字机、拖拽光标、视图切换）见 [references/architecture.zh-CN.md](references/architecture.zh-CN.md) §动画引擎。

### 阶段 7：校验并交付

**未运行校验器绝不交付。**

```bash
python3 scripts/validate.py <output.html>
```

它检查：结构平衡、零 emoji、禁用色、**死 CSS 选择器**（targeting HTML 中不存在的类的规则）、时长一致性、GSAP 是否存在、JSON-LD 是否存在。修完它报告的所有问题，反复运行直到打印 `OK`。

随后按 [references/quality-checklist.zh-CN.md](references/quality-checklist.zh-CN.md) 做浏览器走查：控制台无报错、所有场景按序激活、比例切换正确重排（尤其 9:16——文案与图形必须成组，不可分离）、无溢出滚动条。

## 参考文件

- [references/architecture.zh-CN.md](references/architecture.zh-CN.md) — 完整 HTML/CSS/JS 技术规格、配色系统、DOM 契约、动画引擎片段
- [references/scene-recipes.zh-CN.md](references/scene-recipes.zh-CN.md) — 8 种场景原型的视觉配方与动画节拍
- [references/quality-checklist.zh-CN.md](references/quality-checklist.zh-CN.md) — 静态 + 浏览器验证门禁与常见缺陷
- [assets/skeleton.html](assets/skeleton.html) — 含完整基础设施的复制即用启动模板
- [scripts/validate.py](scripts/validate.py) — 确定性静态校验器
- [README.zh-CN.md](README.zh-CN.md) — 在 Codex / Claude Code / Cursor / Qoder 等工具中的安装与使用

## 生产环境沉淀的反模式

- **死选择器**：HTML 类名是 `.left-copy` 却写成 `.copy` → 规则被静默忽略。务必交叉核对类名；校验器会强制检查。
- **9:16 布局分离**：stacked 模式用 `grid-template-rows: auto 1fr` 会让图形在超高行中浮动，与文案分离。改用 `auto auto` + `align-content: center`。
- **时长漂移**：某个 `yoyo`/`repeat` 补间使时间轴超出 `DURATION`。计算真实结束点，同步全部四处时长引用。
- **emoji 泄漏**：文案里混入 `✓` 或 `→`。扫描并替换为 SVG。
- **GSAP 选择器笔误**：元素用 `class="child"` 却写成 `#id .child` → 空补间告警。校验目标是否存在。
