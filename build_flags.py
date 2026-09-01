# -*- coding: utf-8 -*-
"""
build_flags.py — 用内联 SVG 国旗替换全站的国旗 emoji（方案 A）

============================================================================
为什么需要（2026-09-01 诊断）
----------------------------------------------------------------------------
国旗 emoji 是「区域指示符（regional indicator）组合」。**Windows 的
Segoe UI Emoji 刻意不含国旗字形**（微软为避免地区争议的长期政策），因此：
  • macOS / iOS / Android：正常显示
  • Windows（Chrome / Edge / Firefox）：降级为两位字母码
    🇦🇪 → "AE"，🇸🇦 → "SA"
  • 首页原 h1 的 🇨🇳→🇦🇪🇸🇦🇰🇼🇶🇦🇧🇭🇴🇲 会变成 "CN→AESAKWQABHOM"
    —— 七个字母码连成一串，完全无法阅读。

中东 B2B 买家办公多用 Windows，此问题影响实质。

方案 A：内联 SVG（symbol sprite）
  • 100% 跨平台一致，不依赖任何系统字体
  • symbol 定义一次，全站 <use> 引用，不增加 HTTP 请求
  • 尺寸用 em 单位，自动跟随字号

============================================================================
实现方式（关键：只改单一真相源，不逐个文件改）
----------------------------------------------------------------------------
导航与页脚的国旗 emoji 都存在于 products.html 的 <header> / <footer> 中，
而这两个块会被 tpl_common.py 抽取后注入所有生成页，并由
sync_header_footer.py 同步到手工页。因此**只需改 products.html 的
header + footer**，再跑 build + sync，全站 73 个文件自动同步。

用法: python3 build_flags.py
============================================================================
"""
import os, re

APP = os.path.dirname(os.path.abspath(__file__))
PRODUCTS = os.path.join(APP, 'products.html')

# ---------------------------------------------------------------------------
# 7 面简化国旗（viewBox 0 0 24 16，3:2）
# 小尺寸（约 1.2em）下保留可辨识的核心特征；沙特的铭文、阿曼国徽等细节省略。
# ---------------------------------------------------------------------------
FLAGS = {
    'cn': ('China', '<rect width="24" height="16" fill="#DE2910"/>'
                    '<path d="M5 3l.9 2.1 2.3.2-1.8 1.5.6 2.2L5 7.7 3 9l.6-2.2L1.8 5.3l2.3-.2z" fill="#FFDE00"/>'),
    'ae': ('United Arab Emirates',
           '<rect width="24" height="16" fill="#fff"/>'
           '<rect width="6" height="16" fill="#CE1126"/>'
           '<rect x="6" width="18" height="5.34" fill="#009739"/>'
           '<rect x="6" y="10.66" width="18" height="5.34" fill="#000"/>'),
    'sa': ('Saudi Arabia',
           '<rect width="24" height="16" fill="#006C35"/>'
           '<rect x="6" y="7.2" width="13" height="1.6" fill="#fff"/>'
           '<circle cx="5.2" cy="8" r="1.1" fill="#fff"/>'),
    'kw': ('Kuwait',
           '<rect width="24" height="5.34" fill="#007A3D"/>'
           '<rect y="5.33" width="24" height="5.34" fill="#fff"/>'
           '<rect y="10.66" width="24" height="5.34" fill="#C8102E"/>'
           '<polygon points="0,0 7,4 7,12 0,16" fill="#000"/>'),
    'qa': ('Qatar',
           '<rect width="24" height="16" fill="#fff"/>'
           '<path d="M0,0 L9,0 L7.2,0.89 L9,1.78 L7.2,2.67 L9,3.56 L7.2,4.44 L9,5.33 '
           'L7.2,6.22 L9,7.11 L7.2,8 L9,8.89 L7.2,9.78 L9,10.67 L7.2,11.56 L9,12.44 '
           'L7.2,13.33 L9,14.22 L7.2,15.11 L9,16 L0,16 Z" fill="#8A1538"/>'),
    'bh': ('Bahrain',
           '<rect width="24" height="16" fill="#fff"/>'
           '<path d="M0,0 L7,0 L5.2,1.6 L7,3.2 L5.2,4.8 L7,6.4 L5.2,8 L7,9.6 '
           'L5.2,11.2 L7,12.8 L5.2,14.4 L7,16 L0,16 Z" fill="#CE1126"/>'),
    'om': ('Oman',
           '<rect width="24" height="16" fill="#fff"/>'
           '<rect y="5.33" width="24" height="5.34" fill="#C8102E"/>'
           '<rect y="10.66" width="24" height="5.34" fill="#009739"/>'
           '<rect width="6" height="16" fill="#C8102E"/>'),
}

