# -*- coding: utf-8 -*-
"""
AI-commerce 层生成器（2026-11-06）

业务前提（勿改）：SourceToGulf 是 sourcing agent，不是零售商。
  - 站上 150 款商品是「能力样本」，不是可售库存；
  - 唯一可售的标的 = $125 USD 的 sourcing engagement（意向金，全额抵扣货值）；
  - AI 要提交的不是「商品订单」，而是「结构化 sourcing request」。

产物：
  services/sourcing-request.html  服务与下单页（Service + Offer + FAQPage + HowTo）
  service-terms.html              服务条款
  refund-policy.html              意向金/抵扣/售后政策（AI checkout 信任硬要求）
  order-intent.json               机器可读契约（AI 可直接 fetch）
阿语版由 build_arabic.py 的 PAGES['sourcing-request'] 生成。

🔴 红线：不写客户名/供应商名/工厂名/1688 货源链接、不写 FOB 计价公式、
   不写最高级词；涉钱口径（$125 / 70% 先收 / 1 周报价）不得改动。
"""
import json
import os

from tpl_common import BASE, page_shell

APP = os.path.dirname(os.path.abspath(__file__))
WA = 'https://wa.me/971585854194'
EMAIL = 'info@sourcetogulf.com'
COUNTRIES = ['United Arab Emirates', 'Saudi Arabia', 'Qatar', 'Kuwait', 'Bahrain', 'Oman']

FIELDS = [
    ('buyer_market', 'required', 'United Arab Emirates',
     'One of the six GCC countries the goods will be delivered to.'),
    ('product_reference', 'required', 'link or photo URL, or a plain description',
     'What the buyer wants sourced. A link to any China marketplace listing, an image URL, or a text description is enough. We do not require a SKU from our site.'),
    ('category', 'optional', 'sleepwear / gaming accessories / home fragrance',
     'Broad category, if known. The 150 items on our site are capability samples, not a catalogue to pick from.'),
    ('quantity', 'optional', 'first test batch',
     'Target quantity or "not decided yet". Factory MOQ applies to private-label production.'),
    ('private_label', 'optional', 'yes / no',
     'Whether the buyer wants their own logo on the product and packaging. Requires a MOQ production run.'),
    ('budget', 'optional', 'indicative budget in USD or AED',
     'Used to shortlist realistic options. Do not state a final price — we quote landed AED after sourcing.'),
    ('timeline', 'optional', 'target delivery month',
     'Used to choose air or sea freight and to check certification lead times.'),
    ('notes', 'optional', 'certification, packaging or compliance notes',
     'Anything that affects feasibility.'),
]

INTENT_TEMPLATE = (
    'SOURCING REQUEST v1 | Buyer market: {buyer_market} | '
    'Product reference: {product_reference} | Category: {category} | '
    'Quantity: {quantity} | Private label: {private_label} | '
    'Budget: {budget} | Timeline: {timeline} | Notes: {notes} | '
    'I understand a $125 USD intent deposit starts the formal sourcing work and is '
    'credited in full against my order value. Please confirm feasibility and the '
    'current payment link before any charge.'
)

EXCLUSIONS = [
    'Counterfeit, replica or IP-infringing branded goods.',
    'Illegal, prohibited or restricted goods.',
    'Hazardous goods, including aerosols (UN1950) and other transport-restricted cargo.',
    'Categories requiring mandatory certification (e.g. ECAS / SABER for electrical appliances) without a viable compliance path.',
    'Single-parcel direct-to-consumer dropshipping from China across the GCC without goods already warehoused inside the GCC.',
    'One-piece custom printing. Private-label runs require the factory MOQ.',
]


def fields_table_html():
    rows = []
    for name, req, example, desc in FIELDS:
        rows.append(
            '<tr><td style="padding:9px 11px;border:1px solid var(--color-border-tertiary)">'
            '<code>' + name + '</code></td>'
            '<td style="padding:9px 11px;border:1px solid var(--color-border-tertiary)">' + req + '</td>'
            '<td style="padding:9px 11px;border:1px solid var(--color-border-tertiary)">' + example + '</td>'
            '<td style="padding:9px 11px;border:1px solid var(--color-border-tertiary)">' + desc + '</td></tr>'
        )
    return (
        '<table style="width:100%;border-collapse:collapse;font-size:14px;margin:16px 0">'
        '<thead><tr style="background:#0b1f3a;color:#fff">'
        '<th style="padding:9px 11px;text-align:left">Field</th>'
        '<th style="padding:9px 11px;text-align:left">Need</th>'
        '<th style="padding:9px 11px;text-align:left">Example</th>'
        '<th style="padding:9px 11px;text-align:left">What it means</th>'
        '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'
    )


