#!/usr/bin/env python3
"""
Static validator for product-promo-animation HTML deliverables.
product-promo-animation HTML 交付物的静态校验器。

Usage / 用法:
    python3 validate.py <output.html> [--lang en|zh]

Language / 语言:
    --lang en|zh forces the diagnostic language; omit it to auto-detect
    from PROMO_LANG / LC_ALL / LANG (Chinese locale -> zh, otherwise en).
    --lang en|zh 强制指定输出语言；省略则按 PROMO_LANG / LC_ALL / LANG
    自动检测（中文环境 -> zh，否则 en）。

Checks (errors fail the build, warnings need review) / 检查项（错误=失败，警告=需复核）:
  - Unresolved {{PLACEHOLDER}} tokens / 未替换的占位符
  - Structure balance: <div>, and {} () [] inside the main <script> / 结构平衡
  - Zero emoji / pictograph / arrow glyphs / 零 emoji（含 ✓ →）
  - No forbidden purple/magenta colors / 禁用紫洋红色
  - No dead CSS selectors (a .class in <style> absent from HTML and JS) / 死 CSS 选择器
  - Timing consistency: DURATION vs #time-label vs JSON-LD duration / 时长一致
  - GSAP library referenced, and a local copy exists on disk / 已引用 GSAP,本地副本存在
  - JSON-LD VideoObject present / 存在 JSON-LD VideoObject
  - Logo <img> referenced and the file exists on disk / logo 已引用且存在
  - Scene registry count vs MARKS count / 场景数 vs MARKS 数

Exit code 0 = clean (warnings allowed), 1 = errors present, 2 = usage/file error.
退出码 0 = 通过（允许警告），1 = 存在错误，2 = 用法/文件错误。
"""
import sys, os, re

# ---------------------------------------------------------------- i18n
MESSAGES = {
    "en": {
        "usage": "Usage: python3 validate.py <output.html> [--lang en|zh]",
        "file_not_found": "ERROR: file not found: {path}",
        "unresolved_placeholder": "Unresolved placeholder {tok}",
        "div_imbalance": "<div> imbalance: {o} open vs {c} close",
        "bracket_braces": "braces", "bracket_parens": "parens", "bracket_brackets": "brackets",
        "js_imbalance": "JS {name} imbalance: {oc} '{o}' vs {cc} '{c}'",
        "emoji_found": "Emoji/pictograph glyphs found: {glyphs}",
        "forbidden_colors": "Forbidden purple/magenta colors: {hit}",
        "dead_selectors": "Possibly-dead CSS selectors (class in <style>, absent from HTML/JS): {dead}",
        "duration_mismatch": "Duration mismatch: DURATION={dur} but #time-label shows {lbl}s",
        "jsonld_duration": "JSON-LD duration PT{ld}S vs DURATION {dur}s (should round to match)",
        "no_duration": "No `const DURATION = <number>` found",
        "no_gsap": "GSAP library not referenced",
        "gsap_missing": "GSAP file missing on disk: {lib}",
        "no_jsonld": "Missing JSON-LD VideoObject block",
        "no_logo": "No logo <img> found",
        "logo_missing": "Logo file missing on disk: {lg}",
        "scenes_marks": "Scene registry has {scenes} scenes but MARKS has {marks} entries",
        "report_validating": "Validating: {path}",
        "warn_prefix": "  WARN  {w}",
        "error_prefix": "  ERROR {e}",
        "report_fail": "FAIL — {ne} error(s), {nw} warning(s)",
        "report_ok_warn": "OK (with {nw} warning(s) to review)",
        "report_ok": "OK — all checks passed",
    },
    "zh": {
        "usage": "用法：python3 validate.py <output.html> [--lang en|zh]",
        "file_not_found": "错误：文件不存在：{path}",
        "unresolved_placeholder": "未替换的占位符 {tok}",
        "div_imbalance": "<div> 标签不平衡：开标签 {o} 个 vs 闭标签 {c} 个",
        "bracket_braces": "花括号", "bracket_parens": "圆括号", "bracket_brackets": "方括号",
        "js_imbalance": "JS {name} 数量不平衡：'{o}' 有 {oc} 个，'{c}' 有 {cc} 个",
        "emoji_found": "发现 emoji/象形符号： {glyphs}",
        "forbidden_colors": "发现禁用的紫色/洋红色： {hit}",
        "dead_selectors": "疑似死 CSS 选择器（<style> 中有该类，但 HTML/JS 中不存在）： {dead}",
        "duration_mismatch": "时长不一致：DURATION={dur}，但 #time-label 显示 {lbl}s",
        "jsonld_duration": "JSON-LD 时长 PT{ld}S 与 DURATION {dur}s 不符（四舍五入后应一致）",
        "no_duration": "未找到 `const DURATION = <number>`",
        "no_gsap": "未引用 GSAP 库",
        "gsap_missing": "GSAP 库文件在磁盘上不存在：{lib}",
        "no_jsonld": "缺少 JSON-LD VideoObject 块",
        "no_logo": "未找到 logo <img>",
        "logo_missing": "logo 文件在磁盘上不存在：{lg}",
        "scenes_marks": "场景注册表有 {scenes} 个场景，但 MARKS 有 {marks} 项",
        "report_validating": "正在校验：{path}",
        "warn_prefix": "  警告  {w}",
        "error_prefix": "  错误  {e}",
        "report_fail": "未通过 FAIL — {ne} 个错误，{nw} 个警告",
        "report_ok_warn": "通过 OK（有 {nw} 个警告待复核）",
        "report_ok": "通过 OK — 全部检查通过",
    },
}

