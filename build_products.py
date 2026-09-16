# -*- coding: utf-8 -*-
"""
build_products.py — 单一真相源 SSR 生成 products.html
========================================================
读取 products.clean.json（与品类页 build_cat_products.py 同一数据源），
用 tpl_common.product_card() 渲染所有产品卡（每张带 data-cat），SSR 填充 #pgrid；
同时静态生成筛选 chips、updated-note，以及覆盖全部产品的 ItemList JSON-LD。

彻底移除对 products-data.js（内嵌 PRODUCTS）的依赖 —— 实现全站单一数据源。

重要约束：tpl_common 在 import 时会从当前 products.html 抽取 <style>/<header>/<footer>
作为全站共享模板。本脚本用 page_shell 重写 products.html 时，把抽取到的原块原样嵌回，
下一轮 import 抽取新文件时内容一致，形成无害闭环（不会破坏其他页面样式）。

GA4 去重：旧 products.html 作为源页已自带 GA4，page_shell 会再注入一份，
故生成后 dedupe_ga4() 保证全站只有一份 GA4。
"""
import os, re, json
from tpl_common import (APP, price_of, product_card, page_shell, GA4_SNIPPET)

SRC = os.path.join(APP, 'products.clean.json')
with open(SRC, encoding='utf-8') as f:
    _data = json.load(f)
cats = _data['cats']
prods = _data['prods']
UPDATED = _data.get('updated', '')
BASE = 'https://sourcetogulf.com'
CAT_EN = {c['key']: c['en'] for c in cats}


def card(p):
    """产品卡加 data-cat（供客户端筛选显隐），其余沿用品类页统一样式。"""
    return product_card(p).replace('<div class="pcard">',
                                   '<div class="pcard" data-cat="%s">' % p['cat'], 1)


# ---------------------------------------------------------------- 三大主线
# 用户 2026-09-16 明确：主推 ①服装定制+小单快返 ②时尚珠宝设计定制 ③包装设计定制。
# 其余（LED 狗链、压缩沙发、电镀手机壳等）归为「能找的货 / 已对接工厂」，单独成块。
LINES = [
    {
        'kicker': 'Line 01',
        'title': 'Custom apparel — small batch, fast reorder',
        'promise': 'Abayas, kaftans and modest wear made to your design. Sampling in days, '
                   'and reorders that do not sit behind someone else\'s container.',
        'imgs': [('/images/apparel/fabric-wall-1.jpg',
                  'Hundreds of fabric colour cards on the wall — you choose, we make'),
                 ('/images/apparel/apparel-rack-showroom.jpg',
                  'Sample room rail — styles already developed and ready to adapt')],
        'bullets': ['Fabric library on the wall — pick the hand feel and colour, not a catalogue photo',
                    'In-house sampling room: pattern, cut, stitch, press',
                    'Your own woven label, care label, size tag and hangtag'],
    },
    {
        'kicker': 'Line 02',
        'title': 'Fashion jewelry — design to sample',
        'promise': '316L stainless steel, PVD gold plating and moissanite. Send a sketch or a '
                   'photo and we turn it into a physical sample you can hold before you commit.',
        'imgs': [('/images/gold-rings-bowl.jpg',
                  '18K PVD gold-plated 316L stainless steel rings'),
                 ('/images/jewelry-showroom-table.jpg',
                  'Jewelry showroom table — designs available to customise')],
        'bullets': ['316L stainless steel base — tarnish-resistant, no green finger',
                    'PVD gold plating and GRA-certified moissanite',
                    'Your logo on the pouch, the box and the jewellery tag'],
    },
    {
        'kicker': 'Line 03',
        'title': 'Custom packaging — designed, printed and made in-house',
        'promise': 'Folding cartons, mailer boxes, rigid gift boxes, drawer boxes and paper bags. '
                   'Printing, die-cutting, gluing and pulp inserts all happen in the same factory.',
        'imgs': [('/images/packaging/package-gluing-machine.jpg',
                  'Folder-gluer running a folding carton — made in-house'),
                 ('/images/packaging/package-printing-press.jpg',
                  'Printing press on site — not brokered out')],
        'bullets': ['Printing, die-cutting, gluing and pulp inserts on site',
                    'Structure design from a flat dieline — not just printing your logo',
                    'Hot foil, emboss, spot UV, lamination — we will tell you which are worth it'],
    },
]

WA_GENERIC = 'https://wa.me/971585854194'


