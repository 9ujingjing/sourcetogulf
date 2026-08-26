# -*- coding: utf-8 -*-
"""
build_blog.py — 生成博客"How to"原创深度文（落地用户 GEO 内容框架）
对应 sourcetogulf 的流量策略：
  · 踩中行业热词（社媒/行业动态先引爆）→ 写 HOW TO + 一手原创（代理视角的实战经验），
    而不是大站那种 "What is XXX" 科普（小站干不过大站）。
  · 每篇带 FAQPage JSON-LD（可被 AI 直接引用）+ Article 节点（含 author，强化 E-E-A-T）。
  · 正文前 200 字前置答案、堆事实密度（数字/%、年份）、客观口吻（见 tpl_common 铁律）。
  · 通过 page_shell 复用全站导航/GA4/fx.js，发布零额外成本。

用法: python3 build_blog.py
新增文章: 在 BLOG 字典加一条（file/title/desc/date/cat/read/body/faq）即可。
"""
import os, json
from tpl_common import page_shell, wa_link

APP = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://sourcetogulf.com'

# ===========================================================================
# 文章 1: 2026 SABER 新规下如何进口沙特（买家实战手册）
# 热词来源: 2026 年 SABER 全面升级（12 位 HS 编码、PC 证缩至 6 个月、强制品类破 150 种）
# 角度: 大站写 "What is SABER"；我们写 "How to 作为小买家实操 + 代理一手经验"
# ===========================================================================
SABER_FAQ = [
    ('Does SABER apply to small orders and low-MOQ shipments?',
     'Yes. SABER applies to commercial imports into Saudi Arabia regardless of size — even a low-MOQ trial batch of a few hundred units needs a Shipment Certificate (SC) before it leaves China. The only shipments that escape SABER are personal items below the de-minimis threshold, not goods you intend to sell. Low-MOQ buyers actually need SABER handled more carefully, because the Saudi importer of record must hold the SABER account, and most small buyers use an agent or freight forwarder to act on their behalf.'),
    ('Can I use my Chinese HS code for Saudi customs?',
     'No. Saudi Arabia switched to 12-digit HS codes in 2026 that are synced with ZATCA, and they differ from Chinese codes by roughly 15%. A product classified one way in China can fall under a completely different category in Saudi — for example, a smart light with a camera can be classed as surveillance equipment, or a lithium-powered tool as dangerous goods. The mismatch is a common cause of detention. Always verify the Saudi 12-digit code on the SASO portal before shipping.'),
    ('What happens if my Product Conformity (PC) certificate expires?',
     'You cannot file a Shipment Certificate without a valid PC, so the goods cannot clear. From 2026 the PC validity is split by risk: high-risk goods (chargers, toys, machinery, children\'s items) last 6 months, standard goods last 2 years. Plan renewals about 45 days ahead for high-risk items — previously the window was 30 days — because an expired PC stops the whole batch at the border with no post-arrival fix.'),
    ('Is SABER required for the UAE and other GCC states, or only Saudi Arabia?',
     'SABER is Saudi-specific. The UAE uses ECAS and GCC conformity, Kuwait uses KCAS, Qatar uses QS, Bahrain uses KBSP, and Oman uses DGSM. They are separate systems with separate certificates. A SABER certificate does not clear goods in Dubai or anywhere outside Saudi Arabia, so a multi-country Gulf order needs the right conformity track per destination.'),
    ('How long does Saudi clearance take when SABER is done correctly?',
     'With a valid PC registered, the SC filed before shipment, the correct 12-digit HS code, and Arabic labels in place, clearance typically runs 2–3 days at Jeddah or Dammam. The delay appears when one of those is missing: a wrong code or expired certificate can hold a container for weeks and trigger storage fees.'),
]

