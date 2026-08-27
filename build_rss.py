# -*- coding: utf-8 -*-
"""
build_rss.py — 生成 rss.xml（P3 修复：原本线上 404，从未生成）
汇总站内的「文章/指南/对比页/品类页/人设页」为合法 RSS 2.0，
提供给 Google / Bing / 阅读器 / AI 引擎作为「内容新鲜度」信号。

用法: python3 build_rss.py
输出: rss.xml（部署即被 https://sourcetogulf.com/rss.xml 访问）
"""
import os, re
from email.utils import formatdate
from time import mktime
from datetime import datetime

APP = os.path.dirname(os.path.abspath(__file__))
BASE = "https://sourcetogulf.com"

# 纳入 feed 的页面（相对 app 根目录）。跳过 index/listing 页。
INCLUDE = [
    # 博客文章
    "blog/how-to-find-a-reliable-sourcing-agent-in-china.html",
    "blog/how-to-import-from-china-to-uae.html",
    "blog/how-to-import-from-china-to-saudi-arabia.html",
    "blog/how-to-import-from-china-to-kuwait.html",
    "blog/how-to-import-from-china-to-qatar.html",
    "blog/how-to-import-from-china-to-bahrain.html",
    "blog/how-to-import-from-china-to-oman.html",
    "blog/landed-cost-china-to-gulf-explained.html",
    "blog/sourcing-for-livestream-sellers-gulf.html",
    "blog/saber-2026-saudi-buyers-playbook.html",
    "blog/china-gcc-fta-lower-import-duty.html",
    "blog/source-products-tiktok-shop-saudi-no-container.html",
    "blog/white-friday-2026-china-gulf-small-business.html",
    "blog/skincare-private-label-china-to-saudi-uae.html",
    "blog/gulf-trends-2026-china-sourcing.html",
    "blog/sample-to-container-delivery-journey.html",
    # GCC 指南（根目录）
    "uae-import-guide-from-china.html",
    "saudi-arabia-import-guide-from-china.html",
    "kuwait-import-guide-from-china.html",
    "qatar-import-guide-from-china.html",
    "bahrain-import-guide-from-china.html",
    "oman-import-guide-from-china.html",
    # 对比深度页
    "sourcing-agent-vs-trading-company.html",
    "yiwu-vs-guangzhou-vs-shenzhen.html",
    "alibaba-vs-sourcing-agent.html",
    "composite-partner-vs-single-vendors.html",
    # 品类页
    "category-home-fragrance.html",
    "category-seasonal.html",
    "category-fashion.html",
    "category-tech.html",
    "category-home.html",
    "category-beauty-toys.html",
    # 人设落地页（P2）
    "for-influencers.html",
    "for-small-businesses.html",
    "for-moms.html",
    "for-resellers.html",
    # 核心页
    "products.html",
    "solutions.html",
    "gcc-import-answers.html",
    "about.html",
]

def extract(path):
    full = os.path.join(APP, path)
    if not os.path.exists(full):
        return None
    html = open(full, encoding='utf-8', errors='ignore').read()
    m = re.search(r'<title>([^<]+)</title>', html)
    title = m.group(1).strip() if m else path
    d = re.search(r'<meta name="description" content="([^"]*)"', html)
    desc = d.group(1).strip() if d else ''
    c = re.search(r'<link rel="canonical" href="([^"]*)"', html)
    link = c.group(1).strip() if c else BASE + '/' + path
    # pubDate: 文件 mtime
    mt = os.path.getmtime(full)
    pub = formatdate(mktime(datetime.fromtimestamp(mt).timetuple()), localtime=False)
    return {'title': title, 'desc': desc, 'link': link, 'pub': pub}

def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))

def build():
    items = []
    for p in INCLUDE:
        e = extract(p)
        if e:
            items.append(
                '    <item>\n'
                '      <title>%s</title>\n'
                '      <link>%s</link>\n'
                '      <guid isPermaLink="true">%s</guid>\n'
                '      <description>%s</description>\n'
                '      <pubDate>%s</pubDate>\n'
                '    </item>' % (
                    esc(e['title']), esc(e['link']), esc(e['link']),
                    esc(e['desc']), e['pub']))
    now = formatdate(None, localtime=False)
    rss = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        '  <channel>\n'
        '    <title>SourceToGulf — China Sourcing for the Gulf</title>\n'
        '    <link>%s</link>\n' % BASE +
        '    <atom:link href="%s/rss.xml" rel="self" type="application/rss+xml" />\n' % BASE +
        '    <description>China→Gulf sourcing: import guides, landed-cost explainers, '
        'product comparisons and buyer solutions for the UAE, Saudi Arabia, Qatar and beyond.</description>\n'
        '    <language>en</language>\n'
        '    <lastBuildDate>%s</lastBuildDate>\n' % now +
        '    <generator>build_rss.py</generator>\n'
        '    <docs>https://blogs.law.harvard.edu/tech/rss</docs>\n'
        + '\n'.join(items) + '\n'
        '  </channel>\n'
        '</rss>\n'
    )
    out = os.path.join(APP, 'rss.xml')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(rss)
    print('wrote rss.xml — %d items, %d bytes' % (len(items), len(rss)))

if __name__ == '__main__':
    build()
