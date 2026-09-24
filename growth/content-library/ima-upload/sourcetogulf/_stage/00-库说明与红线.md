# 内容沉淀库（Content Library）

> 一句话：**把你每一次真实的业务动作（询盘 / 报价 / 打样 / 成交 / 失败）都丢进来，我定期扫一遍，提炼成网站与社媒内容。**
>
> 这是 SourceToGulf 的「一手素材真相源」。网站、社媒、案例所有内容都从这里长出来——不再是凭空编，而是从真实生意里提炼。

---

## 为什么需要它

你手里已有：30 天图文包、10 条 TikTok 脚本、trend-radar 周度热点、packaging 报价 Q&A。
但这些**真实业务事件**（Soga 怎么从散件变成礼盒、ZYVO 阿曼小店怎么要 gaming 配件）散落在 WhatsApp、分析文档、你脑子里。

没有统一沉淀 = 每写一篇都要重新回忆 + 重新找数据 + 容易泄露客户隐私。
有了沉淀库 = **丢一次，反复用；扫描一次，多平台出菜。**

---

## 怎么沉淀（两种姿势，越懒越用 A）

### 姿势 A — 零结构「收件箱」（最推荐，每天 30 秒）
打开 `inbox.md`，把今天发生的事**原样粘贴**即可，不用管格式：

```
## 9/24
- WA 来个沙特客户，要 Ramadan 礼盒，量 500，问 MOQ 和烫金
- 给 ZYVO 发了 gaming 报价，他嫌鼠标垫没货，我在找深圳货源
- 工厂寄了 Soga 的样品照，图在 /photos/soga-sample-01.jpg
```

我会（每周一扫）把这些**整理成结构化条目** + 自动出内容角度。你只管"倒"。

### 姿势 B — 结构化条目（要拿来写内容时）
复制 `_template.md` 到对应子目录（`customers/`、`inquiries/`、`quotes/`、`products/`），填 frontmatter。
frontmatter 是**给机器读的**，所以能被脚本扫描、能被自动化调用。

---

## 目录结构

```
content-library/
  README.md              # 本文件
  _template.md           # 结构化条目模板（复制它）
  inbox.md               # 零结构收件箱（每天倒真实动作）
  scan_library.py        # 扫库脚本：输出「内容机会表」
  customers/             # 真实客户案例（匿名）
  inquiries/             # 原始询盘（匿名）
  quotes/                # 报价记录（我们的利润模型）
  products/              # 产品 / 样品 / 实拍素材索引
  work-traces/           # 工作痕迹 / 策略演化 / 对话过程（方法论资产）
  insights/              # 扫描后提炼出的内容（输出区）
```

---

## 当前已沉淀（真实资产清单）

库现在共 **7 条**结构化条目，全部来自你真实业务（非编造）：

| 类型 | 条目 | 来源 |
|---|---|---|
| 客户案例 | Soga 迪拜香水礼盒 | WhatsApp 真询盘 |
| 客户案例 | ZYVO 阿曼 Gaming 店 | WhatsApp 真询盘 |
| 货盘 | 女式运动服混装货盘（26 OCT 批） | `/quote/activewear-pallet-26oct/` |
| 货盘 | 迪拜文具批量 | `/quote/stationery-dubai/` |
| 报价单 | 多 SKU 样品单（匿名 Joelle） | `/quote/joelle/` |
| 报价单 | 卡塔尔赛车模拟设备（匿名 Madani） | `/quote/madani/` |
| 报价单 | WA 混报（匿名号码） | `/quote/wa971564499568/` |

> 网站 `/quote/` 下所有报价/货盘页都带 `noindex`（内部给客户看，不进搜索引擎）。它们是**第一手素材金矿**——含真实 AED 价盘、MOQ、目标市场，但沉淀时客户名/号码一律匿名，公开内容只用脱敏角度。

扫描产出：`insights/2026-09-24-content-ideas.md`（23 条可写内容机会）。

> **工作痕迹（work-traces/）是另一类资产**：不止业务事件值得沉淀——你和我的**对话过程、策略演化、纠错记录**也是资产（见 `work-traces/content-engine-build-2026-09-24.md`）。它回答了"为什么这么做"，可被未来相似情境复用。任何一次有价值的对话结束前，把链接和关键结论倒进 `work-traces/` 即可（格式同 `_template.md`，`type: work-trace`）。这类条目 `status: reference`，不会挤占每周内容选题，但全量扫描时照样产出方法论角度（如"LinkedIn 发我们怎么建内容引擎"）。

---

## 红线（必须遵守）

1. **客户姓名 / 手机号 / 头像 / 账号永不上站**——案例用 `anon_name`（如 "Dubai boutique perfume brand"）。
2. **报价数字可留库内，公开内容一律匿名 + 区间化**（如 "landed AED 18–60/box"，不写具体客户成交价）。
3. **含酒精 / 认证门槛 / 危险品**的询盘要标注合规风险（见 `_template.md` 的 `compliance` 字段）。
4. **`/quote/` 下的 noindex 页面是内部资产**——可提炼脱敏角度，但原文、客户真名、手机号/WA 号不得直接复制发布到网站或社媒。

---

## 下一步

- 读法：`_distill-playbook.md` —— 扫描规则 + 提炼角度矩阵 + Soga 完整示例。
- 跑法：`python3 scan_library.py` —— 扫一遍库，输出本周可写的内容机会表。
- 自动化：已建「每周一扫描沉淀库 → 产出内容选题」的定时任务（见 `_distill-playbook.md` 末尾）。
