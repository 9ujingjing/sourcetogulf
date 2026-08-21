# -*- coding: utf-8 -*-
"""
build_guides.py — 生成 GCC 国家级"进口支柱页"（GEO 权威长文）
首篇：uae-import-guide-from-china.html
后续沙特/卡塔尔照 GUIDES 字典扩即可（每日真实词驱动的扩展点）。

用法: python3 build_guides.py
"""
import os, json
from tpl_common import page_shell, WA, wa_link

APP = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://sourcetogulf.com'

# ----------------------------------------------------------------------------
# UAE 指南数据
# ----------------------------------------------------------------------------
UAE_FAQ = [
    ('What is the customs duty rate for importing from China to the UAE?',
     'Most goods entering the UAE are charged a 5% customs duty calculated on the CIF value (cost + insurance + freight). A few categories are higher: alcoholic drinks 50%, tobacco 100%, and motor vehicles at specific rates. The 5% standard comes from the GCC Common Customs Law and applies uniformly across emirates.'),
    ('Do I pay VAT on imports to the UAE?',
     'Yes. The UAE applies a 5% VAT on imports, charged on the CIF value plus the customs duty. If your business is VAT-registered you can reclaim this input VAT, so for most traders the effective cost is recovered. VAT is collected by UAE Customs at the point of clearance.'),
    ('Do UAE free zones avoid customs duty?',
     'Goods landed in a UAE free zone such as Jebel Ali (JAFZA), DMCC or DAFZA for storage or re-export are not charged duty. Duty only applies when goods are released into the UAE mainland. Free-zone companies also benefit from 0% corporate tax on qualifying income, making them popular for re-export trading.'),
    ('Is SABER required for the UAE?',
     'No. SABER is a Saudi Arabia requirement. The UAE uses its own Emirates Conformity Assessment System (ECAS) and the G-Mark for regulated products such as toys, electronics and low-voltage equipment. Some goods need a Certificate of Conformity, but the Saudi SABER platform does not apply.'),
    ('What documents are required to clear customs in the UAE?',
     'You need a commercial invoice, packing list, bill of lading or air waybill, and a certificate of origin. Regulated products additionally require an ECAS registration or Certificate of Conformity. Clearance is handled through a licensed UAE customs broker using your import code.'),
    ('How long does UAE customs clearance take?',
     'With complete and correct documents, clearance in Dubai typically takes 1 to 3 working days. Delays come from missing certificates, valuation disputes or restricted-goods licensing. Using an experienced broker and a sourcing agent that pre-checks paperwork keeps the timeline short.'),
    ('Do products need Arabic labels for the UAE?',
     'Bilingual (Arabic + English) labels are strongly recommended and mandatory for food, beverage and health or cosmetic products. The UAE is less strict than Saudi Arabia, but clear Arabic labelling speeds shelf placement and consumer trust in the Gulf market.'),
    ('What is the cheapest way to import small orders from China to the UAE?',
     'For samples and small parcels, express courier (DHL / FedEx / UPS) or Cainiao consolidation is fastest. For larger but sub-container loads, sea freight LCL or air consolidation through a sourcing agent lowers the per-unit cost. Consolidating multiple suppliers into one shipment is usually the biggest saving.'),
]

def faq_block(faq):
    out = ['<section class="sec"><div class="wrap">',
           '<div class="sec-head center"><span class="kicker">FAQ</span><h2>UAE Import — Common Questions</h2>',
           '<p class="sub">Straight answers buyers ask before shipping from China to the UAE.</p></div>',
           '<div class="qa-list">']
    for q, a in faq:
        out.append('<div class="qa"><h3>%s</h3><p>%s</p></div>' % (q, a))
    out.append('</div></div></section>')
    return '\n'.join(out)

def faq_jsonld(faq):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq
        ],
    }

def uae_body():
    wa_guide = wa_link('Hi SourceToGulf! I want to import from China to the UAE. Please help with sourcing, duty and clearance.')
    return '''
<section class="sec hero-sec">
  <div class="wrap">
    <span class="kicker">GCC Import Guide</span>
    <h1>Importing from China to the UAE — The Complete 2026 Guide</h1>
    <p class="lead">Importing from China to the UAE means paying a <b>5%% customs duty on the CIF value</b> plus <b>5%% VAT</b> on most goods — but goods landed in a free zone for re-export avoid duty entirely. A China sourcing agent cuts your landed cost and handles quality checks, consolidation and customs clearance end to end.</p>
    <div class="cta-row">
      <a class="btn-wa" href="%s" target="_blank" rel="noopener">💬 Get a UAE import quote on WhatsApp</a>
      <a class="btn-ghost" href="/#calculator">Estimate landed cost →</a>
    </div>
  </div>
</section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>UAE import duties from China</h2></div>
  <p>The UAE follows the GCC Common Customs Law, so the <b>standard customs duty is 5%% of CIF value</b> (cost + insurance + freight) for the large majority of products. A few categories carry higher rates:</p>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">Product type</th>
      <th style="padding:10px 12px;text-align:left">Customs duty</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">Most goods (electronics, apparel, home, toys)</td><td style="padding:10px 12px"><b>5%% of CIF</b></td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">Alcoholic drinks</td><td style="padding:10px 12px">50%%</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">Tobacco products</td><td style="padding:10px 12px">100%%</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">Motor vehicles</td><td style="padding:10px 12px">Specific rates by type/cc</td></tr>
    </tbody>
  </table>
  <p>Duty is assessed on the CIF value, so a lower freight cost or a sharper factory price directly reduces what you pay at the border.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>VAT in the UAE</h2></div>
  <p>The UAE applies a <b>5%% VAT</b> on imported goods, charged on the CIF value <i>plus</i> the customs duty. If your company is VAT-registered, this input VAT is recoverable — for most traders the net cost is effectively neutral. VAT is collected by UAE Customs at clearance, so budget for it in your landed-cost model.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Free zones vs mainland — which should you use?</h2></div>
  <p>Free zones such as <b>Jebel Ali (JAFZA)</b>, DMCC and DAFZA are the backbone of UAE re-export trade. Understanding the difference protects both duty and tax:</p>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">Free zone (e.g. JAFZA)</th>
      <th style="padding:10px 12px;text-align:left">UAE mainland</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">No duty on goods for storage / re-export</td><td style="padding:10px 12px">5%% duty on CIF when released to market</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">0%% corporate tax on qualifying income</td><td style="padding:10px 12px">9%% corporate tax above AED 375,000 profit</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">100%% foreign ownership allowed</td><td style="padding:10px 12px">Local sponsor rules for some activities</td></tr>
    </tbody>
  </table>
  <p>If you sell <b>into</b> the UAE consumer market, goods cross from the free zone to mainland and duty applies. If you re-export to Africa, the wider Gulf or Saudi, keeping stock in a free zone avoids UAE duty entirely.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>Documents required for UAE customs clearance</h2></div>
  <ul class="bullets">
    <li><b>Commercial invoice</b> — showing value, HS code and party details</li>
    <li><b>Packing list</b> — carton counts, weights, dimensions</li>
    <li><b>Bill of lading / air waybill</b> — the transport document</li>
    <li><b>Certificate of origin</b> — confirms China origin for duty treatment</li>
    <li><b>ECAS registration / Certificate of Conformity</b> — for regulated products (toys, electronics, low-voltage goods)</li>
  </ul>
  <p>Clearance is filed by a licensed UAE customs broker using your import code. A sourcing agent that pre-checks paperwork before departure prevents the most common hold-ups.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Customs clearance time &amp; compliance</h2></div>
  <p>With complete documents, Dubai clearance typically takes <b>1–3 working days</b>. The UAE uses the <b>ECAS</b> system and G-Mark (not Saudi SABER) for product conformity. Plan for longer if goods are restricted, under-valued, or missing certificates. Jebel Ali is the largest port in the Middle East, so sea freight lead times from China are reliable at 18–28 days.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>Best Chinese cities to source from</h2></div>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">City</th>
      <th style="padding:10px 12px;text-align:left">Best for</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Yiwu</b></td><td style="padding:10px 12px">Small commodities, gifts, accessories, low MOQ, mixed consolidation</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px"><b>Guangzhou</b></td><td style="padding:10px 12px">Apparel, bags, beauty, watches, wholesale markets</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Shenzhen</b></td><td style="padding:10px 12px">Electronics, gadgets, tech accessories, fast prototyping</td></tr>
    </tbody>
  </table>
  <p>Most Gulf buyers mix all three. A sourcing agent consolidates from multiple cities into one UAE shipment — often the single biggest cost saving.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>How a sourcing agent lowers your UAE landed cost</h2></div>
  <p>A China-based agent compresses three cost lines at once: sharper <b>factory pricing</b> (direct from manufacturers, not trading companies), <b>consolidation</b> that turns several small parcels into one cheap sea shipment, and <b>pre-shipment QC</b> that stops defective goods before they cross the border and trigger re-export fees. Add transparent duty/VAT modelling and you get a predictable landed cost per unit.</p>
  <div class="rel-grid">
    <a class="rel-card" href="/solutions.html"><span>Solutions by buyer type</span><b>Influencer · Wholesaler · Retailer · Small brand</b></a>
    <a class="rel-card" href="/gcc-import-answers.html"><span>GCC import Q&amp;A</span><b>22 answers on duty, VAT, SABER, MOQ, shipping</b></a>
    <a class="rel-card" href="/category-fashion.html"><span>Fashion &amp; apparel</span><b>Yiwu / Guangzhou sourced, UAE-landed prices</b></a>
    <a class="rel-card" href="/category-tech.html"><span>Tech &amp; electronics</span><b>Shenzhen sourced, ECAS-ready</b></a>
  </div>
</div></section>

<section class="sec alt"><div class="wrap" style="text-align:center">
  <div class="sec-head center"><h2>Ready to import from China to the UAE?</h2></div>
  <p class="sub">Send your product list or idea — get a landed-cost estimate and a clearance-ready plan on WhatsApp.</p>
  <a class="btn-wa" href="%s" target="_blank" rel="noopener">💬 Start my UAE import on WhatsApp</a>
</div></section>
''' % (wa_guide, wa_guide)

