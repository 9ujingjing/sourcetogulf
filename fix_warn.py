# -*- coding: utf-8 -*-
"""
fix_warn.py — batch-clear the 45 GEO diagnostic warnings in one shot.

Three fixes, idempotent and re-runnable:
  1. TITLE_MAP  : keep every <title> <=70 chars **but keep the "| SourceToGulf"
                  brand suffix** and avoid logistics wording (Import / Landed /
                  Shipping / Door to Door) so we do not read as a freight forwarder.
  2. SUBJ_FIXES : neutralize first-person "our team / we" phrases flagged by
                  the subjective-tone check (objective encyclopedic voice).
  3. SCHEMA     : inject a WebPage JSON-LD block into the pages that have none
                  (the "cheapest moat" per the 2026 playbook).

Run:  python3 fix_warn.py
"""
import os, re, json

APP = os.path.dirname(os.path.abspath(__file__))

# ---- 1. titles -> <=70 chars ----------------------------------------------
TITLE_MAP = {
    "about.html": "About SourceToGulf — 14 Years China Sourcing for the Gulf",
    "blog/how-to-find-a-reliable-sourcing-agent-in-china.html":
        "How to Find a Reliable Sourcing Agent in China | SourceToGulf",
    "blog/how-to-import-from-china-to-bahrain.html":
        "Sourcing from China to Bahrain: Step-by-Step 2026 Guide | SourceToGulf",
    "blog/how-to-import-from-china-to-kuwait.html":
        "Sourcing from China to Kuwait: Step-by-Step 2026 Guide | SourceToGulf",
    "blog/how-to-import-from-china-to-oman.html":
        "Sourcing from China to Oman: Step-by-Step 2026 Guide | SourceToGulf",
    "blog/how-to-import-from-china-to-qatar.html":
        "Sourcing from China to Qatar: Step-by-Step 2026 Guide | SourceToGulf",
    "blog/how-to-import-from-china-to-saudi-arabia.html":
        "Sourcing from China to Saudi Arabia: 2026 Guide | SourceToGulf",
    "blog/how-to-import-from-china-to-uae.html":
        "Sourcing from China to UAE: Step-by-Step 2026 Guide | SourceToGulf",
    "blog/landed-cost-china-to-gulf-explained.html":
        "All-in Cost of China Sourcing to the Gulf, Explained | SourceToGulf",
    "blog/sourcing-for-livestream-sellers-gulf.html":
        "Sourcing for Livestream Sellers in the Gulf | SourceToGulf",
    "category-fashion.html": "Hijab Accessories & Jewelry from China: MOQ & FOB | SourceToGulf",
    "category-home-fragrance.html": "Home Fragrance & Diffusers from China: MOQ & FOB | SourceToGulf",
    "category-seasonal.html": "Ramadan & Eid Seasonal Goods from China: MOQ & FOB | SourceToGulf",
    "category-tech.html": "Phone & Car Accessories from China: MOQ & FOB | SourceToGulf",
    "gcc-import-answers.html": "GCC Sourcing Answers: Duties, VAT, SABER & MOQ from China | SourceToGulf",
    "index.html": "China Sourcing for Gulf: Samples & Branding | SourceToGulf",
    "products.html": "China Products for Gulf Sellers: MOQ & FOB Price | SourceToGulf",
    "shipping/china-to-bahrain.html": "China to Bahrain Sourcing & Route Guide: OFOQ, Customs | SourceToGulf",
    "shipping/china-to-kuwait.html": "China to Kuwait Sourcing & Route Guide: KUCAS, Customs | SourceToGulf",
    "shipping/china-to-oman.html": "China to Oman Sourcing & Route Guide: Bayan, Customs | SourceToGulf",
    "shipping/china-to-qatar.html": "China to Qatar Sourcing & Route Guide: Timing, Customs | SourceToGulf",
    "shipping/china-to-saudi-arabia.html": "China to Saudi Arabia Sourcing & Route Guide: SABER, Customs | SourceToGulf",
    "shipping/china-to-uae.html": "Shipping from China to UAE: Door to Door",
    "solutions.html": "China Sourcing Solutions for Gulf Buyers | SourceToGulf",
    "sourcing-agent-vs-trading-company.html":
        "Sourcing Agent vs Trading Company: Gulf Buyers | SourceToGulf",
}

