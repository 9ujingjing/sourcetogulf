# -*- coding: utf-8 -*-
"""
build_solutions.py — 买家分群 / 解决方案页 solutions.html
覆盖 4 类买家: Influencer/社媒带货, Wholesaler/批发商, Retailer/零售商, Small Brand/自有品牌,
结合海湾市场语境。复用站点模板。
用法: python3 build_solutions.py
"""
import os, json
from tpl_common import APP, page_shell, wa_link

BASE = 'https://sourcetogulf.com'

SEGMENTS = [
  {
    'icon': '📱',
    'name': 'Influencer & Livestream Sellers',
    'name_ar': 'صناع المحتوى والبث المباشر',
    'tag': '社媒带货',
    'who': 'TikTok KSA, Instagram UAE and livestream sellers who need trend-ready stock fast.',
    'points': [
      'Small MOQ to test viral items — hijab jewelry, phone accessories, beauty tools',
      'Photogenic samples + QC photos/videos you can use in your content',
      'Private label to turn winning items into your own product line',
      'Fast restocks so you never miss a trend window'
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
    'name_ar': 'تجار الجملة والموزعون',
    'tag': '批发商',
    'who': 'Buyers moving volume across the Gulf who need consolidated, mixed-category shipments.',
    'points': [
      'Bulk pricing with mixed categories from many suppliers in one container',
      'Consolidation in Guangzhou — one shipment, one customs entry, lower freight',
      'Repeat-order management with consistent quality and lead times',
      'SABER / documentation handled for Saudi-bound goods'
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
    'name_ar': 'تجار التجزئة والسلاسل',
    'tag': '零售商',
    'who': 'Shops and retail chains that need retail-ready, consistently replenished stock.',
    'points': [
      'Retail-ready packaging, barcodes and consistent sizing',
      'Replenishment planning matched to your sales velocity',
      'Pre-shipment QC so shelves stay consistent, returns stay low',
      'Multi-supplier sourcing so one PO covers a full category'
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
    'name_ar': 'العلامات الناشئة',
    'tag': '自有品牌',
    'who': 'Founders building a private-label line on small minimums.',
    'points': [
      'OEM / private label with your logo at low minimums',
      'Custom packaging — boxes, bags, cards, inserts',
      'Product development support from a physical sample',
      'Same QC and door-to-door shipping as volume buyers'
    ],
    'links': [
      ('/services/custom-branding-packaging.html', 'Private label & packaging'),
      ('/category-fashion.html', 'Hijab & jewelry'),
      ('/category-seasonal.html', 'Ramadan & Eid'),
      ('/services/product-sourcing-china.html', 'Product sourcing'),
    ],
  },
]

def seg_card(s):
    points = ''.join('<li>%s</li>' % p for p in s['points'])
    links = ''.join('<a class="rel-card" href="%s"><span>%s</span></a>' % (l[0], l[1]) for l in s['links'])
    return ('<div class="card" style="text-decoration:none">\n'
            '  <div class="em">%s</div>\n'
            '  <h3>%s</h3>\n'
            '  <p style="color:var(--gold);font-weight:700;font-size:12.5px;margin:-2px 0 8px">%s</p>\n'
            '  <p>%s</p>\n'
            '  <ul style="margin:12px 0 4px 20px;font-size:14.5px">%s</ul>\n'
            '  <div class="rel-grid" style="margin-top:14px">%s</div>\n'
            '</div>' % (s['icon'], s['name'], s['tag'], s['who'], points, links))

def main():
    cards = ''.join(seg_card(s) for s in SEGMENTS)
    body = ('<section class="page-hero"><div class="wrap">\n'
        '<div class="crumb"><a href="/" data-en="Home" data-ar="الرئيسية">Home</a> ← <span>Solutions</span></div>\n'
        '<h1>Sourcing built for how you sell</h1>\n'
        '<p class="sub">Different buyers need different controls. Pick the path that matches your business model — we flex our sourcing, QC and shipping to fit.</p>\n'
        '</div></section>\n'
        '<section style="padding-top:0"><div class="wrap">\n'
        '<div class="grid2">' + cards + '</div>\n'
        '</div></section>\n'
        '<section style="padding-top:0"><div class="wrap">\n'
        '  <div class="cta-box">\n'
        '    <h2>Not sure which fits you?</h2>\n'
        '    <p>WhatsApp us your business model and target products — we\'ll map the right sourcing route.</p>\n'
        '    <a class="wa-btn" style="background:var(--gold);color:#17201C" href="' + wa_link('Hi SourceToGulf! Help me pick the right sourcing plan for my business.') + '" target="_blank" rel="noopener">💬 WhatsApp: +971 58 585 4194</a>\n'
        '  </div>\n'
        '</div></section>')
    url = BASE + '/solutions.html'
    title = 'China Sourcing Solutions for Gulf Buyers | SourceToGulf'
    desc = 'Sourcing, QC, custom branding and samples adapted to your model — influencers, wholesalers, retailers and private-label brands across the Gulf.'
    html = page_shell(title, desc, url, body,
                      json_ld=json.dumps({
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
                          ]
                        }
                      }, ensure_ascii=False))
    with open(os.path.join(APP, 'solutions.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('✓ solutions.html (4 buyer segments)')

if __name__ == '__main__':
    main()