def saber_body():
    wa = wa_link('Hi SourceToGulf! I need to import to Saudi under the 2026 SABER rules. Can you check if my product is controlled and handle the PC/SC certificates?')
    return (
'<section class="sec hero-sec"><div class="wrap">'
'<span class="kicker">Saudi Import · Updated Aug 2026</span>'
'<h1>How to Import to Saudi Arabia Under the 2026 SABER Rules: A Buyer\'s Playbook</h1>'
'<p class="lead">Saudi Arabia\'s SABER system changed in 2026: 12-digit HS codes replaced the old codes, the Product Conformity (PC) certificate now lasts 6 months for high-risk goods (down from 1 year) and 2 years for standard goods, more than 150 product categories are controlled, and certificates must be filed before the goods arrive — there is no post-arrival fix. For a small Gulf buyer the practical path is: confirm whether your product is controlled, let your Saudi importer register the PC certificate on SABER, file a Shipment Certificate (SC) before each batch ships, and make sure Arabic labels and the right HS code match. Done this way, clearance runs 2–3 days instead of weeks.</p>'
'<p class="sub">By the SourceToGulf sourcing team · Updated 24 Aug 2026 · 11 min read</p>'
'<div class="cta-row">'
'<a class="btn-wa" href="' + wa + '" target="_blank" rel="noopener">💬 Check if my product is controlled</a>'
'<a class="btn-ghost" href="/blog/how-to-import-from-china-to-saudi-arabia.html">Full Saudi import guide →</a>'
'</div>'
'</div></section>'

'<section class="sec"><div class="wrap">'
'<div class="sec-head"><h2>What actually changed in SABER for 2026</h2></div>'
'<p>The 2026 update is not a tweak — it is a full reset of how goods are cleared into Saudi. The four changes that affect a small buyer directly:</p>'
'<ul class="bullets">'
'<li><b>12-digit HS codes.</b> From January 2026 SABER uses 12-digit codes synced with ZATCA. Old 8-digit certificates show as invalid with no grace period — goods can be at sea with a dead certificate.</li>'
'<li><b>Split PC validity.</b> High-risk categories (chargers, toys, machinery, children\'s items) dropped from 1 year to <b>6 months</b>; standard goods extended to <b>2 years</b>, but tied to the importer.</li>'
'<li><b>150+ controlled categories.</b> New additions include laptops (Type-C mandatory from 1 April 2026), new-energy devices, some chemicals, and smart-home products. Electronics and toys now need both GCC and SABER certificates.</li>'
'<li><b>No post-arrival certification.</b> Every certificate must be filed before the goods reach Saudi. There is no temporary or after-the-fact option — a missing certificate means the batch sits at the border.</li>'
'</ul>'
'</div></section>'

'<section class="sec alt"><div class="wrap">'
'<div class="sec-head"><h2>Does SABER apply to small orders and low MOQ?</h2></div>'
'<p>Yes. SABER covers commercial imports regardless of size — even a low-MOQ trial batch of a few hundred units needs a Shipment Certificate (SC) before it leaves China. The only escape is personal items below the de-minimis threshold, not goods intended for resale. Low-MOQ buyers need SABER handled more carefully, because the <b>Saudi importer of record</b> must hold the SABER account, and most small buyers outside Saudi rely on an agent or forwarder to act on their behalf.</p>'
'</div></section>'

'<section class="sec"><div class="wrap">'
'<div class="sec-head"><h2>Who files the SABER certificate — you or your supplier?</h2></div>'
'<p>The certificate must be filed by the <b>Saudi importer of record</b> inside their own SABER account. A Chinese factory cannot open or file it. In practice this means: if you are a small buyer in Dubai or Riyadh without a Saudi entity, your agent or freight forwarder coordinates the PC and SC on your behalf using the importer\'s login, then links the SC to the specific shipment. The factory\'s job is to supply the test reports and product details; the Saudi side owns the filing.</p>'
'</div></section>'

'<section class="sec alt"><div class="wrap">'
'<div class="sec-head"><h2>How to classify your product under the new 12-digit HS code</h2></div>'
'<p>Saudi HS codes differ from Chinese codes by roughly <b>15%</b>. A product classified one way in China can fall under a different category in Saudi — a camera light can be classed as surveillance equipment, or a lithium tool as dangerous goods. The mismatch is one of the most common causes of detention. Verify the Saudi 12-digit code on the SASO portal before shipping, and make sure the product description and materials match the code exactly.</p>'
'</div></section>'

'<section class="sec"><div class="wrap">'
'<div class="sec-head"><h2>The step-by-step playbook</h2></div>'
'<ol class="bullets">'
'<li><b>Confirm control status.</b> Check whether your HS code is on the SABER controlled list. Cosmetics, electronics, toys, building materials, new-energy and smart-home items usually are.</li>'
'<li><b>Register the PC certificate.</b> The Saudi importer files the Product Conformity certificate on SABER with test reports (from a SASO-recognised lab). Allow 2–4 weeks for high-risk goods.</li>'
'<li><b>Get Arabic labels right.</b> Product and outer packaging need Arabic information. Missing or wrong Arabic labels are a frequent reason for rejection at clearance.</li>'
'<li><b>Match the 12-digit HS code.</b> Verify on the SASO portal; do not reuse the Chinese code.</li>'
'<li><b>File the SC before shipping.</b> The Shipment Certificate is single-batch, valid 60 days. File it after the PC is approved and the shipment details are known.</li>'
'<li><b>Clear in 2–3 days.</b> With all of the above in place, Jeddah or Dammam clearance typically runs 2–3 days instead of weeks.</li>'
'</ol>'
'</div></section>'

'<section class="sec alt"><div class="wrap">'
'<div class="sec-head"><h2>Worked example: a $2,000 skincare + accessories order to Riyadh</h2></div>'
'<table class="tbl" style="width:100%;border-collapse:collapse;margin:18px 0;font-size:15px">'
'<thead><tr style="background:#0b1f3a;color:#fff"><th style="padding:10px 12px;text-align:left">Step</th><th style="padding:10px 12px;text-align:left">Action</th><th style="padding:10px 12px;text-align:left">Time</th></tr></thead>'
'<tbody>'
'<tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">1</td><td style="padding:10px 12px">Confirm HS 33 (cosmetics) is controlled; request SASO lab report</td><td style="padding:10px 12px">Week 1</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">2</td><td style="padding:10px 12px">Saudi importer files PC on SABER</td><td style="padding:10px 12px">Weeks 2–3</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">3</td><td style="padding:10px 12px">Arabic labels applied at factory; 12-digit code confirmed</td><td style="padding:10px 12px">Week 3</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">4</td><td style="padding:10px 12px">SC filed; goods ship (air ~6–10 days)</td><td style="padding:10px 12px">Week 4</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">5</td><td style="padding:10px 12px">Customs clearance in Riyadh</td><td style="padding:10px 12px">2–3 days</td></tr>'
'</tbody></table>'
'<p>Total lead time from go to shelf: roughly <b>5–6 weeks</b> for a controlled category. Starting SABER after the goods are already at sea is the single most expensive mistake — there is no after-the-fact filing.</p>'
'</div></section>'

'<section class="sec"><div class="wrap">'
'<div class="sec-head"><h2>Common mistakes that get goods stuck</h2></div>'
'<ul class="bullets">'
'<li>Reusing the Chinese HS code instead of the Saudi 12-digit code → detention</li>'
'<li>Letting the PC expire (high-risk goods now last only 6 months) → no SC can be filed</li>'
'<li>Missing or incorrect Arabic labels → rejection at clearance</li>'
'<li>No Saudi importer of record → nobody can open the SABER account</li>'
'<li>Filing SABER after the goods sail → no post-arrival fix exists in 2026</li>'
'</ul>'
'<div class="rel-grid">'
'<a class="rel-card" href="/blog/how-to-import-from-china-to-saudi-arabia.html"><span>Full Saudi import guide</span><b>Duty, VAT, shipping, timelines</b></a>'
'<a class="rel-card" href="/shipping/china-to-saudi-arabia.html"><span>Saudi shipping & SABER</span><b>Door-to-door, compliance handled</b></a>'
'<a class="rel-card" href="/solutions.html"><span>Solutions by buyer type</span><b>Influencer · Small brand · Reseller</b></a>'
'<a class="rel-card" href="/gcc-import-answers.html"><span>GCC import Q&amp;A</span><b>22 answers on SABER, VAT, MOQ</b></a>'
'<a class="rel-card" href="/category-beauty-toys.html"><span>Beauty & toys</span><b>Controlled categories — plan early</b></a>'
'<a class="rel-card" href="/blog/landed-cost-china-to-gulf-explained.html"><span>Landed cost explained</span><b>Every fee to your door</b></a>'
'</div>'
'</div></section>'

'<section class="sec alt"><div class="wrap" style="text-align:center">'
'<div class="cta-box">'
'<h2>Written by the SourceToGulf sourcing team</h2>'
'<p>We clear goods into Saudi every week and track SABER changes as they happen. Send your product list — we confirm whether it is controlled, register the certificates, and quote one landed price to Riyadh or Jeddah.</p>'
'<a class="wa-btn" href="' + wa + '" target="_blank" rel="noopener">💬 Ask about my Saudi shipment</a>'
'</div>'
'</div></section>'
    )

