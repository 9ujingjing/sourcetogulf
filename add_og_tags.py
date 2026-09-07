#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_og_tags.py — 给手工页（不被 build_*.py 生成的）注入 Open Graph + Twitter Card meta。

幂等：已含 og:image 的页面跳过。
原理：从每页自己的 <title> / <meta name="description"> / <link rel="canonical"> 读取，
      生成对应的 og/twitter 块，插在 <meta name="description" /> 行后（与 page_shell 一致）。
"""
import os, re

APP = "/Users/jingjinggu/Desktop/sourcetogulf/Kimi_Agent_货盘供货商定位/app"
OG_IMAGE = "https://sourcetogulf.com/images/og-default.jpg"
OG_SITE = "SourceToGulf"

# 抓取每页元数据（宽松匹配单/双引号）
def grab(html, pattern, group=1):
    m = re.search(pattern, html, re.I | re.S)
    if not m:
        return None
    val = m.group(group).strip()
    return val

def build_og_block(title, description, canonical):
    return (
        f'<meta property="og:title" content="{title}" />\n'
        f'<meta property="og:description" content="{description}" />\n'
        f'<meta property="og:url" content="{canonical}" />\n'
        f'<meta property="og:image" content="{OG_IMAGE}" />\n'
        f'<meta property="og:type" content="website" />\n'
        f'<meta property="og:site_name" content="{OG_SITE}" />\n'
        f'<meta property="og:locale" content="en_US" />\n'
        f'<meta name="twitter:card" content="summary_large_image" />\n'
        f'<meta name="twitter:title" content="{title}" />\n'
        f'<meta name="twitter:description" content="{description}" />\n'
        f'<meta name="twitter:image" content="{OG_IMAGE}" />\n'
    )

files = []
for root, dirs, fnames in os.walk(APP):
    dirs[:] = [d for d in dirs if d not in {".git", "__pycache__"}]
    for f in fnames:
        if f.endswith(".html"):
            files.append(os.path.join(root, f))

changed = []
skipped = []
failed = []

for path in files:
    html = open(path, encoding="utf-8", errors="ignore").read()
    if 'og:image' in html:
        skipped.append(os.path.relpath(path, APP))
        continue
    title = grab(html, r'<title>(.*?)</title>')
    desc  = grab(html, r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']')
    canon = grab(html, r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']')
    if not (title and desc and canon):
        failed.append((os.path.relpath(path, APP), '缺少 title/description/canonical'))
        continue
    block = build_og_block(title, desc, canon)
    # 插在 <meta name="description" ...> 之后（与 page_shell 输出一致）
    # 用宽松匹配：容忍 description 内容里出现撇号/HTML 实体
    new_html, n = re.subn(
        r'(<meta[^>]*\sname=["\']description["\'][^>]*>\s*\n?)',
        r'\1' + block,
        html, count=1
    )
    if n == 0:
        failed.append((os.path.relpath(path, APP), '未找到 description 锚点'))
        continue
    open(path, "w", encoding="utf-8").write(new_html)
    changed.append(os.path.relpath(path, APP))

print(f"已注入: {len(changed)}")
for p in changed[:30]:
    print("  +", p)
if len(changed) > 30:
    print(f"  ... and {len(changed)-30} more")
print(f"\n已含 og:image 跳过: {len(skipped)}")
print(f"\n失败（缺元数据/锚点）: {len(failed)}")
for p, why in failed[:10]:
    print(f"  ! {p}: {why}")