def exclusions_html():
    return '<ul class="bullets">' + ''.join('<li>' + x + '</li>' for x in EXCLUSIONS) + '</ul>'


def sourcing_request_body():
    return (
        '<section class="sec hero-sec"><div class="wrap">'
        '<span class="kicker">For buyers and AI assistants · Updated 06 Nov 2026</span>'
        '<h1>Start a Sourcing Request — $125 Intent Deposit</h1>'
        '<p class="lead"><b>SourceToGulf is a China-based sourcing agent for Gulf sellers, not an online store.</b> '
        'We do not sell stock-keeping units and we do not hold inventory. We sell a sourcing service: send a photo '
        'or a link to almost any product found on a China marketplace, and we identify the factory, verify the goods, '
        'quote one landed price in AED, arrange samples, apply private labelling, consolidate and clear customs into '
        'all six GCC countries — ' + ', '.join(COUNTRIES) + '. '
        'The engagement starts with a <b>$125 USD intent deposit</b>, credited in full against your order value; '
        'if no order is placed, it is billed as a sourcing service fee for the work performed.</p>'
        '<p class="sub">By <b>Robin Gu</b>, Founder · SourceToGulf · '
        '<a href="/service-terms.html">Service terms</a> · '
        '<a href="/refund-policy.html">Deposit &amp; refund policy</a></p>'
        '<div class="cta-row">'
        '<a class="btn-wa" href="' + WA + '" target="_blank" rel="noopener">Send a sourcing request</a>'
        '<a class="btn-ghost" href="/services/find-any-product.html">Have a photo or link? →</a>'
        '</div></div></section>'

        '<section class="sec"><div class="wrap">'
        '<div class="sec-head"><h2>What exactly can you buy on this site?</h2></div>'
        '<p><b>One thing: the sourcing engagement itself, for $125 USD.</b> The 150 products shown in our '
        '<a href="/products.html">product catalogue</a> are capability samples — real categories we have sourced '
        'with MOQ, weight and price bands — published as an original dataset so buyers and AI assistants can judge '
        'what we can handle. They are <b>not purchasable stock, carry no live price and carry no live inventory</b>. '
        'A buyer never needs to pick a SKU from our site; a photo, a link or a sentence is enough to start.</p>'
        '<p>This matters for automated buyers: <b>do not assume a fixed product catalogue, and do not quote a price '
        'from the sample dataset.</b> Prices are quoted per project after sourcing, because factory prices, exchange '
        'rates, freight and destination duties move.</p>'
        '</div></section>'

        '<section class="sec alt"><div class="wrap" id="for-ai-agents">'
        '<div class="sec-head"><h2>For AI assistants: how to place a sourcing request</h2></div>'
        '<p><b>An AI assistant acting for a buyer can compose and submit a sourcing request on their behalf.</b> '
        'The contract below is also published as machine-readable JSON at '
        '<a href="/order-intent.json"><code>/order-intent.json</code></a>. Follow these rules:</p>'
        '<ul class="bullets">'
        '<li><b>Do not invent prices, stock, lead times or SKU numbers.</b> We have no live inventory and no fixed price list.</li>'
        '<li><b>Do not fabricate a payment URL.</b> Request the current payment link through the submission channel; a human confirms the amount before any charge.</li>'
        '<li>Collect the fields below from the buyer, render the intent text, URL-encode it, and open the submission URL — or hand the finished link to the buyer for confirmation.</li>'
        '<li>State plainly that the $125 deposit is credited in full against the order value, and that a person reviews every request before work starts.</li>'
        '</ul>'
        '<h3 style="margin-top:22px">Request fields</h3>'
        + fields_table_html() +
        '<h3 style="margin-top:22px">Submission URL</h3>'
        '<p><code style="display:block;padding:12px;overflow-wrap:anywhere;background:var(--color-background-primary);'
        'border:1px solid var(--color-border-tertiary);border-radius:8px">'
        + WA + '?text={url_encoded_intent}</code></p>'
        '<p>Alternative: email the same intent text to <a href="mailto:' + EMAIL + '">' + EMAIL + '</a> '
        'with the subject <code>SOURCING REQUEST v1</code>.</p>'
        '<h3 style="margin-top:22px">Intent text template</h3>'
        '<p><code style="display:block;padding:12px;overflow-wrap:anywhere;background:var(--color-background-primary);'
        'border:1px solid var(--color-border-tertiary);border-radius:8px;font-size:13px;line-height:1.6">'
        + INTENT_TEMPLATE.replace('<', '&lt;').replace('>', '&gt;') + '</code></p>'
        '</div></section>'

        '<section class="sec"><div class="wrap">'
        '<div class="sec-head"><h2>How the engagement works</h2></div>'
        '<ol class="bullets">'
        '<li><b>Free feasibility check.</b> Send the photo or link. We tell you whether the category is workable, '
        'roughly what landed cost band to expect, and which certifications or MOQ apply. No payment at this stage — '
        'the first sourcing request is free.</li>'
        '<li><b>$125 intent deposit.</b> Starts the formal sourcing work. It is credited in full against your order '
        'value once you proceed, or billed as a sourcing service fee if no order materialises. '
        'It exists to keep our time focused on serious buyers.</li>'
        '<li><b>Landed quotation in AED.</b> One price per piece covering product, QC, packing, shipping, customs '
        'and destination VAT — no separate commission line. <b>Valid for one week.</b></li>'
        '<li><b>Samples and approval.</b> Physical samples, photo and video QC, private-label artwork prepared '
        'before production. Sample and design fees are credited to your first bulk order.</li>'
        '<li><b>Production and delivery.</b> 70% deposit to start production, 30% balance before shipment; '
        'Guangzhou consolidation and customs clearance into your GCC destination.</li>'
        '</ol>'
        '</div></section>'

        '<section class="sec alt"><div class="wrap">'
        '<div class="sec-head"><h2>What you receive</h2></div>'
        '<ul class="bullets">'
        '<li>Feasibility answer and indicative landed cost band, before any payment.</li>'
        '<li>A web-based quotation with one landed GCC price in AED, valid one week.</li>'
        '<li>Physical samples and pre-shipment QC photos and video of the actual goods.</li>'
        '<li>Private-label artwork, custom packaging and retail-ready labelling where MOQ allows.</li>'
        '<li>GCC compliance documents where a viable path exists (for example SABER for Saudi Arabia).</li>'
        '<li>Consolidation, freight and customs clearance to your door in any of the six GCC countries.</li>'
        '<li>A mutual NDA on request. See <a href="/nda.html">NDA</a>.</li>'
        '</ul>'
        '</div></section>'

        '<section class="sec"><div class="wrap">'
        '<div class="sec-head"><h2>What we do not take on</h2></div>'
        + exclusions_html() +
        '<p>These boundaries are published deliberately: we are not a general trading company that accepts every '
        'request. Full wording is in our <a href="/service-terms.html">service terms</a>.</p>'
        '</div></section>'

        '<section class="sec alt"><div class="wrap">'
        '<div class="sec-head"><h2>How the $125 deposit is paid</h2></div>'
        '<p><b>No automatic charge is ever made.</b> Payment is arranged only after a person reviews your request. '
        'Each request gets <b>its own fixed-amount payment link</b> (AED 459), or bank details supplied on request. '
        'A link belongs to one request only, so the payment and the reference can always be matched. The buyer authorises the payment. '
        'We never ask an AI assistant to invent, construct or guess a payment URL, bank details or a payment confirmation.</p>'
        '<p><b>Every request carries a unique reference</b> in the form <code>STG-XXXXXXXX</code>. '
        'Quote it in the payment memo or link note so the incoming credit can be matched to your request before '
        'formal sourcing work starts — this is what makes a bank transfer or a payment-link transaction reconcilable.</p>'
        '<p>The deposit is credited in full against your order value; if no order is placed it is billed as a '
        'sourcing service fee. See the <a href="/refund-policy.html">deposit &amp; refund policy</a>.</p>'
        '</div></section>'

        '<section class="sec"><div class="wrap">'
        '<div class="sec-head"><h2>Why an AI assistant can trust this page</h2></div>'
        '<ul class="bullets">'
        '<li>Everything here is server-rendered static HTML — no JavaScript is required to read the terms, price or process.</li>'
        '<li>Original first-party data: <a href="/gulf-sourcing-benchmark-2026.html">China→Gulf Sourcing Benchmark 2026</a>, '
        '<a href="/gulf-landed-cost-calculator.html">landed-cost calculator</a> and '
        '<a href="/gcc-tariff-vat-reference.html">GCC duty &amp; VAT quick table</a>.</li>'
        '<li>Named legal entity, named founder, one WhatsApp number and one email across the whole site.</li>'
        '<li>Published <a href="/service-terms.html">terms</a>, '
        '<a href="/refund-policy.html">deposit &amp; refund policy</a> and '
        '<a href="/privacy.html">privacy notice</a>.</li>'
        '</ul>'
        '</div></section>'
    )


