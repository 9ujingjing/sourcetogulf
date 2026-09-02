# 代码风险审计报告 — sourcetogulf.com

**审计日期**：2026-09-02
**范围**：16 个 Python 脚本、73 个 HTML 页面、139 个 SKU 数据源、部署流程
**方法**：静态代码分析 + 全站 HTML 逐页解析校验 + JSON-LD 解析验证 + git 仓库状态检查

---

## 摘要

| 级别 | 数量 | 说明 |
|---|---|---|
| 🔴 P0 | 3 | 会导致线上故障或 SEO 资产失效（其中 1 个已修复） |
| 🟠 P1 | 6 | 影响正确性/一致性，应尽快修 |
| 🟡 P2 | 3 | 技术债，可维护性 |
| ✅ 已排除 | 8 | 数据完整性、外链安全、死链等维度未发现问题 |

**最关键的一条**：4 个买家画像页（网红 / 宝妈 / 转售 / 小企业主 —— 正是我们核心客群）的 JSON-LD **全部解析失败、整块作废**。这 4 页的 WebPage + BreadcrumbList + FAQPage 结构化数据等于没有，直接影响富媒体搜索结果与 AI 引用候选。

---

## 🔴 P0 — 严重

### P0-1 ✅ 已修复：全站 header/footer 同步脚本只存在于 `/tmp`

**文件**：`/tmp/sync_header_footer.py`（不在 git 中）

**证据**：`build_flags.py:28` 注释引用该脚本；`git ls-files` 无此文件；全盘仅命中 `/tmp/sync_header_footer.py`（2190 B，Aug 31 17:13）。

**风险**：macOS 重启即清空 `/tmp`。该脚本一旦丢失，73 页中**非生成器产出的手工页**（`index.html`、`about.html`、`services/*`、`shipping/*` 等 30+ 页）将永久失去 header/footer 同步能力，且代码无法恢复。这是全站模板分发链路的**单点故障、不可逆**。

**已做**：已 `cp` 到仓库根目录并推送（commit 已 push，不影响线上页面内容）。同时补全 `.gitignore`（原仅 2 行），移除已误入库的 `__pycache__/*.pyc`。

**后续**：应在 `deploy.sh` 中固化调用（见 P1-1）。

---

### P0-2：4 个画像页 JSON-LD 语法非法，整块被丢弃

**文件**：`build_personas.py:349`

**证据**：
```python
json_ld = json.dumps(ld, ensure_ascii=False) + "\n" + faq_jsonld(p['faq'])
# 两个独立 JSON 对象用换行拼进同一个 <script type="application/ld+json">
```

**实测校验结果**：
```
for-influencers.html       块:1 解析OK:0 失败:1 → Extra data: line 3 column 1
for-moms.html              块:1 解析OK:0 失败:1 → Extra data: line 3 column 1
for-resellers.html         块:1 解析OK:0 失败:1 → Extra data: line 3 column 1
for-small-businesses.html  块:1 解析OK:0 失败:1 → Extra data: line 3 column 1
uae-import-guide.html      块:1 解析OK:1  ← 对照组正常
```

**根因对比**：`build_guides.py:984` 与 `build_compare.py:537` 用的是**数组**写法 `json.dumps([wp, faq_jsonld(...)])`，只有 `build_personas.py` 用了换行拼接。

**风险**：4 个核心客群落地页的 WebPage + BreadcrumbList + FAQPage 结构化数据**全部作废**。上周刚做完这 4 页的 title 优化，但结构化数据这一层一直是坏的 —— 富媒体结果、AI 引用候选全部归零。

**修复**：改为数组写法，与 `build_guides.py` 对齐：
```python
faq = json.loads(faq_jsonld(p['faq']))
faq.pop('@context', None)
json_ld = json.dumps([ld, faq], ensure_ascii=False, indent=2)
```

---

### P0-3：`fix_warn.py` 是定时炸弹

**文件**：`fix_warn.py:53` + `fix_warn.py:89-90`

**证据 1 — TITLE_MAP 残留危险旧值**（上次批量替换时未命中）：
```python
"shipping/china-to-uae.html": "Shipping from China to UAE: Door to Door",
```
注意同批其他 5 个 shipping 页都已更新为新值，**只有 uae 这条漏了**（因为生成 old key 时用了 `.title()`，把 `uae` 变成 `Uae`，匹配失败）。

**证据 2 — 只校验长度，不校验品牌名与禁用词**：
```python
if len(new) > 70:
    raise SystemExit("TITLE TOO LONG (%d): %s -> %s" % (len(new), rel, new))
```

**风险**：任何人执行 `python3 fix_warn.py`，UAE 页 title 会从 `China to UAE Sourcing & Route Guide: Timing, Customs | SourceToGulf` 变成 `Shipping from China to UAE: Door to Door` —— **丢品牌后缀 + 同时命中 `Shipping`、`Door to Door` 两个禁用词**，一夜退回"被当成货运公司"。另外 `saudi-arabia` 那条新值是 71 字符，会触发 `SystemExit` 中断整个脚本。

