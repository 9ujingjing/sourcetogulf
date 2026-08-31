# -*- coding: utf-8 -*-
"""
build_arabic.py — 生成 SSR 阿语页面（/ar/*.html）

============================================================================
为什么需要这个脚本（2026-08-31 关键诊断）
----------------------------------------------------------------------------
站点自称双语，但阿语实际只存在于 `data-ar` 属性中，靠 JS 的 applyLang() 切换：
  • 去掉 <script> 后，页面阿语字符数 ≈ 7
  • 正文阿语覆盖率 = 0%（H2 11个/0、H3 12个/0、P 29个/1）
  • hreflang 只有 en 与 x-default，没有 ar

AI 引擎（ChatGPT / Perplexity / Gemini）的爬虫大多**不执行 JavaScript**，
它们抓到 HTML 源码时看到的是英文可见文本 —— 等于我们是一个纯英文站，
阿语查询完全没有内容可引用。这是引用率 0% 的直接原因之一。

本脚本生成**服务端渲染的真阿语页**（lang="ar" dir="rtl"），
使 AI 引擎无需执行 JS 即可读到完整阿语正文。

用法: python3 build_arabic.py
============================================================================
"""
import os, re, json

APP = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://sourcetogulf.com'
OUT_DIR = os.path.join(APP, 'ar')

_HTML = open(os.path.join(APP, 'products.html'), encoding='utf-8').read()
STYLE = re.search(r'<style>[\s\S]*?</style>', _HTML).group(0)


def to_arabic(html):
    """把 <tag data-en="E" data-ar="A">E</tag> 形式的双语元素转为纯阿语文本。"""
    def rep(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        am = re.search(r'data-ar="([^"]*)"', attrs)
        if am and am.group(1).strip():
            return '<%s%s>%s</%s>' % (tag, attrs, am.group(1), tag)
        return m.group(0)
    # 处理 <tag ...data-ar...>text</tag>
    html = re.sub(r'<(\w+)([^>]*\bdata-ar="[^"]*"[^>]*)>([^<]*)</\1>', rep, html)
    # 处理自闭合或仅带 data-ar 的元素（如 <img>），保留原样
    return html


HEADER_AR = to_arabic(re.search(r'<header>[\s\S]*?</header>', _HTML).group(0))
FOOTER_AR = to_arabic(re.search(r'<footer>[\s\S]*?</footer>', _HTML).group(0))

GA4 = ('<!-- Google tag (gtag.js) GA4 -->\n'
       '<script async src="https://www.googletagmanager.com/gtag/js?id=G-76L0Y9SC5D"></script>\n'
       '<script>\n  window.dataLayer = window.dataLayer || [];\n'
       '  function gtag(){dataLayer.push(arguments);}\n'
       "  gtag('js', new Date());\n  gtag('config', 'G-76L0Y9SC5D');\n</script>\n")

FLOAT_BTN = ('<a class="float-wa" href="https://wa.me/971585146139" target="_blank" rel="noopener" aria-label="واتساب">💬</a>\n'
             '<button id="toTop" aria-label="العودة للأعلى">↑</button>')

MINI_JS = """
var lang='ar';
function toggleMenu(){var m=document.getElementById('mpanel');if(m)m.classList.toggle('open');}
document.addEventListener('DOMContentLoaded',function(){
  var t=document.getElementById('toTop');
  if(t){window.addEventListener('scroll',function(){t.classList.toggle('show',window.scrollY>700);},{passive:true});
  t.onclick=function(){window.scrollTo({top:0,behavior:'smooth'});};}
});
"""


def page(title, desc, canonical_ar, canonical_en, body, faq, extra_ld=None):
    """渲染一个 SSR 阿语页面。"""
    ld_list = [{
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "url": canonical_ar,
        "description": desc,
        "inLanguage": "ar",
        "publisher": {"@type": "Organization", "name": "SourceToGulf", "url": BASE},
    }]
    if faq:
        ld_list.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "inLanguage": "ar",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faq
            ],
        })
    if extra_ld:
        ld_list.extend(extra_ld)

    faq_html = ''
    if faq:
        items = ''.join('<div class="qa"><h3>%s</h3><p>%s</p></div>' % (q, a) for q, a in faq)
        faq_html = ('<section class="sec"><div class="wrap">'
                    '<div class="sec-head center"><span class="kicker">الأسئلة الشائعة</span>'
                    '<h2>أسئلة يطرحها المستوردون في الخليج</h2></div>'
                    '<div class="qa-list">%s</div></div></section>' % items)

    return '''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>%s</title>
<meta name="description" content="%s" />
<link rel="canonical" href="%s" />
<link rel="alternate" hreflang="ar" href="%s" />
<link rel="alternate" hreflang="en" href="%s" />
<link rel="alternate" hreflang="x-default" href="%s" />
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/images/logo/logo-icon-512.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;500;600;700;800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
%s
%s
<link rel="alternate" type="application/rss+xml" title="SourceToGulf" href="https://sourcetogulf.com/rss.xml" />
</head>
<body>
%s
%s
%s
%s
<script>%s</script>
<script type="application/ld+json">
%s
</script>
</body>
</html>
''' % (title, desc, canonical_ar, canonical_ar, canonical_en, canonical_en,
       GA4, STYLE, HEADER_AR, body, faq_html, FOOTER_AR, MINI_JS,
       json.dumps(ld_list, ensure_ascii=False, indent=2))