def build_lines():
    out = ('<section style="padding-top:0"><div class="wrap">\n'
           '<h2 style="margin-bottom:6px">Three lines we actually run</h2>\n'
           '<p class="sub" style="margin-bottom:22px">Not a marketplace of 30 million things. '
           'Three lines where we can put your brand on it, sample it, and reorder it fast.</p>\n')
    for i, L in enumerate(LINES):
        imgs = ''.join(
            '<figure style="margin:0;">'
            '<img src="%s" alt="%s" loading="lazy" style="width:100%%;border-radius:14px;'
            'border:1px solid #E7E1D4;object-fit:cover;aspect-ratio:4/3;">'
            '<figcaption style="font-size:12.5px;color:var(--muted);margin-top:7px;'
            'text-align:center;">%s</figcaption></figure>' % (u, a, a)
            for u, a in L['imgs'])
        bullets = ''.join('<li style="margin:4px 0">%s</li>' % b for b in L['bullets'])
        out += (
            '<div style="display:grid;grid-template-columns:1fr;gap:16px;margin:0 0 26px;'
            'background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px 22px">\n'
            '  <div style="font-size:12px;font-weight:600;letter-spacing:.08em;'
            'text-transform:uppercase;color:var(--gold)">%s</div>\n'
            '  <h3 style="margin:0 0 4px;font-size:17px">%s</h3>\n'
            '  <p style="margin:0 0 14px;color:var(--muted)">%s</p>\n'
            '  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;'
            'margin-bottom:14px">%s</div>\n'
            '  <ul style="margin:0 0 14px;padding-left:20px;font-size:13.5px;'
            'color:var(--muted)">%s</ul>\n'
            '</div>\n' % (L['kicker'], L['title'], L['promise'], imgs, bullets))
    out += ('<div style="text-align:center;margin:-8px 0 0">'
            '<a class="wa-btn" href="' + WA_GENERIC + '" target="_blank" rel="noopener">'
            '💬 Ask about these three lines</a></div>\n')
    out += '</div></section>\n'
    return out


# ---------------------------------------------------------------- 产能背书
# 合作工厂 JOC（江苏海外集团旗下）：只给数字，不给名字 —— 避免客户绕过我们直接找工厂。
CAPACITY_STATS = [('4,800', 'workers · five plants'),
                  ('68', 'production lines'),
                  ('750,000', 'garments per month'),
                  ('BSCI / WRAP', 'audited')]
CAPACITY_PLANTS = [
    ('Jiangsu, China', '200 people · 4 lines · 40,000 a month',
     'Small batches, sampling and reorders. BSCI + WRAP audited.'),
    ('Mandalay, Myanmar', '3,200 people · 41 lines · 350,000 a month',
     'Woven outerwear, wool jackets, trousers, skirts. BSCI audited.'),
    ('Vietnam, two plants', '1,400 people · 23 lines · 360,000 a month',
     'Woven outerwear, trousers, dresses.'),
]


def build_capacity():
    stats = ''.join('<div><b style="font-size:19px;display:block;color:var(--ink)">%s</b>'
                    '<span style="font-weight:400;font-size:12.5px">%s</span></div>'
                    % (v, l) for v, l in CAPACITY_STATS)
    rows = ''.join(
        '<div style="display:flex;flex-wrap:wrap;gap:4px 16px;padding:12px 0;'
        'border-top:1px solid var(--line)">'
        '<div style="flex:1 1 200px"><b style="font-size:13.5px">%s</b>'
        '<span style="display:block;font-size:12.5px;color:var(--muted)">%s</span></div>'
        '<div style="flex:2 1 280px;font-size:12.5px;color:var(--muted)">%s</div></div>'
        % (a, b, c) for a, b, c in CAPACITY_PLANTS)
    return (
        '<section style="padding-top:0"><div class="wrap">\n'
        '<h2 style="margin-bottom:4px">The capacity behind us</h2>\n'
        '<p class="sub" style="margin-bottom:16px">We work from a partner group owned by one of '
        'Jiangsu province\'s pillar enterprises. Numbers, not adjectives.</p>\n'
        '<div class="strip" style="margin-bottom:16px">%s</div>\n'
        '<div style="background:#fff;border:1px solid var(--line);border-radius:16px;'
        'padding:6px 22px 12px">%s</div>\n'
        '<p style="font-size:13px;color:var(--muted);margin-top:12px">Half the group\'s output is '
        'womenswear, and most of it ships to European and US buyers — which is why finishing, '
        'labelling and packing are already at export grade before anything reaches the Gulf.</p>\n'
        '</div></section>\n' % (stats, rows))


# ---------------------------------------------------------------- 长尾：能找的货 / 已对接工厂
LONGTAIL = [('LED pet leads', 'Light-up dog leads and collars, factory direct'),
            ('Compressed sofas', 'Vacuum-packed sofas — shipped flat to save container space'),
            ('Plated phone cases', 'Electroplated iPhone cases, custom finish and logo')]


