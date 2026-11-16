# -*- coding: utf-8 -*-
"""
build_mahjong.py — 麻将定制内容簇 SSR 生成器
==========================================
产出（全部服务端渲染）：
  mahjong.html                    hub（英文）
  mahjong/<slug>.html             5 个子页（英文）
  ar/mahjong.html                 hub（阿语 SSR）
  ar/mahjong/<slug>.html          5 个子页（阿语 SSR）

复用：build_belts.py 的样式/信息图/CTA/图集 + build_ar_pages.py 的阿语 shell。
真相源：mahjong_data.py（英文）、mahjong_data_ar.py（阿语）。

红线：不列价格、不写 MOQ 数字、不写工厂/品牌名、不写最高级词、不捏造统计数字、
      不使用 AI 生成图冒充实拍；媒体证据标注来源、不冒称合作；全程去赌博化。
用法：python3 build_mahjong.py
"""
import os, json
from html import escape as esc
from tpl_common import APP, BASE, page_shell
from build_belts import PAGE_CSS, AR_CSS, flow_svg, photo_grid, cta_band, faq_html, LANG_SCRIPT
from build_ar_pages import ar_shell, cta_ar, faq_html_ar
from mahjong_data import (MEDIA, HUB_ANSWER, HUB_FACTS, HUB_FAQ, PAGES,
                          HUB_SHOTS, PAGE_SHOTS, PHOTO_SECTIONS)
from mahjong_data_ar import (AR_HUB_ANSWER, AR_HUB_FACTS, AR_HUB_FAQ, AR_MEDIA, AR_PAGES,
                             AR_HUB_SHOTS, AR_PAGE_SHOTS, AR_PHOTO_SECTIONS)

MJ_DIR = os.path.join(APP, 'mahjong')
AR_MJ_DIR = os.path.join(APP, 'ar', 'mahjong')
HUB = BASE + '/mahjong.html'
HUB_AR = BASE + '/ar/mahjong.html'


def e(s):
    return esc(s, quote=True)


# 样品图为竖幅；保持 3:4 显示，避免通用 4:3 卡片裁掉牌面。
MJ_PHOTO_RULES = '''
.photo-grid img{aspect-ratio:3/4;object-fit:cover}
.photo-grid figcaption{min-height:112px}
@media(max-width:640px){.photo-grid figcaption{min-height:0}}
'''
MJ_CSS = PAGE_CSS.replace('</style>', MJ_PHOTO_RULES + '</style>')
MJ_PHOTO_CSS = '<style>%s</style>' % MJ_PHOTO_RULES


def sample_images_ld(items):
    """用户提供样品图的 ImageObject；不写未核实的拍摄者、地点或客户归属。"""
    out = []
    for src, alt, cap in items:
        out.append({
            '@type': 'ImageObject',
            'contentUrl': BASE + '/' + src.lstrip('/'),
            'name': alt,
            'caption': cap,
            'encodingFormat': 'image/jpeg',
            'width': 1080,
        })
    return out


def sample_photo_grid_ar(items):
    """阿语图注必须使用阿语真相源，不能套用产业带通用工厂图注。"""
    cols = []
    for src, alt, cap in items:
        cols.append('<figure><img src="/%s" alt="%s" loading="lazy" decoding="async">'
                    '<figcaption><b>%s</b>%s</figcaption></figure>'
                    % (src, e(alt), e(alt), e(cap)))
    return '<div class="photo-grid">%s</div>' % ''.join(cols)