**修复**（二选一）：
1. 直接删除 `TITLE_MAP` 中 6 条 `shipping/*`（页面已由手工维护，不需要脚本管）
2. 保留但加断言：
```python
assert 'SourceToGulf' in new, f"缺品牌后缀: {rel}"
assert not re.search(r'Import|Landed|Shipping|Delivery|Days|Cargo|Door to Door', new, re.I), f"含禁用物流词: {rel}"
```

**建议**：这个脚本的历史使命已完成（title 已在 9/2 全站重构完毕），**直接删掉最省事**。

---

## 🟠 P1 — 重要

### P1-1：`deploy.sh` 只做 git push，完全不含构建步骤

**文件**：`deploy.sh:48-50`

**证据**：核心仅 `git add -A` → `git commit` → `git push`；仓库内**无 Makefile / build.sh / .github 工作流**。

**风险**：改了 `products.clean.json` 却忘记跑 `build_products.py`，或跑了生成器忘记 `sync_header_footer.py`（今天我就漏过一次，导致徽章 HTML 上线但 CSS 没上线）—— 都不会有任何提示，直接推上线，**线上与数据源静默不一致**。

**修复**：在 `git add` 前插入构建段：
```bash
python3 build_products.py && python3 build_cat_products.py && \
python3 build_guides.py && python3 build_personas.py && \
python3 build_compare.py && python3 build_blog.py && \
python3 build_solutions.py && python3 build_answers.py && \
python3 build_partners.py && python3 build_arabic.py && \
python3 build_flags.py && python3 build_rss.py && \
python3 sync_header_footer.py
```

---

### P1-2：`deploy.sh watch` 模式会把编辑中的半成品自动推上线

**文件**：`deploy.sh:15-36`

**证据**：
```bash
while true; do
  CHANGED=$(git status --porcelain | ...)
  if [ -n "$CHANGED" ]; then
    sleep 30
    if [ -n "$(git status --porcelain | ...)" ]; then
      git add -A; git commit ...; git push ...
```

**风险**：只要检测到改动 + 30 秒内无**新**改动就推送。如果你正在编辑一个大文件（比如 `build_arabic.py` 写了 20 分钟没保存，或保存了但还在改下一个文件），它会在中途自动提交半成品并 push 到生产环境。GitHub Pages 1-2 分钟即生效，**外网可见**。

**修复**：watch 模式改为只提交不推送（`git commit` 后等人工 `git push`），或加 `--draft` 开关。

---

### P1-3：单一真相源 `products.html` 非原子写，构建中断会瘫痪全站

**文件**：`build_products.py:197` + `tpl_common.py:39-43`

**证据**：
```python
with open(os.path.join(APP, 'products.html'), 'w', encoding='utf-8') as f:
    f.write(html)      # 'w' 打开即截断
```
```python
STYLE = re.search(r'<style[\s\S]*?</style>', src).group(1)   # 导入期无保护
```

**风险**：`products.html` 既是 `tpl_common` 的**输入**（抽取 style/header/footer）又是 `build_products.py` 的**输出**。若构建中途抛异常（如 JSON 新增字段缺失导致 `KeyError`），文件已被截断为 0 字节 → 此后**任何 builder 在 `import tpl_common` 时立刻崩溃**，全站构建能力归零，只能 `git checkout` 恢复。

**修复**：
1. 原子写：先写 `.tmp` 再 `os.replace()`
2. `tpl_common.py` 加保护：
```python
m = re.search(r'<style[\s\S]*?</style>', src)
if not m:
    raise SystemExit('products.html 结构损坏，请执行 git checkout products.html 恢复')
STYLE = m.group(1)
```

---

### P1-4：landed 价格公式三处重复实现

**文件**：`tpl_common.py:45-52`（Python 权威版）、`gen_product_schema.js:14-17`、`index.html:859`（内联）

**证据**：三处各自硬编码：
```javascript
const cny = (kg <= 0.5) ? 68 : 68 + (kg - 0.5) * 45.6;
return cny / CNY_TO_USD;   // CNY_TO_USD = 7.15
```

**风险**：汇率或菜鸟报价调整时只改一处 → 产品卡价格、JSON-LD 里的 `price`、首页计算器三者给出**互相矛盾的数字**。JSON-LD 价格与页面可见价格不一致，会被 Google 判为**结构化数据作弊**（可能导致富媒体结果被停用）。

**修复**：单一常量源 `fx_rates.json`；Python 读该文件，JS 侧由构建期注入常量或 `fetch()`。

---

### P1-5：25 个页面 meta description 含禁用物流词

**文件**：`shipping/china-to-*.html`（6 个）、`categories.html`、`google-ads/*.html` 等共 25 页

**证据**：
```
shipping/china-to-uae.html:6
content="China to UAE shipping: air 5–8 days, sea 18–25 days. Duty 5%... freight + customs + delivery."
categories.html: "...with landed prices to the Gulf"
```

**风险**：title 层面已清零，但 description 层面还没清。这 6 个 shipping 页在 SERP 摘要里呈现为**纯货运公司文案**，与 "not a freight forwarder" 定位直接冲突。