# ===========================================================================
# 文章 2: 如何用中海合会 FTA 降低海湾进口关税（小进口商 2026 指南）
# 热词来源: 2025-07 中海合会 FTA 框架签署、临时适用，1420 个 HS 编码降税
# 角度: 大站写 "What is the FTA"；我们写 "How to 作为小进口商真正吃到降税 + 代理一手经验"
# ===========================================================================
FTA_FAQ = [
    ('Is the China–GCC Free Trade Agreement fully ratified?',
     'The framework agreement was signed in July 2025, and provisional application clauses mean GCC customs offices are already honouring reduced tariffs on listed goods before full ratification across all six member states is complete. For an importer the practical effect is live now: if your HS code is on the reduced list and you ship with a valid Certificate of Origin, you pay the lower rate today.'),
    ('Does this mean China goods enter the GCC at 0% duty?',
     'No. The FTA reduces tariffs on roughly 1,420 specific HS codes — including all cosmetics (HS 33) and most consumer electronics (HS 85) — by an average of 7.4 percentage points. The standard GCC baseline (5% in the UAE and Saudi) still applies to every product not on the reduced list. Treat it as a targeted cut on named categories, not a blanket zero.'),
    ('Do I need a Certificate of Origin to claim the lower rate?',
     'Yes. The reduced rate is claimed at customs with a valid GCC–China FTA Certificate of Origin that meets the rules of origin. Without it, the shipment is assessed at the standard rate even if the product is on the list. The certificate is the difference between the cut applying and not applying.'),
    ('Which GCC countries apply the FTA?',
     'All six GCC members operate under the GCC Common Customs Law, so the reduced rates apply across the UAE, Saudi Arabia, Kuwait, Qatar, Bahrain and Oman for products on the list. The paperwork requirement — a valid Certificate of Origin — is what unlocks it in each country.'),
    ('How do I know if my product is on the reduced list?',
     'Check your product\'s HS code against the FTA schedule. Cosmetics (HS 33), most consumer electronics (HS 85) and a wide slice of industrial machinery (HS 84) are included. If you are unsure, an agent can verify the code and prepare the Certificate of Origin so the lower rate is claimed correctly.'),
]

def fta_body():
    wa = wa_link('Hi SourceToGulf! I want to use the China-GCC FTA to lower my import duty. Can you check my HS codes and prepare the Certificate of Origin?')
    return (
'<section class="sec hero-sec"><div class="wrap">'
'<span class="kicker">Trade Policy · 2026</span>'
'<h1>How to Use the New China–GCC FTA to Cut Your Gulf Import Duty (2026 Guide for Small Importers)</h1>'
'<p class="lead">The GCC and China signed a framework Free Trade Agreement in July 2025, and provisional application is already cutting tariffs on <b>1,420 HS codes</b> — including all cosmetics (HS 33) and most consumer electronics (HS 85) — by an average of <b>7.4 percentage points</b>. But the cut does not happen automatically: you claim it by shipping with a valid Certificate of Origin that meets GCC rules of origin. For a small Gulf importer the win is real but narrow — it lowers duty on specific listed categories, not on every China shipment — and the paperwork is exactly where most buyers leave money on the table.</p>'
'<p class="sub">By the SourceToGulf sourcing team · Updated 24 Aug 2026 · 10 min read</p>'
'<div class="cta-row">'
'<a class="btn-wa" href="' + wa + '" target="_blank" rel="noopener">💬 Check my HS codes for FTA cuts</a>'
'<a class="btn-ghost" href="/blog/landed-cost-china-to-gulf-explained.html">See landed cost math →</a>'
'</div>'
'</div></section>'

'<section class="sec"><div class="wrap">'
'<div class="sec-head"><h2>What the China–GCC FTA actually does (and does not do)</h2></div>'
'<p>The framework agreement was signed in July 2025. Through provisional application clauses, GCC customs offices already honour reduced tariffs on listed goods before full ratification across all six member states is complete. The headline number: <b>1,420 HS codes</b> get a tariff reduction averaging <b>7.4 percentage points</b>.</p>'
'<p>What it does <b>not</b> do matters more for a small buyer: the UAE and most GCC states still apply a <b>5% baseline</b> duty on the large majority of goods. The FTA lowers specific named categories; it does not zero out duty on every China shipment. Reading "China–GCC FTA signed" as "China goods now enter free" is the most common — and most expensive — misunderstanding.</p>'
'</div></section>'

'<section class="sec alt"><div class="wrap">'
'<div class="sec-head"><h2>Which products actually get the cut</h2></div>'
'<table class="tbl" style="width:100%;border-collapse:collapse;margin:18px 0;font-size:15px">'
'<thead><tr style="background:#0b1f3a;color:#fff"><th style="padding:10px 12px;text-align:left">Category</th><th style="padding:10px 12px;text-align:left">HS chapter</th><th style="padding:10px 12px;text-align:left">Note for Gulf buyers</th></tr></thead>'
'<tbody>'
'<tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Cosmetics & personal care</b></td><td style="padding:10px 12px">HS 33</td><td style="padding:10px 12px">All items; still needs SFDA/SABER per destination</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px"><b>Consumer electronics</b></td><td style="padding:10px 12px">HS 85</td><td style="padding:10px 12px">Most items; ECAS / GCC conformity still required</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Industrial machinery</b></td><td style="padding:10px 12px">HS 84</td><td style="padding:10px 12px">Wide cut; verify exact sub-codes</td></tr>'
'</tbody></table>'
'<p>The cut is applied per HS code, not per product name. The same "beauty device" might sit in HS 33 (cut) or HS 85 (cut) or HS 90 (not on the list) depending on its function — which is why the code, not the listing, decides the rate.</p>'
'</div></section>'

'<section class="sec"><div class="wrap">'
'<div class="sec-head"><h2>How a small importer actually claims it</h2></div>'
'<p>The reduced rate is <b>not</b> automatic at the border. To claim it you need a valid <b>GCC–China FTA Certificate of Origin</b> that meets the rules of origin (typically substantial transformation or a minimum regional value content). Without that certificate, customs assesses the shipment at the standard 5% even if the product is on the list. In practice: the supplier or agent prepares the certificate alongside the commercial invoice, and it is presented at clearance. Most of the saving is lost by buyers who skip this step.</p>'
'</div></section>'

'<section class="sec alt"><div class="wrap">'
'<div class="sec-head"><h2>Where the saving shows up</h2></div>'
'<p>On a <b>$100,000</b> cosmetics shipment (HS 33) to Dubai, the FTA cut of ~7.4 points takes roughly <b>$7,400</b> off the duty bill — often 40–60% of the shipment\'s gross margin. On smaller orders the absolute number is smaller but the percentage gain is the same. The certificate costs far less than the duty it saves, which is why preparing it is the highest-return paperwork in Gulf importing right now.</p>'
'</div></section>'

'<section class="sec"><div class="wrap">'
'<div class="sec-head"><h2>The step-by-step checklist</h2></div>'
'<ol class="bullets">'
'<li><b>Identify the HS code</b> of each product line; confirm whether it sits on the FTA reduced list (HS 33, HS 85, parts of HS 84).</li>'
'<li><b>Confirm rules of origin</b> are met — the goods must qualify, not merely be shipped from China.</li>'
'<li><b>Prepare the Certificate of Origin</b> (GCC–China FTA format) with the supplier or agent.</li>'
'<li><b>Attach it at clearance</b> so customs applies the reduced rate, not the 5% baseline.</li>'
'<li><b>Keep records</b> — GCC customs can re-check origin claims; documentation is your defence.</li>'
'</ol>'
'<div class="rel-grid">'
'<a class="rel-card" href="/blog/landed-cost-china-to-gulf-explained.html"><span>Landed cost explained</span><b>See duty in the full math</b></a>'
'<a class="rel-card" href="/shipping/china-to-uae.html"><span>China to UAE</span><b>5% duty + 5% VAT, free zones</b></a>'
'<a class="rel-card" href="/shipping/china-to-saudi-arabia.html"><span>China to Saudi</span><b>SABER + 5% duty + 15% VAT</b></a>'
'<a class="rel-card" href="/solutions.html"><span>Solutions by buyer type</span><b>Influencer · Small brand · Reseller</b></a>'
'<a class="rel-card" href="/alibaba-vs-sourcing-agent.html"><span>Alibaba vs agent</span><b>Who handles the paperwork</b></a>'
'<a class="rel-card" href="/category-beauty-toys.html"><span>Beauty & toys</span><b>HS 33 — on the FTA list</b></a>'
'</div>'
'</div></section>'

'<section class="sec alt"><div class="wrap" style="text-align:center">'
'<div class="cta-box">'
'<h2>Written by the SourceToGulf sourcing team</h2>'
'<p>We track GCC–China trade changes as they land and prepare the Certificate of Origin so the lower rate is claimed, not left on the table. Send your HS codes — we confirm which lines qualify.</p>'
'<a class="wa-btn" href="' + wa + '" target="_blank" rel="noopener">💬 Check my codes for FTA cuts</a>'
'</div>'
'</div></section>'
    )