# ============================================================================
# 阿语页面内容
# 数据原则：关税/流程数字与英文版一致；SKU 数字取自 products.clean.json 真实在售产品。
# 定位措辞与英文版统一："لسنا شركة شحن" (we are not a freight forwarder)。
# ============================================================================

BAHRAIN_FAQ_AR = [
    ('هل أنتم شركة شحن أم شريك توريد؟',
     'نحن شريك توريد، ولسنا شركة شحن. شركة الشحن تنقل كراتين اشتريتها مسبقاً؛ أما نحن فنقوم بالعمل الذي يسبق ذلك: إيجاد المصنع، وتجهيز التغليف المخصص والعلامة الخاصة، وطلب العيّنات وفحصها، وتجميع الطلبات الصغيرة. نرتب الشحن كخطوة أخيرة، لكن التوريد والتغليف والعيّنات هي صلب خدمتنا.'),
    ('هل يمكنني طلب عيّنات بتغليفي الخاص قبل الطلب بالجملة؟',
     'نعم، وهذه هي الخطوة الأولى المعتادة. نطلب العيّنات من المصنع المختار، ونفحصها بالكاميرا، ويمكننا تطبيق شعارك وتصميمك العربي-الإنجليزي على التغليف بحدود دنيا منخفضة. تُشحن العيّنات جواً إليك لتعتمد الجودة والعلامة قبل الالتزام بأي مخزون.'),
    ('ما هو الحد الأدنى للطلب للدفعة التجريبية الأولى؟',
     'يختلف حسب المنتج، لكن الحدود الدنيا الحالية في كتالوجنا تبدأ من 10 قطع (خاتم مويسانيت 2 قيراط، FOB 42 يوان/قطعة) و20 قطعة (عباية مطرزة مقاسات كبيرة، FOB 78 يوان/قطعة). أجهزة التجميل تبدأ من 50 قطعة. هذه الحدود تسمح للمشتري الصغير باختبار الطلب دون طلب حاوية كاملة.'),
    ('كم يستغرق التخليص الجمركي في البحرين؟',
     'مع مستندات كاملة وصحيحة، يستغرق التخليص في البحرين عادةً من يوم إلى ثلاثة أيام عمل عبر ميناء خليفة بن سلمان. التأخير يأتي غالباً من نقص شهادات المطابقة أو الخلاف على القيمة المصرّح بها.'),
    ('هل أحتاج إلى شهادات SABER للاستيراد إلى البحرين؟',
     'لا. نظام SABER خاص بالسعودية فقط. البحرين تستخدم نافذة OFOQ الموحدة للتجارة، وتطبق شهادات المطابقة الخليجية (GSO) على المنتجات الخاضعة للتنظيم مثل الألعاب والإلكترونيات والأجهزة منخفضة الجهد.'),
]


