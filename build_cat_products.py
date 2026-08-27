# -*- coding: utf-8 -*-
"""
build_cat_products.py — 批量生成品类落地页
读取 products.clean.json（cats / prods），
为每个品类生成静态 HTML 品类页 category-<key>.html（含到岸价、双语导航、ItemList/Product JSON-LD），
并生成 categories.html 品类索引页。
用法: python3 build_cat_products.py
"""
import re, os, json
from tpl_common import (APP, price_of, product_card, page_shell, wa_link, HEADER, FOOTER)

SRC = os.path.join(APP, 'products.clean.json')
with open(SRC, encoding='utf-8') as f:
    _data = json.load(f)
cats = _data['cats']
prods = _data['prods']
UPDATED = _data['updated']

BASE = 'https://sourcetogulf.com'
WA_TEXT = 'Hi SourceToGulf! I want a quote for your {cat} collection (landed price to the Gulf).'

# 每个品类的落地页文案
CAT_COPY = {
  'home-fragrance': {
    'sub': 'Flameless diffusers, reed sets, incense and car fragrances — the home-fragrance lines Gulf retailers and gift shops re-order every month. Landed prices to the UAE shown on every item.',
    'intro': 'Home fragrance is a staple in Gulf gifting and home decor — from oud-style reed diffusers to bakhoor-adjacent incense and car fresheners. Every item below is sourced from Guangzhou & Yiwu markets with factory price + freight already calculated to the UAE.'
  },
  'seasonal': {
    'sub': 'Ramadan & Eid lanterns, lights, tableware and gift packaging — the seasonal range Gulf buyers stock ahead of the busy holiday quarter. Landed prices included.',
    'intro': 'Ramadan and Eid drive the biggest gifting spike of the Gulf calendar. Stock lanterns, festive tableware, LED decorations and gift-ready packaging early — we consolidate and ship so your shelves are full before the season.'
  },
  'fashion': {
    'sub': 'Hijab accessories, fashion jewelry, rings and earrings for modest-fashion and accessory sellers across the Gulf. Landed prices to the UAE on every piece.',
    'intro': 'Hijab pins, statement jewelry, gold-plated rings and earrings — the accessory lines that sell year-round to Gulf modest-fashion and livestream sellers. Small MOQs make it easy to test new styles.'
  },
  'tech': {
    'sub': 'Phone accessories, car chargers, holders and gadgets — high-turnover tech SKUs for Gulf e-commerce and retail. Landed prices to the UAE shown.',
    'intro': 'Phone cases, car chargers, mounts and small gadgets are the highest-velocity tech accessories in Gulf markets. Light, cheap to ship, and easy to bundle — ideal for marketplace and TikTok sellers.'
  },
  'home': {
    'sub': 'Home & kitchenware — cookware, storage, tableware and decor sourced from Guangzhou & Yiwu for Gulf homes. Landed prices to the UAE on every item.',
    'intro': 'From kitchen tools to home organization and tableware, these are the everyday products Gulf households buy in volume. Factory-direct pricing with consolidated door-to-door shipping.'
  },
  'beauty-toys': {
    'sub': 'Beauty tools and accessories — mirrors, brushes, organizers and more for Gulf beauty sellers and salons. Landed prices to the UAE included.',
    'intro': 'Beauty tools and accessories are a fast-growing category for Gulf e-commerce and salon buyers. Small, light and giftable — perfect for bundling and impulse purchases.'
  },
  'modest-fashion': {
    'sub': 'Plus-size and modest fashion — embroidered abayas, open-front robes, two-piece sets and chiffon hijabs for Gulf women. Landed prices to the UAE on every piece.',
    'intro': 'Inclusive modest fashion is one of the fastest-growing segments in Gulf e-commerce: abayas, layering robes, two-piece sets and hijabs in extended sizes. We source from Guangzhou modest-wear factories with Arabic-label and SABER support for Saudi-bound shipments.'
  },
  'women-shoes': {
    'sub': 'Plus-size women\'s shoes — wide-fit flat slides, rhinestone slides and block-heel sandals for sizes 42–45. Landed prices to the UAE.',
    'intro': 'Extended-size women\'s footwear is an underserved niche in the Gulf. We source wide-fit flat slides, soft-gold H-strap sandals, rhinestone slides and modest block heels from Guangzhou and Yiwu with landed pricing to the UAE.'
  },
  'lingerie': {
    'sub': 'Plus-size comfort essentials — full-coverage seamless bra & brief sets and breathable smoothing shapewear. Landed prices to the UAE.',
    'intro': 'Everyday full-coverage essentials for plus-size women: seamless bra & brief sets and smoothing shapewear made from breathable, skin-friendly fabrics. Marketed as modest comfort wear and shipped with consolidated Gulf logistics.'
  },
}

