# -*- coding: utf-8 -*-
"""
build_personas.py — 生成 4 个「买家人设」落地页（P2）
复用 page_shell + STYLE/HEADER/FOOTER，保证全站视觉/导航/GA4/fx.js 一致。

战略定位（2026-08-21 用户明确）：
  我们不跟物流/货代竞争。核心差异化 = 复合能力：
    找货源(sourcing) + 定制包装(custom/private-label packaging)
    + 寄样品(sample shipping) + 小单/低MOQ 代发。
  目标买家人设：网红/KOL、小企业主、宝妈、小卖家/转卖者。

每页结构：
  page-hero → 复合能力(4卡) → 人设痛点→解法(卡片) → How it works(4步)
  → 样例产品(复用 product_card) → 互链 strip → FAQ(FAQPage JSON-LD) → CTA
"""
import json, os
from tpl_common import page_shell, product_card, wa_link

APP = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(APP, 'products.clean.json'), encoding='utf-8'))
PRODS = DATA['prods']

WA_HOME = wa_link("Hi SourceToGulf! I want to start sourcing from China for my business. "
                  "Help me pick the right plan.")

def picks(cat_keys, n=3):
    out, seen = [], set()
    for c in cat_keys:
        for p in PRODS:
            if p['cat'] == c and p['name_en'] not in seen:
                seen.add(p['name_en']); out.append(p)
                if len(out) >= n: return out
    return out

# ---------- 复用人设互链 ----------
PERSONA_LINKS = [
    ("for-influencers.html", "📱 Influencers & KOLs"),
    ("for-small-businesses.html", "🏢 Small Business Owners"),
    ("for-moms.html", "👩 Side-Hustle Moms"),
    ("for-resellers.html", "🛒 Resellers & Small Sellers"),
]

def persona_strip(active):
    cards = []
    for href, label in PERSONA_LINKS:
        cls = 'rel-card' + (' on' if href == active else '')
        cards.append('<a class="rel-card" href="/%s">%s</a>' % (href, label))
    return ('<section><div class="wrap"><div class="sec-head center">'
            '<h2>Which one are you?</h2><p>Four buyer profiles, one sourcing partner. '
            'Pick the path that fits how you sell.</p></div>'
            '<div class="rel-grid">%s</div></div></section>' % ''.join(cards))

# ---------- 复合能力（4 卡，所有页面共用） ----------
COMPOSITE = """
<section><div class="wrap">
  <div class="sec-head center">
    <span class="kicker">One partner, four capabilities</span>
    <h2>Not a freight forwarder — a composite sourcing partner</h2>
    <p><b>We are not a freight forwarder.</b> A forwarder ships cartons you have already
    bought. We do the work that comes first: find the factory, put your brand on the product
    and its packaging, and get physical samples into your hands — so you can test a small
    batch before committing to a container.</p>
  </div>
  <div class="grid2">
    <div class="card"><div class="em">🔎</div><h3>Find the source</h3>
      <p>Send a photo, a link, or a description. We locate the factory, compare quotes,
      and verify the supplier before you commit a dirham.</p></div>
    <div class="card"><div class="em">🎨</div><h3>Custom &amp; private-label packaging</h3>
      <p>Your logo, your colours, your box — at low minimums. Turn a generic item into
      your own branded product line.</p></div>
    <div class="card"><div class="em">📦</div><h3>Ship samples first</h3>
      <p>We send physical samples (and QC photos/videos) so you approve quality before
      any bulk order. No surprises on arrival.</p></div>
    <div class="card"><div class="em">🚪</div><h3>Low MOQ &amp; door-to-door</h3>
      <p>Start with a small batch. We consolidate, clear customs (SABER for KSA) and
      deliver to your door in the UAE, Saudi, Qatar and beyond.</p></div>
  </div>
</div></section>
"""

HOW = """
<section style="background:var(--soft)"><div class="wrap">
  <div class="sec-head center"><h2>How it works</h2>
    <p>Four steps from idea to your door — in English or Arabic, over WhatsApp.</p></div>
  <div class="steps">
    <div class="step"><div class="n">1</div><h3>Tell us what you want</h3>
      <p>Photo, link, or just an idea. We reply with options and a landed-price quote.</p></div>
    <div class="step"><div class="n">2</div><h3>We source &amp; sample</h3>
      <p>We find verified factories, then ship you physical samples to approve.</p></div>
    <div class="step"><div class="n">3</div><h3>You approve &amp; brand</h3>
      <p>Confirm quality, add your logo/packaging, place the batch you're comfortable with.</p></div>
    <div class="step"><div class="n">4</div><h3>We ship to your door</h3>
      <p>QC, consolidation, customs clearance and Gulf delivery — one tracking number.</p></div>
  </div>
</div></section>
"""