# ===========================================================================
# 文章 3: 如何不用集装箱为 TikTok Shop 沙特选品（网红/小卖家 2026 指南）
# 热词来源: TikTok Shop 中东扩张（沙特 2025 上线、2026 扩展）、沙特是海湾最大消费市场
# 角度: 大站写 "What is TikTok Shop"；我们写 "How to 网红/小卖家 0 集装箱起步 + 代理一手经验"
# 钉住买家人设: influencers / resellers / moms
# ===========================================================================
TIKTOK_FAQ = [
    ('Do I need a container to sell on TikTok Shop Saudi?',
     'No. A container is a wholesale restocking tool, not a launch requirement. A creator or small seller typically starts with a low-MOQ batch of a few hundred units, air-shipped to Riyadh or Jeddah. A 20ft container holds roughly 10,000 to 30,000 units and locks up working capital for months; most TikTok Shop sellers never need one. The platform rewards a fast test-and-iterate cycle, which is the opposite of container-scale buying.'),
    ('Can I put my own brand on products sourced from China?',
     'Yes, this is private labelling, and it is the normal way creators build a TikTok Shop line. At low MOQ — often 100 to 500 units for beauty and accessories — a factory can print your logo on the packaging and sometimes on the product itself. We handle the artwork, keep it compliant with Saudi Arabic-labelling rules, and consolidate the branded batch before shipping.'),
    ('How do samples work before I commit to a bulk order?',
     'We shortlist two or three candidate factories, then ship you physical samples to your door in the UAE or Saudi. You approve the one you like on camera, then we place the bulk order against that exact sample. You never buy blind, and the sample becomes the quality benchmark for the whole batch.'),
    ('What compliance do TikTok Shop products need for Saudi Arabia?',
     'The same as any commercial import: SABER for controlled categories (cosmetics, electronics, toys), Arabic labels, and a Saudi importer of record. TikTok Shop does not exempt you from Saudi customs. For controlled goods, plan SABER early — registering the PC certificate adds roughly 4 to 6 weeks, and there is no post-arrival fix in 2026.'),
    ('Which products trend on TikTok Shop in Saudi right now?',
     'Beauty and personal-care tools, modest-fashion accessories, home-organisation items, phone accessories, and small gadgets lead. The winning pattern is a product with a clear demo moment on video — something that looks different in your hand. Pick a product you can show, not just describe.'),
]