# ----------------------------------------------------------------------------
# 沙特阿拉伯 指南数据
# ----------------------------------------------------------------------------
KSA_FAQ = [
    ('What is the customs duty rate for importing from China to Saudi Arabia?',
     'Saudi Arabia applies the GCC Common Customs Law, so the standard customs duty is 5% of the CIF value (cost + insurance + freight) for most goods. Excise categories are much higher: carbonated drinks 50%, and tobacco and energy drinks 100%. Motor vehicles carry specific rates by type. The 5% base is uniform across the Kingdom.'),
    ('Do I pay VAT on imports to Saudi Arabia?',
     'Yes — Saudi Arabia applies a 15% VAT on imports, raised from 5% to 15% on 1 July 2020. It is charged on the CIF value plus the customs duty and collected by ZATCA (Zakat, Tax and Customs Authority) at clearance. VAT-registered businesses can reclaim the input VAT.'),
    ('Is SABER required to import into Saudi Arabia?',
     'Yes, SABER is mandatory. Run by SASO, it requires a PCoC (Product Certificate of Conformity) booked before the order and an SCoC (Shipment Certificate of Conformity) per batch before loading. Without a valid SCoC the shipment cannot clear — SABER is the single biggest compliance step for Saudi imports.'),
     ('Are there free zones in Saudi Arabia like the UAE?',
     'Saudi free zones are newer and narrower than the UAE\'s. The main one is the King Abdullah Economic City (KAEC) special economic zone, with Ras Al Khair, Jazan and a cloud-computing zone added in 2023. Most sectors now allow 100% foreign ownership on the mainland, but retail and some activities still carry restrictions. For re-export, many traders still stage stock in UAE free zones.'),
    ('What documents are required to clear customs in Saudi Arabia?',
     'You need a commercial invoice, packing list, bill of lading or air waybill, and a certificate of origin. Regulated products additionally require a SABER SCoC, and food, beverage, supplements, cosmetics and medical devices require SFDA approval. Clearance is filed by a licensed Saudi customs broker.'),
    ('How long does Saudi customs clearance take?',
     'With complete SABER certificates and correct documents, clearance typically takes 2–5 working days. The usual bottleneck is SABER, not the port. Delays come from missing certificates, wrong HS codes or SFDA licensing for regulated goods.'),
    ('Do products need Arabic labels for Saudi Arabia?',
     'Yes — Arabic labelling is mandatory for most consumer products entering Saudi Arabia under SASO/SABER rules, and required for food, beverage and health or cosmetic items. Clear Arabic labelling and halal certification (where relevant) speed clearance and shelf placement.'),
    ('What is the cheapest way to import small orders from China to Saudi Arabia?',
     'For samples and small parcels, express courier (DHL / FedEx / UPS) is fastest. For larger but sub-container loads, sea freight LCL or air consolidation through a sourcing agent lowers per-unit cost. Consolidating multiple suppliers and pre-booking SABER early is usually the biggest saving.'),
]