# 每个品类的买家 FAQ（GEO：增加可被 AI 引用的问答面；独立陈述、无主观词）
CAT_FAQ = {
  'home-fragrance': [
    ('What is the typical MOQ for home fragrance items?',
     'On SourceToGulf\'s curated picks, home-fragrance MOQs run about 30 to 200 pieces per item. Fully custom scents or private-label production start higher, often 500+ pieces, because the fragrance base and packaging are made to order.'),
    ('Can you handle Arabic labels and Gulf compliance for home fragrance?',
     'Yes. Many Gulf buyers need bilingual or Arabic labeling, so we arrange Arabic printing before shipment. Fragrance and incense items are also screened against destination rules - for Saudi Arabia that means SFDA coordination where applicable.'),
    ('How long does home-fragrance shipping to the Gulf take?',
     'Air freight is typically 7 to 10 days door to door; sea freight (consolidated) is 25 to 35 days. We consolidate with your other categories so one shipment covers everything.'),
  ],
  'seasonal': [
    ('When should I order Ramadan and Eid stock?',
     'Order 2 to 3 months ahead - roughly November to December - so goods clear customs and reach your shelves before Ramadan. We consolidate seasonal stock and ship early to avoid the pre-holiday rush.'),
    ('What are typical MOQs for seasonal items?',
     'Most lanterns, festive tableware and gift packaging start at 50 to 300 pieces per design. Lower-MOQ items let small sellers test a few styles before committing to volume.'),
    ('Do you handle Arabic or gift packaging for seasonal products?',
     'Yes. Custom Arabic and gift-ready packaging is available at low MOQ, which is what makes these items re-orderable through the holiday quarter.'),
  ],
  'fashion': [
    ('What is the MOQ for hijab accessories and fashion jewelry?',
     'Curated picks range from 12 to 200 pieces per style. Custom plating, stone settings or private-label branding start higher, typically 300+ pieces per design.'),
    ('Can fashion items be shipped to Saudi Arabia with SABER?',
     'Yes. We handle SABER registration for the apparel and accessories categories that require it, and arrange Arabic labels so the shipment clears Jeddah or Dammam without delay.'),
    ('How fast can I reorder fashion bestsellers?',
     'Reorders from the same Guangzhou market usually take 10 to 20 days including pre-shipment QC, since the supplier and spec are already confirmed.'),
  ],
  'tech': [
    ('What are typical MOQs for phone accessories?',
     'Most phone cases, chargers and holders run 50 to 500 pieces per model; many curated picks sit around 100 pieces, which suits marketplace and TikTok sellers testing styles.'),
    ('Do tech accessories need GCC conformity like ECAS or QC?',
     'Some do - chargers, power banks and batteries often need conformity certificates (ECAS for the UAE, QC for Qatar, and others). We screen each product and prepare the documents before shipment.'),
    ('How long does tech shipping to the Gulf take?',
     'Air freight is 7 to 10 days door to door; sea consolidation is 25 to 35 days. Light tech accessories are cheap to ship, which is why they turn over fast.'),
  ],
  'home': [
    ('What is the MOQ for home and kitchenware?',
     'Most items run 50 to 300 pieces per product. Because we consolidate, a small brand can mix many home SKUs into one container at per-item minimums.'),
    ('Can you consolidate home goods with other categories?',
     'Yes. Goods from all categories arrive at our single Guangzhou warehouse, get inspected and repacked, then ship as one Gulf shipment - one customs entry, lower freight.'),
    ('Do you handle fragile-item packing?',
     'Yes. Fragile kitchen and decor items get protective packing and a pre-shipment photo/video check, so breakage is caught in China, not at your door.'),
  ],
  'beauty-toys': [
    ('What is the MOQ for beauty tools and accessories?',
     'Most beauty tools and organizers run 50 to 300 pieces per item. Small, light and giftable items are easy to bundle and ideal for impulse and salon buyers.'),
    ('Do beauty items need SFDA or halal documents for Saudi?',
     'Some cosmetics and supplements do. We filter suppliers with the right certifications and prepare the supporting documents so Saudi-bound goods clear without holds.'),
    ('Can beauty tools be private-labeled?',
     'Yes. Low-MOQ custom branding and Arabic labels are available, which is what lets small Gulf brands launch their own beauty line without large minimums.'),
  ],
  'modest-fashion': [
    ('What is the MOQ for plus-size abayas and modest sets?',
     'Curated plus-size abayas start around 20 pieces per style; hijab sets start around 50 pieces. Custom embroidery, fabric or private-label tags start higher, typically 100+ pieces per design.'),
    ('Can abayas ship to Saudi Arabia with SABER and Arabic labels?',
     'Yes. We arrange Arabic care labels and handle SABER registration for apparel categories that require it, so shipments clear Jeddah or Dammam without delay.'),
    ('How long do reorders of modest fashion take?',
     'Reorders from Guangzhou modest-wear factories usually take 14 to 20 days including pre-shipment QC, because the supplier and spec are already confirmed.'),
  ],
  'women-shoes': [
    ('What sizes are available for plus-size women\'s shoes?',
     'We focus on extended sizes 42 to 45 (EU) with wide-fit construction — the range most underserved in Gulf markets. Mixed-size packs are available at MOQ.'),
    ('Can shoes be consolidated with other categories in one shipment?',
     'Yes. Shoes arrive at our Guangzhou warehouse, are inspected, then consolidated with your other categories into a single Gulf-bound shipment.'),
    ('What is the MOQ for plus-size shoe styles?',
     'Plus-size flat slides, rhinestone slides and block-heel sandals run about 30 pairs per style at the curated level. Custom colors or branded footbeds start higher.'),
  ],
  'lingerie': [
    ('What is the MOQ for plus-size comfort essentials?',
     'Full-coverage bra & brief sets start around 50 pieces per size run; shapewear starts around 50 pieces. Mixed-size packs can be arranged.'),
    ('Are these items compliant for Gulf markets?',
     'We source breathable, skin-friendly fabrics and can prepare supporting documents for Gulf-bound shipments. Marketing and imagery stay modest and full-coverage.'),
    ('Can comfort essentials be private-labeled?',
     'Yes. Low-MOQ custom tags, Arabic labels and neutral packaging are available, which lets Gulf brands launch their own everyday essentials line without large minimums.'),
  ],
}