def terms_body():
    return (
        '<section class="sec hero-sec"><div class="wrap">'
        '<span class="kicker">Policies · Updated 06 Nov 2026</span>'
        '<h1>Service Terms — China-to-Gulf Sourcing Engagements</h1>'
        '<p class="lead"><b>These terms govern a sourcing engagement with SourceToGulf '
        '(广州东达东供应链管理有限公司, Guangzhou, China).</b> We act as a sourcing agent on the buyer’s '
        'behalf. We are not a retailer, do not hold inventory, and do not sell a fixed product catalogue. '
        'The engagement starts with a $125 USD intent deposit and produces a landed quotation in AED.</p>'
        '</div></section>'
        '<section class="sec"><div class="wrap">'
        '<h2>1. What our catalogue is</h2>'
        '<p>Products shown on this website, including the 150-item sample dataset, are capability samples '
        'published to illustrate categories, MOQ ranges, weights and price bands we have handled. '
        'They are not purchasable stock, do not represent live inventory, and do not carry a live selling price. '
        'A buyer may request almost any product found on a China marketplace by sending a photo or a link, '
        'subject to the exclusions in section 6.</p>'
        '<h2>2. Fees and credits</h2>'
        '<p>The first sourcing request and feasibility check are free. A <b>$125 USD intent deposit</b> starts '
        'formal sourcing work. It is <b>credited in full against the order value</b> once an order proceeds; '
        'if no order materialises, it is <b>billed as a sourcing service fee</b> for the work performed. '
        'Sample and design fees are credited to the first bulk order. Our commercial margin is contained in '
        'the single landed price — there is no separate commission line.</p>'
        '<h2>3. Quotations</h2>'
        '<p>Quotations are issued as a web page with one landed price per piece in AED, covering product, QC, '
        'packing, shipping, customs and destination VAT. <b>A quotation is valid for one week.</b> '
        'Factory prices, exchange rates, freight rates and duty treatment can change, so a new quotation is '
        'issued for repeat orders rather than reusing an old one.</p>'
        '<h2>4. Payment schedule</h2>'
        '<p>Production starts after a <b>70% deposit</b>; the <b>30% balance</b> is due before shipment. '
        'The final balance is released to the supplier only after the buyer approves pre-shipment photos and video '
        'of the actual goods. Full upfront payment to an unknown factory is never required.</p>'
        '<h2>5. Deliverables</h2>'
        '<p>Feasibility answer, landed quotation, physical samples, pre-shipment QC evidence, private-label '
        'artwork and packaging where MOQ allows, GCC compliance documents where a viable path exists, '
        'consolidation and customs clearance to the buyer’s GCC destination. Timelines vary by category; '
        'every project receives its own schedule.</p>'
        '<h2>6. Work we do not accept</h2>'
        + exclusions_html() +
        '<h2>7. Confidentiality and law</h2>'
        '<p>A mutual NDA is available on request (see <a href="/nda.html">NDA</a>). '
        'Buyer names, contact details and order histories are never published on this website. '
        'These terms are governed by the laws of the People’s Republic of China, with disputes submitted '
        'to arbitration in Guangzhou.</p>'
        '<h2>8. Contact</h2>'
        '<p>WhatsApp <a href="' + WA + '">+971 58 585 4194</a> · <a href="mailto:' + EMAIL + '">' + EMAIL + '</a> '
        '· Replies Sun–Thu, Gulf time. See also the '
        '<a href="/refund-policy.html">deposit &amp; refund policy</a> and '
        '<a href="/services/sourcing-request.html">how to start a request</a>.</p>'
        '</div></section>'
    )