def build_longtail():
    cells = ''.join(
        '<div style="background:#fff;border:1px solid var(--line);border-radius:12px;'
        'padding:14px 16px"><b style="font-size:13.5px">%s</b>'
        '<span style="display:block;font-size:12.5px;color:var(--muted);margin-top:3px">%s</span>'
        '</div>' % (a, b) for a, b in LONGTAIL)
    return (
        '<section style="padding-top:0"><div class="wrap">\n'
        '<h2 style="margin-bottom:4px">Other factories we work with directly</h2>\n'
        '<p class="sub" style="margin-bottom:14px">These are not our core lines, but we already '
        'have the factory relationship — so if you need one, we can quote it this week.</p>\n'
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));'
        'gap:12px">%s</div>\n'
        '<p style="font-size:13px;color:var(--muted);margin-top:12px">Not listed? Send us a photo '
        '— sourcing a new factory is the part we do best.</p>\n'
        '</div></section>\n' % cells)


def build_chips():
    counts = {c['key']: sum(1 for p in prods if p['cat'] == c['key']) for c in cats}
    h = '<div id="chips">\n'
    h += '  <button data-cat="all" class="on">All (%d)</button>\n' % len(prods)
    for c in cats:
        h += '  <button data-cat="%s">%s (%d)</button>\n' % (c['key'], c['en'], counts[c['key']])
    h += '</div>'
    return h


def build_grid():
    return '<div class="pgrid" id="pgrid">\n' + ''.join(card(p) for p in prods) + '\n</div>'


def build_rel():
    h = '<div class="rel-grid" style="margin-top:28px">\n'
    for c in cats:
        n = sum(1 for p in prods if p['cat'] == c['key'])
        h += ('  <a class="rel-card" href="/category-%s.html"><span>%s</span>'
              '<span>%d items · landed prices</span></a>\n' % (c['key'], c['en'], n))
    h += ('  <a class="rel-card" href="/categories.html"><span>Browse all categories →</span>'
          '<span>%d ready-to-order items</span></a>\n' % len(prods))
    h += ('  <a class="rel-card" href="/solutions.html"><span>Solutions by buyer type</span>'
          '<span>Influencer · Wholesale · Retail · Brand</span></a>\n')
    h += '</div>'
    return h


def _desc(p):
    return ('%s — China sourcing for Gulf markets. MOQ %d pcs. FOB CNY %s/pc. '
            'Custom branding (logo on packaging) and physical samples before you commit. '
            'From SourceToGulf, your Guangzhou sourcing partner.') % (p['name_en'], p['moq'], p['fob_cny'])


def json_ld():
    els = []
    for i, p in enumerate(prods, 1):
        pr = price_of(p)
        els.append('    {\n      "@type": "ListItem",\n      "position": %d,\n      "item": {\n'
                   '        "@type": "Product",\n'
                   '        "name": %s,\n        "image": "%s%s",\n'
                   '        "description": %s,\n'
                   '        "brand": {"@type": "Brand", "name": "SourceToGulf"},\n'
                   '        "category": %s,\n        "offers": {\n'
                   '          "@type": "Offer",\n'
                   '          "priceCurrency": "USD",\n          "price": %.2f,\n'
                   '          "availability": "https://schema.org/InStock",\n'
                   '          "minOrderQuantity": %d,\n'
                   '          "hasMerchantReturnPolicy": {\n'
                   '            "@type": "MerchantReturnPolicy",\n'
                   '            "merchantReturnDays": 7,\n'
                   '            "returnMethod": "https://schema.org/ReturnByMail",\n'
                   '            "returnFees": "https://schema.org/FreeReturn"\n'
                   '          },\n'
                   '          "shippingDetails": {\n'
                   '            "@type": "OfferShippingDetails",\n'
                   '            "shippingDestination": {"@type": "DefinedRegion", "addressCountry": ["AE","SA","KW","QA","BH","OM"]},\n'
                   '            "shippingRate": {"@type": "MonetaryAmount", "value": 0, "currency": "USD"},\n'
                   '            "deliveryTime": {\n'
                   '              "@type": "ShippingDeliveryTime",\n'
                   '              "transitTime": {"@type": "QuantitativeValue", "minValue": 25, "maxValue": 35, "unitCode": "DAY"}\n'
                   '            }\n'
                   '          }\n'
                   '        }\n'
                   '      }\n    }' % (
            i, json.dumps(p['name_en']), BASE, p['img'], json.dumps(_desc(p)),
            json.dumps(CAT_EN[p['cat']]), pr['landed'], p['moq']))
    return ('{\n'
            '  "@context": "https://schema.org",\n'
            '  "@type": "ItemList",\n'
            '  "name": "SourceToGulf Hot Picks — China to Gulf landed prices",\n'
            '  "url": "' + BASE + '/products.html",\n'
            '  "numberOfItems": ' + str(len(prods)) + ',\n'
            '  "itemListElement": [\n' + ',\n'.join(els) + '\n  ]\n}')