LANG = "en"


def t(key, **kw):
    tmpl = MESSAGES.get(LANG, MESSAGES["en"]).get(key) or MESSAGES["en"].get(key, key)
    return tmpl.format(**kw) if kw else tmpl


def detect_lang(argv):
    """Parse --lang and split out positional args; auto-detect from locale when unset."""
    lang, positional, i = None, [], 0
    while i < len(argv):
        a = argv[i]
        if a == "--lang" and i + 1 < len(argv):
            lang, i = argv[i + 1], i + 2
            continue
        if a.startswith("--lang="):
            lang, i = a.split("=", 1)[1], i + 1
            continue
        positional.append(a)
        i += 1
    if lang is None:
        env = (os.environ.get("PROMO_LANG") or os.environ.get("LC_ALL") or os.environ.get("LANG") or "").lower()
        lang = "zh" if env.startswith("zh") else "en"
    lang = str(lang).lower()[:2]
    return (lang if lang in ("en", "zh") else "en"), positional


# ---------------------------------------------------------------- constants
FORBIDDEN_COLORS = [
    "#722ED1", "#EB2F96", "#F472B6", "#A855F7",
    "#8B5CF6", "#D946EF", "#C026D3", "#9333EA", "#7C3AED",
]
# emoticons/pictographs, misc symbols + dingbats (incl. check/star), arrows, misc arrows, variation selector
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF\u2190-\u21FF\u2B00-\u2BFF\uFE0F\u2700-\u27BF\u24C2\u203C\u2049]"
)
# classes commonly toggled at runtime; never flag these as dead
STATE_WHITELIST = {
    "active", "on", "off", "show", "ready", "paused", "current", "visible",
    "hidden", "loaded", "dragging", "playing", "controls-force-show",
    "hide-cta", "animate", "done", "selected", "open", "closed",
}


# ---------------------------------------------------------------- helpers
def strip_comments(s):
    """Remove HTML and CSS/JS block comments (arrows/shorthand inside comments are not rendered content)."""
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    return s


def extract_main_script(src):
    """Return the JS of the last plain <script> block (app logic), not JSON-LD or src= tags."""
    blocks = re.findall(r"<script(?![^>]*\bsrc=)(?![^>]*ld\+json)[^>]*>(.*?)</script>", src, re.S)
    return blocks[-1] if blocks else ""


def css_selector_classes(src):
    """Collect every .class used in a <style> selector (the part before each '{')."""
    classes = set()
    for style in re.findall(r"<style[^>]*>(.*?)</style>", src, re.S):
        for selector in re.findall(r"([^{}]+)\{", style):
            if selector.strip().startswith("@"):   # at-rule prelude (media/keyframes name)
                selector = re.sub(r"@[^\s]+", "", selector)
            for m in re.findall(r"\.([A-Za-z_][\w-]*)", selector):
                classes.add(m)
    return classes


def html_and_js_classes(src, js):
    """Collect classes that actually exist: from class=\"...\", className=, classList.*, and JS selector strings."""
    known = set()
    for attr in re.findall(r'class="([^"]*)"', src):
        known.update(attr.split())
    for attr in re.findall(r"class='([^']*)'", src):
        known.update(attr.split())
    for m in re.findall(r"className\s*=\s*['\"]([^'\"]+)['\"]", js):
        known.update(m.split())
    for m in re.findall(r"classList\.(?:add|toggle|remove|contains)\(\s*['\"]([^'\"]+)['\"]", js):
        known.update(m.split())
    for m in re.findall(r"['\"]([^'\"]*)['\"]", js):
        for cls in re.findall(r"\.([A-Za-z_][\w-]*)", m):
            known.add(cls)
    return known