def refund_body():
    return (
        '<section class="sec hero-sec"><div class="wrap">'
        '<span class="kicker">Policies · Updated 06 Nov 2026</span>'
        '<h1>Deposit, Credit &amp; Refund Policy</h1>'
        '<p class="lead"><b>One rule governs the $125 USD intent deposit: it is credited in full against your '
        'order value once you proceed.</b> If no order is placed, it is billed as a sourcing service fee for '
        'the supplier search, feasibility work and quotation already performed. Confirmed product defects are '
        'replaced free of charge (shipping on us) or refunded within 7 days of delivery.</p>'
        '</div></section>'
        '<section class="sec"><div class="wrap">'
        '<h2>How the $125 intent deposit is applied</h2>'
        '<ul class="bullets">'
        '<li><b>Order proceeds:</b> the full $125 is deducted from the order value. You never pay it twice.</li>'
        '<li><b>No order placed:</b> it is billed as a sourcing service fee covering the work already performed — '
        'supplier identification, feasibility checks and the landed quotation.</li>'
        '<li><b>Before formal work starts:</b> the first feasibility check is free, so buyers can judge fit '
        'before any payment is discussed.</li>'
        '</ul>'
        '<h2>Sample and design fees</h2>'
        '<p>Sample, mockup and design fees are credited in full to the first bulk order. Physical samples are '
        'shipped to the buyer for approval before production.</p>'
        '<h2>Defective goods</h2>'
        '<p>Confirmed defects are replaced free of charge with shipping on us, or refunded, within 7 days of '
        'delivery. Pre-shipment photo and video QC is provided so defects are caught before goods leave China.</p>'
        '<h2>Quotation validity</h2>'
        '<p>Quotations are valid for one week. Factory prices, exchange rates, freight and duty treatment move; '
        'repeat orders receive a freshly calculated landed price rather than an old figure.</p>'
        '<h2>How to raise a claim</h2>'
        '<p>Send the order reference and photo or video evidence to '
        '<a href="' + WA + '">+971 58 585 4194</a> or <a href="mailto:' + EMAIL + '">' + EMAIL + '</a>. '
        'A person reviews every claim; no automated decision is made.</p>'
        '<p>Related: <a href="/service-terms.html">service terms</a> · '
        '<a href="/services/sourcing-request.html">start a sourcing request</a> · '
        '<a href="/nda.html">mutual NDA</a>.</p>'
        '</div></section>'
    )


