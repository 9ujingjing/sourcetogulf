# SourceToGulf 社媒矩阵：从零搭建执行计划（Day-0 → 8 周）

> 适用前提：你目前**没有社媒账号、没有网络节点、没有发布工具**。本计划从物理基建开始，到起号、包装、发布、度量闭环。
> 配套文档（已就绪）：`social-media-seo-geo-playbook.md`（策略与帖子模板）、`social-posts-2026-08-24.md`（本周帖文）、`trend-radar.md`（热点选题）、`backlinks-plan.md`（反链）。
> 已有资产：站点 `sourcetogulf.com`、GA4（G-76L0Y9SC5D）、WhatsApp **+971 58 585 4194**、品牌规则（对外只叫 **SourceToGulf**，Papa Claw 仅法律实体）。

---

## 0. 一句话总览

**先搭节点 → 再起 5 个核心账号 → 统一包装 → 按 playbook 频率发 → 用 GA4 看哪个平台真带量 → 第 5 周加 X/Snapchat → 第 2 月扩 Reddit/Quora。**

不要买粉、不要同 IP 多开、不要各平台叫不同名（这三条直接毁 GEO 实体一致性）。

---

## 1. 网络与设备基建（最先做，否则账号起不来 / 易被封）

### 1.1 为什么必须先搞节点
- 国内直连 TikTok / Instagram / Snapchat 不可用，**必须有海外节点**。
- 更关键的是**账号防关联**：TikTok/IG 按「IP + 设备指纹 + 行为」判定多账号。同一 IP 或同一浏览器起多个账号，极易被关联限流甚至封号。所以「一人多号」必须做到**每号独立 IP + 独立指纹**。

### 1.2 节点方案（推荐）
| 项目 | 建议 | 说明 |
|---|---|---|
| 代理类型 | **住宅静态 IP（Residential Static）** | 比机房 IP 稳得多，封号率低；动态住宅每次换 IP 也不利于养号，优先**静态** |
| 地区 | 绑定目标市场：UAE / Dubai 或 MENA 池 | 账号「出生地」IP 最好就是你要做的市场，利于推给海湾用户 |
| 数量 | **每核心账号 1 个独立 IP**（5 个核心号 = 至少 5 条） | 后期 X/Snapchat 再加 |
| 服务商参考 | Bright Data / Oxylabs / 922S5 / IPRoyal 等，挑 **Gulf 覆盖好** 的 | 先买小量测试，别一次囤大 |
| 预算量级 | 住宅静态约 $X–XX / IP / 月（以实测报价为准） | 5 号起步约几百元/月级，远低于封号重来的成本 |

### 1.3 多账号浏览器（必装）
- 用 **AdsPower / MoreLogin / Dolphin** 类工具，每个账号开一个独立浏览器环境：独立 UA、时区（GMT+4）、语言（EN）、Canvas/WebGL 指纹、独立 Cookie。
- 这样 5 个账号在同一台电脑上互不关联。
- 一台**干净专机**（Windows 或 Mac）专门跑这个浏览器 + 代理；不要和日常上网混用。

### 1.4 设备与时区
- 桌面端：专机 + 多账号浏览器 + 代理。
- 手机端：**WhatsApp Business 用你已有的 +971 58 585 4194 实体号**（建议 eSIM/实体卡专机，别用双开）。
- 全环境时区设 **Gulf (GMT+4)**，语言 **English**。

---

## 2. 账号矩阵：开几个、先开哪几个

