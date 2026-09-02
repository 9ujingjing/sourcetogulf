# WhatsApp Business 目录配置（SourceToGulf）

> 2026-09-01。核心原则：**这是"能力展示 + 服务清单"，不是商品价目表。**
> 经核实：WhatsApp 目录的**价格字段为可选**（官方允许 variable pricing 时留空）；目录**支持"服务"条目**不止实体商品；单账号上限 **500 条**；**原产国为必填**。

---

## 0. 三条铁律（先看这个）

1. **价格一律留空。** 你是帮客户找货的，价格随数量/工厂/包装/季节浮动。写死价格 = 要么报错要么亏钱。留空后客户会直接发消息问，正好进入你的咨询流程。
2. **原产国填 China**（必填字段）。
3. **图片必须用你自己的实拍**。网图会被 Meta 审核驳回，而且一眼假。

⚠️ **不要在描述里写 "价格面议 / Price on request"**——这类模糊表述在 Meta 侧可能被判定为诱导行为。用「告诉你需求，我们发方案」的自然说法代替。

---

## 1. 建两个 Collection（合集）

| 合集名 | 放什么 | 作用 |
|---|---|---|
| **How We Work** | 下面 S1–S5 五条服务 | 讲清你能为客户做什么 |
| **What We Source** | 下面 C1–C9 九个品类 | 证明你能找到什么货 |

客户点进目录先看到两个合集，比看到一堆零散商品清楚得多。

---

## 2. 服务类条目 5 条（合集：How We Work）

> 每条：价格留空 · 原产国 China · 链接带 UTM

### S1 · Product Sourcing
**名称**：`Product Sourcing from China`
**描述**：
```
Send us a photo, a link, or just an idea — we find the factory that actually makes it. You get 2–3 matched suppliers with photos and specs, so you compare before you commit. Works for small runs, not just containers.
```
**链接**：`https://sourcetogulf.com/?utm_source=whatsapp&utm_medium=catalog&utm_campaign=svc-sourcing`
**代码**：`STG-SVC-01`
**配图**：广州市场/工厂实拍（有人在场）

### S2 · Sample Box
**名称**：`Sample Box — Test Before You Commit`
**描述**：
```
Order 1–3 physical samples before placing a real order. We check them, photograph them, and ship them to your door anywhere in the GCC. Most buyers test 20–50 units first — that is how you avoid a bad batch.
```
**链接**：`https://sourcetogulf.com/?utm_source=whatsapp&utm_medium=catalog&utm_campaign=svc-sample`
**代码**：`STG-SVC-02`
**配图**：贴好标签的样品箱

### S3 · Private-Label Packaging
**名称**：`Private-Label Packaging`
**描述**：
```
Your name and logo on the box, pouch or label. Low minimums — many suppliers start at 100–300 units of custom packaging. We handle the artwork check, material choice and a photo proof before production starts.
```
**链接**：`https://sourcetogulf.com/?utm_source=whatsapp&utm_medium=catalog&utm_campaign=svc-label`
**代码**：`STG-SVC-03`
**配图**：带客户 logo 的包装盒特写

### S4 · Video QC
**名称**：`Video QC Before Shipping`
**描述**：
```
We film your goods at the factory before anything ships: stitching, finish, function, quantity, packing. You see the real product, not a staged photo. No video, no shipment.
```
**链接**：`https://sourcetogulf.com/?utm_source=whatsapp&utm_medium=catalog&utm_campaign=svc-qc`
**代码**：`STG-SVC-04`
**配图**：验货近景（手在检查商品）

### S5 · Consolidation & Shipping
**名称**：`Consolidation & Shipping to GCC`
**描述**：
```
We collect from multiple suppliers across Guangzhou, Yiwu and Foshan, pack them into one shipment and handle the paperwork. Fewer boxes, one tracking number, less customs friction.
```
**链接**：`https://sourcetogulf.com/?utm_source=whatsapp&utm_medium=catalog&utm_campaign=svc-ship`
**代码**：`STG-SVC-05`
**配图**：装柜/封箱现场

---

## 3. 品类展示 9 条（合集：What We Source）

> 全部对应站内**真实存在且已上线（HTTP 200）**的分类页，不虚构品类。

### C1 · Phone & Car Accessories
**名称**：`Phone & Car Accessories`
**描述**：
```
Mounts, chargers, cables, earbuds and car organisers, sourced in Guangzhou. Built for Gulf heat — we test grip, hinges and charging under load before recommending. Low minimums for trial runs.
```
**链接**：`https://sourcetogulf.com/category-tech.html?utm_source=whatsapp&utm_medium=catalog&utm_campaign=cat-tech`
**代码**：`STG-CAT-01`