def faq_block(qa):
    items = ''.join(
        '<details><summary>%s</summary><div class="a">%s</div></details>' % (q, a)
        for q, a in qa)
    return '<section><div class="wrap narrow"><div class="sec-head"><h2>Frequently asked</h2></div>' \
           '<div class="faq">%s</div></div></section>' % items

def faq_jsonld(qa):
    obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qa
        ]
    }
    return obj

def final_cta():
    return ('<section><div class="wrap"><div class="final">'
            '<h2>Ready to source your first batch?</h2>'
            '<p>WhatsApp us what you want to sell. We\'ll map the right plan and quote a '
            'landed price to your country — free, no obligation.</p>'
            '<a class="wa-btn" href="%s" target="_blank" rel="noopener">'
            '💬 WhatsApp: +971 58 585 4194</a></div></div></section>' % WA_HOME)

# ============================ PERSONAS ============================
PERSONAS = [
{
 "slug": "for-influencers.html",
 "desc": "Gulf creators: turn your audience into your own product line. We source from China, apply your branding and send samples — MOQ from 10 pcs.",
 "title": "Gulf Creators: China Sourcing & Branding | SourceToGulf",
 "h1": "Turn your audience into your own product line",
 "sub": "TikTok KSA, Instagram UAE and livestream creators: launch branded merch from "
        "China with small minimums, samples for content, and fast restocks.",
 "cap": "Influencer & KOL",
 "pain": [
   ("Factories ignore small orders",
    "Most suppliers won't talk to you below a container. We bridge that gap — our volume "
    "lets you order the small batches a creator actually needs."),
   ("You need samples for content",
    "Unboxing and review videos sell. We ship physical samples (and QC clips) so your "
    "content is ready before you ever buy in bulk."),
   ("Viral moments don't wait",
    "Trends move in days. Low MOQ plus fast restock means you can test an item, confirm "
    "it sells, and refill before the wave passes."),
   ("Your brand, not a generic label",
    "Private-label packaging in your colours and logo turns a winning item into YOUR "
    "product — and protects your margin."),
 ],
 "cats": ["fashion", "tech", "beauty-toys"],
 "photo": ("/images/packing.jpg",
           "Jewelry livestream auction run by the SourceToGulf founder — 1,000+ orders shipped, zero returns",
           "Our own livestream selling days: a jewelry auction we ran ourselves — 1,000+ orders shipped, zero returns."),
 "faq": [
   ("Can I order a small quantity as an influencer?",
    "Yes. We aggregate demand so you can start from low MOQs — often a few hundred pieces "
    "across mixed SKUs — instead of a full container."),
   ("Do you send samples before bulk production?",
    "Always. We ship physical samples and QC photos/videos so you can film content and "
    "approve quality before committing to a bulk run."),
   ("Can you put my logo on the products?",
    "Yes. Custom and private-label packaging — boxes, pouches, cards, inserts — at low "
    "minimums, in your brand colours."),
   ("How fast can you restock if an item goes viral?",
    "We keep supplier relationships warm and can usually turn a restock within the same "
    "production window, then air-freight to the Gulf for speed."),
 ],
},
{
 "slug": "for-small-businesses.html",
 "desc": "Gulf small businesses: a verified supply base, QC, custom branding and samples — without hiring a procurement team. One clear price per piece.",
 "title": "Small Gulf Business: China Sourcing & Low MOQ | SourceToGulf",
 "h1": "Your China sourcing department — without the overhead",
 "sub": "Small business owners across the Gulf: get a verified supply base, QC, branding "
        "and door-to-door shipping without hiring a procurement team.",
 "cap": "Small Business Owner",
 "pain": [
   ("No time to vet factories",
    "We shortlist and verify suppliers, compare quotes, and handle the back-and-forth in "
    "Chinese — so you don't burn weeks on Alibaba chats."),
   ("Inconsistent quality hurts repeat sales",
    "Pre-shipment inspection with photo/video proof means what you approve is what arrives, "
    "order after order."),
   ("Cash tied up in inventory",
    "Low MOQs and consolidated shipments let you test demand and reorder based on real "
    "sales, not guesses."),
   ("Customs is a black box",
    "We handle documentation and clearance — including SABER for Saudi-bound goods — and "
    "deliver door to door."),
 ],
 "cats": ["home", "home-fragrance", "seasonal"],
 "faq": [
   ("Do I need to speak Chinese or visit factories?",
    "No. We operate from Guangzhou, negotiate with suppliers, and report to you in English "
    "or Arabic over WhatsApp."),
   ("How do you control quality for a small business?",
    "Every batch gets pre-shipment inspection with photos/videos you can review before we "
    "ship. Samples are sent first for approval."),
   ("Can you handle Saudi customs and SABER?",
    "Yes. We prepare SABER documents and manage clearance so your goods land in the Kingdom "
    "without a customs headache."),
   ("What's the minimum I can start with?",
    "It depends on the product, but we specialise in low-MOQ batches so a small business can "
    "start without a warehouse of cash tied up."),
 ],
},
{
 "slug": "for-moms.html",
 "desc": "Side-hustle moms in the Gulf: launch your own product line with tiny minimums, samples you approve first, and your branding on the packaging.",
 "title": "Home Business: Low-MOQ China Sourcing & Samples | SourceToGulf",
 "h1": "Start a small import business from home",
 "sub": "For side-hustle moms in the Gulf: launch your own product line with tiny minimums, "
        "samples you can see first, and shipping handled to your door.",
 "cap": "Side-Hustle Mom",
 "pain": [
   ("I don't have a big budget",
    "You don't need a container. Low MOQs let you start with a small, affordable test batch "
    "and grow as sales come in."),
   ("I've never imported before",
    "We guide you step by step in plain language — English or Arabic — and handle the factory "
    "talks, QC and shipping for you."),
   ("I want to see it before I buy",
    "We ship physical samples to your door so you know exactly what you're selling before you "
    "commit to a batch."),
   ("Customs and shipping scare me",
    "We clear customs and deliver door to door across the Gulf. You focus on your customers; "
    "we handle the logistics."),
 ],
 "cats": ["home-fragrance", "seasonal", "beauty-toys"],
 "faq": [
   ("I'm a complete beginner — can you help me start?",
    "Absolutely. Many of our buyers start from home with no import experience. Send us an "
    "idea or a photo and we'll guide you through sourcing, samples and shipping."),
   ("What's the smallest order I can place?",
    "We focus on low-MOQ sourcing, so you can begin with a small test batch instead of a "
    "large upfront commitment."),
   ("Will I understand the process in Arabic/English?",
    "Yes. We communicate over WhatsApp in English or Arabic and keep every step clear — no "
    "technical jargon."),
   ("Do you deliver to my home in the Gulf?",
    "Yes. We handle customs clearance and door-to-door delivery to the UAE, Saudi, Qatar, "
    "Kuwait, Bahrain and Oman."),
 ],
},
{
 "slug": "for-resellers.html",
 "desc": "Gulf resellers: low minimums, factory prices and custom branding so your store stands out. Samples before you commit — we are not a freight forwarder.",
 "title": "Gulf Resellers: Low-MOQ Sourcing & Branding | SourceToGulf",
 "h1": "Source trending products to resell — one piece at a time",
 "sub": "Resellers and small sellers in the Gulf: get variety, low minimums, samples and "
        "custom packaging so your store stands out.",
 "cap": "Reseller & Small Seller",
 "pain": [
   ("Containers are out of reach",
    "You sell variety, not pallets of one SKU. We source small batches across many categories "
    "so your catalogue stays fresh."),
   ("You need to see before you list",
    "We ship samples so you can photograph and quality-check every item before it goes live "
    "in your store."),
   ("Your store needs its own look",
    "Custom packaging and private labelling make resold goods feel like your brand — and "
    "justify a higher price."),
   ("Customers want fast delivery",
    "Consolidated Gulf shipping with tracking means you can promise reliable fulfilment "
    "without holding huge stock."),
 ],
 "cats": ["tech", "fashion", "home-fragrance", "beauty-toys"],
 "faq": [
   ("Can I source many different products in one go?",
    "Yes. We consolidate mixed-category small batches from multiple suppliers into one "
    "shipment, saving you freight and customs effort."),
   ("Do you send samples to resellers?",
    "Yes. Samples let you photograph and quality-check items before listing them, so your "
    "store only sells what you've seen."),
   ("Can you add my store's packaging?",
    "Yes. Custom and private-label packaging is available at low minimums so resold products "
    "carry your brand."),
   ("Is this drop-shipping?",
    "We're a sourcing partner, not a drop-shipper. You order low-MOQ batches (with samples "
    "first), and we ship them to you or consolidate for Gulf delivery."),
 ],
},
]