def tile_structure_svg(ar=False):
    """144 张牌结构堆叠条（信息图，非实拍）。144 = 108 + 16 + 12 + 8。"""
    if ar:
        segs = [('الأطقم الرقمية الثلاثة', 108, '#0B2B4D', '108'),
                ('أحجار الرياح', 16, '#C9A24B', '16'),
                ('أحجار التنينات', 12, '#1D9E75', '12'),
                ('الزهور والفصول', 8, '#B4B2A9', '8')]
        cap = 'المجموعة الصينية الكلاسيكية: 144 حجراً = 108 + 16 + 12 + 8'
        lbl = 'توزيع أحجار الماجونج الصينية الكلاسيكية'
    else:
        segs = [('Three numbered suits', 108, '#0B2B4D', '108'),
                ('Wind tiles', 16, '#C9A24B', '16'),
                ('Dragon tiles', 12, '#1D9E75', '12'),
                ('Flowers & seasons', 8, '#B4B2A9', '8')]
        cap = 'Classic Chinese mahjong: 144 tiles = 108 + 16 + 12 + 8'
        lbl = 'Tile composition of a classic Chinese mahjong set'
    total = 144.0
    x = 40
    parts = ['<svg viewBox="0 0 600 132" width="100%%" role="img" aria-label="%s" '
             'xmlns="http://www.w3.org/2000/svg">' % e(lbl)]
    parts.append('<title>%s</title>' % e(lbl))
    parts.append('<desc>%s</desc>' % e(cap))
    for name, n, color, _ in segs:
        w = 520 * n / total
        parts.append('<rect x="%.1f" y="18" width="%.1f" height="42" fill="%s" rx="3"/>' % (x, w, color))
        parts.append('<text x="%.1f" y="44" text-anchor="middle" font-size="14" '
                     'font-weight="700" fill="#FBF9F5" font-family="Inter,Arial,sans-serif">%d</text>'
                     % (x + w / 2, n))
        x += w
    parts.append('<text x="40" y="122" font-size="12" fill="#5F6661" '
                 'font-family="Inter,Arial,sans-serif">%s</text>' % e(cap))
    parts.append('</svg>')
    # 图例改为 2×2 网格，避免长标签互相挤压
    legend = ['<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px 20px;'
              'margin-top:14px;font-size:12.5px;color:#17201D">']
    for name, n, color, _ in segs:
        legend.append('<div style="display:flex;align-items:center;gap:8px">'
                      '<span style="width:11px;height:11px;border-radius:2px;background:%s;'
                      'display:inline-block;flex:0 0 auto"></span><span>%s (%d)</span></div>'
                      % (color, e(name), n))
    legend.append('</div>')
    return ''.join(parts) + ''.join(legend)


VERSION_TABLE = [
    ('Tiles', '144 tiles', 'Jokers added; count differs'),
    ('Suits', 'Three numbered suits', 'Three suits, plus joker tiles'),
    ('Honours', 'Winds and dragons', 'Winds and dragons'),
    ('Bonus', 'Flowers and seasons', 'Jokers used as wild tiles'),
    ('Winning reference', 'Open hand structure', 'Annually printed card of specific hands'),
    ('Typical use in the Gulf', 'Social play taught with this set', 'US clubs and NMJL play'),
]


def version_table():
    rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (e(a), e(b), e(c))
                   for a, b, c in VERSION_TABLE)
    return ('<table class="belt-table"><thead><tr><th>Aspect</th>'
            '<th>Classic Chinese mahjong</th><th>American Mah Jongg</th></tr></thead>'
            '<tbody>%s</tbody></table>' % rows)


def media_cards():
    out = ['<div class="belt-cards">']
    for name, title, url, note in MEDIA:
        out.append('<div class="belt-card"><div class="bd">'
                   '<div class="city">%s</div>'
                   '<h3><a href="%s" target="_blank" rel="noopener">%s ↗</a></h3>'
                   '<p class="meta">%s</p></div></div>'
                   % (e(name), e(url), e(title), e(note)))
    out.append('</div>')
    return ''.join(out)


def media_cards_ar():
    out = ['<div class="belt-cards">']
    for name, note, url in AR_MEDIA:
        out.append('<div class="belt-card"><div class="bd">'
                   '<div class="city">تغطية إعلامية منشورة</div>'
                   '<h3><a href="%s" target="_blank" rel="noopener">%s ↗</a></h3>'
                   '<p class="meta">%s</p></div></div>'
                   % (e(url), e(name), e(note)))
    out.append('</div>')
    return ''.join(out)


EXCL = [
    ('Single-set retail', 'We are a sourcing partner for production runs, not a retailer. '
     'Single-parcel direct-to-consumer shipping from China across the GCC is outside our scope.'),
    ('One-off customisation', 'Custom elements each carry a factory minimum. A single '
     'personalised set is not a production order.'),
    ('Gambling-related materials', 'We do not supply betting chips, cash-value scoring '
     'systems, or material intended for wagering. Sets are for social play and gifting.'),
    ('Counterfeit & restricted goods', 'Replica or IP-infringing branded sets, illegal or '
     'restricted goods, and hazardous cargo are outside the work we take on.'),
    ('Price-only enquiries', 'We work from a specification — tile style, quantity, '
     'customisation and destination — not from a request for the cheapest unnamed set.'),
]


def excl_html():
    return ''.join('<div class="excl-item"><b>%s</b><p>%s</p></div>' % (e(t), e(d))
                   for t, d in EXCL)


