# -*- coding: utf-8 -*-
"""
tpl_common.py — 共享站点模板与工具
从 products.html 抽取 <style>/<header>/<footer>，供品类页/分群页/问答页/广告页复用，
保证全站视觉与双语导航一致。同时提供到岸价计算与最小多语切换脚本。

========================================================================
GEO 内容生成铁律（2026 实战手册，所有 build_*.py 必须遵守）
------------------------------------------------------------------------
1. 答案前置：正文前 200 字必须把主问题一句话答完，不铺垫、不抖包袱。
2. 事实密度：多堆权威数字 / 统计 / 具体金额 / 百分比 / 年份；关键词堆砌对 AI
   无效甚至扣分。目标 fact density ≥ 3 个信号 / 100 词。
3. 客观口吻：删掉 "we believe / I think / our team / we are confident" 这类
   主观词（抬高模型 perplexity，更不易被引用），写成百科式陈述句。
4. 模块化：H2/H3 直接照抄用户在 ChatGPT 里的原话问法，每块 200–400 字自成
   完整答案，并配 FAQPage JSON-LD 直接喂成引用候选。
5. SSR 优先：所有关键文本必须进原始 HTML（page_shell 已保证），绝不靠
   客户端 JS 注入正文 / FAQ / 价格表。
6. 老三样是入场券：title / viewport / canonical 必须存在且为 https。
========================================================================
"""
import re, os

# 内容质量自检清单（供 build 脚本与 geo_diag.py 引用）
SUBJECTIVE_BANNED = ["we believe", "i think", "we think", "our team", "we feel",
                     "in our opinion", "we are proud", "we are confident",
                     "our mission", "we strive"]


APP = os.path.dirname(os.path.abspath(__file__))

def _read(p):
    with open(os.path.join(APP, p), encoding='utf-8') as f:
        return f.read()

_PRODUCTS_HTML = _read('products.html')

# 抽取 <style> 块（products.html 只有一个）
STYLE = re.search(r'<style>([\s\S]*?)</style>', _PRODUCTS_HTML).group(1)
# 抽取 <header> ... </header>
HEADER = re.search(r'<header>([\s\S]*?)</header>', _PRODUCTS_HTML).group(1)
# 抽取 <footer> ... </footer>
FOOTER = re.search(r'<footer>([\s\S]*?)</footer>', _PRODUCTS_HTML).group(1)

CNY_TO_USD = 7.15
def cainiao_ship_usd(kg):
    cny = 68.0 if kg <= 0.5 else 68.0 + (kg - 0.5) * 45.6
    return cny / CNY_TO_USD
def price_of(p):
    fob = p['fob_cny'] / CNY_TO_USD
    ship_per_unit = cainiao_ship_usd(p['moq'] * p['weight_kg']) / p['moq']
    return {'fob': fob, 'landed': fob + ship_per_unit}

# 生成页面用的最小脚本（仅多语切换 + 移动菜单 + 回到顶部，不依赖 products-data.js）
MINI_JS = """
var lang = localStorage.getItem('stg-lang') || ((navigator.language||'').indexOf('ar')===0 ? 'ar':'en');
function applyLang(){
  document.documentElement.lang = lang;
  document.documentElement.dir = (lang==='ar') ? 'rtl' : 'ltr';
  document.querySelectorAll('.lang-btn').forEach(function(b){ b.textContent = (lang==='ar') ? 'English' : 'العربية'; });
  document.querySelectorAll('[data-en]').forEach(function(el){
    var v = el.getAttribute('data-'+lang);
    if(v!==null) el.innerHTML = v;
  });
}
function toggleLang(){ lang = (lang==='en')?'ar':'en'; localStorage.setItem('stg-lang',lang); applyLang(); }
function toggleMenu(){ var m=document.getElementById('mpanel'); if(m) m.classList.toggle('open'); }
document.addEventListener('DOMContentLoaded', function(){
  applyLang();
  var toTop = document.getElementById('toTop');
  if(toTop){
    window.addEventListener('scroll', function(){ toTop.classList.toggle('show', window.scrollY > 700); }, {passive:true});
    toTop.onclick = function(){ window.scrollTo({top:0, behavior:'smooth'}); };
  }
});
"""

