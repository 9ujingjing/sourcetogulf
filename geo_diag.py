# -*- coding: utf-8 -*-
"""
geo_diag.py — SourceToGulf Technical SEO / GEO Diagnostic
=========================================================
Run once, use forever. Scans every HTML page + site-level files and scores
GEO-readiness against the 2026 playbook:

  1. SSR      — main text MUST live in raw HTML, not client JS. If a crawler
                sees a blank page, everything else is worth zero.
  2. robots   — AI bots (GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot,
                Bingbot) must be allowed.
  3. Meta     — title / viewport / canonical / https (the "entry tickets").
  4. Schema   — JSON-LD present (FAQPage / WebPage / etc.). Cheapest moat.
  5. Fact     — fact density proxy ($ / % / years / numbers per 100 words).
  6. Tone     — subjective filler ("we believe", "I think") raises perplexity.
  7. Answer   — first ~200 chars of body text (manual review of answer-first).
  8. Markdown — clean semantic HTML (div depth vs semantic-tag ratio).

Usage:
    python3 geo_diag.py [app_dir]

Outputs geo_diag_report.md next to this script and prints a summary.
"""
import os, re, sys, json, html as _html

APP = os.path.dirname(os.path.abspath(__file__)) if len(sys.argv) < 2 else os.path.abspath(sys.argv[1])

# ---- AI crawlers that must NOT be blocked -------------------------------
AI_BOTS = ["GPTBot", "ClaudeBot", "PerplexityBot", "OAI-SearchBot", "Bingbot", "Googlebot"]

SUBJ = ["we believe", "i think", "we think", "our team", "we feel", "in our opinion",
        "we are proud", "we are confident", "our mission", "we strive"]
FACT_RE = re.compile(r'(\$\s?\d[\d,.]*|\d+(?:\.\d+)?\s?%|20\d{2}|19\d{2}|\b\d{2,}(?:\.\d+)?\b)')
TAG_RE = re.compile(r'<([a-zA-Z][a-zA-Z0-9]*)', re.I)
SCRIPT_RE = re.compile(r'<script[\s\S]*?</script>', re.I)
STYLE_RE = re.compile(r'<style[\s\S]*?</style>', re.I)
COMMENT_RE = re.compile(r'<!--[\s\S]*?-->')
HEAD_RE = re.compile(r'<head[\s\S]*?</head>', re.I)
META_TAG_RE = re.compile(r'<meta\b[^>]*>', re.I)
EXTERNAL_DATA = ["products-data.js", "extract_products.js", "products.clean.json"]

def visible_text(html):
    h = re.sub(HEAD_RE, '', html)  # drop head (nav/title noise for answer-first)
    h = re.sub(SCRIPT_RE, ' ', h)
    h = re.sub(STYLE_RE, ' ', h)
    h = re.sub(COMMENT_RE, ' ', h)
    h = re.sub(r'<[^>]+>', ' ', h)
    h = _html.unescape(h)
    h = re.sub(r'\s+', ' ', h).strip()
    return h

def count_words(t):
    return len(re.findall(r"[A-Za-z0-9']+", t))

def max_div_depth(html):
    depth = 0; mx = 0
    for m in re.finditer(r'<(/?div)\b', html, re.I):
        if m.group(1).startswith('/'):
            depth = max(0, depth - 1)
        else:
            depth += 1; mx = max(mx, depth)
    return mx

def parse_robots(path):
    allowed, blocked = {}, {}
    cur = None
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        k, v = k.strip().lower(), v.strip()
        if k == 'user-agent':
            cur = v
        elif k == 'disallow' and v:
            blocked.setdefault(cur, []).append(v)
        elif k == 'allow' and v:
            allowed.setdefault(cur, []).append(v)
    return allowed, blocked

