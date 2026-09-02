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


def json_ld():
    els = []
    for i, p in enumerate(prods, 1):
        pr = price_of(p)
        els.append('    {\n      "@type": "ListItem",\n      "position": %d,\n      "item": {\n'
                   '        "@type": "Product",\n        "name": %s,\n        "image": "%s%s",\n'
                   '        "category": %s,\n        "offers": {\n          "@type": "Offer",\n'
                   '          "priceCurrency": "USD",\n          "price": %.2f,\n'
                   '          "availability": "https://schema.org/InStock",\n'
                   '          "minOrderQuantity": %d\n        }\n      }\n    }' % (
            i, json.dumps(p['name_en']), BASE, p['img'],
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
    <a class="wa-btn" href="https://wa.me/971585146139" target="_blank" rel="noopener">💬 WhatsApp: +971 58 514 6139</a>
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