def json_ld_for(cat, items):
    els = []
    for i, p in enumerate(items, 1):
        pr = price_of(p)
        els.append('    {\n      "@type": "ListItem",\n      "position": %d,\n      "item": {\n        "@type": "Product",\n        "name": %s,\n        "image": "%s%s",\n        "category": %s,\n        "offers": {\n          "@type": "Offer",\n          "priceCurrency": "USD",\n          "price": %.2f,\n          "availability": "https://schema.org/InStock",\n          "minOrderQuantity": %d\n        }\n      }\n    }' % (
            i,
            json.dumps(p['name_en']),
            BASE, p['img'],
            json.dumps(cat['en']),
            pr['landed'], p['moq']))
    itemlist_str = ('{\n'
        '  "@context": "https://schema.org",\n'
        '  "@type": "ItemList",\n'
        '  "name": ' + json.dumps(cat['en'] + ' — SourceToGulf') + ',\n'
        '  "url": "' + BASE + '/category-' + cat['key'] + '.html",\n'
        '  "numberOfItems": ' + str(len(items)) + ',\n'
        '  "itemListElement": [\n' + ',\n'.join(els) + '\n  ]\n}')
    faq = CAT_FAQ.get(cat['key'])
    if faq:
        faq_ld = json.dumps({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faq
            ]
        }, ensure_ascii=False, indent=2)
        return '[\n' + itemlist_str + ',\n' + faq_ld + '\n]'
    return itemlist_str