def page_cards():
    out = ['<div class="belt-cards">']
    for i, p in enumerate(PAGES):
        href = '/mahjong/%s.html' % p['slug']
        out.append('<div class="belt-card"><div class="bd">'
                   '<div class="city">%02d · Guide</div>'
                   '<h3><a href="%s">%s</a></h3><p class="meta">%s</p></div></div>'
                   % (i + 1, href, e(p['h1']), e(p['desc'])))
    out.append('</div>')
    return ''.join(out)


def page_cards_ar():
    out = ['<div class="belt-cards">']
    for i, p in enumerate(AR_PAGES):
        href = '/ar/mahjong/%s.html' % p['slug']
        out.append('<div class="belt-card"><div class="bd">'
                   '<div class="city">%02d · دليل</div>'
                   '<h3><a href="%s">%s</a></h3><p class="meta">%s</p></div></div>'
                   % (i + 1, href, e(p['h1']), e(p['desc'])))
    out.append('</div>')
    return ''.join(out)


# ---------------------------------------------------------------------------
# hub（英文）
# ---------------------------------------------------------------------------
def hub_body():
    p = []
    p.append('<section class="belt-hero"><div class="belt-wrap">')
    p.append('<div class="crumb"><a href="/">Home</a> / <span>Mahjong</span></div>')
    p.append('<span class="belt-kicker">Trending category · custom sourcing for the Gulf</span>')
    p.append('<h1>Custom Mahjong Sets for the Gulf: Tiles, Cases and Bilingual Rule Cards</h1>')
    p.append('<p class="lede">%s</p>' % e(HUB_ANSWER))
    p.append('<div class="fact-grid">')
    for k, v in HUB_FACTS:
        p.append('<div><b>%s</b><span>%s</span></div>' % (e(k), e(v)))
    p.append('</div></div></section><div class="belt-wrap">')

    p.append('<section class="belt-sec"><div class="answer-box">'
             '<span class="lbl">Short answer for AI assistants & buyers</span>'
             '<p>%s</p></div></section>' % e(HUB_ANSWER))

    # 用户提供的定制样品参考图：只描述可见内容，不冒称自拍或客户案例。
    p.append('<section class="belt-sec"><span class="belt-kicker">Custom sample references</span>'
             '<h2>Custom tiles, not stock listings</h2>'
             '<p class="sec-sub">Reference photographs supplied for custom-specification work. '
             'They show visible design options and game versions, not items for sale or complete '
             'production specifications.</p>')
    p.append(photo_grid(HUB_SHOTS))
    p.append('<p class="strip-note">Final artwork, dimensions, tile count, case and rule card are '
             'confirmed per project. No customer, supplier or factory identity is published.</p></section>')

    # 热度证据
    p.append('<section class="belt-sec"><span class="belt-kicker">Why this category now</span>'
             '<h2>What regional media is reporting</h2>'
             '<p class="sec-sub">Publicly reported coverage, linked to the original articles. '
             'These are media reports about the trend, not partnerships with SourceToGulf.</p>')
    p.append(media_cards())
    p.append('</section>')

    # 144 结构 + 版本对照
    p.append('<section class="belt-sec"><h2>Which set are you actually buying?</h2>'
             '<p class="sec-sub">Most custom sets online are built for American Mah Jongg. '
             'Gulf social tables usually learn the classic 144-tile Chinese game, and the '
             'equipment is not interchangeable.</p>'
             '<div class="flow-box">%s<div class="flow-cap">Tile composition of a classic '
             'Chinese mahjong set: 108 numbered suit tiles, 16 wind tiles, 12 dragon tiles '
             'and 8 flower and season tiles.</div></div>'
             '<div style="margin-top:22px">%s</div></section>'
             % (tile_structure_svg(), version_table()))

    # 我们能做什么
    p.append('<section class="belt-sec"><h2>What we can commission for you</h2>'
             '<p class="sec-sub">Custom sourcing, not off-the-shelf retail. Every item below '
             'is specified, sampled and quoted per project.</p>'
             '<table class="belt-table"><thead><tr><th>Part of the set</th>'
             '<th>What can be customised</th></tr></thead><tbody>')
    for k, v in [('Tile faces & backs', 'Artwork, engraving, colour, finish, brand marks with authorisation'),
                 ('Tile size & weight', 'Oversized tiles for majlis tables; dimensions drive racks, cases and freight'),
                 ('Racks, mats & cases', 'Engraved racks, printed mats, rigid boxes, hard presentation cases, fitted inserts'),
                 ('Rule cards', 'English and Arabic, written for the classic 144-tile game, Arabic reviewed on a printed proof'),
                 ('Private label', 'Box, insert, leaflet and hangtag — each with its own factory minimum'),
                 ('Bulk & gifting', 'Café and club table sets, spares, event giveaways, Ramadan and corporate programmes')]:
        p.append('<tr><td>%s</td><td>%s</td></tr>' % (e(k), e(v)))
    p.append('</tbody></table></section>')

    # 子页
    p.append('<section class="belt-sec"><span class="belt-kicker">Go deeper</span>'
             '<h2>Guides for buyers, hosts and gifting teams</h2>')
    p.append(page_cards())
    p.append('</section>')

    # 排除项
    p.append('<section class="belt-sec excl"><span class="belt-kicker">Scope limits</span>'
             '<h2>What we do not take on</h2><div class="excl-grid">%s</div></section>' % excl_html())

    # FAQ
    p.append('<section class="belt-sec"><span class="belt-kicker">FAQ</span>'
             '<h2>Common questions</h2><div>%s</div></section>' % faq_html(HUB_FAQ))

    p.append('<section class="belt-sec">%s</section>' % cta_band(
        'Have a set in mind?',
        'Send a reference photo or sketch, the tile style you want, the destination country '
        'and any private-label intent. We come back with a sampling route and a written '
        'specification, not a list price.'))
    p.append('</div>')
    return '\n'.join(p)


