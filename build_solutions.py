# -*- coding: utf-8 -*-
"""
build_solutions.py — 解决方案页 solutions.html（7 问框架 + GEO 优化版，2026-10-10 重写）

页面结构（对照「解决方案页 SEO 框架」7 问）：
  ① Who is this for?            4 类买家卡（问题式标题 + 首句直答）
  ② Will this work for me?      适用场景（6 国 + 品类广度证据，Hub 聚合脱敏）
  ③ What do I need to start?     适用条件（方向 / 品牌文件 / 70-30 / $125 意向金）
  ④ How does sourcing work?      5 步流程（不写天数 —— 用户未确认，按品类而定）
  ⑤ What do I get?               交付清单
  ⑥ What can't you source?       限制说明（合规保护向 + 单件直发教训）
  ⑦ Real case studies            4 个匿名案例（零数字 / 零品牌 / 零公式 / 零真名）
  + 答案箱 + Key facts 条 + FAQPage JSON-LD（8 问）+ Last updated
  + hreflang 双向：阿语版由 build_arabic.py 出 /ar/solutions.html

红线：不写 FOB 公式 / 不写供应商与品牌名 / 案例不带具体数字 / 客户匿名 / 禁最高级词。

用法: python3 build_solutions.py
"""
import os, json
from tpl_common import APP, page_shell, wa_link

BASE = 'https://sourcetogulf.com'

# ---- 页面专属 CSS（extra_head = 第二个 <style> 块，sync_header_footer 只替换第一个）----
PAGE_CSS = '''<style>
/* solutions.html 页面专属 —— 第二个 style 块，勿并入第一个（sync 会覆盖） */
.steps5{display:grid;grid-template-columns:repeat(5,1fr);gap:16px}
@media(max-width:980px){.steps5{grid-template-columns:1fr}}
.sol-facts{display:flex;flex-wrap:wrap;gap:10px 26px;align-items:center;justify-content:center;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 26px;font-size:14.5px;font-weight:600;color:var(--muted)}
.sol-facts b{color:var(--teal)}
.limit-list{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:12px}
.limit-list li{display:flex;gap:10px;align-items:flex-start;background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 16px;font-size:14.5px;color:var(--ink);line-height:1.65}
.limit-list li::before{content:"\\2715";color:#B4432E;font-weight:800;flex-shrink:0;line-height:1.65}
.case-tag{font-size:12px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:var(--gold)}
.case-outcome{border-top:1px dashed var(--line);margin-top:12px;padding-top:11px;font-size:13.5px;color:var(--teal);font-weight:600}
</style>'''

