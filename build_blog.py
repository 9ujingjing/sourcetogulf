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