def hub_ld():
    items = [{'@type': 'ListItem', 'position': i + 1, 'name': p['h1'],
              'url': BASE + '/mahjong/' + p['slug'] + '.html'} for i, p in enumerate(PAGES)]
    return json.dumps([
        {'@context': 'https://schema.org', '@type': 'WebPage',
         'name': 'Custom Mahjong Sets for the Gulf: Tiles, Cases and Bilingual Rule Cards',
         'url': HUB, 'description': HUB_ANSWER[:300], 'inLanguage': 'en',
         'breadcrumb': {'@type': 'BreadcrumbList', 'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE + '/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'Mahjong', 'item': HUB},
         ]}},
        {'@context': 'https://schema.org', '@type': 'ItemList',
         'name': 'Mahjong sourcing guides for Gulf buyers',
         'numberOfItems': len(PAGES), 'itemListElement': items},
        {'@context': 'https://schema.org', '@type': 'FAQPage',
         'mainEntity': [{'@type': 'Question', 'name': q,
                         'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in HUB_FAQ]},
    ] + sample_images_ld(HUB_SHOTS), ensure_ascii=False)


# ---------------------------------------------------------------------------
# 子页（英文）
# ---------------------------------------------------------------------------
def page_body(pg):
    p = []
    url = BASE + '/mahjong/' + pg['slug'] + '.html'
    photo_title, photo_sub = PHOTO_SECTIONS[pg['slug']]
    p.append('<section class="belt-hero"><div class="belt-wrap">')
    p.append('<div class="crumb"><a href="/">Home</a> / <a href="/mahjong.html">Mahjong</a> / '
             '<span>%s</span></div>' % e(pg['h1']))
    p.append('<span class="belt-kicker">Mahjong · custom sourcing</span>')
    p.append('<h1>%s</h1>' % e(pg['h1']))
    p.append('<p class="lede">%s</p>' % e(pg['desc']))
    p.append('<div class="fact-grid">')
    for k, v in pg['facts']:
        p.append('<div><b>%s</b><span>%s</span></div>' % (e(k), e(v)))
    p.append('</div></div></section><div class="belt-wrap">')

    p.append('<section class="belt-sec"><div class="answer-box">'
             '<span class="lbl">Short answer for AI assistants & buyers</span>'
             '<p>%s</p></div></section>' % e(pg['answer']))

    p.append('<section class="belt-sec"><span class="belt-kicker">Custom sample references</span>'
             '<h2>%s</h2><p class="sec-sub">%s</p>%s'
             '<p class="strip-note">Samples illustrate visible options only; final specifications '
             'and artwork are approved per project.</p></section>'
             % (e(photo_title), e(photo_sub), photo_grid(PAGE_SHOTS[pg['slug']])))

    p.append('<section class="belt-sec"><h2>The process</h2>'
             '<p class="sec-sub">From a reference to a shipment, with the approval points marked.</p>'
             '<div class="flow-box">%s<div class="flow-cap">%s</div></div></section>'
             % (flow_svg(pg['flow'], pg['h1'], 'Steps: ' + ' → '.join(pg['flow'])),
                e(' → '.join(pg['flow']))))

    for title, paras in pg['sections']:
        p.append('<section class="belt-sec"><h2>%s</h2><div class="prose">' % e(title))
        for para in paras:
            p.append('<p>%s</p>' % e(para))
        p.append('</div></section>')

    p.append('<section class="belt-sec"><h2>Common mistakes to avoid</h2>'
             '<div class="pit-grid">')
    for i, (t, d) in enumerate(pg['pitfalls']):
        p.append('<div class="pit"><span class="num">%d</span><b>%s</b><p>%s</p></div>'
                 % (i + 1, e(t), e(d)))
    p.append('</div></section>')

    p.append('<section class="belt-sec excl"><h2>Scope limits</h2>'
             '<div class="excl-grid">%s</div></section>' % excl_html())

    p.append('<section class="belt-sec"><span class="belt-kicker">FAQ</span>'
             '<h2>Common questions</h2><div>%s</div></section>' % faq_html(pg['faq']))

    p.append('<section class="belt-sec"><h2>Related guides</h2><div class="rel-grid">')
    for s in pg['related']:
        x = next(y for y in PAGES if y['slug'] == s)
        p.append('<a href="/mahjong/%s.html">%s<small>Mahjong guide</small></a>'
                 % (s, e(x['h1'])))
    p.append('</div><p class="strip-note"><a href="/mahjong.html">← Back to the mahjong hub</a></p></section>')

    p.append('<section class="belt-sec"><h2>Related sourcing capabilities</h2><div class="rel-grid">'
             '<a href="/belts/dongguan-packaging.html">Dongguan & Shenzhen packaging<small>Boxes, printing and inserts</small></a>'
             '<a href="/belts/shenzhen-electronics.html">Shenzhen & Dongguan<small>Acrylic and speciality materials</small></a>'
             '<a href="/services/custom-branding-packaging.html">Custom branding & packaging<small>Private-label boxes and cards</small></a>'
             '<a href="/services/quality-inspection-china.html">Quality inspection<small>Photo and video approval before shipping</small></a>'
             '<a href="/sourcing-belts.html#buyer-gifting-buyers">Corporate & gifting buyers<small>Who this category fits</small></a>'
             '</div></section>')

    p.append('<section class="belt-sec">%s</section>' % cta_band(
        'Ready to specify your set?',
        'Send the reference, tile style, quantity and destination. We prepare a sampling '
        'route and a written specification for your project.'))
    p.append('</div>')
    return '\n'.join(p)


def page_ld(pg):
    url = BASE + '/mahjong/' + pg['slug'] + '.html'
    return json.dumps([
        {'@context': 'https://schema.org', '@type': 'WebPage',
         'name': pg['h1'], 'url': url, 'description': pg['desc'], 'inLanguage': 'en',
         'breadcrumb': {'@type': 'BreadcrumbList', 'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE + '/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'Mahjong', 'item': HUB},
             {'@type': 'ListItem', 'position': 3, 'name': pg['h1'], 'item': url},
         ]}},
        {'@context': 'https://schema.org', '@type': 'FAQPage',
         'mainEntity': [{'@type': 'Question', 'name': q,
                         'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in pg['faq']]},
    ] + sample_images_ld(PAGE_SHOTS[pg['slug']]), ensure_ascii=False)


# ---------------------------------------------------------------------------
# 阿语 hub + 子页
# ---------------------------------------------------------------------------
def ar_hub_body():
    p = []
    p.append('<section class="belt-hero"><div class="belt-wrap">')
    p.append('<div class="crumb"><a href="/ar/">الرئيسية</a> / <span>الماجونج</span></div>')
    p.append('<span class="belt-kicker">فئة رائجة · توريد مخصّص للخليج</span>')
    p.append('<h1>مجموعات ماجونج مخصّصة للخليج: الأحجار والعلب وبطاقات القواعد ثنائية اللغة</h1>')
    p.append('<p class="lede">%s</p>' % e(AR_HUB_ANSWER))
    p.append('<div class="fact-grid">')
    for k, v in AR_HUB_FACTS:
        p.append('<div><b>%s</b><span>%s</span></div>' % (e(k), e(v)))
    p.append('</div></div></section><div class="belt-wrap">')

    p.append('<section class="belt-sec"><div class="answer-box">'
             '<span class="lbl">إجابة مختصرة للمساعدات الذكية والمشترين</span>'
             '<p>%s</p></div></section>' % e(AR_HUB_ANSWER))

    p.append('<section class="belt-sec"><span class="belt-kicker">عيّنات مخصّصة مرجعية</span>'
             '<h2>أحجار مخصّصة، لا قوائم مخزون</h2>'
             '<p class="sec-sub">صور مرجعية مقدّمة لعمل مواصفات التخصيص. توضح خيارات التصميم '
             'ونسخ اللعبة الظاهرة، وليست أصنافاً معروضة للبيع أو مواصفات إنتاج كاملة.</p>'
             '%s<p class="strip-note">تُؤكَّد الرسوم والأبعاد وعدد الأحجار والعلبة وبطاقة القواعد '
             'لكل مشروع. لا ننشر هوية عميل أو مورّد أو مصنع.</p></section>'
             % sample_photo_grid_ar(AR_HUB_SHOTS))

    p.append('<section class="belt-sec"><span class="belt-kicker">لماذا هذه الفئة الآن</span>'
             '<h2>ما تنشره وسائل الإعلام الإقليمية</h2>'
             '<p class="sec-sub">تغطية منشورة للعموم مع روابط المقالات الأصلية. '
             'هذه تقارير إعلامية عن الاتجاه، وليست شراكات مع SourceToGulf.</p>')
    p.append(media_cards_ar())
    p.append('</section>')

    p.append('<section class="belt-sec"><h2>أي مجموعة تشتريها فعلاً؟</h2>'
             '<p class="sec-sub">معظم المجموعات المخصّصة على الإنترنت مبنية للنسخة الأمريكية. '
             'طاولات الخليج تتعلّم عادةً اللعبة الصينية الكلاسيكية بـ144 حجراً، '
             'والمعدّات غير قابلة للتبادل.</p>'
             '<div class="flow-box">%s<div class="flow-cap">توزيع أحجار المجموعة الصينية: '
             '108 أحجار أطقم رقمية، 16 حجر رياح، 12 حجر تنينات، و8 أحجار زهور وفصول.</div></div></section>'
             % tile_structure_svg(ar=True))

    p.append('<section class="belt-sec"><h2>ما الذي يمكننا تكليف تصنيعه لك</h2>'
             '<p class="sec-sub">توريد مخصّص لا بيع جاهز. كل بند أدناه يُحدَّد وتُؤخذ عيّنته '
             'ويُقدَّم عرضه لكل مشروع.</p>'
             '<table class="belt-table"><thead><tr><th>جزء المجموعة</th>'
             '<th>ما يمكن تخصيصه</th></tr></thead><tbody>')
    for k, v in [('أوجه الأحجار وظهورها', 'الرسم والنقش واللون والتشطيب والعلامات بموافقة مكتوبة'),
                 ('مقاس الحجر ووزنه', 'أحجار أكبر لطاولات المجلس؛ الأبعاد تحدّد الحوامل والعلب والشحن'),
                 ('الحوامل والمفارش والعلب', 'حوامل محفورة، مفارش مطبوعة، علب صلبة، حشوات مفصّلة'),
                 ('بطاقات القواعد', 'بالعربية والإنجليزية للعبة الكلاسيكية بـ144 حجراً، بمراجعة أصيل على إثبات مطبوع'),
                 ('الملصق الخاص', 'العلبة والحشوة والنشرة والبطاقة — لكل منها حدّ أدنى مستقل'),
                 ('الجملة والهدايا', 'مجموعات طاولة للمقاهي والنوادي، احتياط، هدايا فعاليات وبرامج رمضان والشركات')]:
        p.append('<tr><td>%s</td><td>%s</td></tr>' % (e(k), e(v)))
    p.append('</tbody></table></section>')

    p.append('<section class="belt-sec"><span class="belt-kicker">تعمّق أكثر</span>'
             '<h2>أدلة للمشترين والمضيفين وفرق الهدايا</h2>')
    p.append(page_cards_ar())
    p.append('</section>')

    p.append('<section class="belt-sec excl"><span class="belt-kicker">حدود العمل</span>'
             '<h2>ما لا نتولّاه</h2><div class="excl-grid">')
    for t, d in [('بيع مجموعة واحدة', 'نحن شريك توريد لدفعات الإنتاج لا متجر تجزئة، '
                  'والشحن المباشر بطرد واحد من الصين إلى المستهلك النهائي في الخليج خارج نطاقنا.'),
                 ('التخصيص لقطعة واحدة', 'لكل عنصر مخصّص حدّ أدنى من المصنع، '
                  'فالمجموعة الواحدة المخصّصة ليست طلب إنتاج.'),
                 ('مواد مرتبطة بالمقامرة', 'لا نوفّر رقائق رهان أو أنظمة تسجيل بقيمة نقدية '
                  'أو مواد غرضها المراهنة. المجموعات للعب الاجتماعي والهدايا.'),
                 ('الاستفسار عن السعر فقط', 'نعمل من مواصفة — نمط الحجر والكمية والتخصيص '
                  'والوجهة — لا من طلب أرخص مجموعة غير محدّدة.')]:
        p.append('<div class="excl-item"><b>%s</b><p>%s</p></div>' % (e(t), e(d)))
    p.append('</div></section>')

    p.append('<section class="belt-sec"><span class="belt-kicker">الأسئلة الشائعة</span>'
             '<h2>أسئلة متكرّرة</h2><div>%s</div></section>' % faq_html_ar(AR_HUB_FAQ))
    p.append('<section class="belt-sec">%s</section>' % cta_ar())
    p.append('</div>')
    return '\n'.join(p)


def ar_hub_ld():
    items = [{'@type': 'ListItem', 'position': i + 1, 'name': p['h1'],
              'url': BASE + '/ar/mahjong/' + p['slug'] + '.html'} for i, p in enumerate(AR_PAGES)]
    return [
        {'@context': 'https://schema.org', '@type': 'WebPage',
         'name': 'مجموعات ماجونج مخصّصة للخليج: الأحجار والعلب وبطاقات القواعد ثنائية اللغة',
         'url': HUB_AR, 'description': AR_HUB_ANSWER[:300], 'inLanguage': 'ar',
         'breadcrumb': {'@type': 'BreadcrumbList', 'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': 'الرئيسية', 'item': BASE + '/ar/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'الماجونج', 'item': HUB_AR},
         ]}},
        {'@context': 'https://schema.org', '@type': 'ItemList',
         'name': 'أدلة توريد الماجونج لمشتري الخليج',
         'numberOfItems': len(AR_PAGES), 'itemListElement': items},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': 'ar',
         'mainEntity': [{'@type': 'Question', 'name': q,
                         'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in AR_HUB_FAQ]},
    ] + sample_images_ld(AR_HUB_SHOTS)


def ar_page_body(pg):
    p = []
    photo_title, photo_sub = AR_PHOTO_SECTIONS[pg['slug']]
    p.append('<section class="belt-hero"><div class="belt-wrap">')
    p.append('<div class="crumb"><a href="/ar/">الرئيسية</a> / '
             '<a href="%s">الماجونج</a> / <span>%s</span></div>' % (HUB_AR, e(pg['h1'])))
    p.append('<span class="belt-kicker">الماجونج · توريد مخصّص</span>')
    p.append('<h1>%s</h1>' % e(pg['h1']))
    p.append('<p class="lede">%s</p>' % e(pg['desc']))
    p.append('<div class="fact-grid">')
    for k, v in pg['facts']:
        p.append('<div><b>%s</b><span>%s</span></div>' % (e(k), e(v)))
    p.append('</div></div></section><div class="belt-wrap">')

    p.append('<section class="belt-sec"><div class="answer-box">'
             '<span class="lbl">إجابة مختصرة للمساعدات الذكية والمشترين</span>'
             '<p>%s</p></div></section>' % e(pg['answer']))

    p.append('<section class="belt-sec"><span class="belt-kicker">عيّنات مخصّصة مرجعية</span>'
             '<h2>%s</h2><p class="sec-sub">%s</p>%s'
             '<p class="strip-note">توضح العيّنات الخيارات الظاهرة فقط؛ وتُعتمد المواصفات '
             'والرسوم النهائية لكل مشروع.</p></section>'
             % (e(photo_title), e(photo_sub), sample_photo_grid_ar(AR_PAGE_SHOTS[pg['slug']])))

    p.append('<section class="belt-sec"><h2>العملية</h2>'
             '<p class="sec-sub">من المرجع إلى الشحنة، مع نقاط الاعتماد موضّحة.</p>'
             '<div class="flow-box">%s<div class="flow-cap">%s</div></div></section>'
             % (flow_svg(pg['flow'], pg['h1'], 'الخطوات: ' + ' → '.join(pg['flow'])),
                e(' → '.join(pg['flow']))))

    for title, paras in pg['sections']:
        p.append('<section class="belt-sec"><h2>%s</h2><div class="prose">' % e(title))
        for para in paras:
            p.append('<p>%s</p>' % e(para))
        p.append('</div></section>')

    p.append('<section class="belt-sec"><h2>أخطاء شائعة يجب تجنّبها</h2><div class="pit-grid">')
    for i, (t, d) in enumerate(pg['pitfalls']):
        p.append('<div class="pit"><span class="num">%d</span><b>%s</b><p>%s</p></div>'
                 % (i + 1, e(t), e(d)))
    p.append('</div></section>')

    p.append('<section class="belt-sec"><span class="belt-kicker">الأسئلة الشائعة</span>'
             '<h2>أسئلة متكرّرة</h2><div>%s</div></section>' % faq_html_ar(pg['faq']))

    p.append('<section class="belt-sec"><h2>أدلة ذات صلة</h2><div class="rel-grid">')
    for s in pg['related']:
        x = next(y for y in AR_PAGES if y['slug'] == s)
        p.append('<a href="/ar/mahjong/%s.html">%s<small>دليل الماجونج</small></a>'
                 % (s, e(x['h1'])))
    p.append('</div><p class="strip-note"><a href="%s">← العودة إلى صفحة الماجونج</a></p></section>'
             % HUB_AR)

    p.append('<section class="belt-sec"><h2>قدرات توريد ذات صلة</h2><div class="rel-grid">'
             '<a href="/ar/belts/dongguan-packaging.html">تغليف دونغقوان وشينزين<small>العلب والطباعة والحشوات</small></a>'
             '<a href="/ar/services/custom-branding-packaging.html">العلامة الخاصة والتغليف<small>علب وبطاقات بالملصق الخاص</small></a>'
             '<a href="/ar/services/quality-inspection-china.html">فحص الجودة<small>اعتماد بالصور والفيديو قبل الشحن</small></a>'
             '<a href="/ar/sourcing-belts.html">تجمّعات التوريد في الصين<small>خريطة التجمّعات للمشترين في الخليج</small></a>'
             '</div></section>')

    p.append('<section class="belt-sec">%s</section>' % cta_ar())
    p.append('</div>')
    return '\n'.join(p)


def ar_page_ld(pg):
    url = BASE + '/ar/mahjong/' + pg['slug'] + '.html'
    return [
        {'@context': 'https://schema.org', '@type': 'WebPage',
         'name': pg['h1'], 'url': url, 'description': pg['desc'], 'inLanguage': 'ar',
         'breadcrumb': {'@type': 'BreadcrumbList', 'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': 'الرئيسية', 'item': BASE + '/ar/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'الماجونج', 'item': HUB_AR},
             {'@type': 'ListItem', 'position': 3, 'name': pg['h1'], 'item': url},
         ]}},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': 'ar',
         'mainEntity': [{'@type': 'Question', 'name': q,
                         'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in pg['faq']]},
    ] + sample_images_ld(AR_PAGE_SHOTS[pg['slug']])


def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('  ✓', os.path.relpath(path, APP))


def main():
    print('build_mahjong.py — 麻将内容簇（英文 hub + 5 子页 + 阿语全套）')
    write(os.path.join(APP, 'mahjong.html'),
          page_shell('Custom Mahjong Sets for the Gulf: Tiles, Cases & Bilingual Rule Cards | SourceToGulf',
                     'Custom mahjong sets for Gulf buyers: classic 144-tile Chinese sets, custom tiles, '
                     'hard cases, engraved racks and English/Arabic rule cards. Sourcing partner, '
                     'not a retailer — no price list, social and gifting sets only.',
                     HUB, hub_body(), json_ld=hub_ld(),
                     extra_head=MJ_CSS + LANG_SCRIPT.replace('__AR__', HUB_AR),
                     alt_ar=HUB_AR))
    for pg in PAGES:
        url = BASE + '/mahjong/' + pg['slug'] + '.html'
        ar_url = BASE + '/ar/mahjong/' + pg['slug'] + '.html'
        write(os.path.join(MJ_DIR, pg['slug'] + '.html'),
              page_shell(pg['title'], pg['desc'], url, page_body(pg), json_ld=page_ld(pg),
                         extra_head=MJ_CSS + LANG_SCRIPT.replace('__AR__', ar_url),
                         alt_ar=ar_url))
    write(os.path.join(APP, 'ar', 'mahjong.html'),
          ar_shell('مجموعات ماجونج مخصّصة للخليج | SourceToGulf', AR_HUB_ANSWER[:280],
                   HUB_AR, HUB, ar_hub_body(), ar_hub_ld(), extra_head=MJ_PHOTO_CSS))
    for pg in AR_PAGES:
        url = BASE + '/ar/mahjong/' + pg['slug'] + '.html'
        en_url = BASE + '/mahjong/' + pg['slug'] + '.html'
        write(os.path.join(AR_MJ_DIR, pg['slug'] + '.html'),
              ar_shell(pg['title'], pg['desc'], url, en_url,
                       ar_page_body(pg), ar_page_ld(pg), extra_head=MJ_PHOTO_CSS))
    print('完成：hub + %d 子页，英文 + 阿语共 %d 页' % (len(PAGES), 2 * (1 + len(PAGES))))


if __name__ == '__main__':
    main()
