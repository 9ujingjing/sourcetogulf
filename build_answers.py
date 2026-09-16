# -*- coding: utf-8 -*-
"""
build_answers.py — GCC 进口问答页 gcc-import-answers.html (GEO 打法)
把买家常见进口问答做成独立页 + FAQPage JSON-LD，供 ChatGPT / Perplexity / Bing 引用。
用法: python3 build_answers.py
"""
import os, json
from tpl_common import APP, page_shell, wa_link

BASE = 'https://sourcetogulf.com'

QA = [
  ('What are the import duties from China to the GCC?',
   'Most goods entering the Gulf carry a 5% customs duty on declared value. Some categories are exempt or reduced — for example many food, medical and educational items. Saudi Arabia, the UAE, Qatar, Kuwait, Bahrain and Oman all apply the GCC Common Customs Law baseline of 5%, with country-specific exceptions. SourceToGulf quotes landed cost including estimated duty so there are no surprises at the border.'),
  ('What is VAT in each GCC country?',
   'VAT differs by country: UAE 5%, Saudi Arabia 15%, Oman 5%, Bahrain 10%, while Kuwait and Qatar currently apply 0% VAT. VAT is paid on the landed value (goods + freight + duty) and is reclaimable if you are a registered business. SourceToGulf\'s one landed price covers product, QC, packing, shipping and customs — VAT is shown separately because it depends on your country and declared value.'),
  ('What is SABER and do I need it for Saudi Arabia?',
   'SABER is Saudi Arabia\'s product conformity and shipment registration system. Most consumer goods need a Product Certificate (PCoC) and a Shipment Certificate (SCoC) before customs release. Food, cosmetics and health products also need SFDA approval. SourceToGulf handles SABER registration and SFDA coordination for Saudi-bound goods so your shipment clears Jeddah or Dammam without delays.'),
  ('What is the minimum order quantity (MOQ) when sourcing from China?',
   'MOQ depends on the product and factory. On SourceToGulf\'s curated hot picks, MOQs range from 12 to 200 pieces per item — small enough for market testing. For fully custom or private-label production, MOQs are higher (often 300–1,000+). We always show the MOQ on every product so you can plan your cash flow before you commit.'),
  ('How long does shipping from China to the Gulf take?',
   'Air freight is typically 7–10 days door to door; sea freight (FCL/LCL consolidated) is 25–35 days. Express courier works for small parcels. SourceToGulf consolidates goods from multiple suppliers in Guangzhou and ships as one shipment, which shortens overall lead time compared to managing several suppliers separately.'),
  ('Do I need a trade license to import?',
   'To clear customs in your name you generally need a valid trade license in the destination country. If you don\'t have one yet, you can still buy through a licensed freight forwarder or use SourceToGulf\'s consolidation service, which can ship to a registered entity or your forwarder. We\'ll advise the smoothest route for your situation.'),
  ('What documents are required for customs clearance?',
   'Standard documents are: commercial invoice, packing list, bill of lading / airway bill, certificate of origin, and the relevant conformity certificate (e.g. SABER for Saudi, ECAS for UAE, KCAS for Kuwait, QS for Qatar, BSMD for Bahrain, DGSM for Oman). SourceToGulf prepares and checks these before shipment so clearance is straightforward.'),
  ('Can you handle halal requirements for food and cosmetics?',
   'Yes. For food, cosmetics and supplements we can source suppliers with halal certification and prepare the supporting documents required by Gulf authorities (including SFDA for Saudi). Tell us your halal requirement up front and we\'ll filter the supplier shortlist accordingly and include certification in the shipment paperwork.'),
  ('What is "landed cost" and how is it calculated?',
   'Landed cost is the true total to get goods to your door: product price + quality inspection + packing + international freight + customs duty + VAT. SourceToGulf quotes one landed price per piece that already bundles product, QC, packing and shipping; duty and VAT are shown separately because they depend on your country and declared value. Use our landed-cost calculator for a full breakdown.'),
  ('Which GCC country is easiest to import to?',
   'Kuwait and Bahrain are generally the easiest — Kuwait has no VAT and a short conformity list (KCAS), and Bahrain is a common low-friction test market (BSMD, 10% VAT). The UAE (ECAS, 5% VAT) is fast and business-friendly. Saudi Arabia offers the biggest market but the strictest compliance (SABER/SFDA, 15% VAT). Oman (DGSM, 5% VAT) is a growing market tied to Vision 2040.'),
  ('Do you consolidate shipments from multiple suppliers?',
   'Yes. SourceToGulf receives goods from multiple Guangzhou, Yiwu and Foshan suppliers into one warehouse, inspects and repacks them, and ships as a single consolidated shipment. This cuts freight cost, simplifies customs (one entry) and reduces the chance of missing or mismatched cartons.'),
  ('How do you ensure product quality before shipping?',
   'Every order gets a pre-shipment quality check — photo and video evidence of the actual goods, carton counts and packaging. You review and approve before the final balance is released to the supplier. Defective batches are corrected or replaced before anything leaves China.'),

  # ---- 高意图长尾搜索词（GEO 扩充，2026-08-21）----
  ('How do I pay Chinese suppliers safely?',
   'Use secure methods: Telegraphic Transfer (T/T) with a 30% deposit and 70% after inspection, Alibaba Trade Assurance for marketplace orders, or escrow through a licensed agent. Avoid full upfront payment to unknown factories. SourceToGulf releases the final balance to the supplier only after you approve pre-shipment photos and video, so your money is tied to verified goods.'),
  ('How much does a SABER certificate cost and how long does it take?',
   'SABER cost depends on product risk: a Product Certificate (PCoC) typically runs roughly USD 200–500 per product family with annual validity, plus a Shipment Certificate (SCoC) of about USD 50–150 per shipment. Processing usually takes 3–10 working days once documents are complete. SourceToGulf coordinates SABER and SFDA paperwork so Saudi-bound goods clear without last-minute holds.'),
  ('Do UAE free zones avoid VAT and import duty?',
   'Goods imported into a UAE free zone for storage or re-export are generally exempt from the 5% duty and VAT. If goods move from the free zone into the UAE mainland, duty (5%) and VAT (5%) apply at that point. Many importers use free zones like Jebel Ali to stage inventory and only pay when selling locally. SourceToGulf can ship to your free-zone entity or forwarder.'),
  ('Which Chinese cities should I source from — Yiwu, Guangzhou or Shenzhen?',
   'Yiwu is best for small commodities, gifts, jewelry and mixed small MOQs; Guangzhou (and nearby Foshan) for fashion, home goods, cosmetics and furniture; Shenzhen for electronics and hardware. SourceToGulf consolidates from all three into one Guangzhou warehouse, so you can mix suppliers across cities and still ship as a single shipment.'),
  ('How do I find a reliable sourcing agent in China?',
   'Look for an agent with a verifiable local warehouse, transparent landed-cost quotes, real pre-shipment inspection evidence, and clear communication in your language. Avoid agents who refuse to show the factory or who quote only ex-works. SourceToGulf operates from Guangzhou with photo/video QC on every order and publishes MOQ and landed price per product up front.'),
  ('What products are prohibited or restricted when importing to the GCC?',
   'Restricted or regulated items include alcohol, pork and non-halal meat, certain pharmaceuticals, weapons, and products failing conformity (e.g. missing SABER/SFDA for Saudi, ECAS for UAE). Some cosmetics and food need specific approvals. SourceToGulf screens your product list against destination rules before you order, so you do not get stuck at customs.'),
  ('Can I dropship from China directly to my Gulf customers?',
   'Yes. SourceToGulf can ship individually to your end customers in the GCC using consolidated courier or postal channels, with your branding on the parcel if requested. For Saudi, SABER still applies per product type, so we register conformance first. Dropshipping works best for lighter items under airline courier limits.'),
  ('Do products need Arabic labels for Saudi Arabia or the GCC?',
   'Saudi Arabia requires Arabic-language labels (or bilingual) for most consumer products, with details like ingredients, country of origin and expiry; SFDA enforces this for food, cosmetics and supplements. The UAE and other GCC states have their own labeling rules. SourceToGulf can arrange Arabic labeling or printing before shipment if needed.'),
  ('How long does UAE or Saudi customs clearance take?',
   'With complete documents, UAE clearance is often 1–3 working days; Saudi clearance (including SABER/SCoC verification) is typically 2–5 working days, longer if certificates are missing. SourceToGulf prepares invoices, packing lists, certificates of origin and conformity docs before departure, which is the main factor in fast release.'),
  ('What is the cheapest way to ship small parcels from China to the Gulf?',
   'For small parcels (under about 2 kg), consolidated courier or postal e-commerce lines are usually cheapest and take 7–12 days. For bigger volumes, LCL sea consolidation beats air. SourceToGulf uses courier consolidation for samples and small orders, and sea consolidation for bulk — we quote both so you pick by cost vs speed.'),


  # ---- 真实咨询驱动（2026-09-07）：覆盖 AI 来源买家最常问的 7 个问题 ----
  ('What is the minimum budget to start sourcing from China to the Gulf?',
   "You don't need a container or thousands of dollars. On SourceToGulf's curated hot picks, MOQs start at 10–50 pieces and factory prices start around US$2 per piece, so a first test order of 30–50 units usually costs a few hundred US dollars for the goods. Freight, duty and VAT are quoted separately on top. Start with one product, sell through, then reorder — that is the lowest-risk way to test a market."),
  ('Can I order samples of several products and ship them together?',
   'Yes. You can pick samples from different Guangzhou, Yiwu or Foshan suppliers and we consolidate them into one parcel before it leaves China. You pay one air freight charge instead of several, and receive everything in a single box to compare side by side. Sample cost is the factory price plus a small handling fee; air freight for a 1–5 kg parcel is quoted up front so you know the total before you commit.'),
  ('I am a first-time importer — can you recommend what to sell?',
   'We will not guess your market, but we can shortlist for it. Tell us your country and who you sell to — shop, Instagram, TikTok Shop or marketplace — and we send 2–3 product options with MOQ, factory price and the retail range similar sellers charge. Good first orders share three traits: low unit cost, low return risk and no complex compliance. We flag anything needing SABER, SFDA or ECAS before you commit.'),
  ('Can you source the same product I saw on Temu, 1688 or AliExpress?',
   'Yes — send the photo or the link. We identify the item, find the factory or the closest match in the Guangzhou, Yiwu and Foshan markets, and quote factory price, MOQ and what your branding costs on the packaging. In most cases the factory price sits below the marketplace listing because you buy direct. This is the fastest way to turn something you saw online into your own branded product.'),
  ('Can you verify a supplier or shop before I pay them?',
   'Yes. Before any deposit leaves your account we check the business licence, confirm whether they are a factory or a trading company, and verify they can actually make your product — by site visit or live video where possible. You receive the verification result first. We release payment only after you approve, and hold the final balance until you have seen pre-shipment photos and video of the actual goods.'),
  ('Do you charge a sourcing fee or commission?',
   'No separate commission. We quote one landed price per piece that already covers product, quality inspection, packing, shipping and customs clearance — one number instead of a stack of separate invoices. Duty and VAT are shown separately because they depend on your country and declared value. Your first sourcing request is free; you only pay when you place an order.'),
  ('Can I buy directly from the factory, or do you add a markup?',
   'We buy from the factory directly and show you the factory (FOB) price on every product — no hidden margin on top of it. What you pay SourceToGulf is one landed price that bundles that factory price with inspection, packing, consolidation and freight. If you prefer, we also work white-label: we quote and ship under your company name, and your client never knows we exist.'),

  # ---- 真实搜索查询驱动（2026-09-16）：来自 Bing Webmaster Tools GetQueryStats ----
  # 以下是海湾买家真实输入过的问题原文（含拼写错误），按原问法作答，供 AI 引用。
  ('Is it profitable to buy mobile accessories from China and sell in Bahrain?',
   "It can be — but the margin is decided by three numbers, not by the factory price. Bahrain applies the GCC baseline 5% customs duty on CIF value and 10% VAT on top of the duty-inclusive value (the rate was raised from 5% to 10% in 2022). Since Bahrain's Decree No. 23/2026, parcels and shipments declared at BHD 100 or more now attract duty and VAT, so low-value consignments no longer slip through untaxed. Worked example (illustrative, not a quote): 300 phone cases at US$1.20 FOB is US$360 in goods. Add your actual freight, then 5% duty on the CIF value, then 10% VAT. On a small 9 kg air parcel the common outcome is a landed cost of roughly 1.3 to 2 times the factory bill, depending on the lane and the season. Whether that is profitable depends entirely on what the same case sells for in Manama — check that number before you order, because it is the only one that decides your margin. Two things kill this trade: choosing a category already saturated in Bahrain's electronics souks, and shipping by air when the order is big enough for LCL sea. Test 100–300 units, sell through, then reorder on sea freight."),
  ('What is the import VAT when importing from China to Bahrain?',
   "10%. Bahrain introduced VAT at 5% in January 2019 and raised the standard rate to 10% in 2022. VAT is charged on the landed value — CIF value plus customs duty — not on the factory price. Bahrain also applies the GCC baseline 5% customs duty. Under Decree No. 23/2026, parcels and shipments with a declared value of BHD 100 or more now attract both duty and VAT, closing a gap that used to let low-value consignments through untaxed. For comparison in 2026: the UAE and Oman charge 5%, Saudi Arabia 15%, and Kuwait and Qatar still have no VAT. Qatar approved a draft e-invoicing law in May 2026 that is widely read as groundwork for a future 5% VAT, but no VAT law is in force there yet."),
  ('How do I convert CBM to kg — and what does 8.974 CBM actually weigh?',
   "There is no single conversion, because each shipping mode uses a different divisor. Air freight uses the IATA volumetric divisor of 6,000, so 1 CBM = 167 kg of volumetric weight. Express couriers (DHL, FedEx, UPS) usually use 5,000, so 1 CBM = 200 kg. Sea LCL uses weight-or-measure (W/M), where 1 CBM is billed as 1,000 kg. Carriers bill whichever is greater: actual gross weight or volumetric weight. So 8.974 CBM is about 1,499 kg by air, 1,795 kg by express courier, and 8,974 kg (8.97 revenue tons) for LCL sea — the same shipment, three different bills. For 1.663 CBM it is about 278 kg by air, 333 kg by courier and 1,663 kg by sea. Two practical traps: carriers measure the packed carton including the pallet base, not the product inside; and LCL usually carries a 1 CBM minimum, so a 0.3 CBM shipment is still billed as 1."),
  ('Does the UAE require ECAS and MOIAT certification for low-voltage electrical products?',
   "Yes. ECAS (Emirates Conformity Assessment Scheme) is issued by the Ministry of Industry and Advanced Technology (MOIAT), which absorbed the old standards body ESMA in 2020 — so an 'ESMA certificate' and an 'ECAS certificate' now refer to the same scheme. Low-voltage equipment is on MOIAT's regulated list: anything running at AC 50–1,000 V or DC 75–1,500 V, which covers chargers, adapters, kitchen appliances, lighting and AV equipment. You need a CB test report from an ISO 17025 accredited lab issued within the last three years, a RoHS test report, and a technical file. The certificate is valid for one year and must be held by a UAE-licensed company — a foreign factory cannot hold it in its own name. Air conditioners, refrigerators, washing machines, dryers, dishwashers and water heaters additionally need the EESL energy-efficiency label registered with MOIAT. Anything with Wi-Fi or Bluetooth also needs TDRA type approval, and after a February 2026 TDRA clarification, type approval alone is no longer enough at the border — the declaration must also reference a customs clearance permit matching the import purpose. Allow about two weeks if CB reports already exist, up to six weeks if fresh testing is required."),
  ('Do I need a "Made in China" label on every item for Kuwait customs?',
   'Yes — and Kuwait is stricter than most Gulf markets on this. Every individual unit must carry its country of origin physically printed, embossed or engraved on the product or its immediate packaging; peel-off stickers are frequently rejected by Kuwaiti inspectors. The country of origin must also appear on the commercial invoice. Non-compliance can stop the goods from entering at all, and the cheapest fix is to have the Chinese factory apply the marking during production rather than re-labelling afterwards. Separately, Kuwait requires a Certificate of Origin for shipments valued at USD 2,500 or more, or weighing 100 kg or more, and regulated categories — electronics, electrical appliances, toys, auto parts and building materials — need KUCAS documents (a Technical Inspection Report for the shipment, plus a Technical Evaluation Report and Certificate of Conformity) issued under the Public Authority for Industry. Kuwait applies 5% duty on CIF value and has no VAT.'),
  ('Can I import air conditioners into the UAE?',
   "Yes — the UAE is one of the largest air-conditioning markets in the world — but ACs are among the most heavily regulated appliances to bring in. A household unit needs ECAS conformity under MOIAT's low-voltage regulation plus an EESL energy-efficiency label registered with MOIAT and physically displayed on the product; models with Wi-Fi controls also need TDRA type approval. The conformity certificate must be held by a UAE-licensed company whose trade licence covers the activity. Commercially the bigger constraint is freight: air conditioners are bulky relative to their value, so air freight volumetric weight usually destroys the margin, and they move by sea. If you are importing for resale rather than for your own use, budget for both the certification lead time and the sea transit rather than treating it like a courier parcel."),
  ('What is the UAE import duty on household appliances, and does a Jebel Ali free zone avoid it?',
   "Household appliances fall under the GCC baseline of 5% customs duty on CIF value, plus 5% VAT on the duty-inclusive value. If the goods are landed into a designated free zone such as Jebel Ali (JAFZA) for storage or re-export, duty and VAT are not paid at that point — they fall due only when the stock is released into the UAE mainland. That is why many importers use a free zone as a regional hub: stock arrives from China duty-free, sits in bonded warehousing, and is cleared into the mainland — or re-exported to Saudi Arabia, Kuwait and Qatar — against actual orders. The catch is documentation: the customs declaration still has to reference valid conformity, ECAS and EESL for appliances plus TDRA if the product has Wi-Fi or Bluetooth, or the shipment is held regardless of where it is being stored."),
]