def ksa_body():
    wa_ksa = wa_link('Hi SourceToGulf! I want to import from China to Saudi Arabia. Please help with sourcing, SABER and clearance.')
    return '''
<section class="sec hero-sec">
  <div class="wrap">
    <span class="kicker">GCC Import Guide</span>
    <h1>Importing from China to Saudi Arabia — The Complete 2026 Guide</h1>
    <p class="lead">Importing from China to Saudi Arabia means a <b>5%% customs duty on the CIF value</b> plus a <b>15%% VAT</b> on most goods — and, unlike the UAE, Saudi requires <b>SABER conformity certificates (PCoC + SCoC)</b> before goods can clear. A China sourcing agent handles pricing, consolidation and the SABER paperwork end to end.</p>
    <div class="cta-row">
      <a class="btn-wa" href="%s" target="_blank" rel="noopener">💬 Get a Saudi import quote on WhatsApp</a>
      <a class="btn-ghost" href="/#calculator">Estimate landed cost →</a>
    </div>
  </div>
</section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Saudi import duties from China</h2></div>
  <p>Saudi Arabia applies the GCC Common Customs Law, so the <b>standard customs duty is 5%% of CIF value</b> (cost + insurance + freight) for most products. Excise goods are far higher:</p>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">Product type</th>
      <th style="padding:10px 12px;text-align:left">Customs duty</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">Most goods (electronics, apparel, home, toys)</td><td style="padding:10px 12px"><b>5%% of CIF</b></td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">Carbonated drinks</td><td style="padding:10px 12px">50%%</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">Tobacco &amp; energy drinks</td><td style="padding:10px 12px">100%%</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">Motor vehicles</td><td style="padding:10px 12px">Specific rates by type/cc</td></tr>
    </tbody>
  </table>
  <p>Duty is assessed on CIF, so a sharper factory price and lower freight both reduce what you pay at the border.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>VAT in Saudi Arabia</h2></div>
  <p>Saudi Arabia applies a <b>15%% VAT</b> on imported goods — raised from 5%% to 15%% on 1 July 2020 — charged on the CIF value <i>plus</i> the customs duty. If your company is VAT-registered in the Kingdom, this input VAT is recoverable. Budget for the 15%% gross in your landed-cost model; it is collected by the Zakat, Tax and Customs Authority (ZATCA) at clearance.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>SABER is mandatory — plan for it before shipping</h2></div>
  <p>Unlike the UAE, Saudi clearance depends on the <b>SABER</b> platform run by <b>SASO</b> (Saudi Standards, Metrology and Quality Organization). You need two certificates:</p>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">Certificate</th>
      <th style="padding:10px 12px;text-align:left">When</th>
      <th style="padding:10px 12px;text-align:left">What it covers</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>PCoC</b> (Product CoC)</td><td style="padding:10px 12px">Before order / per product model</td><td style="padding:10px 12px">Confirms the product meets SASO technical regulations</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px"><b>SCoC</b> (Shipment CoC)</td><td style="padding:10px 12px">Per shipment, before loading</td><td style="padding:10px 12px">Confirms this batch matches the PCoC; required to clear</td></tr>
    </tbody>
  </table>
  <p>SABER is the single biggest difference from UAE imports. Missing or wrong certificates block clearance entirely. A sourcing agent that pre-checks HS codes and books SABER early prevents costly holds at Jeddah or Dammam port.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>Documents required for Saudi customs clearance</h2></div>
  <ul class="bullets">
    <li><b>Commercial invoice</b> — value, HS code, party details (Arabic not required on invoice, but product data must be clear)</li>
    <li><b>Packing list</b> — carton counts, weights, dimensions</li>
    <li><b>Bill of lading / air waybill</b> — transport document</li>
    <li><b>Certificate of origin</b> — confirms China origin</li>
    <li><b>SABER SCoC</b> — mandatory shipment certificate for regulated products</li>
    <li><b>SFDA approval</b> — for food, beverage, supplements, cosmetics, medical devices</li>
  </ul>
  <p>Clearance is filed by a licensed Saudi customs broker. Pre-checking paperwork before the goods leave China is the main way to avoid port demurrage.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Customs clearance time &amp; ports</h2></div>
  <p>With complete SABER and documents, Saudi clearance typically takes <b>2–5 working days</b>. The main ports are <b>Jeddah Islamic Port</b> on the Red Sea (west, serves Makkah and Riyadh via inland) and <b>King Abdulaziz Port, Dammam</b> on the Gulf (east). Sea freight from China runs about 18–30 days. SABER is the usual bottleneck — not the port itself.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>Free zones &amp; foreign ownership in Saudi</h2></div>
  <p>Saudi Arabia's free-zone offer is newer and narrower than the UAE's. The headline option is the <b>King Abdullah Economic City (KAEC)</b> special economic zone, with others (Ras Al Khair, Jazan and a cloud-computing zone) added in 2023. Most sectors now allow <b>100%% foreign ownership</b> on the mainland, but retail and a few activities still carry restrictions. For re-export, Saudi free zones are less mature than JAFZA, so many Gulf traders still stage stock in the UAE.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Best Chinese cities to source from</h2></div>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">City</th>
      <th style="padding:10px 12px;text-align:left">Best for</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Yiwu</b></td><td style="padding:10px 12px">Small commodities, gifts, accessories, low MOQ, mixed consolidation</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px"><b>Guangzhou</b></td><td style="padding:10px 12px">Apparel, bags, beauty, watches, wholesale markets</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Shenzhen</b></td><td style="padding:10px 12px">Electronics, gadgets, tech accessories, fast prototyping</td></tr>
    </tbody>
  </table>
  <p>Most Gulf buyers mix all three. A sourcing agent consolidates from multiple cities into one Saudi shipment — and pre-books SABER so it clears on arrival.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>How a sourcing agent lowers your Saudi landed cost</h2></div>
  <p>A China-based agent compresses three cost lines: sharper <b>factory pricing</b> (direct from manufacturers), <b>consolidation</b> that turns several parcels into one sea shipment, and <b>pre-shipment QC</b> that stops defects before SABER inspection. Critically, the agent pre-books SABER PCoC/SCoC and matches HS codes — turning Saudi's hardest compliance step into a planned task rather than a port-side surprise.</p>
  <div class="rel-grid">
    <a class="rel-card" href="/solutions.html"><span>Solutions by buyer type</span><b>Influencer · Wholesaler · Retailer · Small brand</b></a>
    <a class="rel-card" href="/gcc-import-answers.html"><span>GCC import Q&amp;A</span><b>22 answers on duty, VAT, SABER, MOQ, shipping</b></a>
    <a class="rel-card" href="/category-fashion.html"><span>Fashion &amp; apparel</span><b>Guangzhou sourced, SABER-ready</b></a>
    <a class="rel-card" href="/category-tech.html"><span>Tech &amp; electronics</span><b>Shenzhen sourced, SASO-ready</b></a>
  </div>
</div></section>

<section class="sec"><div class="wrap" style="text-align:center">
  <div class="sec-head center"><h2>Ready to import from China to Saudi Arabia?</h2></div>
  <p class="sub">Send your product list — get a landed-cost estimate, SABER plan and clearance-ready shipment on WhatsApp.</p>
  <a class="btn-wa" href="%s" target="_blank" rel="noopener">💬 Start my Saudi import on WhatsApp</a>
</div></section>
''' % (wa_ksa, wa_ksa)

# ----------------------------------------------------------------------------
# 卡塔尔 指南数据
# ----------------------------------------------------------------------------
QATAR_FAQ = [
    ('What is the customs duty rate for importing from China to Qatar?',
     'Qatar applies the GCC Common Customs Law, so the standard customs duty is 5% of the CIF value (cost + insurance + freight) for most goods. A few categories are higher (tobacco 100%, alcohol prohibited), but the 5% base covers electronics, apparel, home goods and toys — the typical Gulf buyer mix.'),
    ('Is there VAT on imports to Qatar?',
     'As of 2026, Qatar has not introduced a standard VAT on imports — the main import cost is the 5% GCC customs duty. Qatar signed the GCC Unified VAT Agreement in 2016 (committing to a standard rate of at least 5%) and approved a draft e-invoicing law in May 2026 as pre-VAT groundwork, with industry estimates pointing to a possible 2027 rollout; none of it is live yet. Qatar\'s tax framework is managed by the General Tax Authority (GTA, gta.gov.qa) — always confirm the current rate there before budgeting.'),
    ('Is SABER required for Qatar?',
     'No. SABER is a Saudi requirement. Qatar uses its own customs and product-conformity process — regulated goods generally need a Certificate of Conformity against GCC standards, handled through Qatar Customs. The Saudi SABER platform does not apply.'),
    ('Are there free zones in Qatar?',
     'Yes — Qatar Free Zones (QFZ) operates two zones: Ras Bufontas Free Zone (next to Hamad International Airport) and Umm Alhoul Free Zone (next to Hamad Port). Goods landed there for storage or re-export are not charged the 5% duty; duty applies when released into the Qatari mainland.'),
    ('What documents are required to clear customs in Qatar?',
     'You need a commercial invoice, packing list, bill of lading or air waybill, and a certificate of origin. Regulated products require a Certificate of Conformity; food and health items need the relevant authority approvals. Clearance is filed by a licensed Qatari customs broker.'),
    ('How long does Qatar customs clearance take?',
     'With complete documents, clearance through Hamad Port or Doha typically takes 2–4 working days. Delays come from missing certificates or valuation queries. Qatar is a small, concentrated market (most volume lands at Hamad Port), so lead times are predictable.'),
    ('Do products need Arabic labels for Qatar?',
     'Bilingual (Arabic + English) labels are recommended and mandatory for food, beverage and health or cosmetic products. As with the wider Gulf, clear Arabic labelling speeds shelf placement and consumer trust.'),
    ('What is the cheapest way to import small orders from China to Qatar?',
     'For samples and small parcels, express courier is fastest. For larger loads, sea freight LCL or air consolidation through a sourcing agent lowers per-unit cost. Because Qatar is a smaller market, many buyers consolidate via a UAE free zone and re-ship, or consolidate multiple Chinese suppliers into one Qatar-bound container.'),
]