# ---- ① 目标客户：4 类买家（问题式标题 + 首句直答）----
SEGMENTS = [
  {
    'icon': '📱',
    'name': 'Influencer & Livestream Sellers',
    'question': 'Selling through Instagram, TikTok or livestreams?',
    'answer': 'We keep MOQs low so you can test trends without dead stock.',
    'who': 'TikTok KSA, Instagram UAE and livestream sellers who need trend-ready stock fast.',
    'points': [
      'Small MOQ to test viral items — hijab jewelry, phone accessories, beauty tools',
      'Photogenic samples + QC photos/videos you can use in your content',
      'Private label to turn winning items into your own product line',
      'Fast restocks so you never miss a trend window',
    ],
    'links': [
      ('/category-fashion.html', 'Hijab & jewelry'),
      ('/category-tech.html', 'Phone & car accessories'),
      ('/category-beauty-toys.html', 'Beauty tools'),
      ('/services/custom-branding-packaging.html', 'Private labelling'),
    ],
  },
  {
    'icon': '📦',
    'name': 'Wholesalers & Distributors',
    'question': 'Running a wholesale or distribution business?',
    'answer': 'We mix categories from many suppliers into one consolidated container.',
    'who': 'Buyers moving volume across the Gulf who need consolidated, mixed-category shipments.',
    'points': [
      'Bulk pricing with mixed categories from many suppliers in one container',
      'Consolidation in Guangzhou — one shipment, one customs entry, lower freight',
      'Repeat-order management with consistent quality and lead times',
      'SABER / documentation handled for Saudi-bound goods',
    ],
    'links': [
      ('/services/consolidation-shipping-china-gulf.html', 'Consolidation & shipping'),
      ('/category-home.html', 'Home & kitchen'),
      ('/category-home-fragrance.html', 'Home fragrance'),
      ('/shipping/china-to-saudi-arabia.html', 'Ship to Saudi (SABER)'),
    ],
  },
  {
    'icon': '🏬',
    'name': 'Retailers & Chains',
    'question': 'Stocking a retail store or chain?',
    'answer': 'You get retail-ready packing and pre-shipment QC without managing ten factories.',
    'who': 'Shops and retail chains that need retail-ready, consistently replenished stock.',
    'points': [
      'Retail-ready packaging, barcodes and consistent sizing',
      'Replenishment planning matched to your sales velocity',
      'Pre-shipment QC so shelves stay consistent, returns stay low',
      'Multi-supplier sourcing so one PO covers a full category',
    ],
    'links': [
      ('/services/custom-branding-packaging.html', 'Custom packaging'),
      ('/services/quality-inspection-china.html', 'Quality inspection'),
      ('/category-home.html', 'Home & kitchen'),
      ('/products.html', 'All hot picks'),
    ],
  },
  {
    'icon': '✨',
    'name': 'Small Brands & Startups',
    'question': 'Building your own brand?',
    'answer': 'Low-MOQ private label and custom packaging, starting from a physical sample.',
    'who': 'Founders building a private-label line on small minimums.',
    'points': [
      'OEM / private label with your logo at low minimums',
      'Custom packaging — boxes, bags, cards, inserts',
      'Product development support from a physical sample',
      'Same QC and door-to-door shipping as volume buyers',
    ],
    'links': [
      ('/services/custom-branding-packaging.html', 'Private label & packaging'),
      ('/category-fashion.html', 'Hijab & jewelry'),
      ('/category-seasonal.html', 'Ramadan & Eid'),
      ('/services/product-sourcing-china.html', 'Product sourcing'),
    ],
  },
]

# ---- ③ 适用条件 ----
PREREQS = [
  ('🔎', 'A product direction',
   'A clear category or product — or pick from this month\'s catalog. A photo or link is enough to start.'),
  ('🎨', 'Brand assets',
   'Logo files if you want private label or custom packaging. No logo yet? We quote plain stock first.'),
  ('💳', 'Payment terms',
   '30% deposit to start production, 70% balance before shipment. Quotes come with landed GCC pricing in AED.'),
  ('🤝', 'Intent deposit & NDA',
   'A $125 USD intent deposit begins the engagement — applied against your first order, or billed as a '
   'sourcing service fee if no order materializes. Mutual NDAs available on request.'),
]

# ---- ④ 流程 5 步（不写天数）----
STEPS = [
  ('Inquiry', 'You send the product, target market and quantity. A photo or a link is enough to start.'),
  ('Quotation', 'A web-based quote with the landed GCC price in AED, valid for one week.'),
  ('Sampling', 'Samples from the shortlisted factory, verified with photos and video.'),
  ('Production & QC', 'Bulk production with inspection — you see photo and video proof before anything ships.'),
  ('Consolidation & shipping', 'Goods consolidated in Guangzhou and shipped to your GCC port or door.'),
]

# ---- ⑥ 限制说明（合规保护向）----
LIMITS = [
  ('Counterfeit, replica or IP-infringing brand goods.',
   ' We don\'t handle products that violate third-party intellectual property — no exceptions.'),
  ('Illegal or restricted items.',
   ' Anything outside legal compliance is out of scope.'),
  ('Hazardous goods.',
   ' Aerosols (UN1950) and other transport-restricted cargo.'),
  ('Certified categories without a compliance path.',
   ' Electrical appliances needing ECAS or SABER certification must have a viable route — or we decline the order.'),
  ('Single-parcel dropshipping from China to end customers across the GCC.',
   ' Our model is bulk consolidation. Single-piece fulfillment requires goods warehoused inside the GCC first.'),
  ('One-piece custom printing.',
   ' Private label runs require MOQ-based production.'),
]