### 2.1 分三批开，不要一次铺满
| 批次 | 平台 | 数量 | 时间 | 理由 |
|---|---|---|---|---|
| **Phase 1（第 1–2 周）** | **TikTok、Instagram、Facebook(Page)、LinkedIn、WhatsApp Business** | **5 个** | 立即 | 最高杠杆：TikTok/IG 命中网红·小卖家人设；FB 可成第 2 大流量源；LinkedIn 做 B2B 可信度；WA 转暖线索 |
| Phase 2（第 3–4 周） | **X / Twitter、Snapchat(KSA)** | +2 | 首月内 | X 做新文放大；Snapchat 吃沙特 18–34 蓝海（渗透~90%） |
| Phase 3（第 2 月） | **Reddit、Quora** | 参与式 | 第 2 月 | **不建品牌号**，用创始人个人号/小号去「回答问题 + 自然带深链」，硬广会被删 |

> **结论：先从 5 个核心账号起步**（TikTok / IG / FB / LinkedIn / WA）。这是资源最省、覆盖最全的起点。X 和 Snapchat 第 2 阶段补，Reddit/Quora 只参与不建号。

### 2.2 团队分工（4 人 vibe 团队可直接套）
| 账号 | 负责人 | 内容供给 |
|---|---|---|
| TikTok + Instagram（短视频/Reels） | Antony（视频）+ Joyi（文案） | 工厂实拍、样品开箱、人设案例 |
| Facebook（Page + 群组）+ LinkedIn | Joyi | 指南分享、教育者文案 |
| WhatsApp Business 广播 | Robin | 暖线索直推链接 |
| X / Snapchat（Phase 2） | Joyi + Robin | 新文放大 / 阿语短片 |

---

## 3. 账号包装规范（统一实体，呼应 playbook §3）

### 3.1 命名（铁律）
- **Handle 全平台统一 `@sourcetogulf`**（小写无空格）。
- 现有 TikTok `@papaclawsourcetogulf` 是混合名 → **改名或重建为 `@sourcetogulf`**，并同步更新 `index.html` 的 `Organization.sameAs`。
- Display name：`SourceToGulf`（首字母大写）。
- **绝不在任何公开位置用 `Papa Claw` 当品牌名**（仅合同/发票等法律场景）。

### 3.2 Bio 模板（各平台同框架、换链接 UTM）
```
SourceToGulf — China→Gulf sourcing partner 🇨🇳→🇦🇪
Sourcing · samples · custom packaging · low-MOQ · door-to-door
🌐 sourcetogulf.com/?utm_source=<平台>&utm_medium=social
📱 WhatsApp +971 58 585 4194
```
- TikTok/IG 用短版（字符限制）；LinkedIn 可加 SABER/落地成本钩子；Snapchat 用阿语版。

### 3.3 视觉包装
- **头像**：全平台同一 logo（我可给你规范/出图方向；建议广州仓库实拍 + 简洁 wordmark）。
- **封面/横幅**：广州档口 / 样品质检 / 团队照，强化「真实在广州」的复合能力证据。
- **统一色调**：与站点一致（暖米 + 深绿/墨），别每平台换风格。

### 3.4 Link-in-bio 中枢（关键）
- 不要在 bio 只放首页。用 **Linktree 或站点 `/link` 页**做中枢，按来源带 UTM，把粉丝导到最相关的深页（指南/人设/计算器）。
- 中枢里至少挂：落地成本指南、沙特进口指南、4 个人设页、计算器。

---

## 4. 内容与发布节奏（直接引用 playbook）

- **频率表**（playbook §2）：TikTok 3–4/周、IG 3/周、LinkedIn 2/周、FB 2–3/周、Snapchat(KSA) 2–3/周、X 发新文当天必发、WA 按需。
- **月度排期**（playbook §4.5 的 4 周日历）：工厂探访 / 样品开箱 / SABER / 人设聚焦 / 创始人视角 轮换。
- **新文 48h 强制清单**（playbook §5）：每篇 How-to 上线，48h 内 X+FB+IG+Snapchat(KSA 相关)+LinkedIn+WA 全发。
- **帖子模板**（playbook §6 + `social-posts-2026-08-24.md`）：复制填空即可。
- **素材供给（瓶颈）**：Antony 需持续产出「工厂实拍 / 样品开箱 / 买家案例」短视频——这是 GEO 最看重的「真实世界证据」。