def qatar_body():
    wa_qa = wa_link('Hi SourceToGulf! I want to import from China to Qatar. Please help with sourcing, duty and clearance.')
    return '''
<section class="sec hero-sec">
  <div class="wrap">
    <span class="kicker">GCC Import Guide</span>
    <h1>Importing from China to Qatar — The Complete 2026 Guide</h1>
    <p class="lead">Importing from China to Qatar means a <b>5%% customs duty on the CIF value</b> for most goods — as of 2026 Qatar has not introduced a standard VAT, so the 5%% duty is usually the main border cost. A China sourcing agent handles pricing, consolidation and clearance into Hamad Port.</p>
    <div class="cta-row">
      <a class="btn-wa" href="%s" target="_blank" rel="noopener">💬 Get a Qatar import quote on WhatsApp</a>
      <a class="btn-ghost" href="/#calculator">Estimate landed cost →</a>
    </div>
  </div>
</section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Qatar import duties from China</h2></div>
  <p>Qatar applies the GCC Common Customs Law, so the <b>standard customs duty is 5%% of CIF value</b> (cost + insurance + freight) for most products. As with other GCC states, a few categories are higher:</p>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">Product type</th>
      <th style="padding:10px 12px;text-align:left">Customs duty</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">Most goods (electronics, apparel, home, toys)</td><td style="padding:10px 12px"><b>5%% of CIF</b></td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">Tobacco products</td><td style="padding:10px 12px">100%%</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">Alcoholic drinks</td><td style="padding:10px 12px">Prohibited</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">Motor vehicles</td><td style="padding:10px 12px">Specific rates by type/cc</td></tr>
    </tbody>
  </table>
  <p>Duty is assessed on CIF, so a sharper factory price and lower freight both reduce the border cost.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>VAT in Qatar</h2></div>
  <p>As of 2026, <b>Qatar has not introduced a standard VAT</b> on imports — the main import cost is the 5%% GCC customs duty. Qatar signed the GCC Unified VAT Agreement in 2016 (committing to a standard rate of at least 5%%) and approved a draft e-invoicing law in May 2026 as pre-VAT groundwork, with industry estimates pointing to a possible 2027 rollout. None of it is live yet. Qatar\'s tax framework is managed by the <b>General Tax Authority (GTA, gta.gov.qa)</b> — always confirm the current rate there before you budget a large order.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Free zones vs mainland</h2></div>
  <p>Qatar runs two free zones under <b>Qatar Free Zones (QFZ)</b>: <b>Ras Bufontas</b> (next to Hamad International Airport) and <b>Umm Alhoul</b> (next to Hamad Port). Goods landed there for storage or re-export are not charged the 5%% duty; duty applies when goods are released into the Qatari mainland.</p>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">Free zone (QFZ)</th>
      <th style="padding:10px 12px;text-align:left">Qatar mainland</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">No duty on goods for storage / re-export</td><td style="padding:10px 12px">5%% duty on CIF when released to market</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">100%% foreign ownership allowed</td><td style="padding:10px 12px">Local rules for some activities</td></tr>
    </tbody>
  </table>
  <p>For re-export to the wider Gulf or beyond, keeping stock in a QFZ avoids Qatari duty. For the local Doha market, goods cross to mainland and the 5%% applies.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>Documents required for Qatar customs clearance</h2></div>
  <ul class="bullets">
    <li><b>Commercial invoice</b> — value, HS code, party details</li>
    <li><b>Packing list</b> — carton counts, weights, dimensions</li>
    <li><b>Bill of lading / air waybill</b> — transport document</li>
    <li><b>Certificate of origin</b> — confirms China origin</li>
    <li><b>Certificate of Conformity</b> — for regulated products against GCC standards</li>
  </ul>
  <p>Clearance is filed by a licensed Qatari customs broker. Pre-checking paperwork before departure prevents the most common holds at Hamad Port.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Customs clearance time &amp; ports</h2></div>
  <p>With complete documents, Qatar clearance typically takes <b>2–4 working days</b>. The main gateway is <b>Hamad Port</b> (opened 2017, replacing the old Doha Port) on the Gulf coast, supplemented by Hamad International Airport for air freight. Sea freight from China runs about 18–28 days. Qatar is a small, concentrated market, so lead times are predictable.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>Best Chinese cities to source from</h2></div>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">City</th>
      <th style="padding:10px 12px;text-align:left">Best for</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Yiwu</b></td><td style="padding:10px 12px">Small commodities, gifts, accessories, low MOQ, mixed consolidation</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px"><b>Guangzhou</b></td><td style="padding:10px 12px">Apparel, bags, beauty, watches, wholesale markets</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Shenzhen</b></td><td style="padding:10px 12px">Electronics, gadgets, tech accessories, fast prototyping</td></tr>
    </tbody>
  </table>
  <p>Most Gulf buyers mix all three. A sourcing agent consolidates from multiple cities into one Qatar-bound shipment — often the single biggest saving for a smaller market like Qatar.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>How a sourcing agent lowers your Qatar landed cost</h2></div>
  <p>A China-based agent compresses three cost lines: sharper <b>factory pricing</b> (direct from manufacturers), <b>consolidation</b> that turns several parcels into one sea shipment, and <b>pre-shipment QC</b> that stops defects before they cross the border. For Qatar\'s compact market, consolidation is especially valuable — it pools small orders into one efficient container rather than paying for several partial loads.</p>
  <div class="rel-grid">
    <a class="rel-card" href="/solutions.html"><span>Solutions by buyer type</span><b>Influencer · Wholesaler · Retailer · Small brand</b></a>
    <a class="rel-card" href="/gcc-import-answers.html"><span>GCC import Q&amp;A</span><b>22 answers on duty, VAT, SABER, MOQ, shipping</b></a>
    <a class="rel-card" href="/category-fashion.html"><span>Fashion &amp; apparel</span><b>Guangzhou sourced, Qatar-landed prices</b></a>
    <a class="rel-card" href="/category-tech.html"><span>Tech &amp; electronics</span><b>Shenzhen sourced, GCC-ready</b></a>
  </div>
</div></section>

<section class="sec alt"><div class="wrap" style="text-align:center">
  <div class="sec-head center"><h2>Ready to import from China to Qatar?</h2></div>
  <p class="sub">Send your product list — get a landed-cost estimate and a clearance-ready plan on WhatsApp.</p>
  <a class="btn-wa" href="%s" target="_blank" rel="noopener">💬 Start my Qatar import on WhatsApp</a>
</div></section>
''' % (wa_qa, wa_qa)

# ----------------------------------------------------------------------------
# 科威特 指南数据
# ----------------------------------------------------------------------------
KUWAIT_FAQ = [
    ('What is the customs duty rate for importing from China to Kuwait?',
     'Kuwait applies the GCC Common Customs Law, so the standard customs duty is 5% of the CIF value (cost + insurance + freight) for most goods. A few categories are higher: tobacco carries 100% duty and excise adds 100% on electronic smoking devices and energy drinks and 50% on carbonated sugary drinks. The 5% base covers electronics, apparel, home goods and toys — the typical Gulf buyer mix.'),
    ('Does Kuwait charge VAT on imports?',
     'No. As of 2026, Kuwait has not introduced VAT, so there is no tax layer on imports — only the 5% customs duty. The UAE charges 5% VAT and Saudi Arabia 15%, so importing into Kuwait saves that entire percentage off your landed cost. Kuwait signed the GCC VAT agreement but has not implemented it; confirm any future change with the Kuwait Ministry of Finance.'),
    ('Is KUCAS required to import into Kuwait?',
     'KUCAS (Kuwait Conformity Assessment Scheme, also written KCAS) is run by the Public Authority for Industry (PAI). It covers a shorter product list than Saudi SABER — mainly electronics, electrical equipment, toys, lighting and some home appliances. Regulated products need a Certificate of Conformity (CoC) from an approved body (TUV, Intertek, SGS) before shipment; most general merchandise ships without one. There is no SABER-style per-shipment certificate for Kuwait.'),
    ('Are there free zones in Kuwait?',
     'Kuwait\'s main free zone is the Kuwait Free Trade Zone (KFTZ) at Shuwaikh. Goods landed there for storage or re-export are not charged the 5% duty; duty applies when released into the Kuwaiti mainland. Foreign ownership is permitted for licensed activities inside the zone.'),
    ('What documents are required to clear customs in Kuwait?',
     'You need a commercial invoice, packing list, bill of lading or air waybill, and a certificate of origin (issued by CCPIT or the Chamber of Commerce, sometimes legalised at the Kuwaiti embassy). Regulated products require a KUCAS CoC. Clearance is filed by a licensed Kuwaiti customs broker. Every product unit must also carry a permanent "Made in China" marking — embossed, printed or engraved, not a sticker.'),
    ('How long does Kuwait customs clearance take?',
     'With complete documents, clearance through Shuwaikh or Shuaiba typically takes 3–7 working days. Since February 2026 all commercial ports run 24-hour radiation-monitoring gates, so electronics or mineral-based goods should carry material-safety paperwork to avoid false-alert holds. The usual delays come from missing KUCAS certificates or embassy-legalisation gaps.'),
    ('Do products need Arabic labels for Kuwait?',
     'Yes — products must carry Arabic or bilingual (Arabic + English) labels. Food, beverage and health or cosmetic items require Arabic labelling, and a permanent "Made in China" origin mark is mandatory on each unit. Clear Arabic labelling speeds clearance and shelf placement in the Kuwaiti market.'),
    ('What is the cheapest way to import small orders from China to Kuwait?',
     'For samples and small parcels, express courier is fastest. For larger but sub-container loads, sea freight LCL or air consolidation through a sourcing agent lowers per-unit cost. Because Kuwait has no VAT, landed cost is simpler to model than in the UAE or Saudi — consolidation is usually the single biggest saving.'),
]