def bahrain_body():
    return '''
<section class="page-hero"><div class="wrap">
  <div class="crumb"><a href="/ar/">الرئيسية</a> ← <span>دليل الاستيراد</span></div>
  <h1>الاستيراد من الصين إلى البحرين — دليل 2026 الشامل</h1>
  <p class="sub">الاستيراد من الصين إلى البحرين يخضع لـ <b>رسم جمركي 5% من قيمة CIF</b> بالإضافة إلى <b>10% ضريبة قيمة مضافة</b>. لا يوجد نظام SABER في البحرين؛ بدلاً منه تستخدم البحرين نافذة <b>OFOQ</b> الموحدة وشهادات المطابقة الخليجية (GSO). التخليص الجمركي يستغرق عادةً <b>1–3 أيام عمل</b> عبر ميناء خليفة بن سلمان.</p>
  <div class="cta-row">
    <a class="btn-wa" href="https://wa.me/971585146139" target="_blank" rel="noopener">💬 احصل على عرض سعر للبحرين عبر واتساب</a>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>الرسوم الجمركية وضريبة القيمة المضافة في البحرين</h2></div>
  <p>تطبق البحرين الرسم الجمركي الموحد لدول مجلس التعاون الخليجي، وهو <b>5% من قيمة CIF</b> (التكلفة + التأمين + الشحن) على غالبية البضائع، إضافة إلى <b>10% ضريبة قيمة مضافة</b>.</p>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:18px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:right">البند</th>
      <th style="padding:10px 12px;text-align:right">النسبة / المدة</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">الرسم الجمركي على معظم البضائع</td><td style="padding:10px 12px"><b>5% من قيمة CIF</b></td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">ضريبة القيمة المضافة</td><td style="padding:10px 12px"><b>10%</b></td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px">التخليص الجمركي (ميناء خليفة بن سلمان)</td><td style="padding:10px 12px">1–3 أيام عمل</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px">المناطق الحرة (المنطقة اللوجستية، BIIP)</td><td style="padding:10px 12px">إعفاء من الرسم لإعادة التصدير</td></tr>
    </tbody>
  </table>
  <p>يُحتسب الرسم على قيمة CIF، لذا فإن خفض تكلفة الشحن أو الحصول على سعر أفضل من المصنع يقلل مباشرة ما تدفعه على الحدود.</p>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>نافذة OFOQ وشهادات المطابقة</h2></div>
  <p>لا تستخدم البحرين نظام SABER السعودي. بدلاً من ذلك، تمر العمليات عبر نافذة <b>OFOQ</b> الموحدة للتجارة، مع تطبيق شهادات المطابقة الصادرة عن هيئة التقييس الخليجية (GSO) على المنتجات الخاضعة للتنظيم.</p>
  <ul class="bullets">
    <li><b>فاتورة تجارية</b> — توضح القيمة والرمز الجمركي وبيانات الأطراف</li>
    <li><b>قائمة تعبئة</b> — عدد الكراتين والأوزان والأبعاد</li>
    <li><b>بوليصة شحن / بوليصة جوية</b> — مستند النقل</li>
    <li><b>شهادة منشأ</b> — تثبت أن البضاعة صينية المنشأ</li>
    <li><b>شهادة مطابقة GSO</b> — للمنتجات الخاضعة للتنظيم (ألعاب، إلكترونيات، أجهزة منخفضة الجهد)</li>
  </ul>
  <p>البحرين تسمح بـ <b>ملكية أجنبية 100%</b> في معظم الأنشطة، ما يجعلها نقطة انطلاق سهلة للتجار الصغار.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head">
    <span class="kicker">ما نفعله فعلياً</span>
    <h2>لسنا شركة شحن — نحن شريك توريد متكامل للبحرين</h2>
  </div>
  <p><b>نحن لسنا شركة شحن.</b> شركة الشحن تنقل كراتين اشتريتها مسبقاً. نحن نقوم بالعمل الذي يسبق ذلك: نجد المصنع، ونضع علامتك التجارية على المنتج وتغليفه، ونرسل لك عيّنات فعلية قبل أن تلتزم بحاوية كاملة. الشحن هو آخر خطوة نرتبها — وليس الخدمة التي نبيعها.</p>
  <p>إذا كنت مشترياً صغيراً في البحرين — صاحب متجر، أو صانع محتوى يبني علامة خاصة، أو شخصاً يختبر منتجه الأول — فإن الجزء الصعب نادراً ما يكون الشحن. الصعب هو إيجاد مصنع يقبل طلباً صغيراً، وطباعة علامتك على العلبة، ورؤية المنتج الحقيقي قبل أن تدفع ثمن المخزون.</p>
  <table class="tbl" style="width:100%%;border-collapse:collapse;margin:20px 0;font-size:15px">
    <thead><tr style="background:#0b1f3a;color:#fff">
      <th style="padding:10px 12px;text-align:right">القدرة</th>
      <th style="padding:10px 12px;text-align:right">ما تغطيه</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>البحث عن المنتجات</b></td><td style="padding:10px 12px">أرسل صورة أو رابطاً — نجد المصنع، ونقارن 2–3 موردين، ونقدم سعر FOB باليوان</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px"><b>التغليف المخصص والعلامة الخاصة</b></td><td style="padding:10px 12px">شعارك على العلبة أو الكيس أو البطاقة، مع تصميم عربي-إنجليزي لرفوف الخليج</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef"><td style="padding:10px 12px"><b>إرسال العيّنات إلى بابك</b></td><td style="padding:10px 12px">نطلب العيّنات ونفحصها بالكاميرا ونشحنها جواً لتتحقق من الجودة قبل الالتزام</td></tr>
      <tr style="border-bottom:1px solid #e6e9ef;background:#f7f9fc"><td style="padding:10px 12px"><b>حد أدنى منخفض للطلب</b></td><td style="padding:10px 12px">ابدأ بعشرات القطع لدفعة تجريبية بدلاً من حاوية كاملة</td></tr>
    </tbody>
  </table>
  <h3>أمثلة حقيقية من كتالوجنا الحالي</h3>
  <p>هذه حدود دنيا وأسعار FOB فعلية لمنتجات نشحنها الآن، وليست أمثلة توضيحية:</p>
  <ul class="bullets">
    <li><b>خاتم مويسانيت 2 قيراط</b> (لون D، VVS) — الحد الأدنى <b>10 قطع</b>، FOB 42 يوان/قطعة</li>
    <li><b>جهاز EMS للوجه والرقبة 3 في 1</b> — الحد الأدنى <b>50 قطعة</b>، FOB 24 يوان/قطعة</li>
    <li><b>عباية باتوينج مطرزة بمقاسات كبيرة</b> (قماش نيدا) — الحد الأدنى <b>20 قطعة</b>، FOB 78 يوان/قطعة</li>
    <li><b>صندل مسطح بمقاسات كبيرة</b> — الحد الأدنى <b>30 قطعة</b>، FOB 28 يوان/قطعة</li>
    <li><b>طقم حمالة صدر وسراويل داخلية بمقاسات كبيرة</b> — الحد الأدنى <b>50 قطعة</b>، FOB 16 يوان/قطعة</li>
  </ul>
  <p>دفعة تجريبية من أي منتج من هذه تبقى أقل بكثير من حمولة حاوية، وهذا هو الهدف: تتحقق من الطلب والتغليف والجودة أولاً، ثم تتوسع.</p>
</div></section>
'''