# ---- ⑦ 匿名案例（Situation → What we did → Outcome，零数字/零品牌/零真名）----
CASES = [
  ('Lifestyle brand launch · Dubai',
   'From opaque quotes to launch-ready stock',
   'A Dubai-based lifestyle brand came to us after finding its previous suppliers\' pricing opaque. '
   'We completed sampling, private-label printing and Guangzhou consolidation for the first product line, '
   'delivering QC-verified samples before the launch window.',
   'Outcome: the brand launched on schedule and publicly recommended the service.'),
  ('Women\'s apparel aggregation · Gulf',
   'Multi-category sourcing under one relationship',
   'A Gulf-based women\'s apparel buyer sourced sleepwear, activewear and coordinated sets from multiple '
   'suppliers, mixed into consolidated shipments with private-label packaging.',
   'Outcome: an ongoing multi-category supply relationship.'),
  ('Equipment integration · Gulf',
   'Multi-model equipment, one window',
   'A Gulf facilities buyer consolidated a multi-model surveillance and storage equipment order through a '
   'single point of contact, with the full GCC compliance documentation prepared on their behalf.',
   'Outcome: single-window delivery for a technically complex order.'),
  ('Boutique trial order · Gulf',
   'Small first order, door to door',
   'A boutique owner started with a small trial order at door-to-door landed pricing, supported from '
   'sampling through first delivery.',
   'Outcome: repeat interest after the trial run.'),
]

# ---- FAQ（可见 HTML 与 FAQPage JSON-LD 共用同一份数据）----
FAQ = [
  ('Do you accept small orders when most factories require large MOQs?',
   'Yes. Our supply lines are built around small test batches — many catalog items start from 10-50 units '
   'so you can validate a product before committing to volume. Private-label runs are the exception: they '
   'need MOQ-based production, and we confirm the exact minimum per product in your quote.'),
  ('Which GCC countries do you ship to?',
   'All six: the UAE, Saudi Arabia, Qatar, Kuwait, Oman and Bahrain. Each has its own customs, VAT and '
   'conformity rules, so we prepare destination-specific documents — SABER for Saudi Arabia, ECAS for the '
   'UAE, KUCAS for Kuwait, OFOQ for Bahrain and Bayan for Oman.'),
  ('How much does it cost to start sourcing with you?',
   'A $125 USD intent deposit starts the engagement. It is applied against your order value once you '
   'proceed, or billed as a sourcing service fee if no order materializes. This keeps our sourcing team '
   'focused on serious buyers.'),
  ('How long is a quotation valid?',
   'One week. Factory prices, exchange rates and freight all move, so quotes older than seven days are '
   're-confirmed before any payment.'),
  ('What are your payment terms?',
   '30% deposit to start production, 70% balance before shipment. Quotations are issued as landed GCC '
   'prices in AED unless agreed otherwise.'),
  ('Do you provide private labeling and custom packaging?',
   'Yes — logo printing, custom boxes, bags, cards and inserts on MOQ-based production runs. We do not '
   'do one-piece custom printing.'),
  ('Can you dropship single pieces directly to my customers across the GCC?',
   'No. We consolidate bulk shipments. Shipping single parcels from China to end customers across six '
   'customs territories is slow, costly and compliance-heavy. If you need single-piece fulfillment, the '
   'workable route is a bulk run with your branding warehoused inside the GCC, then shipped locally.'),
  ('Do you handle branded replicas or hazardous goods?',
   'No. Counterfeit or IP-infringing goods, illegal items and hazardous cargo such as aerosols (UN1950) '
   'are outside our scope.'),
]


def seg_card(s):
    points = ''.join('<li>%s</li>' % p for p in s['points'])
    links = ''.join('<a class="rel-card" href="%s"><span>%s</span></a>' % (l[0], l[1]) for l in s['links'])
    return ('<div class="card" style="text-decoration:none">\n'
            '  <div class="em">%s</div>\n'
            '  <h3>%s</h3>\n'
            '  <p style="color:var(--teal);font-weight:700;font-size:14px;margin:8px 0 6px">%s</p>\n'
            '  <p><b>%s</b> %s</p>\n'
            '  <ul style="margin:12px 0 4px 20px;font-size:14.5px">%s</ul>\n'
            '  <div class="rel-grid" style="margin-top:14px">%s</div>\n'
            '</div>' % (s['icon'], s['name'], s['question'], s['answer'], s['who'], points, links))


def prereq_card(icon, title, text):
    return ('<div class="card"><div class="em">%s</div><h3>%s</h3>'
            '<p>%s</p></div>' % (icon, title, text))