def kuwait_body():
    wa_kw = wa_link('Hi SourceToGulf! I want to import from China to Kuwait. Please help with sourcing, KUCAS and clearance.')
    return '''
<section class="sec hero-sec">
  <div class="wrap">
    <span class="kicker">GCC Import Guide</span>
    <h1>Importing from China to Kuwait — The Complete 2026 Guide</h1>
    <p class="lead">Importing from China to Kuwait means a <b>5%% customs duty on the CIF value</b> — and, unlike the UAE or Saudi, Kuwait has <b>no VAT</b>, so the 5%% duty is the only border tax. The main compliance step is KUCAS conformity for regulated goods. A China sourcing agent handles pricing, consolidation and KUCAS paperwork end to end.</p>
    <div class="cta-row">
      <a class="btn-wa" href="%s" target="_blank" rel="noopener">💬 Get a Kuwait import quote on WhatsApp</a>
      <a class="btn-ghost" href="/#calculator">Estimate landed cost →</a>
    </div>
  </div>
</section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Kuwait import duties from China</h2></div>
  <p>Kuwait applies the GCC Common Customs Law, so the <b>standard customs duty is 5%% of CIF value</b> (cost + insurance + freight) for most products. A few categories carry higher rates:</p>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">Product type</th>
      <th style="padding:10px 12px;text-align:left">Customs duty</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">Most goods (electronics, apparel, home, toys)</td><td style="padding:10px 12px"><b>5%% of CIF</b></td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">Tobacco products</td><td style="padding:10px 12px">100%%</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">Carbonated sugary drinks (excise)</td><td style="padding:10px 12px">50%%</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">Electronic smoking devices / energy drinks (excise)</td><td style="padding:10px 12px">100%%</td></tr>
    </tbody>
  </table>
  <p>Duty is assessed on CIF, so a sharper factory price and lower freight both reduce what you pay at the border — and with no VAT, that duty is the whole tax story.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>VAT in Kuwait</h2></div>
  <p>As of 2026, <b>Kuwait has not introduced VAT</b> — the only import tax is the 5%% GCC customs duty. The UAE (5%%) and Saudi Arabia (15%%) both add a VAT layer, so Kuwait offers the lowest import-tax load in the Gulf. Budget purely on CIF × 5%%. Kuwait signed the GCC Unified VAT Agreement but has not implemented it; always confirm the current position with the Kuwait Ministry of Finance before a large order.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>KUCAS conformity (not SABER)</h2></div>
  <p>Kuwait uses <b>KUCAS</b> (Kuwait Conformity Assessment Scheme, also written KCAS), run by the <b>Public Authority for Industry (PAI)</b>. It covers a <b>shorter list than Saudi SABER</b> — mainly electronics, electrical equipment, toys, lighting and some home appliances. Regulated products need a <b>Certificate of Conformity (CoC)</b> from an approved body (TUV, Intertek, SGS) before shipment; most general merchandise ships without one. There is no SABER-style per-shipment SCoC for Kuwait.</p>
  <p>Two Kuwait-specific rules matter: every product unit must carry a <b>permanent "Made in China" marking</b> (embossed, printed or engraved — adhesive stickers are often rejected), and the certificate of origin is sometimes legalised at the Kuwaiti embassy. A sourcing agent that pre-books KUCAS and checks marking before production prevents port holds.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>Free zones vs mainland</h2></div>
  <p>Kuwait's main free zone is the <b>Kuwait Free Trade Zone (KFTZ)</b> at Shuwaikh. Goods landed there for storage or re-export are not charged the 5%% duty; duty applies when goods are released into the Kuwaiti mainland.</p>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">Free zone (KFTZ, Shuwaikh)</th>
      <th style="padding:10px 12px;text-align:left">Kuwait mainland</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">No duty on goods for storage / re-export</td><td style="padding:10px 12px">5%% duty on CIF when released to market</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">Foreign ownership for licensed activities</td><td style="padding:10px 12px">Local rules for some activities</td></tr>
    </tbody>
  </table>
  <p>For re-export to the wider Gulf or beyond, keeping stock in the KFTZ avoids Kuwaiti duty. For the local Kuwait City market, goods cross to mainland and the 5%% applies.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Documents required for Kuwait customs clearance</h2></div>
  <ul class="bullets">
    <li><b>Commercial invoice</b> — value, 12-digit HS code, party details</li>
    <li><b>Packing list</b> — carton counts, weights, dimensions</li>
    <li><b>Bill of lading / air waybill</b> — transport document</li>
    <li><b>Certificate of origin</b> — CCPIT or Chamber of Commerce, sometimes embassy-legalised</li>
    <li><b>KUCAS Certificate of Conformity</b> — for regulated products (electronics, toys, electrical)</li>
    <li><b>Permanent "Made in China" mark</b> — on each product unit, not just the carton</li>
  </ul>
  <p>Clearance is filed by a licensed Kuwaiti customs broker. Pre-checking paperwork and KUCAS before departure prevents the most common holds at Shuwaikh.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>Customs clearance time &amp; ports</h2></div>
  <p>With complete documents, Kuwait clearance typically takes <b>3–7 working days</b>. The main gateways are <b>Shuwaikh Port</b> (near Kuwait City, general commercial and consumer cargo) and <b>Shuaiba Port</b> (about 40 km south, industrial goods, heavy machinery, bulk). Kuwait International Airport handles air freight. Since 17 February 2026, all commercial ports run <b>24-hour radiation-monitoring gates</b> — carry material-safety docs for electronics or mineral goods to avoid false-alert holds. Sea freight from China runs about 20–30 days.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Best Chinese cities to source from</h2></div>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">City</th>
      <th style="padding:10px 12px;text-align:left">Best for</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Yiwu</b></td><td style="padding:10px 12px">Small commodities, gifts, accessories, low MOQ, mixed consolidation</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px"><b>Guangzhou</b></td><td style="padding:10px 12px">Apparel, bags, beauty, watches, wholesale markets</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Shenzhen</b></td><td style="padding:10px 12px">Electronics, gadgets, tech accessories, fast prototyping</td></tr>
    </tbody>
  </table>
  <p>Most Gulf buyers mix all three. A sourcing agent consolidates from multiple cities into one Kuwait-bound shipment — often the single biggest saving, made simpler by Kuwait's zero-VAT model.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>How a sourcing agent lowers your Kuwait landed cost</h2></div>
  <p>A China-based agent compresses three cost lines: sharper <b>factory pricing</b> (direct from manufacturers), <b>consolidation</b> that turns several parcels into one sea shipment, and <b>pre-shipment QC</b> that stops defects before they cross the border. For Kuwait, the agent also pre-books KUCAS CoC and verifies the "Made in China" marking — turning the one real compliance step into a planned task rather than a port-side surprise.</p>
  <div class="rel-grid">
    <a class="rel-card" href="/solutions.html"><span>Solutions by buyer type</span><b>Influencer · Wholesaler · Retailer · Small brand</b></a>
    <a class="rel-card" href="/gcc-import-answers.html"><span>GCC import Q&amp;A</span><b>22 answers on duty, VAT, KUCAS, MOQ, shipping</b></a>
    <a class="rel-card" href="/category-fashion.html"><span>Fashion &amp; apparel</span><b>Guangzhou sourced, Kuwait-landed prices</b></a>
    <a class="rel-card" href="/category-tech.html"><span>Tech &amp; electronics</span><b>Shenzhen sourced, KUCAS-ready</b></a>
    <a class="rel-card" href="/blog/how-to-import-from-china-to-kuwait.html"><span>Kuwait import — blog version</span><b>Step-by-step short guide (2026)</b></a>
  </div>
</div></section>

<section class="sec"><div class="wrap" style="text-align:center">
  <div class="sec-head center"><h2>Ready to import from China to Kuwait?</h2></div>
  <p class="sub">Send your product list — get a landed-cost estimate (no VAT to model) and a KUCAS-ready plan on WhatsApp.</p>
  <a class="btn-wa" href="%s" target="_blank" rel="noopener">💬 Start my Kuwait import on WhatsApp</a>
</div></section>
''' % (wa_kw, wa_kw)

