# 产品页改造方案：中国产业带 × 中东客户类型（2026-11-06）

> 决策来源：Robin — 「把产品变成中国各种各样的产业带介绍，信息量够、利于 GEO、避免列具体产品和报价；按客户类型分类是对的，但要符合中东市场；dropshipping 客户我们不接。」
> 状态：**方案稿，未上站**。产业带事实已用公开资料核对（义乌/深圳/佛山/中山/汕头/石狮等集群均有来源）。

## 一、核心结构

```
products.html（保留：能力样本 + 三条业务线）
   └─ 首屏加一个入口 → sourcing-belts.html（产业带 hub，主入口）
                          ├─ belts/shantou-chaoyang-sleepwear.html
                          ├─ belts/guangzhou-womenswear.html
                          ├─ belts/fujian-modest-activewear.html
                          ├─ belts/shenzhen-jewellery.html
                          ├─ belts/dongguan-packaging.html
                          ├─ belts/foshan-furniture.html
                          ├─ belts/zhongshan-lighting.html
                          └─ belts/shenzhen-electronics.html
```

**为什么不改 products.html 本体**：它是全站 header/footer 的真相源，改结构风险高；新建独立生成器 `build_belts.py` 产出 hub + 8 页，零风险，且能单独迭代。

**不做的事**：不列 SKU、不写价格、不写 MOQ 数字、不做 dropshipping 入口。

## 二、8 个产业带（先做这批，义乌作第 9 备选）

| # | 产业带 | 主营（对海湾） | 对应我们的真实资产 | 中东相关性 |
|---|---|---|---|---|
| 1 | **汕头 · 潮阳** | 内衣、睡衣、家居服（棉/莫代尔/冰丝/法兰绒） | 睡衣报价 2000+ 款、8 面料分类 | 高：尺码宽容、复购高、斋月礼盒 |
| 2 | **广州** | 快时尚女装、连衣裙、套装 | 女装套装 103 款、生活方式品牌案例 | 高：小单快反、社媒测款 |
| 3 | **福建 · 石狮 & 晋江** | **穆斯林服饰（长袍/abaya 面料）**、运动鞋服 | 运动服货盘、运动服 pallet 报价 | **极高：这条我们此前完全没打** |
| 4 | **深圳 · 水贝** | 时尚珠宝、银饰、培育钻 | 珠宝定制为主打之一 | 高：定制、礼赠、高客单 |
| 5 | **东莞 / 深圳** | 定制包装、印刷、礼盒 | 包装定制为主打之一、包装工坊实拍 | 高：私标必需、斋月/WF 礼盒 |
| 6 | **佛山 · 乐从** | 家具、酒店工程配套 | 可对接（需补供应链） | 高：酒店/别墅/工程单，客单大 |
| 7 | **中山 · 古镇** | 灯饰照明（工程灯、装饰灯） | 可对接（需补供应链） | 高：酒店/清真寺/商业空间 |
| 8 | **深圳 / 东莞** | 消费电子、安防设备、存储 | CCTV + 存储整合案例（六位数 AED） | 高：多型号整合 + 合规文件 |

> 义乌（节庆礼品、斋月装饰）留作第 9 个，等前 8 个跑出收录再补。

## 三、中东客户类型（6 类，明确排除 dropshipping）

| 客户类型 | 他们带来的 | 我们该给的 | 不该说的 |
|---|---|---|---|
| Social sellers / livestreamers | 图/链接、想小批测款 | 小批、可拍素材、私标 | 不承诺单件代发 |
| Boutiques & concept stores | 精选清单、包装要求 | 混款小单、礼盒包装 | 不报裸单价 |
| Wholesalers & distributors | 品类清单、目的地 | 混装拼柜、复购计划 | 不承诺最低价 |
| Brand founders | logo、产品概念 | 私标、打样、包装、认证 | 不接 1 件定制 |
| **Project & hospitality**（酒店/餐饮/诊所/工程） | 多型号设备清单 | 整合采购、合规文件、按项目交付 | 不接无认证路径品类 |
| Corporate & gifting | 预算、数量、节日 | 定制包装、批量、交期倒排 | 不接仿牌/品牌货 |

**明确写出的排除项（筛客用）**：dropshipping / 单件直发六国终端 / 纯比价询盘 / 仿牌与侵权品牌货。

## 四、样例页完整文案（汕头潮阳 · 睡衣）

> 这是可以直接用的成稿，其他 7 页照这个骨架写。

**URL**：`/belts/shantou-chaoyang-sleepwear.html`
**Title**：`Sleepwear & Loungewear Sourcing from Shantou Chaoyang, China | SourceToGulf`
**H1**：`Sleepwear and Loungewear from Shantou Chaoyang: A Gulf Buyer's Guide`

