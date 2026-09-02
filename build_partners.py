# -*- coding: utf-8 -*-
"""
build_partners.py — 生成 /partners.html（渠道与资源合作页）

背景（2026-09-01）：
外链建设走到「用本地人脉换真实提及」这一步。
  • v1（推荐伙伴/佣金制）：用户否决 —— 公开佣金比例会让对方反推我方毛利并压价，
    且"介绍客户换钱"姿态偏低，像在求人。已废弃。
  • v2（本版）：改为**资源互补型合作**叙事 —— 你懂本地市场，我们懂中国供应链，
    我们是你在中国这端的执行团队。商务条款单独约定，页面上不出现任何比例/金额。

合规要点（守外链质量铁律）：
  • 页面不出现 backlink / link to us / guest post / link exchange —— 纯商业合作邀约。
  • 若合作方日后自愿提及我们，那是编辑性提及；事先要求挂链接则属 link scheme。
  • 用服务交换可传递权重的链接属 Google 违规，已明确规避。

用法: python3 build_partners.py
"""
import os, json
from tpl_common import page_shell, wa_link, APP

BASE = 'https://sourcetogulf.com'
CANONICAL = BASE + '/partners.html'

PARTNER_FAQ = [
    ('What does a partnership cost me?',
     'Nothing to start. There is no joining fee, no minimum volume and no need to hire anyone. We are the execution team on the China side; you keep the client relationship. Commercial terms are agreed separately for each partnership rather than published as a fixed rate, because the right structure depends on how your business works.'),
    ('Will you go around me and deal with my client directly?',
     'No, unless you prefer that. Most partners use our white-label arrangement: we quote, communicate and ship under your company name, so from your client\'s perspective the China operation is yours. The client relationship stays where it is — with you.'),
    ('Do I have to handle sourcing, shipping or customs?',
     'No. We handle supplier communication, quality inspection, custom and private-label packaging, sample dispatch and shipping. We also carry a written after-sales policy: confirmed defects are replaced or refunded. Your involvement can be as little as forwarding an enquiry.'),
    ('How are you different from a freight forwarder?',
     'We are not a freight forwarder. A forwarder moves cartons that have already been bought. We do the work that comes first: finding the factory, applying custom and private-label packaging, and sending physical samples so a buyer can test 10–50 units before committing to a container. Shipping is the last step we arrange, not the service we sell. For a partner, that means you can offer clients a sourcing capability, not just a freight quote.'),
    ('What if my client only wants a small order?',
     'That is exactly the case we are built for. Minimum orders in our current catalogue start from 10 pieces (2ct moissanite solitaire ring, FOB CNY 42/pc) and 20 pieces (plus-size embroidered abaya, FOB CNY 78/pc). Small first orders are never turned away, which protects the introduction you made.'),
    ('What support do you give me before I have a client?',
     'A live catalogue with real minimums and FOB prices, Arabic–English quotation templates you can put your own brand on, product photography, and per-market compliance notes (SABER for Saudi Arabia, ECAS for the UAE, KUCAS for Kuwait, OFOQ for Bahrain, Bayan for Oman). You can start quoting enquiries without preparing anything yourself.'),
    ('Can we exchange business in both directions?',
     'Yes, and we prefer it. If you provide local services we need — customs clearance, warehousing, last-mile delivery, retail distribution, marketing or market access — we are glad to send work your way. The most durable partnerships run in both directions.'),
    ('How do we start?',
     'Send us a message on WhatsApp or email with a sentence about your business and the kind of clients you work with. We will reply with how we would structure cooperation for your situation. No contract to sign before you have seen whether it is useful.'),
]


