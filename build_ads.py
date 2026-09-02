# -*- coding: utf-8 -*-
"""
build_ads.py — 生成 google-ads/ 投放落地页
轻量、快加载、单一强 CTA（WhatsApp），供 Google Ads 投放指向。
用法: python3 build_ads.py
"""
import os, json
from tpl_common import APP, page_shell, wa_link, HEADER, FOOTER

BASE = 'https://sourcetogulf.com'

ADS = [
  {
    'file': 'hijab-jewelry.html',
    'title': 'Hijab & Jewelry from China: MOQ & FOB for Gulf Sellers | SourceToGulf',
    'desc': 'Wholesale hijab accessories and fashion jewelry from China to the UAE with all-in prices, small MOQ and QC before dispatch. Get a free quote on WhatsApp.',
    'h1': 'Hijab & Jewelry Wholesale — Landed Price to the UAE',
    'sub': 'Modest-fashion pins, gold-plated rings, earrings and accessories sourced from Guangzhou & Yiwu. Factory price + freight calculated to Dubai, no quoting ping-pong.',
    'bullets': [
      ('Small MOQ', 'Test new styles with low minimums — perfect for Instagram & TikTok sellers.'),
      ('Landed price', 'Every quote includes freight to the UAE. You see the real cost before deposit.'),
      ('QC before shipping', 'Photo/video check of actual goods. You approve, then we send.'),
      ('Door to door', 'Consolidated in Guangzhou, shipped to your door in Dubai / Abu Dhabi.'),
    ],
    'cat_link': '/category-fashion.html',
    'cat_name': 'Hijab accessories & jewelry',
    'wa': 'Hi SourceToGulf! I saw your hijab & jewelry wholesale ad. Please send your all-in prices to UAE.',
  },
  {
    'file': 'ramadan.html',
    'title': 'Ramadan & Eid Wholesale to GCC | SourceToGulf',
    'desc': 'Wholesale Ramadan lanterns, festive tableware and gift packaging from China to the Gulf. Stock early with all-in prices and combined orders from multiple suppliers.',
    'h1': 'Ramadan & Eid Wholesale — Stock Early, Ship to the Gulf',
    'sub': 'Lanterns, LED decorations, festive tableware and gift-ready packaging sourced from Yiwu & Guangzhou. Landed prices and consolidated door-to-door shipping to all six GCC countries.',
    'bullets': [
      ('Seasonal range', 'Lanterns, lights, tableware and gift packaging — the lines Gulf buyers stock before Ramadan.'),
      ('Landed price', 'Factory price + freight included. Plan your margin before you commit.'),
      ('Consolidation', 'Mix Ramadan items with your everyday SKUs in one shipment.'),
      ('All GCC', 'UAE, Saudi, Kuwait, Qatar, Bahrain, Oman — SABER handled for Saudi.'),
    ],
    'cat_link': '/category-seasonal.html',
    'cat_name': 'Ramadan & Eid seasonal',
    'wa': 'Hi SourceToGulf! I saw your Ramadan wholesale ad. Please send the seasonal catalog and all-in prices.',
  },
  {
    'file': 'phone-accessories.html',
    'title': 'Phone & Car Accessories Wholesale to Gulf | SourceToGulf',
    'desc': 'Wholesale phone cases, chargers, car mounts and gadgets from China to the Gulf with all-in prices and low MOQ. Free quote on WhatsApp.',
    'h1': 'Phone & Car Accessories Wholesale — Landed Price to the Gulf',
    'sub': 'High-velocity tech accessories sourced from Guangzhou & Yiwu. Light, cheap to ship, easy to bundle — ideal for marketplace and TikTok sellers across the Gulf.',
    'bullets': [
      ('High turnover', 'Phone cases, chargers, mounts and gadgets — the SKUs Gulf e-commerce sells fastest.'),
      ('Landed price', 'Freight to the Gulf included. Bundle and protect your margin.'),
      ('Small & light', 'Low shipping cost per unit — great for trial orders and restocks.'),
      ('QC before shipping', 'Photo/video proof of actual goods before final payment.'),
    ],
    'cat_link': '/category-tech.html',
    'cat_name': 'Phone & car accessories',
    'wa': 'Hi SourceToGulf! I saw your phone accessories ad. Please send your all-in prices to the Gulf.',
  },
]

def build(ad):
    bullets = ''.join(
        '<div class="card" style="text-decoration:none"><div class="em">✓</div><h3>%s</h3><p>%s</p></div>' % (b[0], b[1])
        for b in ad['bullets'])
    body = ('<section class="page-hero"><div class="wrap">\n'
        '<div class="crumb"><a href="/" data-en="Home" data-ar="الرئيسية">Home</a> ← <span>Wholesale</span></div>\n'
        '<h1>' + ad['h1'] + '</h1>\n'
        '<p class="sub">' + ad['sub'] + '</p>\n'
        '<div class="hero-cta">\n'
        '  <a class="wa-btn" style="background:var(--teal);color:#fff" href="' + wa_link(ad['wa']) + '" target="_blank" rel="noopener">💬 Get a free quote on WhatsApp</a>\n'
        '  <a class="btn-ghost" href="' + ad['cat_link'] + '">Browse the collection →</a>\n'
        '</div>\n'
        '</div></section>\n'
        '<section style="padding-top:0"><div class="wrap">\n'
        '<div class="grid2">' + bullets + '</div>\n'
        '</div></section>\n'
        '<section style="padding-top:0"><div class="wrap">\n'
        '  <div class="cta-box">\n'
        '    <h2>Ready to order?</h2>\n'
        '    <p>WhatsApp us your target products or a photo. We quote the landed price and QC before shipping.</p>\n'
        '    <a class="wa-btn" style="background:var(--gold);color:#17201C" href="' + wa_link(ad['wa']) + '" target="_blank" rel="noopener">💬 WhatsApp: +971 58 585 4194</a>\n'
        '  </div>\n'
        '</div></section>')
    url = BASE + '/google-ads/' + ad['file']
    ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": ad['title'],
        "url": url,
        "description": ad['desc'],
        "inLanguage": "en",
        "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": ad['title'],
             "item": url},
        ]},
    }
    return page_shell(ad['title'], ad['desc'], url, body,
                      json_ld=json.dumps(ld, ensure_ascii=False, indent=2),
                      extra_head='<meta name="robots" content="index,follow">\n')

def main():
    out = os.path.join(APP, 'google-ads')
    os.makedirs(out, exist_ok=True)
    for ad in ADS:
        html = build(ad)
        with open(os.path.join(out, ad['file']), 'w', encoding='utf-8') as f:
            f.write(html)
        print('✓ google-ads/%s' % ad['file'])
    print('Done. %d ad landing pages.' % len(ADS))

if __name__ == '__main__':
    main()