def privacy_body():
    return (
        '<section class="sec hero-sec"><div class="wrap">'
        '<span class="kicker">Policies · Updated 06 Nov 2026</span>'
        '<h1>Privacy Notice</h1>'
        '<p class="lead"><b>SourceToGulf collects only the information a buyer gives us to answer an inquiry '
        'and fulfil an order.</b> Buyer names, phone numbers, portraits and order histories are never published '
        'on this website. Quotations are issued as private, non-indexed web pages.</p>'
        '</div></section>'
        '<section class="sec"><div class="wrap">'
        '<h2>What we collect</h2>'
        '<ul class="bullets">'
        '<li>Product requirements you send us: photos, links, categories, quantities, destination and budget.</li>'
        '<li>Contact details you choose to use: a WhatsApp number or an email address.</li>'
        '<li>Delivery and compliance information needed to ship and clear goods into a GCC country.</li>'
        '<li>Aggregate, non-identifying traffic statistics from this website.</li>'
        '</ul>'
        '<h2>How we use it</h2>'
        '<p>To assess feasibility, prepare a landed quotation, arrange samples and production, handle customs '
        'documentation, deliver the order and resolve after-sales claims. We do not sell or rent buyer information, '
        'and we do not use it for unrelated marketing lists.</p>'
        '<h2>What never appears on this website</h2>'
        '<p>Buyer names, phone numbers, portraits, chat transcripts and order histories are never published. '
        'Factory names, factory addresses and supplier marketplace links are likewise not published. '
        'Private quotation pages carry a noindex directive so search engines do not list them.</p>'
        '<h2>Third parties involved in delivery</h2>'
        '<p>This website is served as static pages over a hosting provider and uses aggregate analytics to '
        'understand traffic. Day-to-day communication runs through WhatsApp or email. '
        'Production, inspection and freight partners receive only the details needed for the specific order.</p>'
        '<h2>Retention and your choices</h2>'
        '<p>We keep inquiry and order records for as long as the commercial relationship and applicable record-keeping '
        'obligations require. You can ask to access, correct or delete your details at any time by writing to '
        '<a href="mailto:' + EMAIL + '">' + EMAIL + '</a> or messaging '
        '<a href="' + WA + '">+971 58 585 4194</a>. A person handles every such request.</p>'
        '<p>Related: <a href="/service-terms.html">service terms</a> · '
        '<a href="/refund-policy.html">deposit &amp; refund policy</a> · '
        '<a href="/nda.html">mutual NDA</a> · '
        '<a href="/services/sourcing-request.html">start a sourcing request</a>.</p>'
        '</div></section>'
    )