---

## 5. 工具清单

| 用途 | 工具 | 备注 |
|---|---|---|
| 多账号隔离 | AdsPower / MoreLogin / Dolphin | 每号独立指纹 |
| 海外节点 | 住宅静态代理（见 §1.2） | 每核心号 1 IP |
| 排期发布 | **Metricool** | 覆盖 TikTok/IG/FB/LinkedIn/X，自带 UTM + 分析，一套管全 |
| 设计 | Canva（Joyi） | Reels 封面、图文 |
| 视频 | 剪映 / CapCut（Antony） | 短视频，含阿语字幕版 |
| 链接中枢 | Linktree 或站点 /link 页 | 带 UTM 深链 |
| 分析 | GA4（已有）+ 平台原生 + `cite_monitor_queries.json` | 看 social 来源占比与 AI 引用率 |

---

## 6. 风险与红线

- ❌ **不买粉 / 不买转发**（playbook §7）：虚假互动不被 AI 当证据，反而稀释实体信号。
- ❌ **同 IP / 同浏览器多开**：必须用 §1 的隔离方案，否则关联封号。
- ❌ **各平台叫不同名**：统一 `SourceToGulf`，否则声量归不到同一实体。
- ⚠️ **内容本地化**：Snapchat / KSA 内容用阿语；其余英文为主（海湾商业通用语）。
- ⚠️ **合规表述**：SABER / 清关 / 关税类内容避免绝对化承诺，标注「以官方为准」。
- ⚠️ **养号期**：新号前 1–2 周先自然互动、少发硬广，权重起来再上频率。

---

## 7. 时间线（8 周）

| 周 | 动作 | 交付 |
|---|---|---|
| **W0** | 买节点 + 装多账号浏览器 + 专机设置；注册 5 个核心账号；按 §3 包装；搭 Link-in-bio 中枢；定 GA4 UTM 方案 | 5 个账号就位、包装一致、中枢上线 |
| **W1** | 养号（互动为主）；首发 3 条（TikTok 工厂实拍 + IG 样品 + LinkedIn 教育者）；加入 5 个海湾进口 FB 群组 | 起量、进群 |
| **W2–4** | 拉到 playbook 频率；任一篇新 How-to 走 48h 清单全平台发；Antony 建立素材周更 | 稳定节奏 |
| **W5–8** | 加 **X + Snapchat(KSA)**；启动 Reddit/Quora 参与；看 GA4 social 来源，加码真带量平台 | 矩阵完整 |
| **第 2 月+** | 反链执行（backlinks-plan.md）；每周一看 trend-radar 选下一篇 How-to；cite_monitor 周跑 | GEO 爬升 |

---

## 8. 我现在能帮你先备好的（无需账号也能做）

1. **账号包装填写表**（handle / display / bio / 头像规范 / 链接）—— 你注册时照填。
2. **Link-in-bio 中枢文案**（各平台 UTM 深链清单）。
3. **Day-0 注册检查清单**（节点→浏览器→注册→包装→首发）。
4. **持续出帖文包**（如 `social-posts-2026-08-24.md`，每周可续更）。
5. （可选）**头像 / 封面图规范 + 出图**——交设计流程。

## 9. 需要你拍板 / 执行的真动作

- [ ] 批节点 + 多账号浏览器预算（§1）。
- [ ] 改 TikTok 账号名为 `@sourcetogulf`（并同步 `index.html` sameAs）。
- [ ] 指定每账号负责人（§2.2）。
- [ ] 确认 Linktree 还是站点 `/link` 页做中枢。
- [ ] Antony 排期：工厂/样品素材周更。

> 底线：基建（节点+隔离）和「统一命名 + 不买粉」是成败前提；内容节奏 playbook 已齐，瓶颈在真实账号运营与素材供给，通常 2–6 周体现在 GSC 与 AI 引用率上。
