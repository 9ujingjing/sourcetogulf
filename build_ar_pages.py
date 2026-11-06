# -*- coding: utf-8 -*-
"""
build_ar_pages.py — 补齐产业带分页 / 服务页的阿语 SSR 版
========================================================
产出（全部服务端渲染，dir=rtl，inLanguage: ar，hreflang 双向）：
  ar/belts/<slug>.html      × 8   （对应 belts/<slug>.html）
  ar/services/<slug>.html   × 5   （对应 services/<slug>.html）

配套数据：belts_data_ar.py（阿语文案）+ belts_data.py（图片/英文页映射）
依赖：build_belts.py 的 PAGE_CSS / AR_CSS / icon_svg / flow_svg / LANG 机制

红线：
  - 阿语必须 SSR（不是 JS 切换），hreflang 双向、JSON-LD inLanguage: ar
  - 可见 FAQ 与 FAQPage schema 同源生成，逐字一致
  - 图片 caption 只描述照片里真实可见的内容
  - 专属 CSS 放第二个 <style> 块（sync 只替换第一个）
用法：python3 build_ar_pages.py
"""
import os, json
from html import escape as e
from tpl_common import APP, BASE, STYLE, HEADER, FOOTER, MINI_JS, GA4_SNIPPET, RSS_LINK
from belts_data import BELTS
from belts_data_ar import (AR_BELTS, AR_SERVICES, AR_PHOTOS_NOTE, AR_EXCL_TITLE,
                           AR_EXCL_SHORT, AR_CTA_TITLE, AR_CTA_TEXT)
from build_belts import PAGE_CSS, AR_CSS, flow_svg, icon_svg

AR_BELT_DIR = os.path.join(APP, 'ar', 'belts')
AR_SVC_DIR = os.path.join(APP, 'ar', 'services')
HUB_EN = BASE + '/sourcing-belts.html'
HUB_AR = BASE + '/ar/sourcing-belts.html'


def ar_shell(title, desc, canonical, en_url, body, ld_list):
    """通用阿语 SSR shell。语言按钮点击跳回对应英文页（覆盖 toggleLang）。"""
    head = [
        '<!doctype html>\n<html lang="ar" dir="rtl">\n<head>\n',
        '<meta charset="UTF-8" />\n',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n',
        '<title>%s</title>\n' % e(title),
        '<meta name="description" content="%s" />\n' % e(desc),
        '<meta property="og:title" content="%s" />\n' % e(title),
        '<meta property="og:description" content="%s" />\n' % e(desc),
        '<meta property="og:url" content="%s" />\n' % canonical,
        '<meta property="og:image" content="%s/images/og-default.jpg" />\n' % BASE,
        '<meta property="og:type" content="website" />\n',
        '<meta property="og:site_name" content="SourceToGulf" />\n',
        '<meta property="og:locale" content="ar_AE" />\n',
        '<meta name="twitter:card" content="summary_large_image" />\n',
        '<link rel="canonical" href="%s" />\n' % canonical,
        '<link rel="alternate" hreflang="ar" href="%s" />\n' % canonical,
        '<link rel="alternate" hreflang="en" href="%s" />\n' % en_url,
        '<link rel="alternate" hreflang="x-default" href="%s" />\n' % en_url,
        '<link rel="icon" href="/favicon.ico" sizes="any">\n',
        '<link rel="apple-touch-icon" href="/images/logo/logo-icon-512.png">\n',
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n',
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Kufi+Arabic:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n',
        '<style>%s</style>\n' % STYLE,
        GA4_SNIPPET + RSS_LINK + PAGE_CSS + AR_CSS,
        '</head>\n<body>\n',
        '<header>\n' + HEADER + '\n</header>\n',
        body,
        '\n<footer>\n' + FOOTER + '\n</footer>\n',
        '<a class="float-wa" href="https://wa.me/971585854194" target="_blank" rel="noopener" aria-label="WhatsApp">💬</a>\n',
        '<button id="toTop" aria-label="Back to top">↑</button>\n',
        '<script>%s</script>\n' % MINI_JS,
        '<script src="/fx.js" defer></script>\n',
    ]
    # 阿语页强制 ar/rtl；语言按钮跳回英文对应页
    head.append('''<script>
window.addEventListener('load',function(){
  try{localStorage.setItem('stg-lang','ar');}catch(err){}
  window.lang='ar';
  if(typeof applyLang==='function'){applyLang();}
  document.documentElement.lang='ar';document.documentElement.dir='rtl';
  document.querySelectorAll('.lang-btn').forEach(function(b){b.textContent='English';});
  window.toggleLang=function(){window.location.href='%s';};
});
</script>''' % en_url)
    head.append('<script type="application/ld+json">\n%s\n</script>\n'
                % json.dumps(ld_list, ensure_ascii=False))
    head.append('</body>\n</html>')
    return ''.join(head)