HOME_FAQ_AR = [
    ('هل أنتم شركة شحن أم شريك توريد؟',
     'نحن شريك توريد متكامل، ولسنا شركة شحن. شركة الشحن تنقل كراتين اشتريتها مسبقاً؛ أما نحن فنجد المصنع، ونضع علامتك على التغليف، ونرسل لك عيّنات فعلية لتجرب 10–50 قطعة قبل الالتزام بحاوية كاملة.'),
    ('ما هو الحد الأدنى للطلب؟',
     'يبدأ من 10 قطع لبعض المنتجات (خاتم مويسانيت 2 قيراط، FOB 42 يوان/قطعة) و20 قطعة للعبايات المطرزة (FOB 78 يوان/قطعة)، و50 قطعة لأجهزة التجميل. الهدف أن تختبر السوق دون طلب حاوية.'),
    ('هل تتولون التغليف بالعلامة الخاصة والتصميم العربي؟',
     'نعم. نطبّق شعارك على العلبة أو الكيس أو البطاقة، ونجهّز تصميماً عربياً-إنجليزياً مناسباً لرفوف الخليج، بحدود دنيا منخفضة تناسب المشتري الصغير.'),
]


def home_body():
    return '''
<section class="hero"><div class="wrap hero-grid">
  <div>
    <h1>توريد من الصين، مصمم للخليج 🇨🇳→🇦🇪🇸🇦🇰🇼🇶🇦🇧🇭🇴🇲<br><em>نلقاه. نوسمه بعلامتك. نرسل لك عيّنة. نشحنه.</em></h1>
    <p class="sub">أنت تبيع — وإحنا ندير كل شيء في الصين. بلا بضاعة غلط، بلا مورّدين يختفون بعد الدفع، بلا مفاجآت: تعتمد بضاعتك الفعلية بالفيديو قبل أي شحن، وبسعر واحد شامل. مقرنا قوانغتشو، و١٤ سنة عايشين في دبي.</p>
    <div style="margin-top:16px;padding:13px 17px;background:#fff;border-inline-start:4px solid var(--gold);border-radius:12px;font-size:14.5px;line-height:1.65;box-shadow:0 6px 20px rgba(23,32,29,.05)">
      <b>نحن لسنا شركة شحن.</b>
      نحن شريك توريد متكامل: نلاقي المصنع، ونطبع علامتك على التغليف، ونرسل لك عيّنات فعلية — حتى تختبر ١٠–٥٠ قطعة قبل ما تلتزم بحاوية كاملة.
    </div>
    <div class="hero-cta">
      <a class="wa-btn" href="https://wa.me/971585146139" target="_blank" rel="noopener">💬 واتساب: ‎+971 58 514 6139</a>
      <a class="btn-ghost" href="/#calculator">جرّب حاسبة التكلفة الشاملة</a>
    </div>
  </div>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head center">
    <span class="kicker">شريك واحد، أربع قدرات</span>
    <h2>لسنا شركة شحن — نحن شريك توريد متكامل</h2>
    <p><b>نحن لسنا شركة شحن.</b> شركة الشحن تنقل كراتين اشتريتها مسبقاً. نحن نقوم بالعمل الذي يسبق ذلك: إيجاد المصنع، ووضع علامتك على المنتج وتغليفه، وإيصال عيّنات فعلية إليك — لتجرب دفعة صغيرة قبل الالتزام بحاوية.</p>
  </div>
  <div class="grid2">
    <div class="card"><div class="em">🔎</div><h3>البحث عن المصدر</h3>
      <p>أرسل صورة أو رابطاً أو وصفاً. نحدد المصنع، ونقارن العروض، ونتحقق من المورّد قبل أن تلتزم بأي مبلغ.</p></div>
    <div class="card"><div class="em">🎨</div><h3>التغليف المخصص والعلامة الخاصة</h3>
      <p>شعارك، وألوانك، وعلبتك — بحدود دنيا منخفضة. حوّل منتجاً عاماً إلى خط إنتاج بعلامتك الخاصة.</p></div>
    <div class="card"><div class="em">📦</div><h3>العيّنات أولاً</h3>
      <p>نرسل عيّنات فعلية (مع صور وفيديو للفحص) لتعتمد الجودة قبل أي طلب بالجملة. بلا مفاجآت عند الوصول.</p></div>
    <div class="card"><div class="em">🚪</div><h3>حد أدنى منخفض والتوصيل للباب</h3>
      <p>ابدأ بدفعة صغيرة. نجمع البضائع، ونخلص الجمارك، ونوصّلها إلى بابك في الإمارات والسعودية وقطر وغيرها.</p></div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head center"><h2>أمثلة على منتجات يمكنك البدء بها</h2>
    <p>حدود دنيا وأسعار FOB حقيقية من كتالوجنا الحالي.</p></div>
  <div class="grid3">
    <div class="card"><h3>خاتم مويسانيت 2 قيراط</h3><p>لون D، نقاوة VVS — الحد الأدنى <b>10 قطع</b>، FOB 42 يوان/قطعة</p></div>
    <div class="card"><h3>عباية باتوينج مطرزة</h3><p>قماش نيدا، مقاسات كبيرة — الحد الأدنى <b>20 قطعة</b>، FOB 78 يوان/قطعة</p></div>
    <div class="card"><h3>جهاز EMS للوجه والرقبة</h3><p>3 في 1 — الحد الأدنى <b>50 قطعة</b>، FOB 24 يوان/قطعة</p></div>
  </div>
  <p style="text-align:center;margin-top:22px"><a class="quote-btn" href="/ar/bahrain-import-guide-from-china.html">اقرأ دليل الاستيراد إلى البحرين</a></p>
</div></section>
'''