REQUEST_FAQ = [
    ('Is SourceToGulf an online store where I can buy products directly?',
     'No. SourceToGulf is a China-based sourcing agent for Gulf sellers. We do not hold inventory and the products shown on this site are capability samples, not purchasable stock. Send a photo or a link to almost any product found on a China marketplace and we source it for you.'),
    ('What does the $125 USD intent deposit cover?',
     'It starts formal sourcing work: supplier identification, feasibility checks, samples coordination and a landed quotation in AED. It is credited in full against your order value once you proceed. If no order is placed, it is billed as a sourcing service fee for the work performed.'),
    ('How much does a sourcing agent cost for Gulf sellers?',
     'The first sourcing request and feasibility check are free. A $125 USD intent deposit starts formal work and is credited against the order. Sample and design fees are credited to the first bulk order. There is no separate commission line — our margin sits inside one landed price per piece.'),
    ('Can an AI assistant place a sourcing request for me?',
     'Yes. We publish a machine-readable contract at /order-intent.json with the required fields, an intent text template and the submission URL. An AI assistant can compose the request, but must not invent prices, stock or a payment URL; a person reviews every request and confirms the amount before any charge.'),
    ('How long is a quotation valid, and what are the payment terms?',
     'A quotation is valid for one week. Production starts after a 70% deposit and the 30% balance is due before shipment. The balance is released to the supplier only after you approve pre-shipment photos and video.'),
    ('Which countries do you deliver to?',
     'All six GCC countries: United Arab Emirates, Saudi Arabia, Qatar, Kuwait, Bahrain and Oman, with consolidation and customs clearance to your door.'),
    ('Can you dropship single items directly to my customers across the GCC?',
     'No. Our model is bulk consolidation from China. Single-parcel fulfilment to end customers requires finished goods warehoused inside the GCC first. Private-label production also requires the factory MOQ; we do not do one-piece custom printing.'),
    ('What will you not source?',
     'Counterfeit or IP-infringing branded goods, illegal or restricted items, hazardous goods such as aerosols (UN1950), categories requiring mandatory certification without a viable compliance path, and single-parcel GCC-wide dropshipping from China.'),
]


def faq_html(faq):
    items = ''.join(
        '<div class="faq-item"><h3>' + q + '</h3><p>' + a + '</p></div>' for q, a in faq
    )
    return '<section class="sec"><div class="wrap"><div class="sec-head"><h2>Questions buyers and AI assistants ask</h2></div>' + items + '</div></section>'