def case_card(tag, h3, body, outcome):
    return ('<div class="card" style="text-decoration:none">'
            '<div class="case-tag">%s</div>'
            '<h3 style="margin:8px 0 8px">%s</h3>'
            '<p>%s</p>'
            '<div class="case-outcome">%s</div></div>' % (tag, h3, body, outcome))


def main():
    # ① 4 类买家
    cards = ''.join(seg_card(s) for s in SEGMENTS)
    # ③ 适用条件
    prereqs = ''.join(prereq_card(*p) for p in PREREQS)
    # ④ 5 步流程
    steps = ''.join('<div class="step"><div class="n">%d</div><h3>%s</h3><p>%s</p></div>'
                    % (i + 1, st[0], st[1]) for i, st in enumerate(STEPS))
    # ⑥ 限制
    limits = ''.join('<li><b>%s.</b>%s</li>' % (b, t) for b, t in LIMITS)
    # ⑦ 案例
    cases = ''.join(case_card(*c) for c in CASES)
    # FAQ 可见部分
    faq_html = ''.join('<details><summary>%s</summary><div class="a">%s</div></details>'
                       % (q, a) for q, a in FAQ)

    body = ('<section class="page-hero"><div class="wrap">\n'
        '<div class="crumb"><a href="/" data-en="Home" data-ar="الرئيسية">Home</a> ← <span>Solutions</span></div>\n'
        '<h1>Sourcing built for how you sell</h1>\n'
        '<p class="sub">Different buyers need different controls. This page maps our sourcing, QC and '
        'shipping to your business model — and states plainly what we can and cannot do.</p>\n'
        '<div class="answer-box"><b>SourceToGulf is a China-based sourcing agency for small and mid-size '
        'sellers across the Gulf.</b> We consolidate goods from vetted Chinese factories into single '
        'shipments for buyers in all six GCC countries — the UAE, Saudi Arabia, Qatar, Kuwait, Oman and '
        'Bahrain — with private labeling, custom packaging, QC reports and quotations in AED. Over 3,000 '
        'orders ship every month on this supply line, backed by 14 years of on-the-ground Gulf '
        'experience.</div>\n'
        '</div></section>\n'
        # Key facts 条（可引用硬数字）
        '<section style="padding:30px 0 0"><div class="wrap">\n'
        '<div class="sol-facts"><span><b>6</b> GCC countries</span><span><b>$125</b> to start</span>'
        '<span><b>1-week</b> quote validity</span><span><b>70/30</b> payment terms</span>'
        '<span><b>3,000+</b> orders/month</span><span><b>14 yrs</b> Gulf experience</span></div>\n'
        '</div></section>\n'
        # ① 目标客户
        '<section><div class="wrap">\n'
        '<div class="sec-head center"><span class="kicker">Who this is for</span>\n'
        '<h2>Who is this for?</h2>\n'
        '<p>Four buyer types we work with every week. Find yours — or WhatsApp us if you sit between them.</p></div>\n'
        '<div class="grid2">' + cards + '</div>\n'
        '</div></section>\n'
        # ② 适用场景
        '<section style="padding-top:0"><div class="wrap">\n'
        '<div class="sec-head center"><span class="kicker">Track record</span>\n'
        '<h2>Will this work for my type of business?</h2></div>\n'
        '<div class="answer-box">We have supported buyers in all six GCC countries, with inquiries '
        'spanning women\'s apparel, gaming accessories, fragrance &amp; oud, stationery, anime merchandise '
        'and security equipment. Whatever you sell, chances are we\'ve sourced something like it — and if '
        'a category needs certification or special handling, we say so up front.</div>\n'
        '</div></section>\n'
        # ③ 适用条件
        '<section style="padding-top:0"><div class="wrap">\n'
        '<div class="sec-head center"><span class="kicker">Before you start</span>\n'
        '<h2>What do I need to get started?</h2></div>\n'
        '<div class="answer-box">A product direction (or pick from our catalog), your logo files for '
        'private label, acceptance of 70/30 payment terms, and a $125 intent deposit.</div>\n'
        '<div class="grid2">' + prereqs + '</div>\n'
        '</div></section>\n'
        # ④ 流程
        '<section><div class="wrap">\n'
        '<div class="sec-head center"><span class="kicker">Step by step</span>\n'
        '<h2>How does the sourcing process work?</h2></div>\n'
        '<div class="steps5">' + steps + '</div>\n'
        '<p style="text-align:center;color:var(--muted);font-size:13.5px;margin-top:18px">Timelines vary '
        'by category — every project gets its own schedule before you commit.</p>\n'
        '</div></section>\n'
        # ⑤ 交付清单
        '<section style="padding-top:0"><div class="wrap">\n'
        '<div class="sec-head center"><span class="kicker">Deliverables</span>\n'
        '<h2>What do I get when I work with SourceToGulf?</h2></div>\n'
        '<div class="strip"><span>📦 Catalog curation</span><span>🧾 Landed-AED quotation</span>'
        '<span>👕 Samples</span><span>📷 QC reports (photo &amp; video)</span><span>🎨 Custom packaging</span>'
        '<span>📄 GCC compliance documents (SABER · ECAS)</span><span>🚢 Consolidation &amp; freight</span></div>\n'
        '</div></section>\n'
        # ⑥ 限制说明
        '<section><div class="wrap">\n'
        '<div class="sec-head center"><span class="kicker">Honest limits</span>\n'
        '<h2>What can\'t you source?</h2></div>\n'
        '<div class="answer-box">We do not source counterfeit or IP-infringing brand goods, illegal or '
        'restricted items, or hazardous goods such as aerosols (UN1950).</div>\n'
        '<ul class="limit-list">' + limits + '</ul>\n'
        '</div></section>\n'
        # ⑦ 案例
        '<section style="padding-top:0"><div class="wrap">\n'
        '<div class="sec-head center"><span class="kicker">Case studies</span>\n'
        '<h2>Real sourcing case studies from the Gulf</h2>\n'
        '<p>Anonymized by policy — client names, brands and figures are withheld.</p></div>\n'
        '<div class="grid2">' + cases + '</div>\n'
        '</div></section>\n'
        # FAQ
        '<section><div class="wrap narrow">\n'
        '<div class="sec-head center"><span class="kicker">FAQ</span>\n'
        '<h2>Sourcing questions Gulf buyers ask</h2></div>\n'
        '<div class="faq">' + faq_html + '</div>\n'
        '</div></section>\n'
        # CTA
        '<section style="padding-top:0"><div class="wrap">\n'
        '<div class="cta-box">\n'
        '<h2>Not sure which fits you?</h2>\n'
        '<p>WhatsApp us your business model and target products — we\'ll map the right sourcing route, '
        'and tell you honestly if we\'re not the right fit.</p>\n'
        '<a class="wa-btn" style="background:var(--gold);color:#17201C" href="'
        + wa_link('Hi SourceToGulf! Help me pick the right sourcing plan for my business.')
        + '" target="_blank" rel="noopener">💬 WhatsApp: +971 58 585 4194</a>\n'
        '</div>\n'
        '<p style="text-align:center;font-size:12.5px;color:var(--muted);margin-top:18px">Last updated: '
        'October 2026 · SourceToGulf · Guangzhou, China</p>\n'
        '</section>')

    url = BASE + '/solutions.html'
    title = 'China Sourcing Solutions for Gulf Buyers: Private Label, Small Batches & QC | SourceToGulf'
    desc = ('Sourcing solutions for buyers in all six GCC countries: small test batches, private label, '
            'custom packaging, QC reports, landed-AED quotes, $125 to start. For influencers, wholesalers, '
            'retailers and new brands.')
    # JSON-LD：WebPage（含 BreadcrumbList）+ FAQPage，同一份数据双喂
    ld = json.dumps([
        {
            '@context': 'https://schema.org',
            '@type': 'WebPage',
            'name': title,
            'url': url,
            'description': desc,
            'breadcrumb': {
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE + '/'},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Solutions', 'item': url},
                ],
            },
        },
        {
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            'mainEntity': [
                {'@type': 'Question', 'name': q,
                 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                for q, a in FAQ
            ],
        },
    ], ensure_ascii=False)
    html = page_shell(title, desc, url, body, json_ld=ld,
                      extra_head=PAGE_CSS,
                      alt_ar=BASE + '/ar/solutions.html')
    with open(os.path.join(APP, 'solutions.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('✓ solutions.html (7-block GEO rewrite, EN + hreflang ar)')

if __name__ == '__main__':
    main()