# ----------------------------------------------------------------------------
# 巴林 指南数据
# ----------------------------------------------------------------------------
BAHRAIN_FAQ = [
    ('What is the customs duty rate for importing from China to Bahrain?',
     'Bahrain applies the GCC Common Customs Law, so the standard customs duty is 5% of the CIF value (cost + insurance + freight) for most goods. A few categories are higher: tobacco and alcohol face heavy excise taxes up to 100%. The 5% base covers electronics, apparel, home goods and toys.'),
    ('Does Bahrain charge VAT on imports?',
     'Yes — Bahrain applies a 10% VAT on imports. It was introduced at 5% and later raised to 10%, so Bahrain now has the second-highest VAT in the GCC after Saudi Arabia\'s 15%. It is charged on the CIF value plus the customs duty and collected by the National Bureau of Revenue at clearance. Combined with the 5% duty, the tax load is about 15% — higher than the UAE\'s ~10.25% but lower than Saudi\'s ~20.25%.'),
    ('Is SABER required to import into Bahrain?',
     'No. Bahrain has no SABER-style platform. It enforces GSO (GCC Standardization Organization) conformity through the OFOQ electronic single window run by Bahrain Customs Affairs. Regulated products need a Certificate of Conformity, but the list is shorter than Saudi SABER and there is no per-shipment SCoC requirement. Clearance is generally lighter than Saudi.'),
    ('Are there free zones in Bahrain?',
     'Yes — Bahrain offers the Bahrain Logistics Zone and the Bahrain International Investment Park (BIIP). Goods held for re-export are not charged duty; duty applies on release to the local market. Bahrain allows 100% foreign ownership for most activities, making it attractive for Gulf re-export and regional headquarters.'),
    ('What documents are required to clear customs in Bahrain?',
     'You need a commercial invoice, packing list, bill of lading or air waybill, and a certificate of origin. The invoice and certificate of origin often need Chamber of Commerce stamping or legalisation. Regulated products require a Certificate of Conformity. Clearance is filed through OFOQ by a licensed Bahraini customs broker.'),
    ('How long does Bahrain customs clearance take?',
     'With complete documents, clearance through Khalifa Bin Salman Port or Bahrain International Airport typically takes 1–3 working days via the OFOQ system. Bahrain is an island linked to Saudi Arabia by the King Fahd Causeway, so many shipments also arrive by feeder vessel or truck from Dammam or Jebel Ali. Sea freight from China runs about 18–30 days.'),
    ('Do products need Arabic labels for Bahrain?',
     'Bilingual (Arabic + English) labels are recommended and mandatory for food, beverage and health or cosmetic products. Arabic labelling speeds clearance and builds consumer trust in the Bahraini market.'),
    ('What is the cheapest way to import small orders from China to Bahrain?',
     'For samples and small parcels, express courier is fastest. For larger but sub-container loads, sea freight LCL or air consolidation through a sourcing agent lowers per-unit cost. Because Bahrain is small and central, consolidation via a UAE or Saudi hub before the short feeder crossing is common.'),
]

def bahrain_body():
    wa_bh = wa_link('Hi SourceToGulf! I want to import from China to Bahrain. Please help with sourcing, duty and clearance.')
    return '''
<section class="sec hero-sec">
  <div class="wrap">
    <span class="kicker">GCC Import Guide</span>
    <h1>Importing from China to Bahrain — The Complete 2026 Guide</h1>
    <p class="lead">Importing from China to Bahrain means a <b>5%% customs duty on the CIF value</b> plus a <b>10%% VAT</b> — Bahrain's VAT is 10%% (raised from 5%%), the highest in the GCC after Saudi. But there is <b>no SABER-style conformity</b>, so clearance is lighter than Saudi. A China sourcing agent handles pricing, consolidation and OFOQ clearance end to end.</p>
    <div class="cta-row">
      <a class="btn-wa" href="%s" target="_blank" rel="noopener">💬 Get a Bahrain import quote on WhatsApp</a>
      <a class="btn-ghost" href="/#calculator">Estimate landed cost →</a>
    </div>
  </div>
</section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Bahrain import duties from China</h2></div>
  <p>Bahrain applies the GCC Common Customs Law, so the <b>standard customs duty is 5%% of CIF value</b> (cost + insurance + freight) for most products. A few categories carry higher rates:</p>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">Product type</th>
      <th style="padding:10px 12px;text-align:left">Customs duty</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">Most goods (electronics, apparel, home, toys)</td><td style="padding:10px 12px"><b>5%% of CIF</b></td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">Tobacco &amp; alcohol (excise)</td><td style="padding:10px 12px">Up to 100%%</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">Motor vehicles</td><td style="padding:10px 12px">Specific rates by type/cc</td></tr>
    </tbody>
  </table>
  <p>Duty is assessed on CIF, so a sharper factory price and lower freight both reduce what you pay at the border.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>VAT in Bahrain</h2></div>
  <p>Bahrain applies a <b>10%% VAT</b> on imported goods — introduced at 5%% and later raised to 10%%, the second-highest in the GCC after Saudi Arabia's 15%%. It is charged on the CIF value <i>plus</i> the customs duty and collected by the National Bureau of Revenue at clearance. Combined with the 5%% duty, the effective tax load is about <b>15%%</b> — higher than the UAE's ~10.25%% but lower than Saudi's ~20.25%%. Budget for the combined rate in your landed-cost model.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Conformity via OFOQ — no SABER</h2></div>
  <p>Unlike Saudi Arabia, Bahrain has <b>no SABER platform</b>. It enforces <b>GSO (GCC Standardization Organization)</b> conformity through the <b>OFOQ</b> electronic single window run by Bahrain Customs Affairs. Regulated products need a <b>Certificate of Conformity</b>, but the list is shorter than Saudi SABER and there is no per-shipment SCoC requirement. For most general merchandise, the only steps are the 5%% duty and 10%% VAT — making Bahrain clearance lighter than Saudi.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>Free zones &amp; foreign ownership</h2></div>
  <p>Bahrain offers the <b>Bahrain Logistics Zone</b> and the <b>Bahrain International Investment Park (BIIP)</b>. Goods held for storage or re-export are not charged duty; duty applies when released to the local market. Bahrain allows <b>100%% foreign ownership</b> for most activities, making it attractive for Gulf re-export and regional headquarters.</p>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">Free zone (Logistics Zone / BIIP)</th>
      <th style="padding:10px 12px;text-align:left">Bahrain mainland</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">No duty on goods for storage / re-export</td><td style="padding:10px 12px">5%% duty + 10%% VAT on CIF when released</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">100%% foreign ownership</td><td style="padding:10px 12px">Local rules for some activities</td></tr>
    </tbody>
  </table>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Documents required for Bahrain customs clearance</h2></div>
  <ul class="bullets">
    <li><b>Commercial invoice</b> — value, HS code, party details (often Chamber-stamped)</li>
    <li><b>Packing list</b> — carton counts, weights, dimensions</li>
    <li><b>Bill of lading / air waybill</b> — transport document</li>
    <li><b>Certificate of origin</b> — often legalised by the Chamber of Commerce</li>
    <li><b>Certificate of Conformity</b> — for regulated products</li>
  </ul>
  <p>Clearance is filed through OFOQ by a licensed Bahraini customs broker. Accurate HS codes and legalised documents prevent the most common holds at KBSP.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>Customs clearance time &amp; ports</h2></div>
  <p>With complete documents, Bahrain clearance typically takes <b>1–3 working days</b> via the OFOQ system. The main gateway is <b>Khalifa Bin Salman Port (KBSP)</b> in Hidd (about 1.4 million TEU capacity, operated by APM Terminals), supplemented by <b>Bahrain International Airport</b>. Bahrain is an island linked to Saudi Arabia by the <b>King Fahd Causeway</b>, so many shipments also arrive by feeder vessel or truck from Dammam or Jebel Ali. Sea freight from China runs about 18–30 days.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Best Chinese cities to source from</h2></div>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">City</th>
      <th style="padding:10px 12px;text-align:left">Best for</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Yiwu</b></td><td style="padding:10px 12px">Small commodities, gifts, accessories, low MOQ, mixed consolidation</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px"><b>Guangzhou</b></td><td style="padding:10px 12px">Apparel, bags, beauty, watches, wholesale markets</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Shenzhen</b></td><td style="padding:10px 12px">Electronics, gadgets, tech accessories, fast prototyping</td></tr>
    </tbody>
  </table>
  <p>Most Gulf buyers mix all three. A sourcing agent consolidates from multiple cities into one Bahrain-bound shipment — and clears it through OFOQ without SABER friction.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>How a sourcing agent lowers your Bahrain landed cost</h2></div>
  <p>A China-based agent compresses three cost lines: sharper <b>factory pricing</b> (direct from manufacturers), <b>consolidation</b> that turns several parcels into one sea shipment, and <b>pre-shipment QC</b> that stops defects before they ship. For Bahrain, the agent also pre-checks HS codes and legalises documents so OFOQ clearance runs in 1–3 days — keeping the 5%% duty + 10%% VAT model predictable.</p>
  <div class="rel-grid">
    <a class="rel-card" href="/solutions.html"><span>Solutions by buyer type</span><b>Influencer · Wholesaler · Retailer · Small brand</b></a>
    <a class="rel-card" href="/gcc-import-answers.html"><span>GCC import Q&amp;A</span><b>22 answers on duty, VAT, OFOQ, MOQ, shipping</b></a>
    <a class="rel-card" href="/category-fashion.html"><span>Fashion &amp; apparel</span><b>Guangzhou sourced, Bahrain-landed prices</b></a>
    <a class="rel-card" href="/category-tech.html"><span>Tech &amp; electronics</span><b>Shenzhen sourced, GSO-ready</b></a>
    <a class="rel-card" href="/blog/how-to-import-from-china-to-bahrain.html"><span>Bahrain import — blog version</span><b>Step-by-step short guide (2026)</b></a>
  </div>
</div></section>

<section class="sec"><div class="wrap" style="text-align:center">
  <div class="sec-head center"><h2>Ready to import from China to Bahrain?</h2></div>
  <p class="sub">Send your product list — get a landed-cost estimate (5%% duty + 10%% VAT) and an OFOQ-ready plan on WhatsApp.</p>
  <a class="btn-wa" href="%s" target="_blank" rel="noopener">💬 Start my Bahrain import on WhatsApp</a>
</div></section>
''' % (wa_bh, wa_bh)

