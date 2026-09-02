#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync <style>, <header>, <footer> and favicon links from products.html to all other HTML pages."""
import os, re

APP = "/Users/jingjinggu/Desktop/sourcetogulf/Kimi_Agent_货盘供货商定位/app"
SRC = os.path.join(APP, "products.html")

def extract(tag, html):
    m = re.search(rf"<{tag}[\s\S]*?</{tag}>", html)
    return m.group(0) if m else None

def replace_tag(tag, html, new):
    pattern = rf"<{tag}[\s\S]*?</{tag}>"
    return re.sub(pattern, new, html, count=1)

src_html = open(SRC, encoding="utf-8").read()
style_new = extract("style", src_html)
header_new = extract("header", src_html)
footer_new = extract("footer", src_html)

favicon_block = '  <link rel="icon" href="/favicon.ico" sizes="any">\n  <link rel="apple-touch-icon" href="/images/logo/logo-icon-512.png">\n'

files = []
for root, dirs, fnames in os.walk(APP):
    dirs[:] = [d for d in dirs if d not in {".git", "node_modules"}]
    for f in fnames:
        if f.endswith(".html"):
            files.append(os.path.join(root, f))

changed = []
for path in files:
    html = open(path, encoding="utf-8").read()
    orig = html
    # favicon: insert after last hreflang or canonical if not present
    if "favicon.ico" not in html:
        m = re.search(r'<link rel="alternate" hreflang="x-default"[^>]+>\n', html)
        if m:
            html = html[:m.end()] + favicon_block + html[m.end():]
        else:
            m2 = re.search(r'<link rel="canonical"[^>]+>\n', html)
            if m2:
                html = html[:m2.end()] + favicon_block + html[m2.end():]
    if style_new and re.search(r"<style>", html):
        html = replace_tag("style", html, style_new)
    if header_new and re.search(r"<header>", html):
        html = replace_tag("header", html, header_new)
    if footer_new and re.search(r"<footer>", html):
        html = replace_tag("footer", html, footer_new)
    if html != orig:
        open(path, "w", encoding="utf-8").write(html)
        changed.append(os.path.relpath(path, APP))

print(f"Updated {len(changed)} files")
for p in changed[:20]:
    print("  -", p)
if len(changed) > 20:
    print(f"  ... and {len(changed)-20} more")