PAGES = {
    'index': {
        'file': 'index.html',
        'en': BASE + '/',
        'title': 'توريد من الصين للخليج — شريك توريد متكامل (لسنا شركة شحن)',
        'desc': 'شريك توريد من الصين للإمارات والسعودية وقطر والكويت والبحرين وعُمان: نجد المصنع، ونطبع علامتك على التغليف، ونرسل عيّنات فعلية بحد أدنى منخفض للطلب. لسنا شركة شحن.',
        'body': home_body(),
        'faq': HOME_FAQ_AR,
    },
    'bahrain': {
        'file': 'bahrain-import-guide-from-china.html',
        'en': BASE + '/bahrain-import-guide-from-china.html',
        'title': 'الاستيراد من الصين إلى البحرين — دليل 2026 الشامل',
        'desc': 'الاستيراد من الصين إلى البحرين: رسم جمركي 5% من قيمة CIF، ضريبة قيمة مضافة 10%، نافذة OFOQ الموحدة وشهادات المطابقة الخليجية GSO (لا يوجد SABER)، تخليص خلال 1–3 أيام، وحد أدنى منخفض للطلب.',
        'body': bahrain_body(),
        'faq': BAHRAIN_FAQ_AR,
    },
}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for key, p in PAGES.items():
        canonical_ar = BASE + '/ar/' + p['file']
        html = page(p['title'], p['desc'], canonical_ar, p['en'], p['body'], p['faq'])
        out = os.path.join(OUT_DIR, p['file'])
        with open(out, 'w', encoding='utf-8') as f:
            f.write(html)
        ar = len(re.findall(r'[\u0600-\u06FF]', re.sub(r'<script[\s\S]*?</script>', '', html)))
        print('✓ wrote ar/%s (%d bytes, %d 阿语字符 SSR, %d FAQ)' % (p['file'], len(html), ar, len(p['faq'])))


if __name__ == '__main__':
    main()
