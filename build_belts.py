# -*- coding: utf-8 -*-
"""
build_belts.py — 中国产业带 × 海湾客户类型 SSR 生成器
=====================================================
产出（全部服务端渲染，无客户端拼接正文）：
  sourcing-belts.html              hub（英文）
  belts/<slug>.html                8 个产业带分页（英文）
  ar/sourcing-belts.html            hub（阿语 SSR，dir=rtl，hreflang 双向）

内容真相源：belts_data.py
用法：python3 build_belts.py

设计约束（站点既有红线）：
  - page_shell 的第一个 <style>/<header>/<footer> 会被 sync_header_footer.py 覆盖，
    因此本页专属 CSS 一律放 extra_head 里的「第二个 <style>」块。
  - 语言按钮必须带 onclick="toggleLang()"（HEADER 已带）。新页用 load 事件覆盖
    toggleLang 为「跳转阿语 SSR 页」，避免正文无 data-ar 时切 dir=rtl 导致英文错乱。
  - 可见 FAQ 与 FAQPage schema 由同一份数据生成，逐字同源。
  - 图片 caption 只描述照片里真实可见的内容，不捏造拍摄地点。
  - 不写客户名/工厂名/1688/品牌名/价格/MOQ 数字/最高级词。
"""
import os, json
from html import escape as esc
from tpl_common import APP, BASE, page_shell, STYLE, HEADER, FOOTER, MINI_JS, GA4_SNIPPET, RSS_LINK
from belts_data import (BELTS, BUYER_TYPES, EXCLUSIONS, HUB_FAQ, HUB_ANSWER, HUB_URL)

BELT_DIR = os.path.join(APP, 'belts')
AR_DIR = os.path.join(APP, 'ar')
TODAY = '2026-11-06'
AR_HUB_URL = BASE + '/ar/sourcing-belts.html'


def e(s):
    """统一 HTML 转义。可见文本与 schema 同源使用。"""
    return esc(s, quote=True)


# ---------------------------------------------------------------------------
# 自绘 SVG（不引用任何外部素材 / 不捏造地图）
# ---------------------------------------------------------------------------
ICONS = {
    'phone': '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M10 5h4"/><circle cx="12" cy="18.5" r="1"/>',
    'hanger': '<path d="M12 6a2.2 2.2 0 1 1 2.2-2.2"/><path d="M12 6v2.5L3.5 15a1.4 1.4 0 0 0 .9 2.5h15.2a1.4 1.4 0 0 0 .9-2.5L12 8.5"/>',
    'boxes': '<rect x="2.5" y="7" width="8" height="8" rx="1"/><rect x="13.5" y="7" width="8" height="8" rx="1"/><rect x="2.5" y="16" width="8" height="5.5" rx="1"/><rect x="13.5" y="16" width="8" height="5.5" rx="1"/>',
    'tag': '<path d="M3 11.5V4a1 1 0 0 1 1-1h7.5L21 12.5 12.5 21z"/><circle cx="7.5" cy="7.5" r="1.4"/>',
    'plan': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 9v12M13 14h5M13 17.5h5"/>',
    'gift': '<rect x="3" y="9" width="18" height="12" rx="1.5"/><path d="M2.5 9h19M12 9v12"/><path d="M12 9C9 9 6.5 8 6.5 5.8A2.3 2.3 0 0 1 9 3.5c1.8 0 3 2.5 3 5.5zM12 9c3 0 5.5-1 5.5-3.2A2.3 2.3 0 0 0 15 3.5c-1.8 0-3 2.5-3 5.5z"/>',
}


def icon_svg(kind, size=30):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '%s</svg>') % (size, size, ICONS.get(kind, ICONS['boxes']))


def flow_svg(steps, title, desc):
    """产业链流程信息图。SVG 内 <text> 与 <title>/<desc> 均可被 AI 抓取。"""
    n = len(steps)
    w, h = 1160, 168
    pad, gap = 26, 12
    bw = (w - pad * 2 - gap * (n - 1)) / n
    parts = [
        '<svg class="belt-flow" viewBox="0 0 %d %d" width="100%%" role="img" '
        'aria-labelledby="bft bfd" xmlns="http://www.w3.org/2000/svg">' % (w, h),
        '<title id="bft">%s</title><desc id="bfd">%s</desc>' % (e(title), e(desc)),
    ]
    # 连接轴
    parts.append('<line x1="%d" y1="62" x2="%d" y2="62" stroke="#E7E1D4" stroke-width="2"/>' % (pad + 10, w - pad - 10))
    for i, s in enumerate(steps):
        x = pad + i * (bw + gap)
        fill = '#0B2B4D' if i % 2 == 0 else '#173B60'
        parts.append('<rect x="%.1f" y="28" width="%.1f" height="68" rx="10" fill="%s"/>' % (x, bw, fill))
        parts.append('<circle cx="%.1f" cy="62" r="15" fill="#C9A24B"/>' % (x + bw / 2))
        parts.append('<text x="%.1f" y="67" text-anchor="middle" font-size="14" font-weight="700" '
                     'fill="#0B2B4D" font-family="Inter,Arial,sans-serif">%d</text>' % (x + bw / 2, i + 1))
        # 换行文字
        words, lines, cur = s.split(), [], ''
        for wd in words:
            t = (cur + ' ' + wd).strip()
            if len(t) > 15 and cur:
                lines.append(cur); cur = wd
            else:
                cur = t
        if cur:
            lines.append(cur)
        for j, ln in enumerate(lines[:2]):
            parts.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="13" font-weight="600" '
                         'fill="#0B2B4D" font-family="Inter,Arial,sans-serif">%s</text>'
                         % (x + bw / 2, 122 + j * 18, e(ln)))
        if i < n - 1:
            parts.append('<path d="M%.1f 62 l6 -4 v8 z" fill="#C9A24B"/>' % (x + bw + 2))
    parts.append('</svg>')
    return ''.join(parts)


def hub_overview_svg():
    """hub 总览：从产业带到海湾货架的链路（非地图，规避地图合规）。"""
    steps = ['Pick a cluster', 'Specify & sample', 'Confirm compliance', 'Production & QC',
             'Consolidate', 'Ship to GCC']
    return flow_svg(steps,
                    'How a China industrial cluster order reaches a Gulf buyer',
                    'Six stages: pick a cluster, specify and sample, confirm the compliance route, '
                    'produce with quality checks, consolidate, then ship to the GCC.')