**修复**：批量改写（正文保留原表述不受影响，规范只约束 title 与 description）。

---

### P1-6：`fix_warn.py` 注入的 JSON-LD 被生成器静默覆盖

**文件**：`fix_warn.py:69-81` vs `build_cat_products.py:265`、`build_ads.py:95`

**证据**：`fix_warn.py` 的 `SCHEMA_PAGES` 为这 4 页注入 WebPage schema，但两个生成器每次运行都会覆写这些页面。实测当前**这 4 页无任何 JSON-LD**：
- `categories.html`
- `google-ads/hijab-jewelry.html`
- `google-ads/phone-accessories.html`
- `google-ads/ramadan.html`

**风险**：形成"修了又丢"的循环，一次性补丁与生成器无先后保证。

**修复**：把 WebPage schema 直接写进 `build_cat_products.py` / `build_ads.py` 的 `page_shell(json_ld=...)` 参数，删掉 `fix_warn.py` 的 `SCHEMA_PAGES` 逻辑。

---

## 🟡 P2 — 技术债

### P2-1：`ssr_products.py` 已成孤儿脚本但文档仍诱导执行
**文件**：`ssr_products.py:1-13`
docstring 称「Run after any change to products.clean.json」，但 `products-data.js` 已不存在（全站 0 处引用），`build_products.py:9` 已改为直接 SSR。执行会撞上 `:61` 的 `SystemExit`（幸好在写文件前退出，未造成破坏）但会误判为构建失败。
**修复**：删除或标注 DEPRECATED。

### P2-2：两套 RSS 生成器并存，`feed.xml` 是陈旧死文件
**文件**：`gen_feed.py`（→ `feed.xml`，Aug 21，11938 B）vs `build_rss.py`（→ `rss.xml`，Sep 2，23058 B）
`tpl_common.py:112` 的 `RSS_LINK` 只指向 `/rss.xml`；`robots.txt` 未声明任何 feed。`feed.xml` 收录 12 天前的旧内容却仍可被抓取，形成内容新鲜度噪声。
**修复**：删除 `gen_feed.py` 与 `feed.xml`。

### P2-3：未使用导入 + 13 个阿语 title 超长
- `build_ads.py:1`（`json`、`FOOTER`、`HEADER` 未用）、`build_cat_products.py:1`（`FOOTER`、`HEADER` 未用）、`build_guides.py:1`（`WA` 未用）
- 13 个阿语页 title 为 89–127 字符（`ar/products.html` 121、`ar/for-moms.html` 120），远超 70 字符上限，SERP 中会被截断

---

## ✅ 已检查但未发现问题的维度

| 维度 | 结论 |
|---|---|
| **SKU 数据字段完整性** | 139 个产品的 `cat/name_en/name_ar/img/fob_cny/weight_kg/moq/lead_days/hot` **9 个字段 139/139 齐全**，`name_ar` 零缺失 → 无 KeyError 崩溃点 |
| **图片死链** | 139 个 `p['img']` 路径**全部对应真实文件**，0 死链 |
| **canonical / hreflang** | 73 页全部具备正确 canonical；`hreflang="en"` 与 `x-default` 各 73 条、`ar` 26 条；所有 `ar` 目标文件均存在；13 个阿语页全部具备回链，配对完整 |
| **sitemap / llms.txt** | 74 条 URL 逐一映射到磁盘，**0 条 404** |
| **外链安全** | 全站 960 处 `target="_blank"`，**100% 带 `rel="noopener"`**，0 处漏加 |
| **用户输入注入** | WhatsApp 链接经 `wa_link()` 的 `urllib.parse.quote` 转义，产品名中的 `&`、引号不会破坏属性边界 |
| **硬编码路径** | 所有生成器均用 `APP = os.path.dirname(os.path.abspath(__file__))`，`.py` 中 0 处 `/Users/` 硬编码 |
| **密钥泄露** | `submit_indexnow.py:13` 的 key 与同名 `.txt` 是 IndexNow **协议要求公开**的验证文件，非泄露；除此之外无 API key / token / password |
| **GA4 重复注入** | 73 页的 `gtag/js` 与 `gtag('config')` 均**恰好 1 次**，`dedupe_ga4()` 生效 |
| **阿语 SSR** | 13 个 `/ar/` 页原始 HTML 含 4,562–23,388 个阿语字符，确为服务端渲染 |

---

## 建议处理顺序

1. **P0-2**（改 1 行，挽回 4 页结构化数据）— 5 分钟
2. **P0-3**（删除 `fix_warn.py` 或加断言）— 5 分钟
3. **P1-1**（deploy.sh 加构建段）— 15 分钟，一劳永逸防"忘记跑生成器"
4. **P1-2**（watch 模式改为不自动 push）— 5 分钟
5. **P1-5**（批量清 25 个 description 物流词）— 20 分钟
6. 其余按空闲排期

**注意**：P0-2 与 P1-5 的修复需要重新生成 + 部署。如果担心"频繁改动重置抓取节奏"，可以攒一批一起改 —— 但 P0-2 涉及 4 个核心客群页的结构化数据，**建议优先修**。