def photo_grid_ar(photos):
    """实拍图组：沿用英文页图片，caption 用阿语通用说明（不捏造地点）。"""
    cols = []
    for src, alt, cap in photos:
        cols.append('<figure><img src="/%s" alt="%s" loading="lazy">'
                    '<figcaption><b>%s</b>%s</figcaption></figure>'
                    % (src, e(alt), e(alt), e(AR_PHOTOS_NOTE)))
    return '<div class="photo-grid">%s</div>' % ''.join(cols)


def faq_html_ar(faq):
    return ''.join('<div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (e(q), e(a))
                   for q, a in faq)


def cta_ar():
    return ('<div class="cta-band"><h2>%s</h2><p>%s</p>'
            '<a class="wa-btn" href="https://wa.me/971585854194" target="_blank" rel="noopener">'
            '💬 أرسل صورة أو مواصفة</a>'
            '<span class="alt">يراجع شخصٌ كل طلب قبل بدء العمل. '
            '<a href="/services/sourcing-request.html">صفحة طلب التوريد</a> و'
            '<a href="/order-intent.json">العقد المقروء آلياً</a> يبيّنان الحقول المطلوبة.</span></div>'
            % (e(AR_CTA_TITLE), e(AR_CTA_TEXT)))


def belt_body_ar(a, en_belt, idx):
    p = []
    p.append('<section class="belt-hero"><div class="belt-wrap">')
    p.append('<div class="crumb"><a href="/ar/">الرئيسية</a> / '
             '<a href="%s">تجمّعات التوريد</a> / <span>%s</span></div>'
             % (HUB_AR, e(a['city'])))
    p.append('<span class="belt-kicker">تجمّع توريد صيني · %s</span>' % e(a['region']))
    p.append('<h1>%s</h1>' % e(a['h1']))
    p.append('<p class="lede">%s</p>' % e(a['desc']))
    p.append('<div class="fact-grid">')
    for k, v in a['facts']:
        p.append('<div><b>%s</b><span>%s</span></div>' % (e(k), e(v)))
    p.append('</div></div></section><div class="belt-wrap">')

    p.append('<section class="belt-sec"><div class="answer-box">'
             '<span class="lbl">إجابة مختصرة للمساعدات الذكية والمشترين</span>'
             '<p>%s</p></div></section>' % e(a['answer']))

    p.append('<section class="belt-sec"><span class="belt-kicker">من زياراتنا الميدانية</span>'
             '<h2>كيف يبدو العمل على أرض الواقع</h2>'
             '<p class="sec-sub">%s</p>%s</section>'
             % (e(AR_PHOTOS_NOTE), photo_grid_ar(en_belt['photos'])))

    p.append('<section class="belt-sec"><h2>سلسلة العمل خلف الطلب</h2>'
             '<p class="sec-sub">أين يجري العمل فعلاً، من المادة الأولية إلى شحنة جاهزة '
             'للخليج. خطوة الامتثال تسبق الإنتاج، لا تأتي عند الحجز.</p>'
             '<div class="flow-box">%s<div class="flow-cap">مخطط العملية: %s. '
             'الخطوات توضيحية لكيفية تخطيط الطلب، وقد يختلف الترتيب بحسب المنتج.</div></div></section>'
             % (flow_svg(a['flow'], 'سلسلة التوريد: ' + a['category'] + ' من ' + a['city'],
                         'تسلسل الخطوات: ' + ' → '.join(a['flow']) + '.'),
                e(' → '.join(a['flow']))))

    p.append('<section class="belt-sec"><h2>لماذا هذا التجمّع</h2><div class="prose">')
    for para in a['intro']:
        p.append('<p>%s</p>' % e(para))
    p.append('</div></section>')

    p.append('<section class="belt-sec"><h2>ما يورّده مشترو الخليج من هنا</h2>'
             '<p class="sec-sub">مرتّب حسب الموسم والمناسبة لا حسب رقم الصنف.</p>'
             '<table class="belt-table"><thead><tr><th>النافذة / الاستخدام</th>'
             '<th>ما يُطلب عادةً</th></tr></thead><tbody>')
    for k, v in a['buys']:
        p.append('<tr><td>%s</td><td>%s</td></tr>' % (e(k), e(v)))
    p.append('</tbody></table></section>')

    p.append('<section class="belt-sec"><h2>الملصقات والشهادات والمستندات</h2>'
             '<p class="sec-sub">المتطلبات تعتمد على المنتج الدقيق والوجهة. هذه الأسئلة '
             'نُغلقها قبل الإنتاج لا بعد صنع الدفعة.</p><ul class="check-list">')
    for c in a['compliance']:
        p.append('<li>%s</li>' % e(c))
    p.append('</ul></section>')

    p.append('<section class="belt-sec"><h2>خمسة أخطاء تُكلّف موسماً</h2>'
             '<p class="sec-sub">أعطال محدّدة نتحقّق منها، وضابط يمنع كل واحد.</p>'
             '<div class="pit-grid">')
    for i, (t, d) in enumerate(a['pitfalls']):
        p.append('<div class="pit"><span class="num">%d</span><b>%s</b><p>%s</p></div>'
                 % (i + 1, e(t), e(d)))
    p.append('</div></section>')

    p.append('<section class="belt-sec excl"><h2>%s</h2><div class="excl-grid">'
             % e(AR_EXCL_TITLE))
    for t, d in AR_EXCL_SHORT:
        p.append('<div class="excl-item"><b>%s</b><p>%s</p></div>' % (e(t), e(d)))
    p.append('</div><p class="strip-note"><a href="%s">القائمة الكاملة '
             'لحدود العمل في صفحة التجمّعات ←</a></p></section>' % HUB_AR)

    p.append('<section class="belt-sec"><span class="belt-kicker">الأسئلة الشائعة</span>'
             '<h2>أسئلة متكرّرة</h2><div>%s</div></section>' % faq_html_ar(a['faq']))

    p.append('<section class="belt-sec"><h2>تجمّعات أخرى يجمعها مشترو الخليج مع هذا التجمّع</h2>'
             '<div class="rel-grid">')
    for s in en_belt['related']:
        x = next((y for y in AR_BELTS if y['slug'] == s), None)
        if x:
            p.append('<a href="/ar/belts/%s.html">%s<small>%s</small></a>'
                     % (s, e(x['city']), e(x['category'])))
    p.append('</div><p class="strip-note"><a href="%s">← العودة إلى التجمّعات الثمانية</a>'
             '</p></section>' % HUB_AR)

    p.append('<section class="belt-sec">%s</section>' % cta_ar())
    p.append('</div>')
    return '\n'.join(p)