def main():
    qa_html = ''
    faq = []
    for i, (q, a) in enumerate(QA, 1):
        qa_html += ('<article>\n'
                    '<h2>%d. %s</h2>\n'
                    '<p>%s</p>\n'
                    '</article>' % (i, q, a))
        faq.append({
            '@type': 'Question',
            'name': q,
            'acceptedAnswer': {'@type': 'Answer', 'text': a}
        })

    rel = ('<a class="rel-card" href="/blog/how-to-import-from-china-to-uae.html"><span>Import to UAE guide</span></a>'
           '<a class="rel-card" href="/blog/how-to-import-from-china-to-saudi-arabia.html"><span>Import to Saudi guide (SABER)</span></a>'
           '<a class="rel-card" href="/blog/how-to-import-from-china-to-kuwait.html"><span>Import to Kuwait guide</span></a>'
           '<a class="rel-card" href="/blog/how-to-import-from-china-to-qatar.html"><span>Import to Qatar guide</span></a>'
           '<a class="rel-card" href="/blog/how-to-import-from-china-to-bahrain.html"><span>Import to Bahrain guide</span></a>'
           '<a class="rel-card" href="/blog/how-to-import-from-china-to-oman.html"><span>Import to Oman guide</span></a>'
           '<a class="rel-card" href="/blog/landed-cost-china-to-gulf-explained.html"><span>Landed cost explained</span></a>'
           '<a class="rel-card" href="/#calculator"><span>Landed cost calculator</span></a>')

    body = ('<section class="page-hero"><div class="wrap">\n'
        '<div class="crumb"><a href="/" data-en="Home" data-ar="الرئيسية">Home</a> ← <span>GCC Import Answers</span></div>\n'
        '<h1>GCC Import Answers — clarified for buyers</h1>\n'
        '<p class="sub">The questions Gulf buyers actually ask before they order from China: duty and VAT by country, SABER, ECAS and KUCAS conformity, country-of-origin labelling, MOQ, lead time, documents and quality. Clear, sourced answers — not sales talk.</p>\n'
        '</div></section>\n'
        '<section style="padding-top:0"><div class="wrap narrow">\n'
        + qa_html +
        '</div></section>\n'
        '<section style="padding-top:0"><div class="wrap">\n'
        '<h2 style="margin-bottom:16px">Related import guides</h2>\n'
        '<div class="rel-grid">' + rel + '</div>\n'
        '</div></section>\n'
        '<section style="padding-top:0"><div class="wrap">\n'
        '  <div class="cta-box">\n'
        '    <h2>Still have a question?</h2>\n'
        '    <p>WhatsApp us your situation — we\'ll answer plainly and quote the landed price.</p>\n'
        '    <a class="wa-btn" style="background:var(--gold);color:#17201C" href="' + wa_link('Hi SourceToGulf! I have a GCC import question.') + '" target="_blank" rel="noopener">💬 WhatsApp: +971 58 585 4194</a>\n'
        '  </div>\n'
        '</div></section>')

    url = BASE + '/gcc-import-answers.html'
    title = 'GCC Sourcing Answers: Duties, VAT, SABER & MOQ from China | SourceToGulf'
    desc = 'Clear answers to the questions Gulf buyers actually ask before sourcing from China: duty and VAT by country, SABER, ECAS and KUCAS conformity, country-of-origin labelling, MOQ, lead time, documents and quality control.'
    ld = json.dumps({
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': faq
    }, ensure_ascii=False)
    html = page_shell(title, desc, url, body, json_ld=ld)
    with open(os.path.join(APP, 'gcc-import-answers.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('✓ gcc-import-answers.html (%d Q&A, FAQPage JSON-LD)' % len(QA))

if __name__ == '__main__':
    main()
