# -*- coding: utf-8 -*-
"""
ssr_products.py — Server-render the product grid into products.html

products.html renders its grid from /products-data.js via innerHTML. That is
invisible to GPTBot / PerplexityBot / OAI-SearchBot (they don't run JS), so the
site's core product content is a blank box to AI crawlers. This script injects a
static, server-rendered grid as the initial content of <div id="pgrid">. The
client JS overwrites it on load for real users, so behavior is unchanged, but
crawlers now see every product name, price and MOQ in raw HTML.

Run after any change to products.clean.json:
    python3 ssr_products.py
"""
import os, re, json
from urllib.parse import quote

APP = os.path.dirname(os.path.abspath(__file__))
CNY_TO_USD = 7.15

def cainiao_ship_usd(kg):
    cny = 68.0 if kg <= 0.5 else 68.0 + (kg - 0.5) * 45.6
    return cny / CNY_TO_USD

def price_of(p):
    fob = p['fob_cny'] / CNY_TO_USD
    ship_per_unit = cainiao_ship_usd(p['moq'] * p['weight_kg']) / p['moq']
    return fob, fob + ship_per_unit

def card_html(p):
    fob, landed = price_of(p)
    hot = '<span class="hot-badge">HOT</span>' if p.get('hot') else ''
    wa_text = ('Hi SourceToGulf! I am interested in: ' + p['name_en'] +
               ' (MOQ ' + str(p['moq']) + ' pcs). Please confirm price and availability.')
    wa = quote(wa_text)
    return ('<div class="pcard in">'
        + hot
        + '<div class="imgbox"><img src="' + p['img'] + '" alt="' + p['name_en'] + '" loading="lazy" onerror="this.parentElement.classList.add(\'bad\')"></div>'
        + '<div class="pbody">'
        + '<h3 data-en="' + p['name_en'] + '" data-ar="' + p['name_ar'] + '">' + p['name_en'] + '</h3>'
        + '<div class="price-row">'
        + '<div class="planded"><small data-en="Landed to UAE" data-ar="سعر التسليم للإمارات">Landed to UAE</small><b>$' + ('%.2f' % landed) + '</b> <i data-en="/pc at MOQ" data-ar="/قطعة بأقل كمية">/pc at MOQ</i></div>'
        + '<div class="pfob"><small data-en="Factory price" data-ar="سعر المصنع">Factory price</small><span>$' + ('%.2f' % fob) + '</span></div>'
        + '</div>'
        + '<div class="pmeta"><span data-en="MOQ" data-ar="أقل كمية">MOQ</span> ' + str(p['moq']) + ' pcs &middot; <span data-en="ships in" data-ar="يشحن خلال">ships in</span> ' + str(p['lead_days']) + ' <span data-en="days" data-ar="أيام">days</span></div>'
        + '<a class="wa-mini" href="https://wa.me/971585854194?text=' + wa + '" target="_blank" rel="noopener" data-en="💬 Ask about this" data-ar="💬 اسأل عن هذا المنتج">💬 Ask about this</a>'
        + '</div></div>')

def main():
    data = json.load(open(os.path.join(APP, 'products.clean.json'), encoding='utf-8'))
    prods = data['prods']
    grid = ''.join(card_html(p) for p in prods)
    html_path = os.path.join(APP, 'products.html')
    html = open(html_path, encoding='utf-8').read()
    # Replace the empty pgrid with the server-rendered grid (keep the id/class).
    new_html, n = re.subn(
        r'<div class="pgrid" id="pgrid">\s*</div>',
        '<div class="pgrid" id="pgrid">' + grid + '</div>',
        html, count=1)
    if n == 0:
        raise SystemExit("Could not find empty <div id=pgrid>. Already SSR'd or markup changed.")
    open(html_path, 'w', encoding='utf-8').write(new_html)
    print("Injected %d static product cards into products.html (SSR fallback)." % len(prods))

if __name__ == '__main__':
    main()