def belt_ld_ar(a, canonical, en_url):
    return [
        {'@context': 'https://schema.org', '@type': 'WebPage',
         'name': a['h1'], 'url': canonical, 'description': a['desc'], 'inLanguage': 'ar',
         'breadcrumb': {'@type': 'BreadcrumbList', 'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': 'الرئيسية', 'item': BASE + '/ar/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'تجمّعات التوريد', 'item': HUB_AR},
             {'@type': 'ListItem', 'position': 3, 'name': a['city'], 'item': canonical},
         ]}},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': 'ar',
         'mainEntity': [{'@type': 'Question', 'name': q,
                         'acceptedAnswer': {'@type': 'Answer', 'text': ans}}
                        for q, ans in a['faq']]},
    ]


def service_body_ar(s):
    p = []
    p.append('<section class="belt-hero"><div class="belt-wrap">')
    p.append('<div class="crumb"><a href="/ar/">الرئيسية</a> / <span>الخدمات</span></div>')
    p.append('<span class="belt-kicker">SourceToGulf · خدمات التوريد</span>')
    p.append('<h1>%s</h1>' % e(s['h1']))
    p.append('<p class="lede">%s</p>' % e(s['desc']))
    p.append('</div></section><div class="belt-wrap">')

    p.append('<section class="belt-sec"><div class="answer-box">'
             '<span class="lbl">إجابة مختصرة للمساعدات الذكية والمشترين</span>'
             '<p>%s</p></div></section>' % e(s['answer']))

    p.append('<section class="belt-sec"><h2>كيف نعمل</h2><div class="pit-grid">')
    for i, (t, d) in enumerate(s['blocks']):
        p.append('<div class="pit"><span class="num">%d</span><b>%s</b><p>%s</p></div>'
                 % (i + 1, e(t), e(d)))
    p.append('</div></section>')

    p.append('<section class="belt-sec excl"><h2>%s</h2><div class="excl-grid">'
             % e(AR_EXCL_TITLE))
    for t, d in AR_EXCL_SHORT:
        p.append('<div class="excl-item"><b>%s</b><p>%s</p></div>' % (e(t), e(d)))
    p.append('</div></section>')

    p.append('<section class="belt-sec"><span class="belt-kicker">الأسئلة الشائعة</span>'
             '<h2>أسئلة متكرّرة</h2><div>%s</div></section>' % faq_html_ar(s['faq']))

    p.append('<section class="belt-sec"><h2>خدمات ذات صلة</h2><div class="rel-grid">')
    for other in AR_SERVICES:
        if other['slug'] != s['slug']:
            p.append('<a href="/ar/services/%s.html">%s<small>SourceToGulf</small></a>'
                     % (other['slug'], e(other['h1'])))
    p.append('</div><p class="strip-note"><a href="%s">خريطة التجمّعات الصناعية '
             'للمشترين في الخليج ←</a></p></section>' % HUB_AR)

    p.append('<section class="belt-sec">%s</section>' % cta_ar())
    p.append('</div>')
    return '\n'.join(p)