# ---------------------------------------------------------------------------
# 页面专属 CSS（第二个 <style> 块，sync 不会覆盖）
# ---------------------------------------------------------------------------
PAGE_CSS = """<style>
.belt-wrap{max-width:1120px;margin:0 auto;padding:0 20px}
.belt-hero{background:linear-gradient(160deg,#0B2B4D 0%,#071E36 100%);color:#FBF9F5;padding:54px 0 46px}
.belt-hero .crumb{font-size:12.5px;opacity:.72;margin-bottom:16px}
.belt-hero .crumb a{color:#C9A24B;text-decoration:none}
.belt-hero h1{font-size:clamp(26px,3.6vw,40px);line-height:1.18;margin:0 0 14px;font-weight:800;letter-spacing:-.02em}
.belt-hero .lede{font-size:15.5px;line-height:1.65;max-width:820px;opacity:.9;margin:0}
.belt-kicker{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#C9A24B;margin-bottom:14px}
.belt-sec{padding:44px 0;border-bottom:1px solid #E7E1D4}
.belt-sec:last-of-type{border-bottom:0}
.belt-sec h2{font-size:clamp(20px,2.3vw,27px);font-weight:800;color:#0B2B4D;margin:0 0 8px;letter-spacing:-.015em}
.belt-sec .sec-sub{font-size:14px;color:#5F6661;margin:0 0 22px;line-height:1.6;max-width:800px}
.answer-box{background:#F3EFE7;border-left:4px solid #C9A24B;border-radius:0 12px 12px 0;padding:20px 24px;margin:0 0 8px}
.answer-box .lbl{font-size:11px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:#8A6D2A;display:block;margin-bottom:9px}
.answer-box p{font-size:15px;line-height:1.75;color:#17201D;margin:0}
.fact-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:26px 0 0}
.fact-grid > div{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.16);border-radius:12px;padding:14px 16px}
.fact-grid b{display:block;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#C9A24B;margin-bottom:7px}
.fact-grid span{font-size:13.5px;line-height:1.5;color:#FBF9F5}
.photo-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin:0 0 6px}
.photo-grid figure{margin:0;background:#fff;border:1px solid #E7E1D4;border-radius:14px;overflow:hidden}
.photo-grid img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;background:#F3EFE7}
.photo-grid figcaption{font-size:12.5px;line-height:1.55;color:#5F6661;padding:12px 14px 14px}
.photo-grid figcaption b{display:block;color:#0B2B4D;font-size:12.5px;margin-bottom:3px}
.flow-box{background:#fff;border:1px solid #E7E1D4;border-radius:14px;padding:18px 16px 10px;overflow-x:auto;margin:0 0 4px}
.belt-flow{min-width:900px;display:block}
.flow-cap{font-size:12.5px;color:#5F6661;line-height:1.55;padding:2px 4px 10px}
.prose p{font-size:14.5px;line-height:1.8;color:#17201D;margin:0 0 14px}
.belt-table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #E7E1D4;border-radius:12px;overflow:hidden;font-size:13.5px}
.belt-table th{background:#0B2B4D;color:#FBF9F5;text-align:left;padding:12px 15px;font-size:12px;letter-spacing:.06em;text-transform:uppercase;font-weight:700}
.belt-table td{padding:13px 15px;border-top:1px solid #E7E1D4;vertical-align:top;line-height:1.6;color:#17201D}
.belt-table td:first-child{font-weight:700;color:#0B2B4D;width:27%}
.check-list{list-style:none;padding:0;margin:0;display:grid;gap:11px}
.check-list li{position:relative;padding-left:28px;font-size:14px;line-height:1.7;color:#17201D}
.check-list li:before{content:"";position:absolute;left:2px;top:8px;width:13px;height:13px;border-radius:3px;background:#C9A24B;opacity:.85}
.pit-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}
.pit{background:#fff;border:1px solid #E7E1D4;border-radius:12px;padding:15px 17px}
.pit .num{display:inline-flex;align-items:center;justify-content:center;width:23px;height:23px;border-radius:50%;background:#0B2B4D;color:#fff;font-size:11px;font-weight:700;margin-bottom:9px}
.pit b{display:block;font-size:14px;color:#0B2B4D;margin-bottom:5px}
.pit p{font-size:13px;line-height:1.65;color:#5F6661;margin:0}
.buyer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px}
.buyer-card{background:#fff;border:1px solid #E7E1D4;border-radius:14px;padding:19px 20px;display:flex;flex-direction:column}
.buyer-card .ic{color:#C9A24B;margin-bottom:10px}
.buyer-card h3{font-size:16px;color:#0B2B4D;margin:0 0 4px;font-weight:800}
.buyer-card .local{font-size:11.5px;color:#8A6D2A;font-weight:600;margin-bottom:11px}
.buyer-card p{font-size:13.3px;line-height:1.65;color:#5F6661;margin:0 0 12px}
.buyer-card dl{margin:0 0 12px;font-size:12.8px;line-height:1.6}
.buyer-card dt{font-weight:700;color:#0B2B4D;display:inline}
.buyer-card dd{display:inline;margin:0;color:#5F6661}
.buyer-card dd:after{content:"";display:block;height:7px}
.buyer-card .belts{font-size:12.5px;margin-top:auto;padding-top:11px;border-top:1px solid #E7E1D4;color:#5F6661}
.buyer-card .belts a{color:#0B2B4D;text-decoration:none;font-weight:600}
.buyer-card .belts a:hover{text-decoration:underline}
.belt-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:16px}
.belt-card{background:#fff;border:1px solid #E7E1D4;border-radius:14px;overflow:hidden;display:flex;flex-direction:column;transition:transform .18s,box-shadow .18s}
.belt-card:hover{transform:translateY(-3px);box-shadow:0 12px 28px rgba(11,43,77,.11)}
.belt-card > a.img{display:block;aspect-ratio:16/9;overflow:hidden;background:#F3EFE7}
.belt-card img{width:100%;height:100%;object-fit:cover;display:block}
.belt-card .bd{padding:17px 19px 19px;display:flex;flex-direction:column;flex:1}
.belt-card .city{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#8A6D2A;font-weight:700;margin-bottom:7px}
.belt-card h3{font-size:17px;color:#0B2B4D;margin:0 0 9px;font-weight:800;line-height:1.3}
.belt-card h3 a{color:inherit;text-decoration:none}
.belt-card h3 a:hover{text-decoration:underline}
.belt-card .meta{font-size:12.8px;color:#5F6661;line-height:1.6;margin:0 0 12px}
.belt-card .tagrow{display:flex;flex-wrap:wrap;gap:6px;margin-top:auto;padding-top:11px;border-top:1px solid #E7E1D4}
.belt-card .tagrow span{font-size:11px;background:#F3EFE7;color:#0B2B4D;border-radius:99px;padding:4px 9px}
.excl{background:#FCF6F3;border:1px solid #EAD9CF;border-radius:14px;padding:22px 24px}
.excl h2{color:#7A3B22}
.excl-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-top:16px}
.excl-item b{display:block;font-size:13.5px;color:#7A3B22;margin-bottom:5px}
.excl-item p{font-size:12.8px;line-height:1.65;color:#5F6661;margin:0}
.faq-item{border-bottom:1px solid #E7E1D4;padding:15px 0}
.faq-item:last-child{border-bottom:0}
.faq-item h3{font-size:15px;color:#0B2B4D;margin:0 0 7px;font-weight:700}
.faq-item p{font-size:13.8px;line-height:1.75;color:#5F6661;margin:0}
.rel-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:11px}
.rel-grid a{display:block;background:#fff;border:1px solid #E7E1D4;border-radius:11px;padding:13px 15px;text-decoration:none;color:#0B2B4D;font-size:13.5px;font-weight:600}
.rel-grid a:hover{border-color:#C9A24B}
.rel-grid a small{display:block;color:#5F6661;font-weight:400;margin-top:3px;font-size:12px}
.cta-band{background:#0B2B4D;color:#FBF9F5;border-radius:16px;padding:30px 32px;text-align:center}
.cta-band h2{color:#fff;font-size:22px;margin:0 0 9px;font-weight:800}
.cta-band p{font-size:14px;line-height:1.7;opacity:.88;max-width:680px;margin:0 auto 18px}
.cta-band .wa-btn{background:#C9A24B;color:#0B2B4D;font-weight:800;border-radius:99px;padding:12px 26px;text-decoration:none;display:inline-block;font-size:14px}
.cta-band .alt{display:block;font-size:12.5px;opacity:.75;margin-top:12px}
.cta-band .alt a{color:#C9A24B}
.bridge{background:#F3EFE7;border-radius:14px;padding:22px 24px;display:flex;gap:20px;align-items:center;flex-wrap:wrap}
.bridge .tx{flex:1 1 320px}
.bridge h3{font-size:16px;color:#0B2B4D;margin:0 0 6px}
.bridge p{font-size:13.2px;line-height:1.65;color:#5F6661;margin:0}
.bridge a.btn{flex:0 0 auto;background:#0B2B4D;color:#fff;border-radius:99px;padding:11px 22px;text-decoration:none;font-size:13px;font-weight:700}
.strip-note{font-size:12.5px;color:#5F6661;line-height:1.6;margin-top:14px}
@media(max-width:720px){.fact-grid{grid-template-columns:repeat(2,1fr)}.belt-hero{padding:38px 0 34px}.belt-sec{padding:32px 0}}
@media(max-width:420px){.fact-grid{grid-template-columns:1fr}}
</style>"""