def tiktok_body():
    wa = wa_link('Hi SourceToGulf! I want to launch a private-label product on TikTok Shop Saudi. Can you find trending products, send me samples, and handle the packaging + Saudi shipping?')
    return (
'<section class="sec hero-sec"><div class="wrap">'
'<span class="kicker">TikTok Shop · 2026</span>'
'<h1>How to Source Products for TikTok Shop Saudi Without a Container (2026 Guide for Influencers &amp; Small Sellers)</h1>'
'<p class="lead">TikTok Shop is live in Saudi Arabia and expanding across the Gulf in 2026, and the sellers winning are not importers — they are creators and small sellers who test a product, brand it, and ship a few hundred units at a time. You do not need a container, Chinese-language skills, or a customs licence to start. The practical path is: pick a product with a strong video demo, have us send you samples, approve one, add your private-label packaging, clear it through SABER where required, and air-ship a low-MOQ batch to your door. Most launches start under $3,000 and never touch a container.</p>'
'<p class="sub">By the SourceToGulf sourcing team · Updated 24 Aug 2026 · 9 min read</p>'
'<div class="cta-row">'
'<a class="btn-wa" href="' + wa + '" target="_blank" rel="noopener">💬 Start my TikTok Shop product</a>'
'<a class="btn-ghost" href="/for-influencers.html">For influencers →</a>'
'</div>'
'</div></section>'

'<section class="sec"><div class="wrap">'
'<div class="sec-head"><h2>Why TikTok Shop Saudi is a small-seller opening</h2></div>'
'<p>Saudi Arabia is the largest consumer market in the Gulf, and TikTok Shop gives a creator with an audience a direct storefront without the capital a traditional import business needs. The model that works is not "buy a container and hope" — it is "find a product that demos well, prove demand with a small batch, then scale the winners." That flips the old import math: low MOQ, fast air shipping, and branding you control.</p>'
'</div></section>'

'<section class="sec alt"><div class="wrap">'
'<div class="sec-head"><h2>The four things you do not need</h2></div>'
'<ul class="bullets">'
'<li><b>A container.</b> A 20ft container holds roughly 10,000 to 30,000 units and ties up capital for months. A launch batch is usually a few hundred units, air-shipped.</li>'
'<li><b>Chinese-language skills.</b> We negotiate with factories, verify them, and relay decisions to you in English or Arabic.</li>'
'<li><b>A customs licence.</b> Our Saudi importer of record handles SABER and clearance on your behalf.</li>'
'<li><b>Big upfront capital.</b> Most private-label launches start under $3,000 for product, samples, packaging and first air shipment.</li>'
'</ul>'
'</div></section>'

'<section class="sec"><div class="wrap">'
'<div class="sec-head"><h2>The step-by-step path from idea to TikTok listing</h2></div>'
'<ol class="bullets">'
'<li><b>Pick a demo-friendly product.</b> Choose something that looks different in your hand — a tool, a gadget, a beauty item. Avoid products that need a container or cold-chain logistics.</li>'
'<li><b>We shortlist factories.</b> Two or three candidate suppliers, verified, with MOQ low enough for a test batch.</li>'
'<li><b>Samples to your door.</b> We ship physical samples to your UAE or Saudi address so you approve on camera.</li>'
'<li><b>Private-label packaging.</b> Your logo on the box (100 to 500 unit MOQ typical), Arabic labels included for Saudi compliance.</li>'
'<li><b>Clear SABER where needed.</b> Cosmetics, electronics and toys are controlled — register the PC certificate early (adds 4 to 6 weeks).</li>'
'<li><b>Air-ship the batch.</b> A few hundred units arrive in days, not weeks; list on TikTok Shop and iterate.</li>'
'</ol>'
'</div></section>'

'<section class="sec alt"><div class="wrap">'
'<div class="sec-head"><h2>Worked example: a $2,400 beauty-influencer line, no container</h2></div>'
'<table class="tbl" style="width:100%;border-collapse:collapse;margin:18px 0;font-size:15px">'
'<thead><tr style="background:#0b1f3a;color:#fff"><th style="padding:10px 12px;text-align:left">Step</th><th style="padding:10px 12px;text-align:left">Action</th><th style="padding:10px 12px;text-align:left">Cost</th></tr></thead>'
'<tbody>'
'<tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">1</td><td style="padding:10px 12px">3 factory samples of a LED beauty tool shipped to Riyadh</td><td style="padding:10px 12px">$120</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">2</td><td style="padding:10px 12px">Approve 1 sample; design private-label box (MOQ 300)</td><td style="padding:10px 12px">$350</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">3</td><td style="padding:10px 12px">SABER PC + SC for HS 85 device</td><td style="padding:10px 12px">$480</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">4</td><td style="padding:10px 12px">300 units, branded, air-shipped to Saudi</td><td style="padding:10px 12px">$1,450</td></tr>'
'</tbody></table>'
'<p>Total launch cost: about <b>$2,400</b> for a branded, compliant, door-delivered batch of 300 units — no container, no Chinese required. The same product at container scale would be 30 to 100 times the capital before a single unit sold.</p>'
'</div></section>'

'<section class="sec"><div class="wrap">'
'<div class="sec-head"><h2>Mistakes that sink a TikTok Shop launch</h2></div>'
'<ul class="bullets">'
'<li>Listing before samples arrive — you cannot vouch for a product you have not held.</li>'
'<li>Skipping SABER on controlled goods — TikTok Shop does not exempt you from Saudi customs, and there is no post-arrival fix in 2026.</li>'
'<li>Choosing a product that needs a container or cold chain — it breaks the fast-test model.</li>'
'<li>No private label — selling a generic item means competing on price with every other reseller.</li>'
'</ul>'
'<div class="rel-grid">'
'<a class="rel-card" href="/for-influencers.html"><span>For influencers</span><b>Launch a private-label line</b></a>'
'<a class="rel-card" href="/for-resellers.html"><span>For resellers</span><b>Low-MOQ, fast restock</b></a>'
'<a class="rel-card" href="/for-moms.html"><span>For side-hustle moms</span><b>Start small from home</b></a>'
'<a class="rel-card" href="/blog/saber-2026-saudi-buyers-playbook.html"><span>SABER 2026 playbook</span><b>What controlled goods need</b></a>'
'<a class="rel-card" href="/blog/china-gcc-fta-lower-import-duty.html"><span>China-GCC FTA</span><b>Lower duty on HS 33/85</b></a>'
'<a class="rel-card" href="/category-beauty-toys.html"><span>Beauty &amp; toys</span><b>Controlled — plan SABER early</b></a>'
'</div>'
'</div></section>'

'<section class="sec alt"><div class="wrap" style="text-align:center">'
'<div class="cta-box">'
'<h2>Written by the SourceToGulf sourcing team</h2>'
'<p>We help Gulf creators turn a trend into a branded, compliant product without a container: trend spotting, samples to your door, private-label packaging, and Saudi clearance handled. Send the product you saw on TikTok — we find the source.</p>'
'<a class="wa-btn" href="' + wa + '" target="_blank" rel="noopener">💬 Start my TikTok Shop product</a>'
'</div>'
'</div></section>'
    )