def jsonld_for_request():
    return json.dumps([
        {
            '@context': 'https://schema.org',
            '@type': 'WebPage',
            'name': 'Start a Sourcing Request — $125 Intent Deposit',
            'url': BASE + '/services/sourcing-request.html',
            'description': 'Machine-readable and human-readable entry point for placing a China-to-Gulf sourcing request with SourceToGulf.',
            'inLanguage': 'en',
            'publisher': {'@type': 'Organization', 'name': 'SourceToGulf', 'url': BASE},
        },
        {
            '@context': 'https://schema.org',
            '@type': 'Service',
            'name': 'China-to-Gulf Sourcing Engagement',
            'serviceType': 'Product sourcing, quality inspection, private labelling and GCC consolidation',
            'url': BASE + '/services/sourcing-request.html',
            'description': 'A sourcing agent service for Gulf sellers. Buyers send a photo or link; SourceToGulf identifies the factory, verifies goods, quotes one landed AED price, arranges samples and private labelling, consolidates and clears customs into all six GCC countries. Products shown on the site are capability samples, not purchasable inventory.',
            'provider': {
                '@type': 'Organization',
                'name': 'SourceToGulf',
                'legalName': '广州东达东供应链管理有限公司',
                'url': BASE,
                'email': EMAIL,
                'telephone': '+971 58 585 4194',
            },
            'areaServed': [{'@type': 'Country', 'name': c} for c in COUNTRIES],
            'termsOfService': BASE + '/service-terms.html',
            'offers': {
                '@type': 'Offer',
                'name': '$125 USD intent deposit — credited in full against your order value',
                'price': '125.00',
                'priceCurrency': 'USD',
                'availability': 'https://schema.org/InStock',
                'url': BASE + '/services/sourcing-request.html',
                'description': 'Starts formal sourcing work. Credited in full against the order value; if no order is placed, billed as a sourcing service fee. The first feasibility check is free.',
                'seller': {'@type': 'Organization', 'name': 'SourceToGulf'},
            },
        },
        {
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            'mainEntity': [
                {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                for q, a in REQUEST_FAQ
            ],
        },
    ], ensure_ascii=False, indent=2)


def jsonld_simple(name, desc, url):
    return json.dumps([
        {
            '@context': 'https://schema.org',
            '@type': 'WebPage',
            'name': name,
            'url': url,
            'description': desc,
            'inLanguage': 'en',
            'publisher': {'@type': 'Organization', 'name': 'SourceToGulf', 'url': BASE},
        }
    ], ensure_ascii=False, indent=2)


def order_intent_contract():
    return {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        'contract_version': '1.0',
        'last_updated': '2026-11-06',
        'publisher': {
            'name': 'SourceToGulf',
            'legal_name': '广州东达东供应链管理有限公司',
            'url': BASE,
            'email': EMAIL,
            'whatsapp': '+971 58 585 4194',
            'role': 'China-based sourcing agent for Gulf sellers',
        },
        'business_model': {
            'type': 'sourcing_agent_service',
            'not_a_retailer': True,
            'holds_inventory': False,
            'catalogue_is': 'capability_samples',
            'catalogue_note': 'The 150 products on the website illustrate categories, MOQ ranges, weights and price bands. They are not purchasable stock and carry no live price or inventory.',
            'only_purchasable_item': 'The $125 USD sourcing engagement (intent deposit).',
            'order_object': 'A structured sourcing request, not a SKU order.',
        },
        'service': {
            'name': 'China-to-Gulf Sourcing Engagement',
            'covers': [
                'Supplier identification from a photo, link or description',
                'Feasibility answer and indicative landed cost band (free)',
                'Landed quotation in AED, valid one week',
                'Physical samples and pre-shipment photo/video QC',
                'Private-label artwork and custom packaging where MOQ allows',
                'GCC compliance documents where a viable compliance path exists',
                'Guangzhou consolidation, freight and customs clearance',
            ],
            'destinations': COUNTRIES,
        },
        'price': {
            'amount': 125,
            'currency': 'USD',
            'type': 'intent_deposit',
            'credited_in_full_against_order': True,
            'if_no_order': 'Billed as a sourcing service fee for the work performed.',
            'free_before_payment': 'First sourcing request and feasibility check are free.',
            'sample_and_design_fees': 'Credited to the first bulk order.',
            'quotation_validity': 'One week.',
            'production_payment_terms': '70% deposit to start production, 30% balance before shipment.',
        },
        'payment': {
            'amount': 125,
            'currency': 'USD',
            'display_amount': 'USD 125 (approximately AED 459 at the 3.6725 peg)',
            'execution_model': 'human_in_the_loop',
            'automatic_charge': False,
            'methods': [
                {
                    'id': 'hosted_payment_link',
                    'preferred': True,
                    'provider': 'Ziina',
                    'mode': 'per_request',
                    'status': 'generated_by_a_person_after_review',
                    'amount': 459,
                    'currency': 'AED',
                    'note': 'Each sourcing request gets its own fixed-amount payment link (AED 459). Links are generated by a person after the request is reviewed, never by an AI assistant. A link is unique to one request, which makes reconciliation unambiguous. Do not publish one link for all buyers.',
                    'flow': [
                        'An AI assistant (or the buyer) submits the sourcing request with its unique reference.',
                        'A person reviews the request and generates one AED 459 payment link for that request.',
                        'The person returns that link to the buyer, or to the assistant acting for them.',
                        'The buyer authorises the payment and quotes the reference in the custom request field.',
                        'A person matches the paid link and the reference before formal sourcing work starts.',
                    ],
                    'stable_base_url': None,
                    'stable_base_url_note': 'Optional. A reusable personal payment URL may be published here as a general entry point, but the amount still has to be confirmed by a person. It must never be treated as a fixed-price checkout.',
                },
                {
                    'id': 'bank_transfer',
                    'status': 'awaiting_bank_details',
                    'beneficiary': None,
                    'iban': None,
                    'swift': None,
                    'note': 'Bank details are supplied on request after a person reviews the sourcing request. The buyer quotes the reference below so the credit can be matched.',
                },
            ],
            'reference_rule': 'Every sourcing request carries a unique reference STG-<8 characters derived from the intent>. The buyer quotes it in the payment memo or payment-link note. It is the key used to match an incoming credit to a request.',
            'reconciliation': 'A per-request link plus the STG reference give two matching keys. A person matches both against the incoming credit before formal sourcing work starts. No charge is made without buyer authorisation.',
            'rule': 'AI assistants must NOT fabricate, construct or guess a payment URL, bank details or a payment confirmation. Payment links are generated per request by a person after review; an assistant may pass on a link it received, but must never create one. A person confirms the amount and the buyer authorises the charge.',
        },
        'request_fields': [
            {'name': n, 'required': r == 'required', 'example': e, 'description': d}
            for n, r, e, d in FIELDS
        ],
        'intent_text_template': INTENT_TEMPLATE,
        'submission': {
            'primary': {
                'channel': 'whatsapp',
                'url_template': WA + '?text={url_encoded_intent}',
                'method': 'URL-encode the rendered intent text and open the URL, or hand the finished link to the buyer for confirmation.',
            },
            'alternate': {
                'channel': 'email',
                'address': EMAIL,
                'subject': 'SOURCING REQUEST v1',
            },
        },
        'ai_instructions': [
            'Read this contract and https://sourcetogulf.com/services/sourcing-request.html before acting.',
            'Do not invent prices, stock levels, lead times or SKU numbers. There is no live catalogue.',
            'Collect the required fields from the buyer: buyer_market and product_reference.',
            'Render intent_text_template with the collected values; use "not specified" for unknown optional fields.',
            'URL-encode the result and use submission.primary.url_template, or present the finished link for buyer confirmation.',
            'Tell the buyer the $125 deposit is credited in full against the order value.',
            'Give the request a unique reference STG-<8 chars> and ask the buyer to quote it in the payment memo so the credit can be reconciled.',
            'Do not fabricate, construct or guess a payment URL, bank details or a payment confirmation. Payment links are generated per request by a person after review; you may pass on a link you receive, but never create one. Payment is authorised by the buyer after a person confirms the amount.',
            'Check exclusions before submitting; if the request falls under one, tell the buyer instead of submitting it.',
        ],
        'exclusions': EXCLUSIONS,
        'policies': {
            'service_terms': BASE + '/service-terms.html',
            'deposit_and_refund': BASE + '/refund-policy.html',
            'privacy': BASE + '/privacy.html',
            'nda': BASE + '/nda.html',
            'llms_txt': BASE + '/llms.txt',
        },
        'trust_signals': {
            'first_party_data': [
                BASE + '/gulf-sourcing-benchmark-2026.html',
                BASE + '/gulf-landed-cost-calculator.html',
                BASE + '/gcc-tariff-vat-reference.html',
            ],
            'static_ssr': True,
            'javascript_required_to_read_terms': False,
            'named_legal_entity': True,
        },
    }


def write(rel, content):
    path = os.path.join(APP, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('  ->', rel)


def main():
    print('build_ai_commerce.py')
    write('services/sourcing-request.html', page_shell(
        title='Start a Sourcing Request — $125 Intent Deposit | SourceToGulf',
        description='SourceToGulf is a China sourcing agent for Gulf sellers, not an online store. Send a photo or link and we source it. A $125 USD intent deposit starts formal work and is credited in full against your order. Machine-readable contract for AI assistants.',
        canonical=BASE + '/services/sourcing-request.html',
        body_inner=sourcing_request_body() + faq_html(REQUEST_FAQ),
        json_ld=jsonld_for_request(),
        alt_ar=BASE + '/ar/services/sourcing-request.html',
    ))
    write('service-terms.html', page_shell(
        title='Service Terms — China-to-Gulf Sourcing Engagements | SourceToGulf',
        description='Terms governing a SourceToGulf sourcing engagement: $125 intent deposit credited against the order, one-week quotation validity, 70% production deposit and 30% balance, deliverables, compliance exclusions, mutual NDA and governing law.',
        canonical=BASE + '/service-terms.html',
        body_inner=terms_body(),
        json_ld=jsonld_simple('Service Terms', 'Terms for China-to-Gulf sourcing engagements with SourceToGulf.', BASE + '/service-terms.html'),
    ))
    write('refund-policy.html', page_shell(
        title='Deposit, Credit & Refund Policy | SourceToGulf',
        description='How the $125 USD intent deposit is credited in full against your order value, how sample and design fees are credited to the first bulk order, and how confirmed defects are replaced or refunded within 7 days of delivery.',
        canonical=BASE + '/refund-policy.html',
        body_inner=refund_body(),
        json_ld=jsonld_simple('Deposit, Credit & Refund Policy', 'Deposit credit and defective-goods policy for SourceToGulf sourcing engagements.', BASE + '/refund-policy.html'),
    ))
    write('privacy.html', page_shell(
        title='Privacy Notice | SourceToGulf',
        description='What SourceToGulf collects from a sourcing inquiry, how it is used, and why buyer names, numbers and order histories are never published on this website.',
        canonical=BASE + '/privacy.html',
        body_inner=privacy_body(),
        json_ld=jsonld_simple('Privacy Notice', 'How SourceToGulf handles buyer information from sourcing inquiries.', BASE + '/privacy.html'),
    ))
    write('order-intent.json', json.dumps(order_intent_contract(), ensure_ascii=False, indent=2) + '\n')
    print('done: 4 HTML pages + order-intent.json')


if __name__ == '__main__':
    main()