**答案箱（首段，AI 可直接引用）**：
> Chaoyang district in Shantou, Guangdong is one of China's major knitwear and intimate-apparel clusters. Gulf buyers source sleepwear, lounge sets and modest homewear here in small runs with private labels — combed cotton, modal, ice silk and fleece — with Arabic/English care labelling and SASO/SABER textile documentation prepared before shipment.

**区块 1 · 为什么是潮阳**
面料、织造、染整、成衣、包装集中在同一区域，所以小批量改款和补货的响应比分散采购快；同一批面料可以在几百件量级上完成打样到出货。

**区块 2 · 海湾买家在这里买什么**
- 夏季与全年：冰丝、莫代尔、薄棉（阿联酋、卡塔尔、阿曼全年；沙特内陆夏季更长）
- 冬季窗口（11–2 月）：法兰绒、摇粒绒、针织夹棉（沙特利雅得、约旦边境转口）
- 礼盒化：斋月与 White Friday 的成套礼盒（对应第 5 个产业带做包装）

**区块 3 · 合规与标签（最容易翻车的地方）**
- 沙特零售：SASO/SABER 纺织品要求，纤维成分、护理标识、原产国上标，**阿拉伯语标签**
- 阿联酋：儿童睡衣涉及阻燃安全，走 ECAS；成人常规睡衣按纺织品类目处理
- 通用做法：EN/AR 双语洗水标 + 成分标，出厂前完成

**区块 4 · 五个常见坑**
1. 克重虚标（写 180g 实际 150g）→ 要求留样封存
2. 色差（不同缸号）→ 同批同缸，分批发货要留色卡
3. 缩水率（棉质未预缩）→ 要求预缩处理并写进规格
4. 私标 MOQ 被低估（洗水标/吊牌/礼盒各有起订量）→ 三项分开确认
5. 交期倒排不足（斋月前 45 天必须上船）

**区块 5 · 我们不接什么**
不接 1 件定制、不接仿牌或侵权品牌货、不接无 GCC 海外仓前提下的单件直发、不接危险品。

**FAQ（FAQPage schema，6 条）**
1. What is Chaoyang known for? → knitwear, underwear and sleepwear cluster in Shantou, Guangdong.
2. Can I order a small test run? → Yes, factory MOQ applies per style; samples first.
3. Do you handle Arabic labels? → Yes, EN/AR care and composition labels prepared before shipment.
4. Is SABER required for sleepwear to Saudi Arabia? → Textile labelling and conformity requirements apply; we prepare the file set.
5. What fabrics suit Gulf summers? → ice silk, modal and light combed cotton; fleece for the short winter window.
6. Can you make gift boxes for Ramadan? → Yes, via our packaging cluster (link).

**内链**：`/services/product-sourcing-china.html`、`/services/quality-inspection-china.html`、`/services/custom-branding-packaging.html`、`/belts/dongguan-packaging.html`、`/services/sourcing-request.html`

## 五、hub 页结构（sourcing-belts.html）

1. H1：`Where Things Are Actually Made in China — Mapped for Gulf Buyers`
2. 答案箱：一句话（中国制造高度集中在少数集群；按集群采购比按品类搜索更准）
3. **6 类客户入口**（先认领身份）
4. **8 张产业带卡片**（城市 / 主营 / 适合谁 / 认证提示）
5. 明确排除项（dropshipping、单件直发、纯比价、仿牌）
6. 能力样本入口 → products.html
7. FAQ + `ItemList` + `FAQPage` schema

## 六、工程量与分步

| 步 | 内容 | 预估 |
|---|---|---|
| 1 | `build_belts.py` + hub + 2 个样板页（潮阳睡衣、广州女装） | 一次完成 |
| 2 | 剩余 6 页（同一数据表驱动） | 一次完成 |
| 3 | products.html 首屏加入口 + 导航/页脚登记 + sitemap/llms/RSS | 一次完成 |
| 4 | 阿语 hub（分页暂不做，观察收录） | 后续 |

**GEO 配套**：每页 `WebPage + FAQPage + BreadcrumbList`；hub 加 `ItemList`；sitemap/llms.txt/llms-full.txt 全登记；IndexNow + Bing 官方 API 推送。

## 七、红线核对

- 不写客户名、供应商/工厂名、1688 链接、价格、FOB 公式、MOQ 数字
- 不写最高级词（用 major / one of the clusters，不用 densest / largest）
- 产业带只写城市/区镇 + 公开集群事实，不编造"占全国 X%"
- 涉钱口径不动：$125 意向金、70% 先收、报价 1 周