def photo_block(p):
    """可选配图区块（小尺寸 max-width:38rem，用于不显眼但内容相关的位置）。

    仅当画像条目带 'photo' 键时渲染。直播场景照从首页迁至此——首页原为
    全宽 .img-slot（1076px），过于醒目且画质一般，移至内页小图更合适。
    """
    ph = p.get('photo')
    if not ph:
        return ''
    src, alt, cap = ph
    return ('<section style="padding-top:0"><div class="wrap">'
            '<div style="max-width:38rem;margin-inline:auto"><figure style="margin:0">'
            '<img src="%s" alt="%s" loading="lazy" '
            'style="width:100%%;border-radius:14px;object-fit:cover;aspect-ratio:4/3;'
            'border:1px solid #E7E1D4">'
            '<figcaption style="font-size:.85rem;color:#5F6661;margin-top:.45rem">%s</figcaption>'
            '</figure></div></div></section>' % (src, alt, cap))


def render(p):
    cat = p['cats']
    sample = picks(cat, 3)
    sample_html = ''.join(product_card(x) for x in sample)
    pain_cards = ''.join(
        '<div class="card"><div class="em">⚠️</div><h3>%s</h3><p>%s</p></div>' % (t, d)
        for t, d in p['pain'])
    body = (
        '<section class="page-hero"><div class="wrap">'
        '<div class="crumb"><a href="/" data-en="Home" data-ar="الرئيسية">Home</a> ← '
        '<a href="/solutions.html">Solutions</a> ← <span>%s</span></div>'
        '<h1>%s</h1><p class="sub">%s</p>'
        '<div class="hero-cta"><a class="btn-ghost" href="%s" target="_blank" rel="noopener">'
        '💬 WhatsApp us to start</a></div>'
        '</div></section>' % (p['cap'], p['h1'], p['sub'], WA_HOME)
        + COMPOSITE
        + '<section><div class="wrap"><div class="sec-head center">'
          '<span class="kicker">Built for %s</span><h2>Your pain points, solved</h2></div>'
          '<div class="grid2">%s</div></div></section>' % (p['cap'], pain_cards)
        + photo_block(p)
        + HOW
        + '<section><div class="wrap"><div class="sec-head center">'
          '<h2>Sample products you could start with</h2>'
          '<p>Landed prices to the Gulf, MOQ and lead time — all quoted up front.</p></div>'
          '<div class="pgrid">%s</div>'
          '<p class="updated-note">Prices are indicative landed-to-UAE estimates; '
          'final quote depends on qty and destination.</p></div></section>' % sample_html
        + persona_strip(p['slug'])
        + faq_block(p['faq'])
        + final_cta()
    )
    ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": p['title'],
        "url": "https://sourcetogulf.com/" + p['slug'],
        "description": p['sub'],
        "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": "https://sourcetogulf.com/"},
            {"@type": "ListItem", "position": 2, "name": "Solutions",
             "item": "https://sourcetogulf.com/solutions.html"},
            {"@type": "ListItem", "position": 3, "name": p['cap'],
             "item": "https://sourcetogulf.com/" + p['slug']},
        ]},
    }
    json_ld = json.dumps([ld, faq_jsonld(p['faq'])], ensure_ascii=False, indent=2)
    return page_shell(
        title=p['title'],
        description=p.get('desc', p['sub']),
        canonical="https://sourcetogulf.com/" + p['slug'],
        body_inner=body,
        json_ld=json_ld,
        # 阿语版互链（/ar/<slug> 由 build_arabic.py 生成）
        alt_ar="https://sourcetogulf.com/ar/" + p['slug'],
    )

if __name__ == '__main__':
    for p in PERSONAS:
        html = render(p)
        out = os.path.join(APP, p['slug'])
        with open(out, 'w', encoding='utf-8') as f:
            f.write(html)
        print('wrote', p['slug'], len(html), 'bytes')
