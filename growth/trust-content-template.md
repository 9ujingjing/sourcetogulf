# 项目感内容模板（Project-Proof Content Kit）

> **用途**：把"打样 → 包装 → 寄样 → 备货 → 装柜"落成可复用图文序列，作为所有品类页 / 社媒的信任素材。
> **原则（守用户铁律）**：从真实产品出发、不假大空、不拍脑袋、不伪造照片。占位框标注"真实照待补"，由你提供实拍后替换。
> **已落地实例**：正式博文 `/blog/sample-to-container-delivery-journey.html` 就是本模板的实例化（图片为占位框，待补真实照）。

---

## 一、为什么需要"项目感"内容

中东 B2B 客户选供应商，心里只确认三件事：
1. **能不能给我看真东西**（不是目录渲染图）
2. **能不能打我的品牌**（定制包装 / 私牌）
3. **能不能顺利清关到货**（SABER / ECAS 已办）

纯产品九宫格回答不了这三点；而"过程 / 交付"内容能。竞品基本只发产品图——这一块是我们可以拉开的 **GEO 差异化突破口**。

---

## 二、5 步序列（每篇 / 每条都按这个骨架）

| 步 | 主题 | 中东客户在确认什么 | 必拍实况 |
|----|------|--------------------|----------|
| 1 | 打样对比 | 你给我看的是真东西 | 样品实物 + 细节（重量 / 电镀 / 石质 / 扣头） |
| 2 | 定制包装 | 能打我的品牌 | 定制盒 / 吊牌 / 阿拉伯文标 |
| 3 | 寄样到门 | 开箱体验对 | 样品箱 + 运单（DXB / RUH） |
| 4 | 工厂备货 / QC | 量大也稳 | 产线 / 备货堆 / 质检台 |
| 5 | 装柜发货 | 能顺利到货 | 装柜照 + SABER / ECAS 已办 |

---

## 三、每步文案公式（英文，可直接发 LinkedIn / 品类页）

- **Step 1**："Before any bulk order, we ship a real sample of [SKU] to your door. You check [weight / finish / stone], then we lock the spec."
- **Step 2**："Private-label means the product carries your brand. Custom box + Arabic label where SFDA / ECAS require."
- **Step 3**："Sample kit (product + branded packaging) air-shipped to Dubai / Riyadh in 3–5 days."
- **Step 4**："On approval we bulk-produce and QC against the approved sample. Lead time 15–25 days by category."
- **Step 5**："SABER PC / SC (Saudi) or ECAS (UAE) confirmed before loading. Container ships to Jebel Ali, ~18–25 days."

> 数据用真实 SKU 的 MOQ / FOB 价（见 `products.clean.json`），例如沙金戒指 MOQ 20 / ¥16、莫桑 2ct 戒指 MOQ 10 / ¥42、LED 面膜 MOQ 30 / ¥58。

---

## 四、可嵌入站点的 HTML 组件（已内置 `.img-slot` 占位框）

复制下面片段到任意品类页 / 博文即可（与 `delivery-journey` 博文同款）：

```html
<section class="sec"><div class="wrap">
<div class="sec-head"><h2>Step 1 — Sample proofing: you see the real item first</h2></div>
<p>Before any bulk order, we ship a physical sample of the exact SKU you will sell.</p>
<div class="img-slot"><div class="hint"><b>Real photo: sample in hand</b>Replace with a photo of the actual sample — weight, finish, stone close-up.</div></div>
</div></section>

<section class="sec alt"><div class="wrap">
<div class="sec-head"><h2>Step 2 — Private-label packaging: it carries your brand</h2></div>
<p>Custom boxes, hang tags and Arabic labels where required.</p>
<div class="img-slot"><div class="hint"><b>Real photo: custom box &amp; label</b>Replace with the custom box, hang tag and Arabic label.</div></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><h2>Step 3 — Sample shipping to your door</h2></div>
<p>Sample kit air-shipped to Dubai / Riyadh in 3–5 days.</p>
<div class="img-slot"><div class="hint"><b>Real photo: sample parcel &amp; waybill</b>Replace with the shipped sample box and courier waybill.</div></div>
</div></section>

<section class="sec alt"><div class="wrap">
<div class="sec-head"><h2>Step 4 — Factory stock-up and QC</h2></div>
<p>Bulk production checked against the approved sample.</p>
<div class="img-slot"><div class="hint"><b>Real photo: production line / QC bench</b>Replace with the bulk batch being made or QC'd.</div></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><h2>Step 5 — Container loading and compliant shipment</h2></div>
<p>SABER (Saudi) / ECAS (UAE) confirmed before loading.</p>
<div class="img-slot"><div class="hint"><b>Real photo: container loading</b>Replace with the actual container being loaded.</div></div>
</div></section>
```

---

## 五、社媒版（复用同一套素材，零额外成本）

- **LinkedIn 图文**：5 步各 1 图 + 第三节文案，连发 5 天或合 1 长帖，带 `#GulfSourcing #PrivateLabel #ChinaSourcing` 并深链回 `/blog/sample-to-container-delivery-journey.html`。
- **TikTok 短视频**：拍"装柜 / 质检 / 样品箱"无声 15–30s，字幕用 Step 文案，bio 链站点该页。不露脸、不讲故事、只解决"你能不能交付"这一个具体问题（参考那个综合布线账号的打法）。

---

## 六、拍摄清单（你这边补真实照）

- [ ] 样品实物平铺 + 细节特写（每品类 1–2 张）
- [ ] 定制包装盒 / 吊牌 / 阿拉伯文标
- [ ] 寄样箱 + 运单
- [ ] 工厂产线或备货堆
- [ ] 装柜瞬间

拍完发我，我替换占位框并重新部署 —— 真实供应链照片一旦上线，就是竞品没有的 GEO 信任资产。
