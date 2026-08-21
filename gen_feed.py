# -*- coding: utf-8 -*-
"""
gen_feed.py — 生成 RSS 2.0 feed.xml（低成本 SEO 增益）
汇总博客指南 + 新品类页，输出标准 RSS，供订阅与聚合。
用法: python3 gen_feed.py
"""
import os, re, glob
from datetime import datetime, timezone
from xml.sax.saxutils import escape

APP = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://sourcetogulf.com'

def grab_meta(html):
    title = re.search(r'<title>([^<]*)</title>', html)
    desc = re.search(r'<meta name="description" content="([^"]*)"', html)
    return (title.group(1).strip() if title else ''), (desc.group(1).strip() if desc else '')

# 各页面最后更新日期（与 sitemap 对齐）
LASTMOD = {
    'blog/how-to-import-from-china-to-uae.html': '2026-08-21',
    'blog/how-to-import-from-china-to-saudi-arabia.html': '2026-08-21',
    'blog/how-to-import-from-china-to-kuwait.html': '2026-08-21',
    'blog/how-to-import-from-china-to-qatar.html': '2026-08-21',
    'blog/how-to-import-from-china-to-bahrain.html': '2026-08-21',
    'blog/how-to-import-from-china-to-oman.html': '2026-08-21',
    'blog/how-to-find-a-reliable-sourcing-agent-in-china.html': '2026-08-19',
    'blog/landed-cost-china-to-gulf-explained.html': '2026-08-19',
    'blog/sourcing-for-livestream-sellers-gulf.html': '2026-08-19',
    'products.html': '2026-08-21',
    'categories.html': '2026-08-21',
    'category-home-fragrance.html': '2026-08-21',
    'category-seasonal.html': '2026-08-21',
    'category-fashion.html': '2026-08-21',
    'category-tech.html': '2026-08-21',
    'category-home.html': '2026-08-21',
    'category-beauty-toys.html': '2026-08-21',
    'uae-import-guide-from-china.html': '2026-08-21',
    'saudi-arabia-import-guide-from-china.html': '2026-08-21',
    'qatar-import-guide-from-china.html': '2026-08-21',
    'kuwait-import-guide-from-china.html': '2026-08-21',
    'bahrain-import-guide-from-china.html': '2026-08-21',
    'oman-import-guide-from-china.html': '2026-08-21',
    'sourcing-agent-vs-trading-company.html': '2026-08-21',
    'yiwu-vs-guangzhou-vs-shenzhen.html': '2026-08-21',
}

def rfc822(d):
    return datetime.strptime(d, '%Y-%m-%d').replace(tzinfo=timezone.utc).strftime('%a, %d %b %Y 00:00:00 +0000')

items = []

# 博客指南
for fn in sorted(glob.glob(os.path.join(APP, 'blog', '*.html'))):
    name = os.path.basename(fn)
    if name == 'index.html':
        continue
    html = open(fn, encoding='utf-8').read()
    t, d = grab_meta(html)
    if not t:
        continue
    items.append({
        'title': t,
        'link': '%s/blog/%s' % (BASE, name),
        'desc': d or t,
        'date': LASTMOD.get('blog/' + name, '2026-08-19'),
    })

# 品类页 + 产品页
for name in ['products.html', 'categories.html',
             'category-home-fragrance.html', 'category-seasonal.html',
             'category-fashion.html', 'category-tech.html',
             'category-home.html', 'category-beauty-toys.html']:
    fn = os.path.join(APP, name)
    if not os.path.exists(fn):
        continue
    html = open(fn, encoding='utf-8').read()
    t, d = grab_meta(html)
    if not t:
        continue
    items.append({
        'title': t,
        'link': '%s/%s' % (BASE, name),
        'desc': d or t,
        'date': LASTMOD.get(name, '2026-08-21'),
    })

# 国家级进口支柱页（GEO 权威长文）
for name in sorted(glob.glob(os.path.join(APP, '*-import-guide-*.html'))):
    name = os.path.basename(name)
    fn = os.path.join(APP, name)
    html = open(fn, encoding='utf-8').read()
    t, d = grab_meta(html)
    if not t:
        continue
    items.append({
        'title': t,
        'link': '%s/%s' % (BASE, name),
        'desc': d or t,
        'date': LASTMOD.get(name, '2026-08-21'),
    })

# 横向对比评测页（GEO 高价值内容）
for name in ['sourcing-agent-vs-trading-company.html', 'yiwu-vs-guangzhou-vs-shenzhen.html']:
    fn = os.path.join(APP, name)
    if not os.path.exists(fn):
        continue
    html = open(fn, encoding='utf-8').read()
    t, d = grab_meta(html)
    if not t:
        continue
    items.append({
        'title': t,
        'link': '%s/%s' % (BASE, name),
        'desc': d or t,
        'date': LASTMOD.get(name, '2026-08-21'),
    })

# 按日期倒序
items.sort(key=lambda x: x['date'], reverse=True)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
lines.append('  <channel>')
lines.append('    <title>SourceToGulf — China Sourcing for the Gulf</title>')
lines.append('    <link>%s</link>' % BASE)
lines.append('    <description>New product picks, category updates and import guides for sourcing from China to the UAE, Saudi Arabia, Kuwait, Qatar, Bahrain and Oman.</description>')
lines.append('    <language>en</language>')
lines.append('    <lastBuildDate>%s</lastBuildDate>' % rfc822('2026-08-21'))
lines.append('    <atom:link href="%s/feed.xml" rel="self" type="application/rss+xml" />' % BASE)
for it in items:
    lines.append('    <item>')
    lines.append('      <title>%s</title>' % escape(it['title']))
    lines.append('      <link>%s</link>' % escape(it['link']))
    lines.append('      <guid isPermaLink="true">%s</guid>' % escape(it['link']))
    lines.append('      <description>%s</description>' % escape(it['desc']))
    lines.append('      <pubDate>%s</pubDate>' % rfc822(it['date']))
    lines.append('    </item>')
lines.append('  </channel>')
lines.append('</rss>')

with open(os.path.join(APP, 'feed.xml'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print('✓ feed.xml generated with %d items' % len(items))