def check():
    pages = []
    for root, _, files in os.walk(APP):
        # skip blog/index and similar? no, scan all html
        for f in files:
            if f.endswith('.html'):
                pages.append(os.path.join(root, f))
    pages.sort()

    rep = []
    rep.append("# SourceToGulf — GEO / Technical SEO Diagnostic\n")
    rep.append("Scanned: %d HTML pages under `%s`\n" % (len(pages), APP))

    fails = []
    warns = []

    per_page = []
    for p in pages:
        raw = open(p, encoding='utf-8').read()
        size = len(raw)
        vt = visible_text(raw)
        vlen = len(vt)
        rel = p.replace(APP, '').lstrip('/')
        words = count_words(vt)
        ratio = vlen / size if size else 0

        # meta
        title = re.search(r'<title>([\s\S]*?)</title>', raw, re.I)
        title_txt = title.group(1).strip() if title else ''
        has_viewport = 'name="viewport"' in raw.lower()
        can = re.search(r'rel="canonical"\s+href="([^"]*)"', raw, re.I)
        can_url = can.group(1) if can else ''
        has_https_can = can_url.startswith('https://')
        mixed = len(re.findall(r'http://sourcetogulf\.com', raw))  # mixed content risk

        # ssr risk: a page is truly blank to a crawler only when raw HTML holds
        # almost no visible words. A heavy inline <style> block skews a byte-ratio
        # metric, so we judge by visible-word count of the script/style-stripped text.
        uses_ext_data = any(x in raw for x in EXTERNAL_DATA)
        if words < 120:
            fails.append("%s: SSR FAIL — only %d words of visible text in raw HTML (crawler sees blank)%s" % (
                rel, words, " + loads external data JS" if uses_ext_data else ""))
        elif words < 250:
            warns.append("%s: thin — only %d visible words (consider expanding)" % (rel, words))

        # schema
        lds = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', raw, re.I)
        types = []
        for block in lds:
            try:
                obj = json.loads(block)
                def walk(o):
                    if isinstance(o, dict):
                        if '@type' in o:
                            t = o['@type']
                            types.append(t if isinstance(t, str) else ','.join(t))
                        for v in o.values():
                            walk(v)
                    elif isinstance(o, list):
                        for v in o:
                            walk(v)
                walk(obj)
            except Exception:
                pass
        has_schema = bool(types)

        # fact density
        facts = len(FACT_RE.findall(vt))
        fact_density = (facts / words * 100) if words else 0

        # subjective
        low = vt.lower()
        subj_hits = sum(low.count(s) for s in SUBJ)

        # semantic vs div
        depth = max_div_depth(raw)
        tags = TAG_RE.findall(raw)
        div_n = sum(1 for t in tags if t.lower() == 'div')
        sem_n = sum(1 for t in tags if t.lower() in
                    ('h1','h2','h3','h4','p','ul','ol','li','table','section','article','main','blockquote'))
        sem_ratio = sem_n / div_n if div_n else 0

        # answer-first snippet (first 200 chars of body text after head stripped)
        idx = vt.find(' ', 60)
        snippet = vt[:200]

        pp = {
            'page': rel, 'words': words, 'text_ratio': round(ratio*100, 1),
            'title_len': len(title_txt), 'has_viewport': has_viewport,
            'canonical': can_url, 'has_https_can': has_https_can, 'mixed': mixed,
            'uses_ext_data': uses_ext_data, 'schema': types,
            'fact_density': round(fact_density, 1), 'subj': subj_hits,
            'div_depth': depth, 'sem_ratio': round(sem_ratio, 2),
            'snippet': snippet,
        }
        per_page.append(pp)

        # meta checks -> fails/warns
        if not title_txt:
            fails.append("%s: missing <title>" % rel)
        elif not (10 <= len(title_txt) <= 70):
            warns.append("%s: title length %d (ideal 10-70)" % (rel, len(title_txt)))
        if not has_viewport:
            fails.append("%s: missing viewport meta" % rel)
        if not can_url:
            fails.append("%s: missing canonical" % rel)
        elif not has_https_can:
            fails.append("%s: canonical not https" % rel)
        if mixed:
            warns.append("%s: %d http:// mixed-content links" % (rel, mixed))
        if not has_schema:
            warns.append("%s: no JSON-LD schema" % rel)
        if uses_ext_data and words < 250:
            warns.append("%s: loads external data JS — ensure core content also present in raw HTML" % rel)
        if subj_hits:
            warns.append("%s: %d subjective phrases (raise model perplexity)" % (rel, subj_hits))

    # ---- site level ----
    rep.append("\n## Site-level\n")
    # robots
    robots_path = os.path.join(APP, 'robots.txt')
    if os.path.exists(robots_path):
        allowed, blocked = parse_robots(robots_path)
        rep.append("### robots.txt — AI bot allow/disallow\n")
        for bot in AI_BOTS:
            dis = blocked.get(bot, [])
            if dis:
                fails.append("robots.txt: %s DISALLOWED (%s) — blocked from AI discovery!" % (bot, dis))
                rep.append("- ❌ **%s**: disallowed %s" % (bot, dis))
            else:
                rep.append("- ✅ %s: allowed" % bot)
        rep.append("")
    else:
        fails.append("robots.txt MISSING")
        rep.append("- ❌ robots.txt missing")

    # sitemap
    sm_path = os.path.join(APP, 'sitemap.xml')
    if os.path.exists(sm_path):
        sm = open(sm_path, encoding='utf-8').read()
        urls = re.findall(r'<loc>([^<]+)</loc>', sm)
        nonhttps = [u for u in urls if not u.startswith('https://')]
        rep.append("### sitemap.xml — %d URLs" % len(urls))
        if nonhttps:
            fails.append("sitemap: %d non-https <loc>" % len(nonhttps))
        rep.append("- Bing submission: **ACTION NEEDED** — ChatGPT live search is Bing-driven. Submit %s to Bing Webmaster Tools (manual, needs account)." % "https://sourcetogulf.com/sitemap.xml")
        rep.append("")

    # llms
    for f in ('llms.txt', 'llms-full.txt'):
        if os.path.exists(os.path.join(APP, f)):
            rep.append("- ✅ %s present" % f)
        else:
            warns.append("%s missing" % f)

    # ---- per-page table ----
    rep.append("\n## Per-page\n")
    rep.append("| Page | Words | Text% | Title | Viewport | Canonical(https) | Schema | Fact/100w | Subj | DivDepth | Sem/Div |")
    rep.append("|------|-------|-------|-------|----------|------------------|--------|-----------|------|----------|----------|")
    for pp in per_page:
        rep.append("| %s | %d | %.1f%% | %d | %s | %s | %s | %.1f | %d | %d | %.2f |" % (
            pp['page'], pp['words'], pp['text_ratio'], pp['title_len'],
            '✅' if pp['has_viewport'] else '❌',
            '✅' if pp['has_https_can'] else '❌',
            ','.join(pp['schema']) if pp['schema'] else '—',
            pp['fact_density'], pp['subj'], pp['div_depth'], pp['sem_ratio']))
    rep.append("")

    # answer-first snippets (manual review)
    rep.append("\n## Answer-first review (first ~200 chars of body text)\n")
    rep.append("_Per the playbook, the opening must answer the question directly. Spot-check below._\n")
    for pp in per_page:
        rep.append("**%s** (%.1f%% / %d words)\n> %s\n" % (pp['page'], pp['text_ratio'], pp['words'], pp['snippet']))

    # ---- verdict ----
    rep.append("\n## Verdict\n")
    rep.append("❌ FAILS (%d):" % len(fails))
    for f in fails:
        rep.append("  - " + f)
    rep.append("⚠️ WARNINGS (%d):" % len(warns))
    for w in warns:
        rep.append("  - " + w)
    if not fails and not warns:
        rep.append("  - All clear. 🎉")

    out = "\n".join(rep)
    out_path = os.path.join(APP, 'geo_diag_report.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(out)

    # console summary
    print("Scanned %d pages." % len(pages))
    print("FAILS: %d | WARNINGS: %d" % (len(fails), len(warns)))
    for f in fails:
        print("  ❌", f)
    for w in warns[:25]:
        print("  ⚠️", w)
    if len(warns) > 25:
        print("  ... +%d more warnings" % (len(warns)-25))
    print("Report written: %s" % out_path)
    return fails, warns

if __name__ == '__main__':
    check()