# 轻量筛选：仅按 data-cat 显隐已渲染的卡片，不依赖任何外部数据源
FILTER_JS = '''
<script>
(function(){
  var chips = document.querySelectorAll('#chips button');
  if(!chips.length) return;
  chips.forEach(function(b){
    b.addEventListener('click', function(){
      var cat = b.getAttribute('data-cat');
      chips.forEach(function(x){ x.classList.remove('on'); });
      b.classList.add('on');
      document.querySelectorAll('#pgrid .pcard').forEach(function(c){
        c.style.display = (cat==='all' || c.getAttribute('data-cat')===cat) ? '' : 'none';
      });
    });
  });
})();
</script>
'''


def dedupe_ga4(html):
    """旧源页已自带 GA4，page_shell 会再注入一份，这里去重为仅一份。"""
    pat = re.compile(
        r'<!-- Google tag \(gtag\.js\) GA4 -->\s*'
        r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=[^>]*></script>\s*'
        r'<script>\s*window\.dataLayer[\s\S]*?</script>\s*', re.S)
    if len(pat.findall(html)) > 1:
        html = pat.sub('', html)
        html = html.replace('</head>', GA4_SNIPPET + '\n</head>', 1)
    return html


def main():
    body = (
        '''<section class="page-hero"><div class="wrap">
<div class="crumb"><a href="/">Home</a> ← <span>Hot Picks</span></div>
<h1>This Month's Hot Picks — Landed Prices Included</h1>
<p class="sub">A short, curated list of what Gulf sellers are actually re-ordering. Every price already includes freight to the UAE — no quoting ping-pong, just order.</p>
</div></section>

<section style="padding-top:0"><div class="wrap">
<div class="img-row" style="grid-template-columns:repeat(2,1fr);margin-bottom:24px;">
<figure style="margin:0;">
<img src="/images/earrings-display.jpg" alt="Fashion earrings sample from Yiwu market" loading="lazy" style="width:100%;border-radius:14px;border:1px solid #E7E1D4;object-fit:cover;aspect-ratio:4/3;">
<figcaption style="font-size:13px;color:var(--muted);margin-top:8px;text-align:center;">Fashion jewelry samples from Yiwu market</figcaption>
</figure>
<figure style="margin:0;">
<img src="/images/gold-rings-bowl.jpg" alt="Gold-plated rings sample from Guangzhou market" loading="lazy" style="width:100%;border-radius:14px;border:1px solid #E7E1D4;object-fit:cover;aspect-ratio:4/3;">
<figcaption style="font-size:13px;color:var(--muted);margin-top:8px;text-align:center;">Gold-plated rings sample from Guangzhou market</figcaption>
</figure>
</div>
'''
        + build_lines() + '\n'
        + build_capacity() + '\n'
        + build_longtail() + '\n'
        + '''<section style="padding-top:0"><div class="wrap">
<h2 style="margin-bottom:4px">Ready-to-order picks</h2>
<p class="sub" style="margin-bottom:16px">Already-developed items with real MOQ and landed price — order as-is, or use them as a starting point for your own version.</p>
'''
        + build_chips() + '\n'
        + build_grid() + '\n'
        + '''<p class="updated-note" id="updated-note"><span>Updated ''' + UPDATED + ''' · new picks every month</span></p>
<div class="strip" style="margin-top:34px">
  <div><b>How we price</b><span>Factory price + Cainiao Middle East line freight at MOQ weight. Reference, not a binding quote — final price confirmed before deposit.</span></div>
  <div><b>Duties &amp; VAT</b><span>Not included — they depend on your country and declared value. Use our calculator for a full landed cost.</span></div>
  <div><b>QC on every order</b><span>Photo/video check before anything ships. You approve, then we send.</span></div>
</div>
'''
        + build_rel() + '\n'
        + FILTER_JS + '\n'
        + '''</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="final">
    <h2>30 million products in Yiwu. We listed the few that sell.</h2>
    <p>Can't find what you need? WhatsApp us a photo — we'll find it, quote the landed price, and QC it before it ships.</p>
    <a class="wa-btn" href="https://wa.me/971585854194" target="_blank" rel="noopener">💬 WhatsApp: +971 58 585 4194</a>
  </div>
</div></section>'''
    )
    html = page_shell(
        "China Products for Gulf Sellers: MOQ & FOB Price | SourceToGulf",
        "China products for Gulf sellers with real MOQ, factory (FOB) and all-in prices. Start from 10 pcs — custom branding, physical samples and QC before you commit.",
        BASE + '/products.html',
        body,
        json_ld=json_ld(),
        # 阿语版互链（/ar/products.html 由 build_arabic.py 生成）
        alt_ar=BASE + '/ar/products.html'
    )
    html = dedupe_ga4(html)
    with open(os.path.join(APP, 'products.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('✓ products.html (%d items · SSR · single source: products.clean.json)' % len(prods))


if __name__ == '__main__':
    main()
