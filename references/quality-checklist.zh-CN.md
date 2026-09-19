> **语言：** [English](quality-checklist.md) | 简体中文

# 质量门禁与校验清单（Quality Gate & Checklist）

两道门禁，按顺序执行。**两道都通过后才可交付。**

---

## 门禁 1 — 静态校验（自动化）

```bash
python3 scripts/validate.py <output.html>
```

退出码：`0` = OK（可能有警告）、`1` = 发现错误、`2` = 用法/文件错误。修完**所有**错误；逐条过一遍警告，确认其无害。

校验器覆盖：

- [ ] **无遗留占位符**（`{{TOKEN}}` 必须全部替换）
- [ ] **结构平衡**（标签配平；`<script>`/`<style>` 数量合理）
- [ ] **零 emoji**（扫描内容中已剥离注释后的 emoji、`✓`、`→`）
- [ ] **无禁用色**（`#722ED1`/`#EB2F96`/`#F472B6`/`#A855F7`/`#8B5CF6`/`#D946EF`/`#C026D3`，除非品牌使用）
- [ ] **无死 CSS 选择器**（每个类选择器都对得上 HTML/JS 中真实的类）
- [ ] **时长一致**（`DURATION` == 时间标签 == JSON-LD `PT..S`）
- [ ] **GSAP 存在**（script 标签 + `gsap.timeline`）
- [ ] **JSON-LD 存在**（`VideoObject`）
- [ ] **logo 存在**（引用了 logo 资源）
- [ ] **scenes 与 marks 匹配**（场景数 == `MARKS` 条目数）

> 死选择器检查是最高价值门禁——它能捕获那些 targeting 错误类名、因而**静默失效**的响应式规则（历史上最难发现的 bug 类别）。

---

## 门禁 2 — 浏览器走查（人工）

在浏览器中打开文件（用本地服务器以正确解析 `./assets/`）：

```bash
python3 -m http.server 8000
# 访问 http://localhost:8000/<output.html>
```

- [ ] **控制台无报错**（打开 DevTools Console；零红色错误）
- [ ] **播放/暂停** 生效（按钮 + 空格键）
- [ ] **重播** 从头重置
- [ ] **进度拖拽** 可定位到任意时刻
- [ ] **全部场景按序激活**（S1→S8，无跳过、无卡死）
- [ ] **场景导航点** 可跳转到对应场景
- [ ] **每个画幅比例都能正确重排：**
  - [ ] 16:9 — 双栏，文案 | 图形
  - [ ] 4:3 — 双栏，收窄
  - [ ] 1:1 — 堆叠，成组居中（文案紧贴图形）
  - [ ] 9:16 — 堆叠，成组居中；**文案与图形绝不分离**；无溢出
- [ ] **无滚动条**，任何比例下内容都不溢出舞台
- [ ] **CTA 开关** 可切换按钮/URL 显隐（+ `C` 键）
- [ ] **键盘快捷键** 全部生效（`Space` `R` `1-4` `←` `→` `C`）
- [ ] **控件自动隐藏** 在闲置约 2.6s 后淡出、鼠标移动时复现

### 浏览器探针（可选）

在 DevTools Console 中粘贴，以编程方式断言状态：

```js
// 时间轴已暴露且时长匹配
console.assert(window.__tl, '__tl 缺失');
console.log('duration:', window.__tl.duration());

// 跳转并激活每个场景，确认 .active 应用
const marks = [0, 2.6, 6.0, 9.4, 12.8, 16.2, 19.4, 22.4];
marks.forEach((t, i) => {
  window.__tl.pause(t + 0.05);
  const active = document.querySelector('.scene.active');
  console.log(`场景 ${i + 1} @${t}:`, active ? active.id : '无');
});

// 每个比例都设置了 data-aspect
['16:9','4:3','1:1','9:16'].forEach(r => {
  setAspect(r);
  console.assert(document.getElementById('stage').dataset.aspect === r, `比例 ${r} 失败`);
});
```

---

## 常见缺陷对照表

| 症状 | 根因 | 修复 |
|------|------|------|
| 9:16 下文案/图形分离 | stacked grid 用了 `auto 1fr` | `auto auto` + `align-content: center` |
| stacked 下图形零宽 | `justify-items: center` | 改为 `stretch` |
| 响应式规则无效 | 死选择器（类名不匹配，如 `.copy` vs `.left-copy`） | 匹配真实类名；跑校验器 |
| 表格增高无效 | targeting `.tc`/`.tr` 但实为 `<table>` | 用 `.data-table th/td` |
| 文案出现 emoji | 用了 `✓`/`→` 或表情 | 替换为 SVG 图标 |
| 时长标签不符 | `DURATION` ≠ 真实时间轴长度 | 重算结束点；同步全部四处 |
| 补间为空/告警 | GSAP 选择器笔误（`#id .x` 不存在） | 核对目标存在 |
| 控件不显示 | `#viewport:hover #controls`（它们是兄弟） | `body:hover #controls` + JS 闲置隐藏 |
| 某比例内容溢出 | 图形无显式高度 | 给每个图形容器设 `height` |
| 出现紫色/洋红 | 用了默认禁用色 | 换成协调的品牌辅助色 |

---

## 交付总结模板

走查通过后，向用户报告：

```
✓ 已生成 <product>-promo.html（单文件，自包含）
  • 时长：<NN>s，<K> 个场景
  • 比例：16:9 / 4:3 / 1:1 / 9:16（全部走查通过）
  • 品牌：<主色> 抓取自 <官网>
  • 图标：<M> 个 SVG symbol，零 emoji
  • 校验：validate.py → OK（退出码 0）
  • 浏览器：控制台无报错，全部场景 + 比例 + 快捷键已验证
```