# ---------------------------------------------------------------- main
def main():
    global LANG
    LANG, positional = detect_lang(sys.argv[1:])
    if not positional:
        print(t("usage"))
        return 2
    path = positional[0]
    if not os.path.isfile(path):
        print(t("file_not_found", path=path))
        return 2
    src = open(path, encoding="utf-8").read()
    js = extract_main_script(src)
    errors, warnings = [], []

    # 1. unresolved placeholders
    for tok in sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", src))):
        errors.append(t("unresolved_placeholder", tok=tok))

    # 2. structure balance
    d_open, d_close = len(re.findall(r"<div\b", src)), len(re.findall(r"</div>", src))
    if d_open != d_close:
        errors.append(t("div_imbalance", o=d_open, c=d_close))
    for key, o, c in [("braces", "{", "}"), ("parens", "(", ")"), ("brackets", "[", "]")]:
        if js.count(o) != js.count(c):
            errors.append(t("js_imbalance", name=t("bracket_" + key), o=o, oc=js.count(o), c=c, cc=js.count(c)))

    # 3. emoji / pictographs in rendered content (comments stripped to avoid false positives)
    glyphs = sorted(set(EMOJI_RE.findall(strip_comments(src))))
    if glyphs:
        errors.append(t("emoji_found", glyphs=" ".join(glyphs)))

    # 4. forbidden colors
    upper = src.upper()
    hit = [c for c in FORBIDDEN_COLORS if c.upper() in upper]
    if hit:
        errors.append(t("forbidden_colors", hit=", ".join(hit)))

    # 5. dead CSS selectors
    css_classes = css_selector_classes(src)
    known = html_and_js_classes(src, js) | STATE_WHITELIST
    dead = sorted(css_classes - known)
    if dead:
        warnings.append(t("dead_selectors", dead=", ".join("." + d for d in dead)))

    # 6. timing consistency
    dur_m = re.search(r"const\s+DURATION\s*=\s*([0-9.]+)", js)
    if dur_m:
        dur = float(dur_m.group(1))
        lbl = re.search(r'id="time-label">[^<]*?/\s*([0-9.]+)s', src)
        if lbl and abs(float(lbl.group(1)) - dur) > 0.05:
            errors.append(t("duration_mismatch", dur=dur, lbl=lbl.group(1)))
        ld = re.search(r'"duration"\s*:\s*"PT([0-9]+)S"', src)
        if ld and abs(int(ld.group(1)) - round(dur)) > 1:
            warnings.append(t("jsonld_duration", ld=ld.group(1), dur=dur))
    else:
        warnings.append(t("no_duration"))

    # 7. GSAP present, and any local copy actually exists (mirrors the logo check)
    if not re.search(r"<script[^>]*src=[^>]*gsap", src) and "gsap.timeline" not in js:
        errors.append(t("no_gsap"))
    for lib in set(re.findall(r'<script[^>]*src="([^"]*gsap[^"]*)"', src, re.I)):
        if lib.startswith(("http://", "https://", "//")):
            continue
        lp = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(path)), lib))
        if not os.path.isfile(lp):
            errors.append(t("gsap_missing", lib=lib))

    # 8. JSON-LD VideoObject
    if '"@type": "VideoObject"' not in src and '"@type":"VideoObject"' not in src:
        errors.append(t("no_jsonld"))

    # 9. logo referenced + exists
    base = os.path.dirname(os.path.abspath(path))
    logos = re.findall(r'<img[^>]*src="([^"]*logo[^"]*)"', src, re.I)
    if not logos:
        warnings.append(t("no_logo"))
    else:
        for lg in set(logos):
            if lg.startswith(("http://", "https://", "//")):
                continue
            lp = os.path.normpath(os.path.join(base, lg))
            if not os.path.isfile(lp):
                errors.append(t("logo_missing", lg=lg))

    # 10. scenes vs marks
    scenes_n = len(re.findall(r"\{\s*id:\s*['\"]s\d+['\"]", js))
    marks_m = re.search(r"const\s+MARKS\s*=\s*\[([^\]]*)\]", js)
    if marks_m and scenes_n:
        marks_n = len([x for x in marks_m.group(1).split(",") if x.strip()])
        if marks_n != scenes_n:
            warnings.append(t("scenes_marks", scenes=scenes_n, marks=marks_n))

    # ---- report ----
    print("=" * 60)
    print(t("report_validating", path=path))
    print("=" * 60)
    for w in warnings:
        print(t("warn_prefix", w=w))
    for e in errors:
        print(t("error_prefix", e=e))
    print("-" * 60)
    if errors:
        print(t("report_fail", ne=len(errors), nw=len(warnings)))
        return 1
    if warnings:
        print(t("report_ok_warn", nw=len(warnings)))
        return 0
    print(t("report_ok"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
