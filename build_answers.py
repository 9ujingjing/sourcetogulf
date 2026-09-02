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
        '<p class="sub">The questions Gulf importers actually ask before they order from China: duties, VAT, SABER, MOQ, shipping time, documents and quality. Clear, sourced answers — not sales talk.</p>\n'
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
        '    <a class="wa-btn" style="background:var(--gold);color:#17201C" href="' + wa_link('Hi SourceToGulf! I have a GCC import question.') + '" target="_blank" rel="noopener">💬 WhatsApp: +971 58 514 6139</a>\n'
        '  </div>\n'
        '</div></section>')

    url = BASE + '/gcc-import-answers.html'
    title = 'GCC Sourcing Answers: Duties, VAT, SABER & MOQ from China | SourceToGulf'
    desc = 'Clear answers to the questions Gulf buyers ask before importing from China: import duties, VAT by country, SABER, MOQ, shipping time, documents and quality control.'
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