def body():
    wa = wa_link('Hi SourceToGulf! I would like to explore a partnership — my business works with Gulf clients who import from China.')
    return '''
<section class="page-hero"><div class="wrap">
  <div class="crumb"><a href="/">Home</a> ← <span>Partners</span></div>
  <h1>You know the Gulf market. We know the Chinese supply chain.</h1>
  <p class="sub">SourceToGulf works with Gulf traders, consultants, agencies and community operators who need a reliable execution team in China. You keep the client relationship; we handle sourcing, custom and private-label packaging, sampling, compliance and shipping. <b>We are not a freight forwarder</b> — we are a composite sourcing partner, so what you gain is a sourcing capability, not a shipping quote.</p>
  <div class="hero-cta">
    <a class="wa-btn" href="%s" target="_blank" rel="noopener">💬 Start a conversation on WhatsApp</a>
    <a class="btn-ghost" href="/products.html">See the product catalogue →</a>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head center">
    <span class="kicker">What partnership gives you</span>
    <h2>Add China sourcing to your business without building a China operation</h2>
  </div>
  <div class="grid2">
    <div class="card">
      <h3>A wider service to offer</h3>
      <p>Clients already ask you where to buy, how to brand it and what it will cost to land. Instead of turning that away, you can answer it — we are the team behind you doing the work.</p>
    </div>
    <div class="card">
      <h3>Stronger hold on your clients</h3>
      <p>Solving the sourcing problem makes you harder to replace. A client who can buy through you does not need to go looking for a supplier elsewhere.</p>
    </div>
    <div class="card">
      <h3>No cost, no headcount</h3>
      <p>You do not need an office in China, a sourcing staff or a quality inspector. We are already on the ground in Guangzhou and Yiwu, and we carry the operational load.</p>
    </div>
    <div class="card">
      <h3>Material you can use immediately</h3>
      <p>Real catalogue with minimums and FOB prices, Arabic–English quotation templates you can put your own brand on, product photography and per-market compliance notes.</p>
    </div>
  </div>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head center">
    <span class="kicker">How we work together</span>
    <h2>Three arrangements, picked to fit your business</h2>
    <p>Commercial terms are agreed per partnership rather than published as a fixed rate, because the right structure depends on how you operate.</p>
  </div>
  <div class="grid3">
    <div class="card">
      <div class="em">🤝</div>
      <h3>Refer &amp; support</h3>
      <p>You introduce the client and stay in the relationship. We quote, source, brand and ship. You stay informed at every stage and the client still sees you as their contact.</p>
      <span class="painline">For those who want to stay close to the client without doing the work.</span>
    </div>
    <div class="card">
      <div class="em">🏷️</div>
      <h3>White-label</h3>
      <p>We operate entirely under your company name — quotations, packaging artwork and shipment documents all carry your brand. Your client never needs to know we exist.</p>
      <span class="painline">For those protecting client ownership.</span>
    </div>
    <div class="card">
      <div class="em">🔄</div>
      <h3>Two-way exchange</h3>
      <p>You send us sourcing enquiries; we send you the local work we need — customs clearance, warehousing, last-mile delivery, distribution or market access. Both sides grow.</p>
      <span class="painline">The most durable kind of partnership.</span>
    </div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>What we take off your plate</h2></div>
  <div class="grid3">
    <div class="card"><h3>Finding the factory</h3><p>Send a photo or a link. We locate the factory, compare two or three suppliers and quote FOB in CNY.</p></div>
    <div class="card"><h3>Branding the product</h3><p>Custom and private-label packaging — your logo on box, pouch or hangtag, with Arabic–English artwork for Gulf shelves.</p></div>
    <div class="card"><h3>Samples before commitment</h3><p>We order, inspect on camera and air-ship samples so the client approves quality before paying for stock.</p></div>
    <div class="card"><h3>Small minimums</h3><p>Current catalogue starts from 10 pieces, so a client testing a first product is never turned away.</p></div>
    <div class="card"><h3>Compliance per market</h3><p>SABER for Saudi Arabia, ECAS for the UAE, KUCAS for Kuwait, OFOQ for Bahrain, Bayan for Oman.</p></div>
    <div class="card"><h3>After-sales in writing</h3><p>Confirmed defects replaced or refunded — your client is never left arguing with a factory.</p></div>
  </div>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head center"><h2>Who we work well with</h2></div>
  <div class="grid2">
    <div class="card"><h3>Traders and wholesalers in the Gulf</h3>
      <p>You already supply retailers or online sellers. Adding sourcing means capturing the part of the value chain you currently hand to someone else.</p></div>
    <div class="card"><h3>Consultants and buying agents</h3>
      <p>You advise businesses on importing or setup. We act as the execution arm, so you can take on sourcing work without building a China operation.</p></div>
    <div class="card"><h3>Agencies, creators and community operators</h3>
      <p>Your audience wants to launch products. We supply the sourcing side with real minimums that suit first-time sellers — and you keep the relationship.</p></div>
    <div class="card"><h3>Local service providers</h3>
      <p>Clearance, warehousing, delivery, distribution or marketing. If we can send work your way while you send sourcing ours, the partnership runs in both directions.</p></div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head center"><h2>Starting takes one message</h2></div>
  <div class="steps">
    <div class="step"><div class="n">1</div><h3>Tell us your business</h3>
      <p>One message on WhatsApp or email — who you work with and what your clients buy.</p></div>
    <div class="step"><div class="n">2</div><h3>We propose a structure</h3>
      <p>We reply with how cooperation would work for your situation, including which of the three arrangements fits.</p></div>
    <div class="step"><div class="n">3</div><h3>First enquiry</h3>
      <p>Send us one real enquiry. See how we quote and deliver before committing to anything.</p></div>
  </div>
</div></section>
''' % wa


def final_cta():
    wa = wa_link('Hi SourceToGulf! I would like to explore a partnership — my business works with Gulf clients who import from China.')
    return '''
<section class="sec"><div class="wrap">
  <div class="cta-box">
    <h2>Let's see whether this is useful</h2>
    <p>No joining fee, no volume commitment and nothing to sign before you have tested us on one enquiry. Message us with a sentence about your business and we will take it from there.</p>
    <a class="wa-btn" href="%s" target="_blank" rel="noopener">💬 WhatsApp: +971 58 514 6139</a>
    <p style="margin-top:14px"><a href="mailto:info@sourcetogulf.com?subject=Partnership%%20Enquiry" style="color:#fff;text-decoration:underline">info@sourcetogulf.com</a></p>
  </div>
</div></section>
''' % wa


def json_ld():
    wp = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "You know the Gulf market. We know the Chinese supply chain.",
        "url": CANONICAL,
        "description": "SourceToGulf partners with Gulf traders, consultants, agencies and local service providers as their execution team in China — sourcing, private-label packaging, sampling, compliance and shipping, under your brand if you prefer.",
        "inLanguage": "en",
        "publisher": {"@type": "Organization", "name": "SourceToGulf", "url": BASE},
        "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Partners", "item": CANONICAL},
        ]},
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in PARTNER_FAQ
        ],
    }
    return json.dumps([wp, faq], ensure_ascii=False, indent=2)


def main():
    html = page_shell(
        title='Partner With Us: China Sourcing & Branding | SourceToGulf',
        description='Gulf traders, agencies and consultants: add China sourcing without a China team. We find factories, apply your branding and send samples — under your name.',
        canonical=CANONICAL,
        body_inner=body() + final_cta(),
        json_ld=json_ld(),
        # 阿语版互链（/ar/partners.html 由 build_arabic.py 生成）
        alt_ar=BASE + '/ar/partners.html',
    )
    out = os.path.join(APP, 'partners.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    print('✓ wrote partners.html (%d bytes, %d FAQ)' % (len(html), len(PARTNER_FAQ)))


if __name__ == '__main__':
    main()