# ===========================================================================
# 文章 4: 如何从中国为 White Friday 2026 备货（海湾小商家指南）
# 热词来源: White Friday 2026 = 2026-11-27，沙特/阿联酋全年第二大线上销售窗口
# 角度: 大站写 "When is White Friday 2026"；我们写 "How to 作为海湾小商家从中国备货 + 代理一手经验"
# 钉住买家人设: small business owners / resellers / influencers / moms
# 配图: /images/blog/white-friday-hero.png / white-friday-sourcing.png / white-friday-delivery.png
# ===========================================================================
WHITE_FRIDAY_FAQ = [
    ('When is White Friday 2026 and why does it matter for Gulf sellers?',
     'White Friday 2026 falls on <b>27 November</b>. In Saudi Arabia and the UAE it is the biggest online sales event after Ramadan, and a large share of annual electronics, beauty and home-goods sales is concentrated in the last week of November. For a small seller the window is short and unforgiving: stock that arrives too late misses the sale; stock that arrives too early ties up capital. The buyers who win are the ones who plan the timeline backwards from 27 November.'),
    ('Do I need a container to stock for White Friday?',
     'No. A container is for proven, high-volume SKUs and needs roughly 60–90 days of buffer. Most small sellers and creators launch White Friday with a low-MOQ air-shipped batch of 200–1,000 units. It costs more per unit than sea freight, but it keeps working capital low, lets you test several products, and gets stock to your door in time for the sale. The goal for a first White Friday is to prove demand, not to fill a warehouse.'),
    ('How early should I start sourcing from China for White Friday?',
     'Work backwards from 27 November. Allow: <b>2–3 weeks</b> for samples and factory selection, <b>2–3 weeks</b> for private-label artwork and packaging production, <b>2–4 weeks</b> for bulk production, <b>1–2 weeks</b> for air shipping and customs clearance, and <b>1 week</b> of buffer for warehouse prep. That means product selection and samples should start by <b>early September</b>; bulk must ship from China by <b>mid-October</b> at the latest. Wait until October and you are gambling on every step being perfect.'),
    ('Which products sell best on White Friday in Saudi and UAE?',
     'The categories that consistently move are beauty tools and accessories, phone accessories, home organisation, small kitchen gadgets, modest-fashion accessories, LED lighting and smartwatches. The best picks share three traits: low MOQ available in China, a strong demo moment on video, and straightforward compliance for Saudi (SABER) or the UAE (ECAS). Avoid anything that needs refrigeration, hazmat certification, or a long testing cycle — those will not fit the White Friday timeline.'),
    ('Can a small seller private-label products in time for White Friday?',
     'Yes, if the artwork is locked by late September. Most China factories can add a logo and customise retail packaging at MOQs of 100–500 units in about 2–3 weeks. Arabic labels for Saudi must be included in the artwork. The common delay is not production — it is the buyer changing their mind on the logo or packaging design twice. Lock the artwork once, and the batch stays on schedule.'),
]