# load 事件覆盖：语言按钮跳到阿语 SSR 页，避免英文正文被切成 rtl
LANG_SCRIPT = """<script>
window.addEventListener('load',function(){
  try{localStorage.setItem('stg-lang','en');}catch(err){}
  window.lang='en';
  if(typeof applyLang==='function'){applyLang();}
  document.documentElement.lang='en';document.documentElement.dir='ltr';
  document.querySelectorAll('.lang-btn').forEach(function(b){b.textContent='العربية';});
  window.toggleLang=function(){window.location.href='__AR__';};
});
</script>"""


def images_ld(items):
    """实拍图的 ImageObject schema —— 让 AI 读到「图里有什么」。"""
    out = []
    for src, alt, cap in items:
        out.append({
            '@type': 'ImageObject',
            'contentUrl': BASE + '/' + src.lstrip('/'),
            'name': alt,
            'caption': cap,
            'creditText': 'SourceToGulf — photographed on sourcing trips in China',
        })
    return out


def photo_grid(items):
    cols = []
    for src, alt, cap in items:
        cols.append(
            '<figure><img src="/%s" alt="%s" loading="lazy">'
            '<figcaption><b>%s</b>%s</figcaption></figure>'
            % (src, e(alt), e(alt), e(cap)))
    return '<div class="photo-grid">%s</div>' % ''.join(cols)


