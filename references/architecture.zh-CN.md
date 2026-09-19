> **语言：** [English](architecture.md) | 简体中文

# 架构参考（Architecture Reference）

本文件是 `assets/skeleton.html` 所体现的单文件宣传动画的完整技术规格。构建时逐节对照。

## 目录

1. [文件拓扑](#1-文件拓扑)
2. [Head 与 SEO 元数据](#2-head-与-seo-元数据)
3. [舞台与画幅比例变量系统](#3-舞台与画幅比例变量系统)
4. [场景 DOM 契约](#4-场景-dom-契约)
5. [stacked 模式响应式规则](#5-stacked-模式响应式规则)
6. [配色系统](#6-配色系统)
7. [SVG 图标系统](#7-svg-图标系统)
8. [控件条](#8-控件条)
9. [JavaScript 基础设施](#9-javascript-基础设施)
10. [动画引擎与可复用片段](#10-动画引擎与可复用片段)

---

## 1. 文件拓扑

```
<product>-promo.html      # 单文件产出（全部 CSS + JS 内联）
assets/<product>-logo.png # 唯一外部资源，除 GSAP 外
```

外部依赖（仅此两项）：
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<img src="./assets/<product>-logo.png" alt="...">
```

文件内部顺序：
```
<head>  meta + JSON-LD + OG + <style>（全部 CSS）
<body>
  <div id="viewport"><div id="stage"> ...全部场景... </div></div>
  <div id="controls"> ...播放 UI... </div>
  <svg id="svg-defs"><symbol>...</symbol>...</svg>   <!-- 图标库 -->
  <script> ...GSAP 时间轴 + 基础设施... </script>
```

---

## 2. Head 与 SEO 元数据

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{PRODUCT_NAME}} — {{TAGLINE}} | 产品宣传片</title>
<meta name="description" content="{{一句以动作为导向、含关键词的产品描述}}">
<link rel="canonical" href="{{PAGE_URL}}">

<!-- JSON-LD：让搜索引擎将页面理解为视频 -->
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

`duration` 必须是 ISO 8601 时长格式（`PT26S`），并与 JS 的 `DURATION` 一致。

---

## 3. 舞台与画幅比例变量系统

动画运行在一个**固定尺寸的虚拟舞台**上，由 `fitStage()` 缩放以适配任意窗口。这保证各比例下布局像素级一致。

```css
html, body {
  margin: 0; width: 100%; height: 100%;
  background: #070b18; overflow: hidden;
}
#viewport { position: fixed; inset: 0; overflow: hidden; }
#stage {
  position: absolute; left: 50%; top: 50%;
  width: 1920px; height: 1080px;              /* 16:9 默认 */
  background: var(--bg); overflow: hidden;
  transform: translate(-50%, -50%) scale(1);
  transform-origin: center center;
}
```

画幅比例把全部布局变量写在 `#stage` 上，使每个场景自动重排：

```css
:root {
  --bg: #070b18;
  --brand: #165DFF;        /* 抓取自官网 */
  --brand-light: #4080FF;
  --accent: #00C4B4;       /* 青绿 */
  --accent-warm: #FF7D00;  /* 暖橙 */
  --text: #ffffff;
  --text-muted: #8b96b0;
}

/* 16:9（默认）— 双栏：文案 | 图形 */
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
/* 1:1 — 堆叠 */
#stage[data-aspect="1:1"] {
  --sw: 1080px; --sh: 1080px;
  --pad-x: 70px; --col-left: 100%; --col-gap: 40px;
  --title-size: 62px; --stack-mode: 1;
}
/* 9:16 — 堆叠（竖屏）*/
#stage[data-aspect="9:16"] {
  --sw: 1080px; --sh: 1920px;
  --pad-x: 60px; --col-left: 100%; --col-gap: 36px;
  --title-size: 60px; --stack-mode: 1;
}
```

`fitStage()`（见 §9）读取 `data-aspect`，把 `#stage` 宽高设为 `--sw`/`--sh`，并按 `min(视口宽/舞台宽, 视口高/舞台高)` 计算缩放。

---

## 4. 场景 DOM 契约

**每个场景都必须遵循此结构**，否则双栏↔堆叠响应式系统会失效。

```html
<section class="scene" id="sN">
  <!-- 氛围背景：网格 + 光晕 -->
  <div class="grid-bg"></div>
  <div class="glow-orb orb-a"></div>
  <div class="glow-orb orb-b"></div>

  <!-- 布局：恰好 2 个直接子元素 -->
  <div class="layout">
    <!-- 子元素 1：文案（badge → 标题 → 副标题 → chips）-->
    <div class="left-copy">
      <div class="scene-badge"><svg class="ico"><use href="#ic-..."/></svg> Badge 文本</div>
      <h2 class="scene-title">主标题</h2>
      <p class="scene-sub">一句描述性副标题。</p>
      <div class="chip-row">
        <div class="chip"><svg class="ico"><use href="#ic-..."/></svg> 能力 A</div>
        <div class="chip"><svg class="ico"><use href="#ic-..."/></svg> 能力 B</div>
      </div>
    </div>

    <!-- 子元素 2：图形可视化（任意容器类）-->
    <div class="my-stage"> ...div/SVG 构建的演示... </div>
  </div>
</section>
```

布局 CSS：

```css
.scene { position: absolute; inset: 0; opacity: 0; visibility: hidden; }
.scene.active { opacity: 1; visibility: visible; }

.layout {
  position: absolute; inset: 0;
  display: grid;
  grid-template-columns: var(--col-left) 1fr;   /* 文案 | 图形 */
  align-items: center;
  gap: var(--col-gap);
  padding: 64px var(--pad-x);
}

.left-copy { display: flex; flex-direction: column; gap: 24px; max-width: var(--col-left); }
.scene-title { font-size: var(--title-size); font-weight: 800; line-height: 1.1; }
.scene-sub { font-size: 26px; color: var(--text-muted); line-height: 1.6; }
.chip-row { display: flex; flex-wrap: wrap; gap: 14px; }
```

**契约规则：**
- `.layout` 恰好有 **2 个子元素**：文案块与图形块。
- 图形块是 `.layout` 的直接子元素（不要外包一层 `.right` 容器——那样堆叠规则就 targeting 错了）。
- 用与类名匹配的选择器编写图形 CSS；校验器会标记任何不匹配 HTML 的类选择器。

场景 badge / 标题 / 副标题 / chips：

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

## 5. stacked 模式响应式规则

当 `--stack-mode: 1`（1:1 与 9:16）时，布局从双栏翻转为居中堆叠列。**这是各比例间最易出问题的部分。**

```css
#stage[data-aspect="1:1"] .layout,
#stage[data-aspect="9:16"] .layout {
  grid-template-columns: 1fr;
  grid-template-rows: auto auto;    /* 关键：绝不用 auto 1fr */
  align-content: center;            /* 文案+图形作为一组垂直居中 */
  justify-items: stretch;           /* 关键：不用 center，否则 width:100% 图形会塌陷 */
  align-items: stretch;
  gap: 40px;
}
```

**两条不可协商的堆叠规则：**

1. **`grid-template-rows: auto auto`（绝非 `auto 1fr`）。** 用 `1fr` 会把第二行（图形）撑满剩余高度，使图形在超高行内居中，与文案分离、上下留大片空白。`auto auto` + `align-content: center` 才能把两者作为一组紧凑居中。

2. **`justify-items: stretch`（而非 `center`）。** 图形容器常用 `width: 100%`；`center` 会使其塌陷为零宽。用 `stretch` 让每个子元素填满列宽，再各自内部居中。

文案在 stacked 模式下居中：

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

**图形高度（防止溢出）。** 9:16 竖向空间充裕，可放大图形；1:1 必须收小避免溢出：

```css
/* 9:16：放大图形（竖屏空间充裕）*/
#stage[data-aspect="9:16"] .my-stage { height: 700px; }
/* 1:1：收紧（空间受限）*/
#stage[data-aspect="1:1"] .my-stage { height: 560px; }
```

为**每个**图形容器设置显式高度；否则其内在高度在堆叠布局中可能溢出。

**表格类图形：** 若用真正的 `<table>`（语义化的 `th`/`td`），以元素选择器增高，而非类名：
```css
#stage[data-aspect="9:16"] .data-table th,
#stage[data-aspect="9:16"] .data-table td { padding: 16px 14px; }
```

---

## 6. 配色系统

把品牌色定义为 `:root` 上的 token，全程复用。切勿硬编码一次性色值。

```css
:root {
  --brand: #165DFF;         /* 主色 — 抓取自官网 */
  --brand-light: #4080FF;   /* 亮色变体 */
  --accent: #00C4B4;        /* 青绿辅助 */
  --accent-warm: #FF7D00;   /* 暖橙（告警/CTA）*/
  --success: #00B42A;       /* 绿色完成态 */
  --gold: #FFB800;          /* 金黄高亮 */
  --rose: #F53F3F;          /* 玫红强调 */
  --bg: #070b18;            /* 深色舞台背景 */
  --surface: rgba(255,255,255,.04);
  --border: rgba(255,255,255,.09);
  --text: #ffffff;
  --text-muted: #8b96b0;
}
```

**禁用色（除非品牌本身使用）：** `#722ED1`、`#EB2F96`、`#F472B6`、`#A855F7`、`#8B5CF6`、`#D946EF`、`#C026D3`。校验器会扫描这些。

渐变应混合品牌色与协调的辅助色：
```css
background: linear-gradient(135deg, var(--brand), var(--accent));
```

---

## 7. SVG 图标系统

页面底部一个 `<svg id="svg-defs">` 承载全部图标作为 `<symbol>`。用 `<use href="#ic-name">` 引用。

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
  <!-- 更多 symbol... -->
</svg>
```

用法（`ico` 类统一设定尺寸与描边）：
```html
<svg class="ico"><use href="#ic-database"/></svg>
```
```css
.ico { width: 20px; height: 20px; stroke: currentColor; fill: none; }
```

**规则：**
- 24×24 viewBox、`fill="none"`、`stroke="currentColor"`、`stroke-width="2"`、圆角端点/连接。
- 颜色继承自父元素的 `color`，使图标随场景配色变化。
- **绝不使用 emoji**——校验器会标记常见 emoji、`✓`、`→`。

---

## 8. 控件条

固定于底部的播放 UI，与 `#stage` 同级（是兄弟，不是子元素）。

```html
<div id="controls">
  <div class="progress-track" id="progress-track"><div class="progress-fill" id="progress-fill"></div></div>
  <button id="btn-play" class="ctrl-btn" title="播放/暂停 (Space)">...</button>
  <button id="btn-replay" class="ctrl-btn" title="重播 (R)">...</button>
  <span class="time-label" id="time-label">0.0s / {{NN}}s</span>
  <div class="scene-nav" id="scene-nav"><!-- 每场景一个 .dot --></div>
  <div class="aspect-switcher" id="aspect-switcher">
    <button data-aspect="16:9" class="on">16:9</button>
    <button data-aspect="4:3">4:3</button>
    <button data-aspect="1:1">1:1</button>
    <button data-aspect="9:16">9:16</button>
  </div>
</div>
```

自动隐藏（`#controls` 是 `#viewport` 的兄弟，故用 `body:hover`）：
```css
#controls { opacity: 0; transition: opacity .3s; }
body:hover #controls,
body.controls-force-show #controls { opacity: 1; }
```
一段 JS IIFE 管理 `controls-force-show` 与闲置定时器（鼠标静止 ~2.6s 后隐藏）。见骨架。

---

## 9. JavaScript 基础设施

骨架提供以下部分。理解它们，再添加时间轴。

```js
const stage = document.getElementById('stage');
const scenes = Array.from(document.querySelectorAll('.scene'));
let currentAspect = '16:9';

// 等比缩放固定舞台以适配窗口
function fitStage() {
  const w = window.innerWidth, h = window.innerHeight;
  const sw = parseFloat(getComputedStyle(stage).width);
  const sh = parseFloat(getComputedStyle(stage).height);
  const scale = Math.min(w / sw, h / sh);
  stage.style.transform = `translate(-50%, -50%) scale(${scale})`;
}

// 切换画幅比例：设置尺寸变量 + 重新缩放
function setAspect(ratio) {
  currentAspect = ratio;
  stage.setAttribute('data-aspect', ratio);
  // --sw/--sh 已在 CSS 中定义，fitStage 读取计算后的尺寸
  fitStage();
}

// 场景可见性（供时间轴回调使用）
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

// 进度条 + 时间标签
function updateProgress() {
  const t = window.__tl.time();
  progressFill.style.width = (t / DURATION * 100) + '%';
  timeLabel.textContent = t.toFixed(1) + 's / ' + DURATION.toFixed(1) + 's';
}
```

**场景标记与时长**（驱动一切）：
```js
const DURATION = 26.2;                              // 须等于时间轴真实长度
const MARKS = [0, 2.6, 6.0, 9.4, 12.8, 16.2, 19.4, 22.4];  // 每个场景起点
```

**键盘快捷键：**
| 键 | 动作 |
|----|------|
| `Space` | 播放 / 暂停 |
| `R` | 重播 |
| `1` `2` `3` `4` | 切画幅 16:9 / 4:3 / 1:1 / 9:16 |
| `←` `→` | 上/下一场景标记 |
| `C` | 切换结尾 CTA |

---

## 10. 动画引擎与可复用片段

一条主时间轴，`paused: true`，暴露于 `window.__tl` 以便调试：

```js
window.__tl = gsap.timeline({ paused: true, onUpdate: updateProgress });
const tl = window.__tl;

// S1（标记 0）
showScene('s1', 0);
tl.from('#s1 .brand-logo', { opacity: 0, scale: .8, duration: .8, ease: 'back.out(1.7)' }, 0.1)
  .from('#s1 .scene-title', { opacity: 0, y: 30, duration: .7 }, 0.5)
  .from('#s1 .scene-sub',   { opacity: 0, y: 20, duration: .6 }, 0.9);
hideScene('s1', 2.1);

// S2（标记 2.6）……依此类推
```

### 可复用节拍片段

**数字滚动（count-up）：**
```js
function countUp(el, to, dur, at, prefix = '', suffix = '') {
  const obj = { v: 0 };
  tl.to(obj, { v: to, duration: dur, ease: 'power1.out',
    onUpdate: () => el.textContent = prefix + Math.round(obj.v).toLocaleString() + suffix
  }, at);
}
```

**路径描边绘制（用于连接线/下划线）：**
```js
tl.fromTo(path, { strokeDasharray: len, strokeDashoffset: len },
                { strokeDashoffset: 0, duration: .8, ease: 'power2.inOut' }, at);
```

**环形图（donut）填充：**
```js
tl.fromTo(circle, { strokeDashoffset: C }, { strokeDashoffset: C * (1 - pct), duration: 1 }, at);
```

**打字机效果：**
```js
function typeText(el, text, at, cps = 30) {
  tl.call(() => { el.textContent = ''; }, null, at);
  [...text].forEach((ch, i) =>
    tl.call(() => el.textContent += ch, null, at + i / cps));
}
```

**拖拽光标（把卡片从 A 移到 B）：**
```js
tl.to(cursor, { x: targetX, y: targetY, duration: .6, ease: 'power2.inOut' }, at)
  .to(card,   { x: targetX, y: targetY, duration: .5, ease: 'back.out(1.4)' }, at + .3);
```

**视图切换（table → kanban → …）：** 对标签用 stagger `.to()` 做激活态切换，配合容器 `opacity`/`scale` 的交叉淡入淡出。

**中心辐射（hub-spoke）入场：** 中心 logo 缩放弹入，随后各节点沿圆周用 `back.out` stagger，连接线描边绘制。

**Logo 呼吸（收尾）：**
```js
tl.to(logo, { scale: 1.06, duration: 1.4, yoyo: true, repeat: 1, ease: 'sine.inOut' }, at);
```
> 注意：`yoyo`/`repeat` 会拉长真实时间轴。计算结束点并同步 `DURATION`。