# ----------------------------------------------------------------------------
# 阿曼 指南数据
# ----------------------------------------------------------------------------
OMAN_FAQ = [
    ('What is the customs duty rate for importing from China to Oman?',
     'Oman applies the GCC Common Customs Law, so the standard customs duty is 5% of the CIF value (cost + insurance + freight) for most goods — the general range is 0–5%, with most merchandise at 5%. Higher rates apply to alcohol, tobacco and pork products. The 5% base covers electronics, apparel, home goods and toys.'),
    ('Does Oman charge VAT on imports?',
     'Yes — Oman applies a 5% VAT on imports, in force since April 2021. It is charged on the CIF value plus the customs duty, so the combined effective rate is about 10.25% for standard goods. VAT is collected by the Oman Tax Authority at clearance through the Bayan system. It is the same rate as the UAE, below Bahrain\'s 10% and Saudi\'s 15%.'),
    ('Is SABER required to import into Oman?',
     'No. Oman has no SABER-style platform. It uses the Bayan single-window system, and regulated products (electronics, telecom, food, cosmetics, chemicals) need a Certificate or Declaration of Conformity; wireless and telecom items also need TRA Type Approval. The conformity list is shorter than Saudi SABER — a sourcing agent pre-checks HS codes and books conformity before shipment.'),
    ('Are there free zones in Oman?',
     'Yes — Oman runs several free zones: Sohar Free Zone, Salalah Free Zone and Al Mazunah (near the Yemen border). Goods held for storage or re-export are not charged duty or VAT while inside the zone; duty and VAT apply when released to the Omani mainland. 100% foreign ownership is allowed in the zones.'),
    ('What documents are required to clear customs in Oman?',
     'You need a commercial invoice (with 12-digit GCC HS code and CIF value), packing list, bill of lading or air waybill, and a certificate of origin. Regulated products require a conformity certificate; telecom needs TRA approval. Unattested documents can trigger a 2% duty-deposit surcharge. Clearance is filed through Bayan by a licensed Omani customs broker.'),
    ('How long does Oman customs clearance take?',
     'With complete documents, Oman clearance through Bayan typically takes 1–3 working days (2–5 for regulated or telecom shipments). The main gateway is Sohar Port, primary for containerized imports from China serving Muscat and northern Oman; Salalah Port serves the south and Port Sultan Qaboos handles Muscat general cargo. Sea freight from China runs about 18–30 days.'),
    ('Do products need Arabic labels for Oman?',
     'Bilingual (Arabic + English) labels are recommended and mandatory for food, beverage and health or cosmetic products. Clear Arabic labelling supports clearance and the local Omani market.'),
    ('What is the cheapest way to import small orders from China to Oman?',
     'For samples and small parcels, express courier is fastest. For larger but sub-container loads, sea freight LCL or air consolidation through a sourcing agent lowers per-unit cost. Consolidating multiple Chinese suppliers into one Sohar-bound container is the usual biggest saving for Oman.'),
]

