# SEO/GEO 审计报告 — sourcetogulf.com（2026-09-07）

> 扫描 62 个 HTML 页（47 英文 + 14 阿语 + index）+ 基础设施文件。结论：**基础设施和结构化数据很扎实，最大短板是社交分享标签完全缺失（直伤 WhatsApp 主获客通道）**。

---

## ✅ 做得好的（别动）

| 项 | 状态 |
|---|---|
| sitemap.xml | 77 条 URL ✅ |
| robots.txt | **明确放行 GPTBot/ClaudeBot/PerplexityBot/OAI-SearchBot** — GEO 最佳实践（很多站还屏蔽 AI 爬虫） |
| llms.txt / llms-full.txt | 13.5KB + 10.7KB ✅ |
| rss.xml | 23KB ✅（feed.xml 是死文件，可删，属已知 P2） |
| title / meta description / canonical / H1 | **62 页全有，零缺失，每页正好 1 个 H1** |
| JSON-LD 结构化数据 | **极丰富**：351 条 FAQ Q&A、278 个 Product（带 Offer/Shipping/Return）、57 个 FAQPage、59 Organization、16 Article、8 BreadcrumbList |
| 内容深度 | 无薄内容页（<200 词 = 0 个） |
| 阿语 SSR | 14 页 + hreflang 双向（13 个英文页回指阿语版） |

---

## ❌ 优化空间（按优先级）

### 🔴 P0 — Open Graph / Twitter Card 标签全站缺失（最大缺口）
- **62 页一个 og: 标签都没有**（og:title / og:description / og:image / og:url 全缺），twitter:card 也没有
- **影响**：任何人在 **WhatsApp / Facebook / LinkedIn / iMessage** 分享 sourcetogulf.com 链接时，**没有预览图、没有标题卡，只有裸 URL**
- **为什么最痛**：WhatsApp 是你已验证的 #1 获客通道（AI 引荐来的客户都走 WA）。链接没预览 = 点击率掉一大截
- **修法**：在 `tpl_common.page_shell()` 里加 og:title/og:description/og:image/og:url/twitter:card 输出 → 重跑全部 `build_*.py` → `sync_header_footer.py` 同步手工页 → 需要一张默认社交分享图（1200×630，放 `images/og-default.jpg`）
- **工作量**：中等（改模板 + 1 张图 + 重跑生成器）

### 🟠 P1 — Title 过长被 Google 截断（39/61 页）
- 英文页 29/47、阿语页 10/14 的 title 超过 60 字符
- Google SERP 约 60 字符后截断，AI 引擎抓取也受影响
- **修法**：英文页在各自 `build_*.py` / 手工页源码里精简 title；阿语页在 `build_arabic.py` 的数据源里缩标题（已知"14 个阿语 title 89-127 字符"问题）

### 🟠 P1 — Meta description 过长（31 页 >160 字符）
- 同样被截断，影响 SERP 点击率
- **修法**：同上，在生成器数据源里精简

### 🟡 P2 — 阿语 SSR 覆盖薄（GEO 蓝海未充分利用）
- 只有 14 个阿语页，对应 ~62 个英文页里的一小部分
- **记忆里的判断**：阿语侧政府源占 AI 引用 68% 但内容生硬、不讲"怎么操作/花多少/多久/小批量起步"——那正是我们的差异化缺口
- **机会**：把 `blog/how-to-import-from-china-to-*`（6 篇国别指南）+ 关键 category 页翻成阿语 SSR，能显著扩大 AI 在阿语查询里的引用面
- **铁律**：必须走 `build_arabic.py`（加 `COUNTRY_DATA`/内容条目），不能手改 HTML；新增后必扫 U+FFFD 乱码

### 🟡 P2 — hreflang=ar 反向链接只 13 个
- 与 P2 阿语覆盖绑定：阿语页扩多少，反向 hreflang 就加多少（英文页由 `page_shell(alt_ar=...)` 输出）
- 单独修没意义，随阿语扩展一起做

---

## 没列但值得将来查的

- **E-E-A-T / 作者信号**：blog 文章没有 author 标记。Robin"14 年迪拜"是强信任资产，可在 blog 加 `Person` + author bio，强化 AI 引用可信度
- **内链结构**：未审计内链锚文本分布（可后续跑一个）
- **Core Web Vitals**：图片刚批量压小（10 张打码后体积降 50-70%），LCP 应有改善；可用 PageSpeed Insights 实测
- **外链**：Crunchbase ✅ / Clutch 审核中 / Bayt 待查——按记忆既定外链策略推进

---

## 建议执行顺序

1. **先做 P0（og 标签）** — 投入产出比最高，直接喂主获客通道，1-2 小时可上线
2. 再做 P1（title/desc 精简）— 生成器源数据改，批量
3. P2 阿语扩展 — 内容活，按周排