def white_friday_body():
    wa = wa_link('Hi SourceToGulf! I want to stock for White Friday 2026 from China. Can you help me pick products, send samples, and handle packaging + shipping to the Gulf?')
    return (
'<section class="sec hero-sec"><div class="wrap">'
'<span class="kicker">White Friday 2026 · Gulf E-commerce</span>'
'<h1>How to Stock for White Friday 2026 from China (Gulf Small Business Guide)</h1>'
'<p class="lead">White Friday 2026 falls on <b>27 November</b>. In Saudi Arabia and the UAE it is the biggest online sales window after Ramadan, and a large share of annual electronics, beauty and home-goods sales is concentrated in that final week. You do not need a container or a big warehouse to take part. The small sellers who win are the ones who start early, pick demo-friendly products, brand the packaging, and air-ship a low-MOQ batch so it clears customs and reaches the warehouse by mid-November. The practical path is: confirm your shortlist by early September, approve samples and artwork by late September, ship bulk by mid-October, and land goods by mid-November. Miss the September window and every remaining step becomes a gamble.</p>'
'<p class="sub">By the SourceToGulf sourcing team · Updated 26 Aug 2026 · 10 min read</p>'
'<div class="cta-row">'
'<a class="btn-wa" href="' + wa + '" target="_blank" rel="noopener">💬 Plan my White Friday stock</a>'
'<a class="btn-ghost" href="/for-small-businesses.html">For small businesses →</a>'
'</div>'
'</div></section>'

'<section class="sec"><div class="wrap">'
'<img src="/images/blog/white-friday-hero.png" alt="A small Gulf e-commerce seller preparing product boxes for White Friday sales season" style="width:100%;max-width:100%;border-radius:12px;margin:18px 0;box-shadow:0 4px 14px rgba(0,0,0,.08);" loading="lazy">'
'<div class="sec-head"><h2>Why White Friday is a small-seller opening, not just a big-brand game</h2></div>'
'<p>Large retailers plan White Friday six months ahead with containers. Small sellers do not have to copy that. The creator and reseller model that works in the Gulf is the opposite: launch several small tests, double down on the one that sells, and use private-label packaging to stand out from generic listings. The math is different too. A first White Friday batch can start under <b>$5,000</b> landed — product, samples, branded packaging, air freight, duty and VAT included — and still leave room for margin.</p>'
'<p>White Friday is also a strong GEO signal for Google and AI engines because it is a recurring, date-anchored event. Search demand for "White Friday 2026 Saudi deals" and related product queries starts climbing in late September and peaks in the week before 27 November. Sellers who publish their offer and content early are the ones the algorithms learn to surface.</p>'
'</div></section>'

'<section class="sec alt"><div class="wrap">'
'<div class="sec-head"><h2>The White Friday 2026 sourcing timeline (work backwards from 27 Nov)</h2></div>'
'<table class="tbl" style="width:100%;border-collapse:collapse;margin:18px 0;font-size:15px">'
'<thead><tr style="background:#0b1f3a;color:#fff"><th style="padding:10px 12px;text-align:left">Date / window</th><th style="padding:10px 12px;text-align:left">What to lock in</th><th style="padding:10px 12px;text-align:left">Why it matters</th></tr></thead>'
'<tbody>'
'<tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Early September</b></td><td style="padding:10px 12px">Product shortlist, factories, samples requested</td><td style="padding:10px 12px">Gives you time to compare suppliers and reject bad fits</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px"><b>Late September</b></td><td style="padding:10px 12px">Sample approved, artwork finalised, packaging locked</td><td style="padding:10px 12px">Design changes after this point push production</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Mid-October</b></td><td style="padding:10px 12px">Bulk production complete, goods ship from China</td><td style="padding:10px 12px">Last safe air-freight departure for mid-November landing</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px"><b>Early November</b></td><td style="padding:10px 12px">Customs clearance, warehouse received</td><td style="padding:10px 12px">Leaves a buffer for listing, photography, ads prep</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>20–27 November</b></td><td style="padding:10px 12px">Sale live, ads on, restock fast sellers by air</td><td style="padding:10px 12px">Peak demand window; best sellers often sell out</td></tr>'
'</tbody></table>'
'<p>The most common mistake is treating <b>mid-October</b> as the start date. By then it is usually too late to sample, brand and air-ship in time.</p>'
'</div></section>'

'<section class="sec"><div class="wrap">'
'<div class="sec-head"><h2>What to stock: products that move in Saudi and UAE</h2></div>'
'<p>The products that work share three traits: <b>low MOQ</b> from China, a <b>strong demo moment</b> on video or in a photo, and <b>straightforward compliance</b> for the destination. Based on what we see moving into Gulf warehouses ahead of sale seasons:</p>'
'<ul class="bullets">'
'<li><b>Beauty tools and accessories</b> — LED mirrors, gua-sha sets, makeup organisers, brush sets. HS 33, SABER/SFDA territory in Saudi, so plan certificates early.</li>'
'<li><b>Phone and tech accessories</b> — cables, cases, wireless chargers, holders. High demand, but ECAS/GCC conformity required in the UAE and Saudi.</li>'
'<li><b>Home organisation</b> — kitchen organisers, drawer dividers, storage boxes. Light, cheap to ship, easy to demo.</li>'
'<li><b>Modest-fashion accessories</b> — scarves, pins, headbands, belts. Strong Gulf audience, low return rate.</li>'
'<li><b>Small gadgets and LED lighting</b> — novelty lights, portable lamps, smartwatch accessories. Visual and giftable.</li>'
'</ul>'
'<p>Avoid refrigerated goods, hazmat, large appliances, or anything that needs a long certification cycle. Those are not first-White-Friday products.</p>'
'</div></section>'

'<section class="sec alt"><div class="wrap">'
'<img src="/images/blog/white-friday-sourcing.png" alt="China sourcing agent sample table with product samples and blank private-label packaging" style="width:100%;max-width:100%;border-radius:12px;margin:18px 0;box-shadow:0 4px 14px rgba(0,0,0,.08);" loading="lazy">'
'<div class="sec-head"><h2>Samples to your door before you commit</h2></div>'
'<p>Never order a White Friday batch from a photo. We shortlist two or three factories, ship physical samples to your UAE or Saudi address, and let you approve the one you want on camera. The sample becomes the quality benchmark for the whole batch. For a $5,000 launch, sampling usually costs $100–200 and saves far more by avoiding a bad bulk order.</p>'
'<p>This is where a composite sourcing partner differs from a freight forwarder or a packaging-only shop. We handle the factory search, the sample shipment, the packaging design and the final delivery — so the product that arrives at your door matches the one you approved.</p>'
'</div></section>'

'<section class="sec"><div class="wrap">'
'<div class="sec-head"><h2>Private-label packaging: the fastest way to stand out</h2></div>'
'<p>Generic products compete on price. Branded products compete on trust. For White Friday, even a simple logo on the box and a thank-you card inside lifts perceived value and protects margin. At 100–500 unit MOQs most China factories can add custom retail packaging in 2–3 weeks.</p>'
'<p>The artwork must include Arabic labelling for Saudi-bound goods and a clear product description for customs. Lock the design by late September; every revision after that pushes the production date and risks missing the mid-October shipping window.</p>'
'</div></section>'

'<section class="sec alt"><div class="wrap">'
'<div class="sec-head"><h2>Worked example: a $5,000 White Friday launch batch</h2></div>'
'<table class="tbl" style="width:100%;border-collapse:collapse;margin:18px 0;font-size:15px">'
'<thead><tr style="background:#0b1f3a;color:#fff"><th style="padding:10px 12px;text-align:left">Line item</th><th style="padding:10px 12px;text-align:left">What you get</th><th style="padding:10px 12px;text-align:left">Approx. cost</th></tr></thead>'
'<tbody>'
'<tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Samples (3 products)</b></td><td style="padding:10px 12px">Shipped to your door for approval</td><td style="padding:10px 12px">$150</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px"><b>Bulk product</b></td><td style="padding:10px 12px">300 units of the winning SKU</td><td style="padding:10px 12px">$2,100</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Custom packaging</b></td><td style="padding:10px 12px">Logo box + Arabic label, MOQ 300</td><td style="padding:10px 12px">$400</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px"><b>SABER/ECAS</b></td><td style="padding:10px 12px">PC + SC or conformity clearance</td><td style="padding:10px 12px">$500</td></tr>'
'<tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Air freight + duty/VAT</b></td><td style="padding:10px 12px">Door to UAE or Saudi</td><td style="padding:10px 12px">$1,350</td></tr>'
'</tbody></table>'
'<p>Total landed cost: roughly <b>$5,500</b> for 300 branded, compliant units delivered to your door. Sell at a 2.5x landed price and the batch grosses about $13,750. Adjust the SKU and volume up or down, but the ratio stays similar for most first-time White Friday sellers.</p>'
'</div></section>'

'<section class="sec"><div class="wrap">'
'<div class="sec-head"><h2>Mistakes that make sellers miss White Friday</h2></div>'
'<ul class="bullets">'
'<li><b>Starting in October.</b> By then you have no margin for sample rejects, artwork revisions or shipping delays.</li>'
'<li><b>Ordering blind.</b> A great Alibaba photo does not guarantee the product that arrives at your door.</li>'
'<li><b>Ignoring compliance.</b> SABER/ECAS for electronics, toys and cosmetics cannot be fixed after arrival.</li>'
'<li><b>Generic packaging.</b> You end up competing on price with every other reseller.</li>'
'<li><b>Shipping sea freight to save money.</b> It is cheaper per unit but usually misses the sale window for a first-timer.</li>'
'</ul>'
'<div class="rel-grid">'
'<a class="rel-card" href="/blog/saber-2026-saudi-buyers-playbook.html"><span>SABER 2026 playbook</span><b>Compliance timeline for Saudi goods</b></a>'
'<a class="rel-card" href="/blog/source-products-tiktok-shop-saudi-no-container.html"><span>TikTok Shop Saudi</span><b>How creators launch without a container</b></a>'
'<a class="rel-card" href="/services/custom-branding-packaging.html"><span>Custom packaging</span><b>Logo boxes + Arabic labels</b></a>'
'<a class="rel-card" href="/for-small-businesses.html"><span>For small businesses</span><b>Low-MOQ sourcing playbook</b></a>'
'<a class="rel-card" href="/for-resellers.html"><span>For resellers</span><b>Fast restock and branding</b></a>'
'<a class="rel-card" href="/blog/china-gcc-fta-lower-import-duty.html"><span>China-GCC FTA</span><b>Cut duty on HS 33/85</b></a>'
'</div>'
'</div></section>'

'<section class="sec alt"><div class="wrap" style="text-align:center">'
'<img src="/images/blog/white-friday-delivery.png" alt="Small parcels air-shipped from China arriving at a Gulf small business owner desk" style="width:100%;max-width:100%;border-radius:12px;margin:18px 0;box-shadow:0 4px 14px rgba(0,0,0,.08);" loading="lazy">'
'<div class="cta-box">'
'<h2>Written by the SourceToGulf sourcing team</h2>'
'<p>We help Gulf sellers build a White Friday batch from China without a container: product shortlisting, samples to your door, branded packaging, compliance and air shipping — all in one workflow. Tell us your budget and target country and we will map the timeline.</p>'
'<a class="wa-btn" href="' + wa + '" target="_blank" rel="noopener">💬 Plan my White Friday 2026 stock</a>'
'</div>'
'</div></section>'
    )