# 浮动 WhatsApp + 回到顶部按钮（位于 footer 之后）
FLOAT_BTN = '<a class="float-wa" href="https://wa.me/971585146139" target="_blank" rel="noopener" aria-label="WhatsApp">💬</a>\n<button id="toTop" aria-label="Back to top">↑</button>'

WA = '971585146139'

# Google Analytics 4 衡量代码（全站统一注入；重跑生成器不会丢失）
GA4_ID = 'G-76L0Y9SC5D'
GA4_SNIPPET = (
    '<!-- Google tag (gtag.js) GA4 -->\n'
    '<script async src="https://www.googletagmanager.com/gtag/js?id=' + GA4_ID + '"></script>\n'
    '<script>\n'
    '  window.dataLayer = window.dataLayer || [];\n'
    '  function gtag(){dataLayer.push(arguments);}\n'
    '  gtag(\'js\', new Date());\n'
    '  gtag(\'config\', \'' + GA4_ID + '\');\n'
    '</script>\n'
)

def wa_link(text):
    """生成 WhatsApp 深链（已 encode）"""
    from urllib.parse import quote
    return 'https://wa.me/%s?text=%s' % (WA, quote(text))

def product_card(p):
    """生成一张静态产品卡（含到岸价），供品类页使用。"""
    pr = price_of(p)
    hot = '<span class="hot-badge">HOT</span>' if p.get('hot') else ''
    wa_text = ('Hi SourceToGulf! I am interested in: ' + p['name_en'] +
               ' (MOQ ' + str(p['moq']) + ' pcs). Please confirm price and availability.')
    return ('<div class="pcard">'
        + hot
        + '<div class="imgbox"><img src="' + p['img'] + '" alt="' + p['name_en'] + '" loading="lazy" onerror="this.parentElement.classList.add(\'bad\')"></div>'
        + '<div class="pbody">'
        + '<h3>' + p['name_en'] + '</h3>'
        + '<div class="price-row">'
        + '<div class="planded"><small>Landed to UAE</small><b>$' + ('%.2f' % pr['landed']) + '</b> <i>/pc at MOQ</i></div>'
        + '<div class="pfob"><small>Factory price</small><span>$' + ('%.2f' % pr['fob']) + '</span></div>'
        + '</div>'
        + '<div class="pmeta">MOQ ' + str(p['moq']) + ' pcs &middot; ships in ' + str(p['lead_days']) + ' days</div>'
        + '<a class="wa-mini" href="' + wa_link(wa_text) + '" target="_blank" rel="noopener">💬 Ask about this</a>'
        + '</div></div>')

def page_shell(title, description, canonical, body_inner, json_ld=None, extra_head=''):
    """组装一个完整 HTML 页面。"""
    ld = ''
    if json_ld:
        ld = '<script type="application/ld+json">\n' + json_ld + '\n</script>'
    return ('<!doctype html>\n'
        '<html lang="en" dir="ltr">\n'
        '<head>\n'
        '<meta charset="UTF-8" />\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
        '<title>' + title + '</title>\n'
        '<meta name="description" content="' + description + '" />\n'
        '<link rel="canonical" href="' + canonical + '" />\n'
        '<link rel="alternate" hreflang="en" href="' + canonical + '" />\n'
        '<link rel="alternate" hreflang="x-default" href="' + canonical + '" />\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Kufi+Arabic:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n'
        '<style>' + STYLE + '</style>\n'
        + GA4_SNIPPET
        + extra_head +
        '</head>\n'
        '<body>\n'
        + '<header>\n' + HEADER + '\n</header>\n'
        + body_inner + '\n'
        + '<footer>\n' + FOOTER + '\n</footer>\n'
        + FLOAT_BTN + '\n'
        '<script>' + MINI_JS + '</script>\n'
        '<script src="/fx.js" defer></script>\n'
        + ld + '\n'
        '</body>\n'
        '</html>')

if __name__ == '__main__':
    print('STYLE len:', len(STYLE))
    print('HEADER len:', len(HEADER))
    print('FOOTER len:', len(FOOTER))