def build_category_page(cat, items, other_cats):
    key = cat['key']
    url = BASE + '/category-' + key + '.html'
    cards = ''.join(product_card(p) for p in items)
    copy = CAT_COPY.get(key, {'sub': cat['en'] + ' sourced from China to the Gulf.', 'intro': ''})
    # 其他品类互链
    rel = ''
    for o in other_cats:
        if o['key'] == key:
            continue
        rel += ('<a class="rel-card" href="/category-%s.html"><span>%s</span><span>%d items · landed prices</span></a>'
                % (o['key'], o['en'], len([p for p in prods if p['cat'] == o['key']])))
    faq = CAT_FAQ.get(key)
    faq_html = ''
    if faq:
        faq_items = ''.join('<div class="qa"><h3>%s</h3><p>%s</p></div>' % (q, a) for q, a in faq)
        faq_html = ('<section style="padding-top:0"><div class="wrap">'
            '<div class="sec-head"><span class="kicker">FAQ</span><h2>%s - common questions</h2></div>'
            '<div class="qa-list">' % cat['en']) + faq_items + '</div></div></section>'
    body = ('<section class="page-hero"><div class="wrap">\n'
        '<div class="crumb"><a href="/" data-en="Home" data-ar="الرئيسية">Home</a> ← <a href="/products.html" data-en="Hot Picks" data-ar="أبرز المنتجات">Hot Picks</a> ← <span>' + cat['en'] + '</span></div>\n'
        '<h1>' + cat['en'] + '</h1>\n'
        '<p class="sub">' + copy['sub'] + '</p>\n'
        '</div></section>\n'
        '<section style="padding-top:0"><div class="wrap">\n'
        '<div class="pgrid">\n' + cards + '\n</div>\n'
        '<p class="updated-note"><span>Updated ' + UPDATED + ' &middot; new picks every month</span></p>\n'
        '<div class="strip" style="margin-top:34px">\n'
        '  <div><b>How we price</b><span>Factory price + Cainiao Middle East line freight at MOQ weight. Reference price, not a binding quote.</span></div>\n'
        '  <div><b>Duties &amp; VAT</b><span>Not included — depends on your country &amp; declared value. Use our calculator for full landed cost.</span></div>\n'
        '  <div><b>QC on every order</b><span>Photo/video check before anything ships. You approve, then we send.</span></div>\n'
        '</div>\n'
        '</div></section>\n'
        '<section style="padding-top:0"><div class="wrap">\n'
        '<h2 style="margin-bottom:18px">Browse other categories</h2>\n'
        '<div class="rel-grid">' + rel + '</div>\n'
        '</div></section>\n'
        + faq_html + '\n'
        '<section style="padding-top:0"><div class="wrap">\n'
        '  <div class="cta-box">\n'
        '    <h2>Want a custom ' + cat['en'] + ' list?</h2>\n'
        '    <p>WhatsApp us a photo or link — we source it, quote the landed price, and QC before shipping.</p>\n'
        '    <a class="wa-btn" href="' + wa_link(WA_TEXT.format(cat=cat['en'])) + '" target="_blank" rel="noopener">💬 WhatsApp: +971 58 514 6139</a>\n'
        '  </div>\n'
        '</div></section>')
    title = cat['en'] + ' from China to the Gulf | SourceToGulf Landed Prices'
    desc = copy['sub']
    return page_shell(title, desc, url, body, json_ld=json_ld_for(cat, items))

def build_index_page():
    url = BASE + '/categories.html'
    cards = ''
    for c in cats:
        n = len([p for p in prods if p['cat'] == c['key']])
        copy = CAT_COPY.get(c['key'], {'intro': ''})['intro']
        cards += ('<a class="card" href="/category-%s.html" style="text-decoration:none">\n'
                  '  <div class="em">📦</div>\n'
                  '  <h3>%s <span style="font-weight:400;color:var(--muted)">· %s</span></h3>\n'
                  '  <p>%d ready-to-order items with landed prices to the Gulf.</p>\n'
                  '  <span class="painline">Browse %s →</span>\n'
                  '</a>' % (c['key'], c['en'], c['ar'], n, c['en']))
    body = ('<section class="page-hero"><div class="wrap">\n'
        '<div class="crumb"><a href="/" data-en="Home" data-ar="الرئيسية">Home</a> ← <span>Categories</span></div>\n'
        '<h1>Shop by Category — Landed Prices to the Gulf</h1>\n'
        '<p class="sub">Every product below is sourced from Guangzhou &amp; Yiwu markets with factory price + freight already calculated to the UAE. Pick a category to see landed prices, MOQ and lead time.</p>\n'
        '</div></section>\n'
        '<section style="padding-top:0"><div class="wrap">\n'
        '<div class="grid3">' + cards + '</div>\n'
        '</div></section>\n'
        '<section style="padding-top:0"><div class="wrap">\n'
        '  <div class="cta-box">\n'
        '    <h2>Can\'t find your product?</h2>\n'
        '    <p>WhatsApp us a photo — we\'ll source it, quote the landed price, and QC before shipping.</p>\n'
        '    <a class="wa-btn" href="' + wa_link('Hi SourceToGulf! I am looking for a product not listed. Can you source it?') + '" target="_blank" rel="noopener">💬 WhatsApp: +971 58 514 6139</a>\n'
        '  </div>\n'
        '</div></section>')
    return page_shell('Shop by Category | SourceToGulf Landed Prices to the Gulf',
                      'Browse SourceToGulf product categories with landed prices to the Gulf: home fragrance, Ramadan & Eid, hijab & jewelry, phone & car accessories, home & kitchen, beauty tools.',
                      url, body)

def main():
    for c in cats:
        items = [p for p in prods if p['cat'] == c['key']]
        html = build_category_page(c, items, cats)
        fn = os.path.join(APP, 'category-' + c['key'] + '.html')
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(html)
        print('✓ category-%s.html (%d items)' % (c['key'], len(items)))
    idx = build_index_page()
    with open(os.path.join(APP, 'categories.html'), 'w', encoding='utf-8') as f:
        f.write(idx)
    print('✓ categories.html (index)')
    print('Done.')

if __name__ == '__main__':
    main()