BLOG = {
    'saber-2026': {
        'file': 'blog/saber-2026-saudi-buyers-playbook.html',
        'title': 'How to Import to Saudi Arabia Under the 2026 SABER Rules: A Buyer\u2019s Playbook',
        'desc': 'A practical 2026 SABER playbook for small Gulf buyers: 12-digit HS codes, split PC validity, 150+ controlled categories, who files the certificate, and a step-by-step clearance path from a team that clears Saudi goods weekly.',
        'date': '2026-08-24',
        'canonical': BASE + '/blog/saber-2026-saudi-buyers-playbook.html',
        'body': saber_body(),
        'faq': SABER_FAQ,
    },
    'gcc-fta-2026': {
        'file': 'blog/china-gcc-fta-lower-import-duty.html',
        'title': 'How to Use the New China\u2013GCC FTA to Cut Your Gulf Import Duty (2026 Guide for Small Importers)',
        'desc': 'How small Gulf importers actually claim the China\u2013GCC FTA tariff cut: 1,420 HS codes reduced by ~7.4 points, the Certificate of Origin requirement, and a step-by-step checklist from a China sourcing team.',
        'date': '2026-08-24',
        'canonical': BASE + '/blog/china-gcc-fta-lower-import-duty.html',
        'body': fta_body(),
        'faq': FTA_FAQ,
    },
    'tiktok-saudi-2026': {
        'file': 'blog/source-products-tiktok-shop-saudi-no-container.html',
        'title': 'How to Source Products for TikTok Shop Saudi Without a Container (2026 Guide for Influencers and Small Sellers)',
        'desc': 'How Gulf influencers and small sellers source TikTok Shop products from China without a container: low MOQ, samples to your door, private-label packaging, SABER compliance, and air shipping, from a China sourcing team.',
        'date': '2026-08-24',
        'canonical': BASE + '/blog/source-products-tiktok-shop-saudi-no-container.html',
        'body': tiktok_body(),
        'faq': TIKTOK_FAQ,
    },
    'white-friday-2026': {
        'file': 'blog/white-friday-2026-china-gulf-small-business.html',
        'title': 'How to Stock for White Friday 2026 from China (Gulf Small Business Guide)',
        'desc': 'A practical guide for Gulf small sellers sourcing White Friday 2026 stock from China: timeline, best products, samples, private-label packaging, landed cost example, and compliance — from a China sourcing team.',
        'date': '2026-08-26',
        'canonical': BASE + '/blog/white-friday-2026-china-gulf-small-business.html',
        'body': white_friday_body(),
        'faq': WHITE_FRIDAY_FAQ,
    },
}

def faq_block(faq):
    out = ['<section class="sec"><div class="wrap">',
           '<div class="sec-head center"><span class="kicker">FAQ</span><h2>Common Questions</h2>',
           '<p class="sub">Straight answers buyers ask before importing under the new rules.</p></div>',
           '<div class="qa-list">']
    for q, a in faq:
        out.append('<div class="qa"><h3>%s</h3><p>%s</p></div>' % (q, a))
    out.append('</div></div></section>')
    return '\n'.join(out)

def jsonld_for(g):
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": g['title'],
        "description": g['desc'],
        "author": {"@type": "Organization", "name": "SourceToGulf", "url": BASE},
        "publisher": {"@type": "Organization", "name": "SourceToGulf", "url": BASE},
        "datePublished": g['date'],
        "dateModified": g['date'],
        "inLanguage": "en",
        "mainEntityOfPage": {"@type": "WebPage", "@id": g['canonical']},
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in g['faq']
        ],
    }
    return json.dumps([article, faq], ensure_ascii=False, indent=2)

def main():
    for key, g in BLOG.items():
        html = page_shell(
            title=g['title'],
            description=g['desc'],
            canonical=g['canonical'],
            body_inner=g['body'] + '\n' + faq_block(g['faq']),
            json_ld=jsonld_for(g),
        )
        out = os.path.join(APP, g['file'])
        with open(out, 'w', encoding='utf-8') as f:
            f.write(html)
        print('wrote', g['file'], '(%d bytes)' % len(html))

if __name__ == '__main__':
    main()
