# 扫描 → 提炼方法论（Distill Playbook）

> 目的：**把沉淀库里的真实业务，变成网站 + 社媒的高转化内容。**
> 核心认知：你不缺"写什么"的创意，你缺的是**把真实生意系统化提炼成内容**的管道。
> 这套管道 = `inbox 倒料` → `结构化条目` → `脚本扫库` → `5 平台出菜`。

---

## 一、扫描规则（谁进内容池）

| 条目状态 | 是否进内容池 | 说明 |
|---|---|---|
| `sample` / `quoted` / `negotiating` / `lead` | ✅ 优先 | 进行中、有故事、可匿名 |
| `won` | ✅ 最佳 | 已成交，可做成完整案例 |
| `lost` | ⚠️ 谨慎 | 只提炼"踩坑教训"，不点名 |
| `anon_ok: false` | 🔒 仅内部 | 不进公开内容，只做策略参考 |

扫描命令：
```bash
python3 scan_library.py --week --markdown > insights/$(date +%Y-%m-%d)-content-ideas.md
```

---

## 二、提炼角度矩阵（一条真实事件 → 5 处内容）

任何一条沉淀条目，都能按下面矩阵拆成多平台内容。**同一素材，五处改写**（复用你已有的 30 天包逻辑）。

| 平台 | 角色 | 从这字段取料 | 形式 |
|---|---|---|---|
| **LinkedIn** | 找人/立专家 | `pain_points` + `our_value` | 观点长文（"为什么 UAE 小品牌需要一个包装系统，不是一只盒子"） |
| **Instagram** | 建信任 | `media` + `product` | 图文卡 / Reels（工厂实拍、样品细节） |
| **TikTok** | 破圈引流 | `content_angles` 里最有画面感的 1 条 | 15–40s 竖版（"一个迪拜香水品牌的礼盒诞生记"） |
| **网站 Blog/FAQ** | 接 AI 引用 | `pain_points` + 行业 Q&A | How-to / FAQ（GEO 弹药） |
| **WhatsApp 目录** | 成交落地 | `product` + `moq` + `landed_aed` | 目录项 + 私信话术 |

**铁律（来自品牌红线）：**
- 真实感 > 精致感：用工厂实拍 / 样品照，不画概念图。
- 不写 superlative（best/leading/#1），Walmart 奖例外。
- 客户一律匿名，报价一律区间化。

---

## 三、完整示例：SOGA 香水盒 → 4 平台内容

**原料**（来自 `customers/soga-perfume-box.md`）：
> 迪拜小香水品牌，卖散件没包装体系，想"out of the box"做差异化；我们给了 3 个盒型概念（Discovery / Velvet Octagon / Modest Set），MOQ 200–500，7 天出样。

| 平台 | 标题 / 角度 | 取料字段 |
|---|---|---|
| LinkedIn | 《为什么迪拜小香水品牌需要的不是一只盒子，而是一套包装系统》 | pain_points + our_value |
| IG Carousel | 6 图：散件 vs 3 盒型对比 + 烫金细节实拍 | product + media |
| TikTok | "一个迪拜 boutique 的礼盒诞生记：从散装香水到丝绒八角盒"（15s） | content_angles[0] |
| 网站 FAQ | "Why does a Gulf perfume brand need a packaging system, not just a box?"（GEO） | pain_points |
| WhatsApp | 目录项：Perfume Gift Box MOQ 200 · landed AED 18–60/box | product + moq + landed_aed |

→ 这一条真实案例，喂饱一周内容，且**每条都来自真实生意，不是编的**。

---

## 四、闭环节奏（建议你照这个跑）

1. **每天**：真实动作倒进 `inbox.md`（30 秒）。
2. **每周一**：我（或自动化）扫 `inbox` → 整理成结构化条目 → 跑 `scan_library.py --week` → 产出本周内容选题表，存 `insights/`。
3. **你挑 1–2 条** → 按矩阵拆成 5 平台草稿（复用 30 天包 / 10 条脚本模板）。
4. **发布**：TikTok 你拍剪 → 同步 IG Reels + FB → WhatsApp 收口。

---

## 五、已配置的自动化

已用 `automation_update` 建了**每周一 10:00** 的定时任务：
- 名称：`扫描内容沉淀库 → 产出本周内容选题`
- 动作：读 `content-library/inbox.md` + 各子目录条目 → 整理结构化 → 跑扫描 → 生成 `insights/YYYY-MM-DD-content-ideas.md` 选题表，并给出"本周建议写哪 1–2 条"。
- 这样"沉淀 → 扫描 → 提炼"自动转起来，你只负责倒料 + 挑写。