def _flag_emoji(code):
    """由 ISO 3166-1 双字母码生成国旗 emoji（区域指示符组合）。

    区域指示符 A = U+1F1E6，按字母顺序递增。
    手写码点极易出错（曾把 AE 误写为 CA），故统一用函数生成。
    """
    return ''.join(chr(0x1F1E6 + ord(c.upper()) - ord('A')) for c in code)


# emoji → symbol id
EMOJI_MAP = {
    _flag_emoji('AE'): 'ae',
    _flag_emoji('CN'): 'cn',
    _flag_emoji('SA'): 'sa',
    _flag_emoji('KW'): 'kw',
    _flag_emoji('QA'): 'qa',
    _flag_emoji('BH'): 'bh',
    _flag_emoji('OM'): 'om',
}

SPRITE = (
    '<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true" '
    'focusable="false">\n'
    + ''.join(
        '<symbol id="f-%s" viewBox="0 0 24 16"><title>%s</title>%s</symbol>\n' % (k, v[0], v[1])
        for k, v in FLAGS.items())
    + '</svg>'
)

FLAG_CSS = (
    '/* ===== inline SVG flags (replace flag emoji — Windows cannot render them) ===== */\n'
    '.flag{width:1.2em;height:.8em;display:inline-block;vertical-align:-.12em;'
    'border-radius:2px;flex-shrink:0;box-shadow:0 0 0 .5px rgba(0,0,0,.14)}'
)


def use_tag(key):
    name = FLAGS[key][0]
    return '<svg class="flag" aria-hidden="true" focusable="false"><use href="#f-%s"/></svg>' % key


def sweep_all():
    """扫描全站 HTML，处理 header/footer 同步不到的残留 emoji。

    两种情况需区别对待：
    1) `<option>` 内 —— HTML 规范规定 <option> 只允许文本内容，不能放 SVG。
       首页落地成本计算器的国家下拉即属此类，直接删除 emoji，保留文字。
    2) 其余位置 —— 替换为内联 SVG <use> 引用。
    """
    def em(code):
        return _flag_emoji(code)

    codes = ['AE', 'CN', 'SA', 'KW', 'QA', 'BH', 'OM']
    emojis = {em(c): c.lower() for c in codes}

    changed_files = 0
    removed_in_option = 0
    replaced_svg = 0

    for root, dirs, fnames in os.walk(APP):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules'}]
        for f in fnames:
            if not f.endswith('.html'):
                continue
            p = os.path.join(root, f)
            try:
                h = open(p, encoding='utf-8').read()
            except Exception:
                continue
            orig = h

            # 1) <option> 内的 emoji：删除（规范不允许放 SVG）
            for e in emojis:
                # 形如 <option value="AE">🇦🇪 UAE ...</option>
                h_new = re.sub(r'(<option[^>]*>)\s*' + re.escape(e) + r'\s*', r'\1', h)
                if h_new != h:
                    removed_in_option += h.count(e) - h_new.count(e)
                    h = h_new

            # 2) 其余位置：替换为 SVG
            for e, key in emojis.items():
                n = h.count(e)
                if n:
                    h = h.replace(e, use_tag(key))
                    replaced_svg += n

            if h != orig:
                open(p, 'w', encoding='utf-8').write(h)
                changed_files += 1

    print('✓ sweep: 更新 %d 个文件' % changed_files)
    print('    替换 SVG: %d 处' % replaced_svg)
    print('    <option> 内删除（规范不允许 SVG）: %d 处' % removed_in_option)


def main():
    html = open(PRODUCTS, encoding='utf-8').read()
    orig = html

    # 1) 注入 sprite（放在 <header> 内最前，随 header 同步到全站）
    if 'id="f-ae"' not in html:
        html = html.replace('<header>', '<header>\n' + SPRITE, 1)

    # 2) 注入 CSS（放在 </style> 前）
    if '.flag{' not in html:
        html = html.replace('</style>', FLAG_CSS + '\n</style>', 1)

    # 3) 把 emoji 替换为 <use> 引用
    replaced = 0
    for emoji, key in EMOJI_MAP.items():
        n = html.count(emoji)
        if n:
            html = html.replace(emoji, use_tag(key))
            replaced += n
            print('  %s → #f-%s  (%d 处)' % (emoji, key, n))

    if html != orig:
        open(PRODUCTS, 'w', encoding='utf-8').write(html)
        print('✓ products.html 已更新，共替换 %d 处国旗 emoji' % replaced)
    else:
        print('= products.html 无需改动（可能已替换过）')

    # 报告剩余 emoji
    left = sum(html.count(e) for e in EMOJI_MAP)
    print('  剩余国旗 emoji: %d' % left)

    # 处理 header/footer 同步不到��残留（手工页 body 内的 emoji）
    sweep_all()


if __name__ == '__main__':
    main()