def oman_body():
    wa_om = wa_link('Hi SourceToGulf! I want to import from China to Oman. Please help with sourcing, conformity and clearance.')
    return '''
<section class="sec hero-sec">
  <div class="wrap">
    <span class="kicker">GCC Import Guide</span>
    <h1>Importing from China to Oman — The Complete 2026 Guide</h1>
    <p class="lead">Importing from China to Oman means a <b>5%% customs duty on the CIF value</b> plus a <b>5%% VAT</b> (since April 2021) — about <b>10.25%% combined</b>. Oman uses the <b>Bayan</b> single window and a shorter conformity list than Saudi SABER. A China sourcing agent handles pricing, consolidation and Bayan clearance into Sohar.</p>
    <div class="cta-row">
      <a class="btn-wa" href="%s" target="_blank" rel="noopener">💬 Get an Oman import quote on WhatsApp</a>
      <a class="btn-ghost" href="/#calculator">Estimate landed cost →</a>
    </div>
  </div>
</section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Oman import duties from China</h2></div>
  <p>Oman applies the GCC Common Customs Law, so the <b>standard customs duty is 5%% of CIF value</b> (cost + insurance + freight) for most products — the general range is 0–5%%, with most merchandise at 5%%. A few categories carry higher rates:</p>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">Product type</th>
      <th style="padding:10px 12px;text-align:left">Customs duty</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">Most goods (electronics, apparel, home, toys)</td><td style="padding:10px 12px"><b>5%% of CIF</b></td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">Alcohol / tobacco / pork</td><td style="padding:10px 12px">Higher excise rates</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">Motor vehicles</td><td style="padding:10px 12px">Specific rates by type/cc</td></tr>
    </tbody>
  </table>
  <p>Duty is assessed on CIF, so a sharper factory price and lower freight both reduce what you pay at the border.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>VAT in Oman</h2></div>
  <p>Oman applies a <b>5%% VAT</b> on imported goods, in force since <b>April 2021</b>. It is charged on the CIF value <i>plus</i> the customs duty, so the combined effective rate is about <b>10.25%%</b> for standard goods. VAT is collected by the Oman Tax Authority at clearance through the Bayan system — the same 5%% rate as the UAE, below Bahrain's 10%% and Saudi's 15%%. Budget for the combined rate in your landed-cost model.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Conformity via Bayan — no SABER</h2></div>
  <p>Oman uses the <b>Bayan</b> single-window platform. It has <b>no SABER-style platform</b>; regulated products (electronics, telecom, food, cosmetics, chemicals) need a <b>Certificate or Declaration of Conformity</b>, and wireless or telecom items additionally need <b>TRA Type Approval</b>. The conformity list is shorter than Saudi SABER. A sourcing agent pre-checks HS codes and books conformity before shipment so Bayan clearance runs in 1–3 days.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>Free zones vs mainland</h2></div>
  <p>Oman runs several free zones: <b>Sohar Free Zone</b>, <b>Salalah Free Zone</b> and <b>Al Mazunah</b> (near the Yemen border). Goods held for storage or re-export are not charged duty or VAT while inside the zone; duty and VAT apply when released to the Omani mainland.</p>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">Free zone (Sohar / Salalah / Al Mazunah)</th>
      <th style="padding:10px 12px;text-align:left">Oman mainland</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">No duty / VAT on goods for storage / re-export</td><td style="padding:10px 12px">5%% duty + 5%% VAT on CIF when released</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">100%% foreign ownership in zones</td><td style="padding:10px 12px">Local rules for some activities</td></tr>
    </tbody>
  </table>
  <p>For re-export to the wider Gulf or East Africa, keeping stock in a free zone avoids Omani duty and VAT. For the local Muscat/Sohar market, goods cross to mainland and the 10.25%% combined applies.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Documents required for Oman customs clearance</h2></div>
  <ul class="bullets">
    <li><b>Commercial invoice</b> — with 12-digit GCC HS code and CIF value</li>
    <li><b>Packing list</b> — carton counts, weights, dimensions</li>
    <li><b>Bill of lading / air waybill</b> — transport document</li>
    <li><b>Certificate of origin</b> — attested by the Chamber of Commerce</li>
    <li><b>Conformity certificate / TRA approval</b> — for regulated or wireless products</li>
  </ul>
  <p>Clearance is filed through Bayan by a licensed Omani customs broker. Unattested documents can trigger a 2%% duty-deposit surcharge, so attest the certificate of origin before departure.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>Customs clearance time &amp; ports</h2></div>
  <p>With complete documents, Oman clearance typically takes <b>1–3 working days</b> (2–5 for regulated or telecom shipments). The main gateway is <b>Sohar Port</b> — primary for containerized imports from China, serving Muscat and northern Oman. <b>Salalah Port</b> serves the south (and is a major transshipment hub), and <b>Port Sultan Qaboos</b> handles Muscat general cargo. Sea freight from China runs about 18–30 days. Oman's Vision 2040 targets logistics and re-export as growth pillars, so port capacity is expanding.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>Best Chinese cities to source from</h2></div>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:left">City</th>
      <th style="padding:10px 12px;text-align:left">Best for</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Yiwu</b></td><td style="padding:10px 12px">Small commodities, gifts, accessories, low MOQ, mixed consolidation</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px"><b>Guangzhou</b></td><td style="padding:10px 12px">Apparel, bags, beauty, watches, wholesale markets</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>Shenzhen</b></td><td style="padding:10px 12px">Electronics, gadgets, tech accessories, fast prototyping</td></tr>
    </tbody>
  </table>
  <p>Most Gulf buyers mix all three. A sourcing agent consolidates from multiple cities into one Sohar-bound container — often the single biggest saving for Oman.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>How a sourcing agent lowers your Oman landed cost</h2></div>
  <p>A China-based agent compresses three cost lines: sharper <b>factory pricing</b> (direct from manufacturers), <b>consolidation</b> that turns several parcels into one sea shipment, and <b>pre-shipment QC</b> that stops defects before they ship. For Oman, the agent also pre-checks HS codes, books conformity/TRA approval and attests the certificate of origin so Bayan clearance runs in 1–3 days — keeping the 5%% duty + 5%% VAT model predictable.</p>
  <div class="rel-grid">
    <a class="rel-card" href="/solutions.html"><span>Solutions by buyer type</span><b>Influencer · Wholesaler · Retailer · Small brand</b></a>
    <a class="rel-card" href="/gcc-import-answers.html"><span>GCC import Q&amp;A</span><b>22 answers on duty, VAT, Bayan, MOQ, shipping</b></a>
    <a class="rel-card" href="/category-fashion.html"><span>Fashion &amp; apparel</span><b>Guangzhou sourced, Oman-landed prices</b></a>
    <a class="rel-card" href="/category-tech.html"><span>Tech &amp; electronics</span><b>Shenzhen sourced, TRA-ready</b></a>
    <a class="rel-card" href="/blog/how-to-import-from-china-to-oman.html"><span>Oman import — blog version</span><b>Step-by-step short guide (2026)</b></a>
  </div>
</div></section>

<section class="sec"><div class="wrap" style="text-align:center">
  <div class="sec-head center"><h2>Ready to import from China to Oman?</h2></div>
  <p class="sub">Send your product list — get a landed-cost estimate (5%% duty + 5%% VAT) and a Bayan-ready plan on WhatsApp.</p>
  <a class="btn-wa" href="%s" target="_blank" rel="noopener">💬 Start my Oman import on WhatsApp</a>
</div></section>
''' % (wa_om, wa_om)

GUIDES = {
    'uae': {
        'file': 'uae-import-guide-from-china.html',
        'title': 'Importing from China to the UAE — The Complete 2026 Guide',
        'desc': 'UAE import duties (5% CIF), 5% VAT, free-zone vs mainland, ECAS compliance, documents, 1–3 day clearance, and how a China sourcing agent lowers landed cost.',
        'canonical': BASE + '/uae-import-guide-from-china.html',
        'body': uae_body(),
        'faq': UAE_FAQ,
    },
    'ksa': {
        'file': 'saudi-arabia-import-guide-from-china.html',
        'title': 'Importing from China to Saudi Arabia — The Complete 2026 Guide',
        'desc': 'Saudi import duties (5% CIF), 15% VAT, mandatory SABER (PCoC + SCoC), SFDA, documents, 2–5 day clearance via Jeddah/Dammam, and how a China sourcing agent handles SABER and lowers landed cost.',
        'canonical': BASE + '/saudi-arabia-import-guide-from-china.html',
        'body': ksa_body(),
        'faq': KSA_FAQ,
    },
    'qatar': {
        'file': 'qatar-import-guide-from-china.html',
        'title': 'Importing from China to Qatar — The Complete 2026 Guide',
        'desc': 'Qatar import duties (5% CIF), no standard VAT yet (GCC 5% committed, e-invoicing law May 2026), QFZ free zones (Ras Bufontas, Umm Alhoul), documents, 2–4 day clearance via Hamad Port, and how a China sourcing agent lowers landed cost.',
        'canonical': BASE + '/qatar-import-guide-from-china.html',
        'body': qatar_body(),
        'faq': QATAR_FAQ,
    },
    'kuwait': {
        'file': 'kuwait-import-guide-from-china.html',
        'title': 'Importing from China to Kuwait — The Complete 2026 Guide',
        'desc': 'Kuwait import duties (5% CIF), no VAT as of 2026, KUCAS conformity (PAI), Shuwaikh/Shuaiba ports, 3–7 day clearance, "Made in China" marking, and how a China sourcing agent lowers landed cost.',
        'canonical': BASE + '/kuwait-import-guide-from-china.html',
        'body': kuwait_body(),
        'faq': KUWAIT_FAQ,
    },
    'bahrain': {
        'file': 'bahrain-import-guide-from-china.html',
        'title': 'Importing from China to Bahrain — The Complete 2026 Guide',
        'desc': 'Bahrain import duties (5% CIF), 10% VAT, OFOQ single window + GSO conformity (no SABER), Bahrain Logistics Zone / BIIP, 100% foreign ownership, 1–3 day clearance via Khalifa Bin Salman Port, and how a China sourcing agent lowers landed cost.',
        'canonical': BASE + '/bahrain-import-guide-from-china.html',
        'body': bahrain_body(),
        'faq': BAHRAIN_FAQ,
    },
    'oman': {
        'file': 'oman-import-guide-from-china.html',
        'title': 'Importing from China to Oman — The Complete 2026 Guide',
        'desc': 'Oman import duties (5% CIF), 5% VAT (since April 2021, ~10.25% combined), Bayan single window + conformity/TRA approval (no SABER), Sohar/Salalah free zones, 1–3 day clearance via Sohar Port, and how a China sourcing agent lowers landed cost.',
        'canonical': BASE + '/oman-import-guide-from-china.html',
        'body': oman_body(),
        'faq': OMAN_FAQ,
    },
}

def jsonld_for(g):
    wp = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": g['title'],
        "url": g['canonical'],
        "description": g['desc'],
        "inLanguage": "en",
        "publisher": {"@type": "Organization", "name": "SourceToGulf", "url": BASE},
    }
    return json.dumps([wp, faq_jsonld(g['faq'])], ensure_ascii=False, indent=2)

def main():
    for key, g in GUIDES.items():
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
        print('✓ wrote', g['file'], '(%d bytes)' % len(html))

if __name__ == '__main__':
    main()