### C2 · Home & Kitchen
**名称**：`Home & Kitchen`
**描述**：
```
Small appliances, organisers and kitchen tools that ship easily and don't need heavy certification. Good margins and steady repeat orders for home and gift shops across the GCC.
```
**链接**：`https://sourcetogulf.com/category-home.html?utm_source=whatsapp&utm_medium=catalog&utm_campaign=cat-home`
**代码**：`STG-CAT-02`

### C3 · Modest & Plus-Size Fashion
**名称**：`Modest & Plus-Size Fashion`
**描述**：
```
Abayas, kaftans and everyday modest wear from workshops that accept low minimums. We send fabric swatches on video first, so you can check weight and colour before ordering.
```
**链接**：`https://sourcetogulf.com/category-modest-fashion.html?utm_source=whatsapp&utm_medium=catalog&utm_campaign=cat-modest`
**代码**：`STG-CAT-03`

### C4 · Hijab Accessories & Fashion Jewelry
**名称**：`Hijab Accessories & Fashion Jewelry`
**描述**：
```
Scarves, pins and costume jewelry, with your own label available. We check plating thickness, clasps and finishing so the pieces last. Fashion jewelry only — we do not handle fine gold.
```
**链接**：`https://sourcetogulf.com/category-fashion.html?utm_source=whatsapp&utm_medium=catalog&utm_campaign=cat-fashion`
**代码**：`STG-CAT-04`

### C5 · Beauty Tools
**名称**：`Beauty Tools & Accessories`
**描述**：
```
Brushes, LED mirrors, organisers and nail kits. Tools rather than creams — they ship easily and avoid product registration. Strong sellers for home-based beauty businesses.
```
**链接**：`https://sourcetogulf.com/category-beauty-toys.html?utm_source=whatsapp&utm_medium=catalog&utm_campaign=cat-beauty`
**代码**：`STG-CAT-05`

### C6 · Home Fragrance & Diffusers
**名称**：`Home Fragrance & Diffusers`
**描述**：
```
Bakhoor burners, diffusers and home scent sets. Popular as gifts across the Gulf, especially around Ramadan and Eid. Custom packaging available from low quantities.
```
**链接**：`https://sourcetogulf.com/category-home-fragrance.html?utm_source=whatsapp&utm_medium=catalog&utm_campaign=cat-fragrance`
**代码**：`STG-CAT-06`

### C7 · Comfort Essentials
**名称**：`Comfort Essentials`
**描述**：
```
Everyday comfort basics in extended sizes, sourced from factories that actually stock them. We check fabric stretch and finishing, and send size sets before bulk production.
```
**链接**：`https://sourcetogulf.com/category-lingerie.html?utm_source=whatsapp&utm_medium=catalog&utm_campaign=cat-comfort`
**代码**：`STG-CAT-07`

### C8 · Ramadan & Eid Seasonal
**名称**：`Ramadan & Eid Seasonal`
**描述**：
```
Seasonal gifts, décor and packaging for the two biggest retail moments in the Gulf. We help you plan two months ahead, so stock lands before the rush instead of during it.
```
**链接**：`https://sourcetogulf.com/category-seasonal.html?utm_source=whatsapp&utm_medium=catalog&utm_campaign=cat-seasonal`
**代码**：`STG-CAT-08`

### C9 · Women's Shoes — Extended Sizes
**名称**：`Women's Shoes — Extended Sizes`
**描述**：
```
Footwear in extended sizes, from factories that handle mixed size runs. We check sole bonding and heel strength before shipping, and can put your own label on the box.
```
**链接**：`https://sourcetogulf.com/category-women-shoes.html?utm_source=whatsapp&utm_medium=catalog&utm_campaign=cat-shoes`
**代码**：`STG-CAT-09`

---

## 4. 合规红线（目录里绝对不能出现）

| 禁售 | 原因 |
|---|---|
| 无人机 / 带摄像头飞行设备 | 迪拜禁飞 + 海关 AI 专查，罚 AED 10–200 万 |
| 摄像/AI 眼镜 | 需 TDRA 型式核准 + UAE 隐私法刑事风险 |
| 真金 / 贵金属首饰 | 需 hallmarking 检验 |
| 护肤膏霜 / 化妆品本体 | 需 MOHAP / ESMA 注册 |

目录只放**合规品类**；上面这些连"展示用"都别放，避免客户来问。

---

## 5. 上线后怎么用

1. **目录链接放三处**：Instagram bio、Facebook 主页、邮箱签名
2. **客户问"你卖什么"** → 聊天里点回形针 → Catalog，直接发整个目录或单条
3. ** WhatsApp Status 发目录链接**，所有联系人可见，不用群发
4. **每条带 UTM**，GA4 里能看到从 WhatsApp 来了多少流量

---

## 6. 维护节奏

- 每季换一次图片（保持真实感，别用旧图）
- 淡旺季调整合集顺序（Ramadan 前把 C8 提到最前）
- 新增品类先在网站建分类页，再进目录——保证链接有效