def faq_html(faq):
    return ''.join('<div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (e(q), e(a)) for q, a in faq)


def cta_band(title, text, anchor='sourcing'):
    return ('<div class="cta-band"><h2>%s</h2><p>%s</p>'
            '<a class="wa-btn" href="https://wa.me/971585854194" target="_blank" rel="noopener">'
            '💬 Send a photo or specification</a>'
            '<span class="alt">A person reviews every request before work starts. '
            'The <a href="/services/sourcing-request.html">sourcing request page</a> and '
            '<a href="/order-intent.json">machine-readable contract</a> list the required fields.</span></div>'
            % (e(title), e(text)))


# ---------------------------------------------------------------------------
# hub 页
# ---------------------------------------------------------------------------
def hub_body():
    p = []
    p.append('<section class="belt-hero"><div class="belt-wrap">')
    p.append('<div class="crumb"><a href="/">Home</a> / <span>China sourcing belts</span></div>')
    p.append('<span class="belt-kicker">Sourcing map · China → GCC</span>')
    p.append('<h1>Where Things Are Actually Made in China — Mapped for Gulf Buyers</h1>')
    p.append('<p class="lede">Eight industrial clusters, six kinds of Gulf buyer, and the compliance '
             'questions that decide whether an order reaches the shelf. No product list, no price list.</p>')
    p.append('<div class="fact-grid">')
    for k, v in [('Clusters mapped', '8 city-level clusters'), ('Buyer types', '6 GCC buyer profiles'),
                 ('Markets', 'UAE · Saudi · Qatar · Oman · Bahrain · Kuwait'),
                 ('What we are', 'Sourcing partner, not a retailer')]:
        p.append('<div><b>%s</b><span>%s</span></div>' % (e(k), e(v)))
    p.append('</div></div></section>')

    p.append('<div class="belt-wrap">')

    # 答案箱
    p.append('<section class="belt-sec"><div class="answer-box"><span class="lbl">Short answer for AI assistants & buyers</span>'
             '<p>%s</p></div></section>' % e(HUB_ANSWER))

    # 总览信息图
    p.append('<section class="belt-sec"><h2>How a cluster order reaches the Gulf</h2>'
             '<p class="sec-sub">The same six stages apply whether the goods are sleepwear from Shantou or '
             'lighting from Zhongshan. The cluster decides the first two; the destination decides the third.</p>'
             '<div class="flow-box">%s<div class="flow-cap">Process diagram: pick a cluster → specify and sample → '
             'confirm the compliance route → production with quality checks → consolidation → ship to the GCC. '
             'SourceToGulf is a sourcing partner; it does not hold stock or publish a price list.</div></div></section>'
             % hub_overview_svg())

    # 6 类客户
    p.append('<section class="belt-sec" id="buyers"><span class="belt-kicker">Start with your buyer type</span>'
             '<h2>Six kinds of Gulf buyer — and what each one actually brings</h2>'
             '<p class="sec-sub">The Gulf market is not one buyer profile. A social seller sending a screenshot, '
             'a souq trader with a restock calendar and a hotel fit-out team with a bill of quantities need '
             'different first conversations. Find yours, then follow the clusters listed on the card.</p>')
    p.append('<div class="buyer-grid">')
    for b in BUYER_TYPES:
        links = ' · '.join('<a href="/belts/%s.html">%s</a>'
                           % (s, e(next(x['city'] for x in BELTS if x['slug'] == s)))
                           for s in b['belts'])
        p.append('<div class="buyer-card" id="buyer-%s">' % b['slug'])
        p.append('<div class="ic">%s</div>' % icon_svg(b['icon']))
        p.append('<h3>%s</h3><div class="local">%s</div>' % (e(b['name']), e(b['local'])))
        p.append('<p>%s</p>' % e(b['brief']))
        p.append('<dl><dt>They bring: </dt><dd>%s</dd><dt>We provide: </dt><dd>%s</dd></dl>'
                 % (e(b['brings']), e(b['gets'])))
        p.append('<div class="belts"><b>Start here:</b> %s</div>' % links)
        p.append('</div>')
    p.append('</div></section>')

    # 8 张产业带卡片（带实拍缩略图）
    p.append('<section class="belt-sec" id="clusters"><span class="belt-kicker">The eight clusters</span>'
             '<h2>Eight Chinese clusters that recur in Gulf sourcing</h2>'
             '<p class="sec-sub">Each card leads to a full guide: what the cluster makes, what Gulf buyers '
             'order there by season, the labelling and certification watchpoints, and the five mistakes '
             'that cost a season. Photographs show real market and workshop visits.</p>')
    p.append('<div class="belt-cards">')
    for i, b in enumerate(BELTS):
        src = b['photos'][0][0]
        fits = [next(x for x in BUYER_TYPES if x['slug'] == s)['name'] for s in b['perfect_for']]
        p.append('<div class="belt-card"><a class="img" href="/belts/%s.html">'
                 '<img src="/%s" alt="%s" loading="lazy"></a><div class="bd">'
                 % (b['slug'], src, e(b['photos'][0][1])))
        p.append('<div class="city">%02d · %s</div>' % (i + 1, e(b['city'])))
        p.append('<h3><a href="/belts/%s.html">%s</a></h3>' % (b['slug'], e(b['category'])))
        p.append('<p class="meta">%s</p>' % e(b['facts'][0][1]))
        p.append('<div class="tagrow">%s</div>'
                 % ''.join('<span>%s</span>' % e(t) for t in fits[:2]))
        p.append('</div></div>')
    p.append('</div></section>')

    # 排除项
    p.append('<section class="belt-sec excl" id="exclusions"><span class="belt-kicker">Read this before you enquire</span>'
             '<h2>What we do not take on</h2>'
             '<p class="sec-sub">Stating this plainly saves both sides time. These are scope limits, '
             'not judgements on a buyer.</p><div class="excl-grid">')
    for t, d in EXCLUSIONS:
        p.append('<div class="excl-item"><b>%s</b><p>%s</p></div>' % (e(t), e(d)))
    p.append('</div></section>')

    # 实拍图墙
    wall = [
        ('images/market-variety.jpg', 'Wholesale market aisle with stacked seasonal goods',
         'A wholesale market aisle in China, photographed on a sourcing trip. Buying starts with seeing '
         'what actually exists, not with a catalogue of assumed SKUs.'),
        ('images/apparel/apparel-fabriccards.jpg', 'Hands selecting fabric swatch cards',
         'Selecting physical fabric swatch cards. Material is chosen from a real card before a garment '
         'specification is written.'),
        ('images/packaging/package-printing-press.jpg', 'Printing press on a packaging production floor',
         'A printing press on a packaging production floor. Printing, die-cutting and gluing are '
         'separate steps, each with its own minimum.'),
        ('images/jewelry-market-yiwu.jpg', 'Gold chains on a jewellery counter',
         'Gold chains on a jewellery counter. Base metal and plating are recorded as a specification, '
         'not described as a colour.'),
    ]
    p.append('<section class="belt-sec"><span class="belt-kicker">From our own visits</span>'
             '<h2>What the workshops and markets actually look like</h2>'
             '<p class="sec-sub">These photographs are from our own sourcing trips in China. They show '
             'processes we check — fabric selection, printing, packing, sampling — rather than a '
             'styled product shot. Each caption states what is visible in the frame.</p>')
    p.append(photo_grid(wall))
    p.append('<p class="strip-note">We do not publish factory names, supplier identities or customer '
             'identifiers on this site. Photographs are illustrative of working processes, not of a '
             'specific named supplier.</p></section>')

    # 桥接 products.html（慢慢替代）
    p.append('<section class="belt-sec"><h2>Still want to browse examples?</h2>'
             '<p class="sec-sub">These cluster guides are the reference layer. If you want to see the '
             'kinds of categories we handle, the older product page is still available.</p>'
             '<div class="bridge"><div class="tx"><h3>Capability samples, not a price list</h3>'
             '<p>The items on the product page illustrate categories, weights and typical minimums. '
             'They are not purchasable stock, and prices there are examples rather than a live catalogue. '
             'We are adding cluster guides gradually and keeping both available while we do.</p></div>'
             '<a class="btn" href="/products.html">Browse capability samples →</a></div></section>')

    # FAQ
    p.append('<section class="belt-sec"><span class="belt-kicker">FAQ</span>'
             '<h2>Common questions</h2><div>%s</div></section>' % faq_html(HUB_FAQ))

    p.append('<section class="belt-sec">%s</section>' % cta_band(
        'Start from a specification, not a price list',
        'Send a photo, a link or a written specification plus your destination market. We confirm the '
        'cluster, the sampling route and the compliance questions before any production is discussed.'))

    p.append('</div>')
    return '\n'.join(p)


def hub_ld():
    item_list = []
    for i, b in enumerate(BELTS):
        item_list.append({
            '@type': 'ListItem', 'position': i + 1,
            'name': '%s — %s' % (b['city'], b['category']),
            'url': BASE + '/belts/' + b['slug'] + '.html',
        })
    all_photos = [b['photos'][0] for b in BELTS]
    wall = [
        ('images/market-variety.jpg', 'Wholesale market aisle with stacked seasonal goods',
         'A wholesale market aisle in China, photographed on a sourcing trip.'),
        ('images/apparel/apparel-fabriccards.jpg', 'Hands selecting fabric swatch cards',
         'Selecting physical fabric swatch cards before a specification is written.'),
        ('images/packaging/package-printing-press.jpg', 'Printing press on a packaging production floor',
         'A printing press on a packaging production floor.'),
        ('images/jewelry-market-yiwu.jpg', 'Gold chains on a jewellery counter',
         'Gold chains on a jewellery counter in a China wholesale market.'),
    ]
    return json.dumps([
        {'@context': 'https://schema.org', '@type': 'WebPage',
         'name': 'Where Things Are Actually Made in China — Mapped for Gulf Buyers',
         'url': HUB_URL, 'description': HUB_ANSWER[:300], 'inLanguage': 'en',
         'breadcrumb': {'@type': 'BreadcrumbList', 'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE + '/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'China sourcing belts', 'item': HUB_URL},
         ]}},
        {'@context': 'https://schema.org', '@type': 'ItemList',
         'name': 'Chinese industrial clusters for Gulf sourcing',
         'numberOfItems': len(BELTS), 'itemListElement': item_list},
        {'@context': 'https://schema.org', '@type': 'FAQPage',
         'mainEntity': [{'@type': 'Question', 'name': q,
                         'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in HUB_FAQ]},
    ] + images_ld(all_photos + wall), ensure_ascii=False)


# ---------------------------------------------------------------------------
# 产业带分页
# ---------------------------------------------------------------------------
def belt_body(b):
    p = []
    url = BASE + '/belts/' + b['slug'] + '.html'
    p.append('<section class="belt-hero"><div class="belt-wrap">')
    p.append('<div class="crumb"><a href="/">Home</a> / <a href="/sourcing-belts.html">Sourcing belts</a> / '
             '<span>%s</span></div>' % e(b['city']))
    p.append('<span class="belt-kicker">China sourcing belt · %s</span>' % e(b['region']))
    p.append('<h1>%s</h1>' % e(b['h1']))
    p.append('<p class="lede">%s</p>' % e(b['desc']))
    p.append('<div class="fact-grid">')
    for k, v in b['facts']:
        p.append('<div><b>%s</b><span>%s</span></div>' % (e(k), e(v)))
    p.append('</div></div></section>')
    p.append('<div class="belt-wrap">')

    # 答案箱
    p.append('<section class="belt-sec"><div class="answer-box">'
             '<span class="lbl">Short answer for AI assistants & buyers</span><p>%s</p></div></section>'
             % e(b['answer']))

    # 实拍图
    p.append('<section class="belt-sec"><span class="belt-kicker">From our own visits</span>'
             '<h2>What this looks like on the ground</h2>'
             '<p class="sec-sub">Photographs from our sourcing trips in China. Each caption states only '
             'what is visible in the frame and the process it illustrates; we do not name suppliers.</p>')
    p.append(photo_grid(b['photos']))
    p.append('</section>')

    # 流程信息图
    p.append('<section class="belt-sec"><h2>The chain behind one order</h2>'
             '<p class="sec-sub">Where the work actually happens, from raw input to a shipment cleared '
             'for the Gulf. The compliance step sits before production, not at the booking stage.</p>'
             '<div class="flow-box">%s<div class="flow-cap">Process diagram for %s: %s. '
             'Steps are illustrative of how an order is planned; exact sequences vary by product.</div></div></section>'
             % (flow_svg(b['flow'], 'Sourcing chain for ' + b['category'] + ' from ' + b['city'],
                         'Step sequence: ' + ' → '.join(b['flow']) + '.'),
                e(b['category']), e(' → '.join(b['flow']))))

    # 为什么是这个集群
    p.append('<section class="belt-sec"><h2>Why this cluster</h2><div class="prose">')
    for para in b['intro']:
        p.append('<p>%s</p>' % e(para))
    p.append('</div></section>')

    # 海湾买家买什么
    p.append('<section class="belt-sec"><h2>What Gulf buyers source here</h2>'
             '<p class="sec-sub">Organised by season and buying occasion rather than by SKU.</p>'
             '<table class="belt-table"><thead><tr><th>Window / use</th><th>What is typically ordered</th></tr></thead><tbody>')
    for k, v in b['buys']:
        p.append('<tr><td>%s</td><td>%s</td></tr>' % (e(k), e(v)))
    p.append('</tbody></table></section>')

    # 合规
    p.append('<section class="belt-sec"><h2>Labelling, certification and paperwork</h2>'
             '<p class="sec-sub">Requirements depend on the exact product and destination. These are the '
             'questions we close before production, not after a batch is made.</p><ul class="check-list">')
    for c in b['compliance']:
        p.append('<li>%s</li>' % e(c))
    p.append('</ul></section>')

    # 常见坑
    p.append('<section class="belt-sec"><h2>Five things that cost a season</h2>'
             '<p class="sec-sub">Concrete failure modes we check for, and the control that prevents each one.</p>'
             '<div class="pit-grid">')
    for i, (t, d) in enumerate(b['pitfalls']):
        p.append('<div class="pit"><span class="num">%d</span><b>%s</b><p>%s</p></div>' % (i + 1, e(t), e(d)))
    p.append('</div></section>')

    # 适合谁
    fits = [x for x in BUYER_TYPES if x['slug'] in b['perfect_for']]
    p.append('<section class="belt-sec"><h2>Who this cluster fits</h2>'
             '<p class="sec-sub">Follow your buyer profile back to the hub for the full picture.</p>'
             '<div class="rel-grid">')
    for f in fits:
        p.append('<a href="/sourcing-belts.html#buyer-%s">%s<small>%s</small></a>'
                 % (f['slug'], e(f['name']), e(f['local'])))
    p.append('</div></section>')

    # 不接什么
    p.append('<section class="belt-sec excl"><h2>Limits on the work we take on</h2>'
             '<div class="excl-grid">')
    for t, d in EXCLUSIONS[:4]:
        p.append('<div class="excl-item"><b>%s</b><p>%s</p></div>' % (e(t), e(d)))
    p.append('</div><p class="strip-note"><a href="/sourcing-belts.html#exclusions">'
             'See the full list of exclusions on the sourcing belts hub →</a></p></section>')

    # FAQ
    p.append('<section class="belt-sec"><span class="belt-kicker">FAQ</span><h2>Common questions</h2>'
             '<div>%s</div></section>' % faq_html(b['faq']))

    # 相关
    p.append('<section class="belt-sec"><h2>Other clusters Gulf buyers combine with this one</h2>'
             '<div class="rel-grid">')
    for s in b['related']:
        x = next(y for y in BELTS if y['slug'] == s)
        p.append('<a href="/belts/%s.html">%s<small>%s</small></a>'
                 % (s, e(x['city']), e(x['category'])))
    p.append('</div><p class="strip-note"><a href="/sourcing-belts.html">'
             '← Back to all eight sourcing belts</a></p></section>')

    p.append('<section class="belt-sec">%s</section>' % cta_band(
        'Have a specification for %s?' % b['category'],
        'Send the photo, material, quantity and destination. We confirm the sampling route, the factory '
        'minimums for each private-label element, and the applicable compliance path before production.'))

    p.append('</div>')
    return '\n'.join(p)


def belt_ld(b):
    url = BASE + '/belts/' + b['slug'] + '.html'
    return json.dumps([
        {'@context': 'https://schema.org', '@type': 'WebPage',
         'name': b['h1'], 'url': url, 'description': b['desc'], 'inLanguage': 'en',
         'breadcrumb': {'@type': 'BreadcrumbList', 'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE + '/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'China sourcing belts', 'item': HUB_URL},
             {'@type': 'ListItem', 'position': 3, 'name': b['city'], 'item': url},
         ]}},
        {'@context': 'https://schema.org', '@type': 'FAQPage',
         'mainEntity': [{'@type': 'Question', 'name': q,
                         'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in b['faq']]},
    ] + images_ld(b['photos']), ensure_ascii=False)


# ---------------------------------------------------------------------------
# 阿语 hub（SSR，dir=rtl，hreflang 双向，JSON-LD inLanguage: ar）
# ---------------------------------------------------------------------------
AR_BELTS = [
    ('شانتو · تشاويانغ', 'ملابس النوم والمنزل', 'shantou-chaoyang-sleepwear'),
    ('قوانغتشو', 'الأزياء النسائية والأزياء المحتشمة', 'guangzhou-womenswear'),
    ('شيشي وجينجيانغ، فوجيان', 'الملابس الرياضية والكاجوال', 'fujian-sportswear'),
    ('شينزين · شويبي', 'المجوهرات والفضة', 'shenzhen-jewellery'),
    ('دونغقوان وشينزين', 'التغليف والطباعة حسب الطلب', 'dongguan-packaging'),
    ('فوشان · ليكونغ', 'الأثاث وتجهيز المشاريع', 'foshan-furniture'),
    ('تشونغشان · قوتشن', 'الإضاءة والإضاءة الزخرفية', 'zhongshan-lighting'),
    ('شينزين ودونغقوان', 'الإلكترونيات والأجهزة الاستهلاكية', 'shenzhen-electronics'),
]
AR_BUYERS = [
    ('بائعو التجارة الاجتماعية', 'إنستغرام · تيك توك · واتساب · سلة / زد'),
    ('متاجر الأزياء المحتشمة والعبايات', 'الرياض · جدة · دبي · الدوحة · الكويت'),
    ('تجار الجملة والأسواق وإعادة التصدير', 'ديرة · دراجون مارت · مناطق الجملة'),
    ('مؤسسو العلامات والملصقات الخاصة', 'العطور · البخور · العناية · نمط الحياة'),
    ('مشترو الضيافة والمشاريع والتجهيزات', 'الفنادق · المطاعم · العيادات · المساحات التجارية'),
    ('الهدايا المؤسسية والموسمية', 'رمضان · العيد · اليوم الوطني · الجمعة البيضاء'),
]
AR_EXCL = [
    ('الشحن المباشر بالقطعة الواحدة',
     'لا نتولّى الشحن المباشر بطرد واحد من الصين إلى المستهلك النهائي في دول الخليج، '
     'ما لم تكن البضاعة مخزّنة أصلاً داخل دول مجلس التعاون.'),
    ('التخصيص لقطعة واحدة',
     'تخضع طلبات الملصق الخاص للحد الأدنى لكل عنصر: الملصق المنسوج، ملصق العناية، '
     'البطاقة والعلبة، ولكل منها حدّه الخاص.'),
    ('البضائع المقلّدة والمحظورة',
     'البضائع المقلّدة أو المعتدية على العلامات، والبضائع غير القانونية أو المحظورة، '
     'والمواد الخطرة مثل العبوات الهوائية (UN1950).'),
    ('غياب مسار الامتثال',
     'الفئات التي تتطلب شهادة إلزامية (مثل ECAS أو SABER للأجهزة الكهربائية) '
     'دون مسار امتثال قابل للإكمال قبل الشحن.'),
    ('الاستفسار عن السعر فقط',
     'نعمل من مواصفة مكتوبة — صورة، مادة، كمية ووجهة — وليس من طلب أقل سعر لمنتج غير محدّد.'),
]
AR_FAQ = [
    ('لماذا ننظّم التوريد حسب التجمّعات الصناعية بدلاً من المنتج؟',
     'لأن التصنيع في الصين يتركّز في عدد محدود من التجمّعات على مستوى المدن، لكل منها مواده وعملياته '
     'ومتطلبات امتثاله. البحث حسب التجمّع يخبر المشتري بما يمكن أخذ عيّنة منه وتعديله وإعادة طلبه فعلياً.'),
    ('ما أهم التجمّعات للمشترين في الخليج؟',
     'ثمانية تجمّعات: شانتو تشاويانغ لملابس النوم، قوانغتشو للأزياء النسائية والمحتشمة، '
     'فوجيان للملابس الرياضية، شينزين شويبي للمجوهرات، دونغقوان وشينزين للتغليف، '
     'فوشان ليكونغ للأثاث، تشونغشان قوتشن للإضاءة، وشينزين ودونغقوان للإلكترونيات.'),
    ('هل تنشرون catalogue أسعار للمنتجات؟',
     'لا. نحن شريك توريد ولسنا بائع تجزئة، ولا نحتفظ بمخزون ولا ننشر قائمة أسعار قابلة للشراء. '
     'يبدأ العمل من صورة أو رابط أو مواصفة، ثم يُعدّ عرض مكتوب لذلك الطلب تحديداً.'),
    ('هل تتعاملون مع تجار الشحن المباشر (dropshipping)؟',
     'لا. الشحن المباشر بطرد واحد من الصين إلى المستهلك النهائي في دول الخليج، دون بضاعة مخزّنة '
     'داخل الخليج، خارج نطاق عملنا. كذلك لا نتولّى التخصيص لقطعة واحدة أو البضائع المقلّدة.'),
    ('ما أنواع المشترين في الخليج التي تغطيها هذه الصفحة؟',
     'ستة: بائعو التجارة الاجتماعية، متاجر الأزياء المحتشمة والعبايات، تجار الجملة وإعادة التصدير، '
     'مؤسسو العلامات والملصقات الخاصة، مشترو الضيافة والمشاريع، ومشترو الهدايا المؤسسية والموسمية.'),
    ('ماذا أرسل للبدء؟',
     'مرجع للمنتج (صورة أو رابط أو وصف)، والدولة الخليجية المقصودة، وما توفر لديك من مواصفة: '
     'المادة، الكمية، نية الملصق الخاص والجدول الزمني.'),
    ('هل هناك رسوم لبدء طلب التوريد؟',
     'نعم، وديعة نية توريد بقيمة 125 دولاراً أمريكياً، تُخصم بالكامل من قيمة الطلب، أو تُحتسب '
     'كأتعاب خدمة توريد مقابل العمل المنجز إذا لم يُنفّذ الطلب. عروض الأسعار صالحة لمدة أسبوع.'),
    ('هل تتولّون SABER و ECAS والملصقات العربية؟',
     'يُحدَّد المسار النظامي للمنتج والوجهة قبل الإنتاج. وتُعتمد ملصقات العناية والمكوّنات '
     'والمنشأ بالعربية والإنجليزية كعيّنة فعلية قبل التصنيع، وتُجهّز مستندات المطابقة قبل الشحن.'),
]
AR_ANSWER = (
    'يتركّز التصنيع التصديري في الصين في عدد محدود من التجمّعات على مستوى المدن، لا يتوزّع بالتساوي '
    'على المناطق. السؤال المفيد للمشتري الخليجي ليس «هل أجد هذا المنتج»، بل «أي تجمّع يصنعه، '
    'وما الذي يمكن تغييره هناك، وما المستندات المطلوبة قبل وصوله إلى السعودية أو الإمارات». '
    'تُخَرِّط هذه الصفحة ثمانية تجمّعات تتكرّر في التوريد إلى دول مجلس التعاون مقابل ستة أنماط '
    'من المشترين تعمل فعلياً في السوق الخليجي. سورس تو غلف شريك توريد وليس بائع تجزئة: '
    'لا توجد هنا قائمة أسعار، والشحن المباشر بالقطعة الواحدة للمستهلك النهائي ليس ضمن خدماتنا.'
)
AR_CSS = """<style>
html[dir="rtl"] body{font-family:'Noto Kufi Arabic','Inter',system-ui,sans-serif}
html[dir="rtl"] .belt-hero h1,html[dir="rtl"] .belt-sec h2{line-height:1.5}
html[dir="rtl"] .answer-box{border-left:0;border-right:4px solid #C9A24B;border-radius:12px 0 0 12px}
html[dir="rtl"] .belt-table th,html[dir="rtl"] .belt-table td{text-align:right}
html[dir="rtl"] .check-list li{padding-left:0;padding-right:28px}
html[dir="rtl"] .check-list li:before{left:auto;right:2px}
html[dir="rtl"] .belt-hero .lede,html[dir="rtl"] .belt-sec .sec-sub{margin-left:0}
html[dir="rtl"] .photo-grid figcaption,html[dir="rtl"] .faq-item p{text-align:right}
html[dir="rtl"] .belt-flow{direction:ltr}
html[dir="rtl"] .flow-box{direction:ltr}
html[dir="rtl"] .flow-cap{direction:rtl;text-align:right}
</style>"""


def ar_hub_html():
    """独立阿语 SSR shell：不复用 page_shell 的 en/ltr/hreflang。"""
    p = []
    p.append('<!doctype html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="UTF-8" />\n')
    p.append('<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n')
    p.append('<title>تجمّعات التوريد في الصين للمشترين في الخليج | SourceToGulf</title>\n')
    p.append('<meta name="description" content="%s" />\n' % e(AR_ANSWER[:280]))
    p.append('<link rel="canonical" href="%s" />\n' % AR_HUB_URL)
    p.append('<link rel="alternate" hreflang="ar" href="%s" />\n' % AR_HUB_URL)
    p.append('<link rel="alternate" hreflang="en" href="%s" />\n' % HUB_URL)
    p.append('<link rel="alternate" hreflang="x-default" href="%s" />\n' % HUB_URL)
    p.append('<link rel="icon" href="/favicon.ico" sizes="any">\n')
    p.append('<link rel="apple-touch-icon" href="/images/logo/logo-icon-512.png">\n')
    p.append('<link rel="preconnect" href="https://fonts.googleapis.com">\n')
    p.append('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Kufi+Arabic:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n')
    p.append('<style>%s</style>\n' % STYLE)
    p.append(GA4_SNIPPET + RSS_LINK + PAGE_CSS + AR_CSS)
    p.append('</head>\n<body>\n<header>\n' + HEADER + '\n</header>\n')

    p.append('<section class="belt-hero"><div class="belt-wrap">')
    p.append('<div class="crumb"><a href="/ar/">الرئيسية</a> / <span>تجمّعات التوريد في الصين</span></div>')
    p.append('<span class="belt-kicker">خريطة التوريد · الصين ← الخليج</span>')
    p.append('<h1>أين تُصنَّع البضائع فعلياً في الصين — دليل للمشتري الخليجي</h1>')
    p.append('<p class="lede">ثمانية تجمّعات صناعية، وستة أنماط من المشترين في الخليج، '
             'وأسئلة الامتثال التي تحدّد وصول الطلب إلى الرفّ. دون قوائم منتجات أو أسعار.</p>')
    p.append('<div class="fact-grid">')
    for k, v in [('التجمّعات', '8 تجمّعات على مستوى المدن'), ('أنماط المشترين', '6 ملفات خليجية'),
                 ('الأسواق', 'الإمارات · السعودية · قطر · عُمان · البحرين · الكويت'),
                 ('ما نحن عليه', 'شريك توريد، لا بائع تجزئة')]:
        p.append('<div><b>%s</b><span>%s</span></div>' % (e(k), e(v)))
    p.append('</div></div></section><div class="belt-wrap">')

    p.append('<section class="belt-sec"><div class="answer-box">'
             '<span class="lbl">إجابة مختصرة للمساعدات الذكية والمشترين</span><p>%s</p></div></section>'
             % e(AR_ANSWER))

    p.append('<section class="belt-sec"><span class="belt-kicker">ابدأ من نوع المشتري</span>'
             '<h2>ستة أنماط من المشترين في الخليج</h2>'
             '<p class="sec-sub">ليس في السوق الخليجي نمط واحد. البائع عبر إنستغرام، وتاجر الجملة '
             'الذي يعمل بجدول إعادة طلب، وفريق تجهيز فندقي يعمل بقائمة كميات، يحتاج كل منهم '
             'إلى حوار أول مختلف.</p><div class="buyer-grid">')
    for name, local in AR_BUYERS:
        p.append('<div class="buyer-card"><div class="ic">%s</div><h3>%s</h3>'
                 '<div class="local">%s</div></div>' % (icon_svg('boxes'), e(name), e(local)))
    p.append('</div></section>')

    p.append('<section class="belt-sec"><span class="belt-kicker">التجمّعات الثمانية</span>'
             '<h2>ثمانية تجمّعات صينية تتكرّر في التوريد إلى الخليج</h2>'
             '<p class="sec-sub">كل بطاقة تفتح دليلاً كاملاً بالإنجليزية: ما يصنعه التجمّع، '
             'ما يطلبه المشترون الخليجيون حسب الموسم، متطلبات الملصقات والشهادات، '
             'وخمسة أخطاء تُكلّف موسماً كاملاً.</p><div class="belt-cards">')
    for i, (city, cat, slug) in enumerate(AR_BELTS):
        b = next(x for x in BELTS if x['slug'] == slug)
        p.append('<div class="belt-card"><a class="img" href="/belts/%s.html">'
                 '<img src="/%s" alt="%s" loading="lazy"></a><div class="bd">'
                 '<div class="city">%02d · %s</div><h3><a href="/belts/%s.html">%s</a></h3>'
                 '<p class="meta">%s</p></div></div>'
                 % (slug, b['photos'][0][0], e(b['photos'][0][1]), i + 1, e(city), slug, e(cat),
                    e(b['facts'][0][1])))
    p.append('</div></section>')

    p.append('<section class="belt-sec excl"><span class="belt-kicker">اقرأ هذا قبل الاستفسار</span>'
             '<h2>ما لا نتولّاه</h2><p class="sec-sub">نوضّح هذا مقدّماً توفيراً لوقت الطرفين. '
             'هذه حدود نطاق العمل، لا أحكام على المشتري.</p><div class="excl-grid">')
    for t, d in AR_EXCL:
        p.append('<div class="excl-item"><b>%s</b><p>%s</p></div>' % (e(t), e(d)))
    p.append('</div></section>')

    p.append('<section class="belt-sec"><span class="belt-kicker">الأسئلة الشائعة</span>'
             '<h2>أسئلة متكرّرة</h2><div>')
    for q, a in AR_FAQ:
        p.append('<div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (e(q), e(a)))
    p.append('</div></section>')

    p.append('<section class="belt-sec"><div class="cta-band"><h2>ابدأ من مواصفة، لا من قائمة أسعار</h2>'
             '<p>أرسل صورة أو رابطاً أو مواصفة مكتوبة مع السوق المقصودة. نؤكّد التجمّع ومسار '
             'العينات وأسئلة الامتثال قبل أي حديث عن الإنتاج.</p>'
             '<a class="wa-btn" href="https://wa.me/971585854194" target="_blank" rel="noopener">'
             '💬 أرسل صورة أو مواصفة</a>'
             '<span class="alt">يراجع شخصٌ كل طلب قبل بدء العمل. '
             '<a href="/services/sourcing-request.html">صفحة طلب التوريد</a> و'
             '<a href="/order-intent.json">العقد المقروء آلياً</a> يبيّنان الحقول المطلوبة.</span>'
             '</div></section>')
    p.append('</div>')

    p.append('<footer>\n' + FOOTER + '\n</footer>\n')
    p.append('<a class="float-wa" href="https://wa.me/971585854194" target="_blank" rel="noopener" aria-label="WhatsApp">💬</a>\n'
             '<button id="toTop" aria-label="Back to top">↑</button>\n')
    p.append('<script>%s</script>\n' % MINI_JS)
    p.append('<script src="/fx.js" defer></script>\n')
    # 阿语页：强制 ar/rtl，语言按钮切回英文 hub
    p.append('''<script>
window.addEventListener('load',function(){
  try{localStorage.setItem('stg-lang','ar');}catch(err){}
  window.lang='ar';
  if(typeof applyLang==='function'){applyLang();}
  document.documentElement.lang='ar';document.documentElement.dir='rtl';
  document.querySelectorAll('.lang-btn').forEach(function(b){b.textContent='English';});
  window.toggleLang=function(){window.location.href='%s';};
});
</script>''' % HUB_URL)
    ld = json.dumps([
        {'@context': 'https://schema.org', '@type': 'WebPage',
         'name': 'أين تُصنَّع البضائع فعلياً في الصين — دليل للمشتري الخليجي',
         'url': AR_HUB_URL, 'description': AR_ANSWER[:300], 'inLanguage': 'ar',
         'breadcrumb': {'@type': 'BreadcrumbList', 'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': 'الرئيسية', 'item': BASE + '/ar/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'تجمّعات التوريد', 'item': AR_HUB_URL},
         ]}},
        {'@context': 'https://schema.org', '@type': 'FAQPage',
         'mainEntity': [{'@type': 'Question', 'name': q,
                         'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in AR_FAQ]},
    ], ensure_ascii=False)
    p.append('<script type="application/ld+json">\n%s\n</script>\n' % ld)
    p.append('</body>\n</html>')
    return ''.join(p)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('  ✓', os.path.relpath(path, APP))


def main():
    print('build_belts.py — 产业带 hub + 8 分页 + 阿语 hub')

    # hub（英文）—— alt_ar 指向 SSR 阿语页，hreflang 双向
    html = page_shell(
        'Where Things Are Actually Made in China — Mapped for Gulf Buyers | SourceToGulf',
        'Eight Chinese industrial clusters mapped against six Gulf buyer types: what each cluster makes, '
        'seasonal demand, labelling and certification watchpoints, and explicit scope limits. '
        'No product list, no price list.',
        HUB_URL, hub_body(), json_ld=hub_ld(),
        extra_head=PAGE_CSS + LANG_SCRIPT.replace('__AR__', AR_HUB_URL),
        alt_ar=AR_HUB_URL)
    write(os.path.join(APP, 'sourcing-belts.html'), html)

    # 8 个分页
    for b in BELTS:
        url = BASE + '/belts/' + b['slug'] + '.html'
        html = page_shell(b['title'], b['desc'], url, belt_body(b), json_ld=belt_ld(b),
                          extra_head=PAGE_CSS + LANG_SCRIPT.replace('__AR__', AR_HUB_URL))
        write(os.path.join(BELT_DIR, b['slug'] + '.html'), html)

    # 阿语 hub（SSR）
    write(os.path.join(AR_DIR, 'sourcing-belts.html'), ar_hub_html())
    print('完成：%d 个产业带分页 + hub + 阿语 hub' % len(BELTS))


if __name__ == '__main__':
    main()