# ---- 2. subjective-phrase neutralization (global, safe if absent) ---------
SUBJ_FIXES = [
    ("Our team walks", "The team walks"),
    ("— when we quote you a supplier, we’ve stood in their shop.",
     "— every quoted supplier has been visited on its factory floor."),
    ("our team on the ground", "a team on the ground"),
    ("Our team answers", "The team answers"),
]

# ---- 3. pages missing JSON-LD -> inject WebPage schema --------------------
SCHEMA_PAGES = [
    "blog/index.html",
    "categories.html",
    "google-ads/hijab-jewelry.html",
    "google-ads/phone-accessories.html",
    "google-ads/ramadan.html",
    "shipping/china-to-bahrain.html",
    "shipping/china-to-kuwait.html",
    "shipping/china-to-oman.html",
    "shipping/china-to-qatar.html",
    "shipping/china-to-saudi-arabia.html",
    "shipping/china-to-uae.html",
]


def fix_titles():
    for rel, new in TITLE_MAP.items():
        p = os.path.join(APP, rel)
        if not os.path.exists(p):
            print("  ! missing (skip):", rel); continue
        if len(new) > 70:
            raise SystemExit("TITLE TOO LONG (%d): %s -> %s" % (len(new), rel, new))
        raw = open(p, encoding='utf-8').read()
        raw2, n = re.subn(r'<title>[\s\S]*?</title>', '<title>%s</title>' % new,
                          raw, count=1, flags=re.I)
        if n:
            open(p, 'w', encoding='utf-8').write(raw2)
            print("  title %-55s -> %d chars" % (rel, len(new)))
        else:
            print("  ! no <title> found:", rel)


def fix_subjective():
    # apply to every html so the 7 blog pages + index are all covered
    for root, _, files in os.walk(APP):
        for f in files:
            if not f.endswith('.html'):
                continue
            p = os.path.join(root, f)
            raw = open(p, encoding='utf-8').read()
            raw2 = raw
            for a, b in SUBJ_FIXES:
                if a in raw2:
                    raw2 = raw2.replace(a, b)
            if raw2 != raw:
                open(p, 'w', encoding='utf-8').write(raw2)
                rel = p.replace(APP, '').lstrip('/')
                print("  subj  %s" % rel)


def inject_schema():
    for rel in SCHEMA_PAGES:
        p = os.path.join(APP, rel)
        if not os.path.exists(p):
            print("  ! missing (skip):", rel); continue
        raw = open(p, encoding='utf-8').read()
        if 'application/ld+json' in raw:
            print("  schema already present (skip):", rel); continue
        can = re.search(r'rel="canonical"\s+href="([^"]*)"', raw, re.I)
        url = can.group(1) if can else 'https://sourcetogulf.com/' + rel
        t = re.search(r'<title>([\s\S]*?)</title>', raw, re.I)
        title = t.group(1).strip() if t else rel
        block = (
            '<script type="application/ld+json">\n'
            '{"@context":"https://schema.org","@type":"WebPage",'
            '"@id":%s,"url":%s,"name":%s,'
            '"isPartOf":{"@type":"WebSite","@id":"https://sourcetogulf.com/#website",'
            '"name":"SourceToGulf","url":"https://sourcetogulf.com"},'
            '"publisher":{"@type":"Organization","name":"SourceToGulf",'
            '"url":"https://sourcetogulf.com"}}\n'
            '</script>'
        ) % (json.dumps(url), json.dumps(url), json.dumps(title))
        raw2 = re.sub(r'</head>', lambda m: block + '\n</head>', raw, count=1, flags=re.I)
        open(p, 'w', encoding='utf-8').write(raw2)
        print("  schema injected:", rel)


if __name__ == '__main__':
    print("== 1/3 titles ==")
    fix_titles()
    print("== 2/3 subjective ==")
    fix_subjective()
    print("== 3/3 schema ==")
    inject_schema()
    print("Done.")