def service_ld_ar(s, canonical):
    return [
        {'@context': 'https://schema.org', '@type': 'WebPage',
         'name': s['h1'], 'url': canonical, 'description': s['desc'], 'inLanguage': 'ar',
         'breadcrumb': {'@type': 'BreadcrumbList', 'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': 'الرئيسية', 'item': BASE + '/ar/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'الخدمات', 'item': canonical},
         ]}},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': 'ar',
         'mainEntity': [{'@type': 'Question', 'name': q,
                         'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                        for q, a in s['faq']]},
    ]


def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('  ✓', os.path.relpath(path, APP))


def sync_en_hreflang():
    """给 5 个英文服务页补 hreflang="ar"（幂等）。

    服务页是手工页、没有生成器重写，但 deploy 会跑 sync_header_footer.py；
    把这一步放进生成器可保证 hreflang 双向长期存在，且不依赖一次性手改。
    """
    changed = []
    for s in AR_SERVICES:
        rel = os.path.join('services', s['slug'] + '.html')
        path = os.path.join(APP, rel)
        if not os.path.exists(path):
            continue
        html = open(path, encoding='utf-8').read()
        ar_url = BASE + '/ar/services/' + s['slug'] + '.html'
        if 'hreflang="ar" href="%s"' % ar_url in html:
            continue
        # 插在 x-default 行之后（与全站顺序一致）
        marker = '<link rel="alternate" hreflang="x-default" href="https://sourcetogulf.com/services/%s.html" />' % s['slug']
        if marker not in html:
            print('  ! 未找到插入锚点，跳过', rel)
            continue
        html = html.replace(marker, marker + '\n<link rel="alternate" hreflang="ar" href="%s" />' % ar_url, 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        changed.append(rel)
    print('  ✓ 英文服务页 hreflang ar 同步：%d 个变更' % len(changed))
    for c in changed:
        print('    -', c)


def main():
    print('build_ar_pages.py — 产业带分页 / 服务页 阿语 SSR')
    by_slug = {b['slug']: b for b in BELTS}
    for idx, a in enumerate(AR_BELTS):
        en_url = BASE + '/belts/' + a['slug'] + '.html'
        canonical = BASE + '/ar/belts/' + a['slug'] + '.html'
        html = ar_shell(a['h1'] + ' | SourceToGulf', a['desc'], canonical, en_url,
                        belt_body_ar(a, by_slug[a['slug']], idx),
                        belt_ld_ar(a, canonical, en_url))
        write(os.path.join(AR_BELT_DIR, a['slug'] + '.html'), html)
    for s in AR_SERVICES:
        en_url = BASE + '/services/' + s['slug'] + '.html'
        canonical = BASE + '/ar/services/' + s['slug'] + '.html'
        html = ar_shell(s['title'], s['desc'], canonical, en_url,
                        service_body_ar(s), service_ld_ar(s, canonical))
        write(os.path.join(AR_SVC_DIR, s['slug'] + '.html'), html)
    sync_en_hreflang()
    print('完成：%d 产业带分页 + %d 服务页' % (len(AR_BELTS), len(AR_SERVICES)))


if __name__ == '__main__':
    main()
