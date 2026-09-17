# -*- coding: utf-8 -*-
"""
build_nda.py — 生成 /nda.html（保密协议线上签署页）

背景（2026-09-17）：
客户（阿联酋服装品牌）要发设计稿给我们报价打样，需要先签 NDA。
做成静态页部署在自有域名下，客户打开链接即可阅读 + 手写签名 + 提交，
比第三方电子签链接更品牌一致、客户信任度更高。

技术约束：
  • 站点是 GitHub Pages 静态站，无后端 → 表单提交走第三方（默认 FormSubmit，
    无需注册；如需换 Formspree 只改 FORM_ENDPOINT 一个常量即可）。
  • 签名用 canvas 采集 → toDataURL() 转 base64 PNG → 作为隐藏字段随表单提交，
    避开文件上传的大小/类型限制。
  • 本页 noindex：NDA 页不需要 SEO，也不应被公开检索到。
  • 不加入 sitemap.xml（同上理由）。

用法: python3 build_nda.py
"""
import os
from tpl_common import page_shell, APP

BASE = 'https://sourcetogulf.com'
CANONICAL = BASE + '/nda.html'

# 表单提交端点。默认 FormSubmit（无需注册，endpoint 即目标邮箱）。
# ⚠️ AJAX 提交必须用 /ajax/ 路径 —— 不带的话 FormSubmit 返回 HTML"感谢页"
#    而不是 JSON，页面会把成功误判为失败。
# 换成 Formspree 只需把这里改成 https://formspree.io/f/xxxxxxxx
FORM_ENDPOINT = 'https://formsubmit.co/ajax/info@sourcetogulf.com'

# 条款数据：(en_title, en_body, ar_title, ar_body)
CLAUSES = [
    ("1. Purpose",
     "The Parties wish to explore a potential business relationship concerning the development, sourcing, costing, sampling, and/or production of apparel, garments, clothing, textiles, fashion accessories and related products in the People's Republic of China for the Client.",
     "١. الغرض",
     "يرغب الطرفان في دراسة علاقة تجارية محتملة تتعلق بتطوير وتوريد وتسعير وإنتاج العينات و/أو تصنيع الملابس والأزياء والمنسوجات وإكسسوارات الأزياء والمنتجات ذات الصلة في جمهورية الصين الشعبية لصالح العميل."),

    ("2. Confidential Information",
     "Non-public information disclosed by one Party to the other, in any form, that is designated as confidential or that a reasonable person would understand to be confidential. It includes designs, fashion sketches, technical drawings, tech packs, patterns, grading and size specifications, bill of materials, fabric and trim specifications, colour standards, artwork, logos and brand assets; factory identities, mill and supplier contacts, sourcing channels, cost breakdowns and pricing models; and the existence and content of discussions between the Parties.",
     "٢. المعلومات السرية",
     "أي معلومات غير علنية يُفصح عنها أحد الطرفين للآخر بأي شكل، ويتم تحديدها على أنها سرية أو ما يفهمه الشخص المعقول على أنها سرية. وتشمل التصاميم والرسومات التخطيطية للأزياء والرسومات الفنية وحزم المعلومات التقنية (تيك باك) والأنماط والتدرج ومواصفات المقاسات وقوائم المواد ومواصفات الأقمشة والإكسسوارات والمعايير اللونية والأعمال الفنية والشعارات وأصول العلامة التجارية؛ وهويات المصانع وبيانات الاتصال بمصانع الأقمشة والموردين وقنوات التوريد وتفصيلات التكاليف ونماذج التسعير؛ ووجود ومحتوى المناقشات بين الطرفين."),

    ("3. Obligations of the Recipient",
     "Each Recipient shall keep the other Party's Confidential Information confidential and not disclose it to any third party except as permitted in Clause 4; use it solely for the Purpose; protect it with no less than reasonable care; and not reverse engineer or disassemble any sample or garment provided, except as strictly necessary for the Purpose.",
     "٣. التزامات الطرف المتلقي",
     "يلتزم كل طرف متلقٍ بالحفاظ على سرية المعلومات السرية للطرف الآخر وعدم الإفصاح عنها لأي طرف ثالث إلا على النحو المسموح به في المادة ٤؛ واستخدامها لغرض الغرض فقط؛ وحمايتها بدرجة عناية لا تقل عن العناية المعقولة؛ وعدم إجراء هندسة عكسية أو تفكيك أي عينة أو قطعة ملابس مُقدَّمة، إلا بالقدر الضروري لتحقيق الغرض."),

    ("4. Permitted Disclosure",
     "SourceToGulf may disclose the Client's designs, tech packs, patterns, specifications and samples to its fabric mills, trim and accessory suppliers, printing, embroidery, washing, dyeing and finishing houses, pattern makers, sample rooms, garment manufacturers (cut-make-trim), quality inspectors, testing laboratories, freight forwarders and professional advisers, solely to the extent necessary for the Purpose, provided each is bound by confidentiality obligations no less protective than these. The Client acknowledges that apparel development cannot proceed without such disclosure, and that it shall not constitute a breach of this Agreement.",
     "٤. الإفصاح المسموح به",
     "يجوز لسورس تو جلف الإفصاح عن تصاميم العميل وحزم المعلومات التقنية والأنماط والمواصفات والعينات إلى مصانع الأقمشة وموردي الإكسسوارات والمستلزمات ودور الطباعة والتطريز والغسيل والصباغة والتشطيب وصانعي الأنماط وغرف العينات ومصانع الملابس ومفتشي الجودة والمختبرات ووكلاء الشحن والمستشارين المهنيين، وذلك بالقدر اللازم لتحقيق الغرض فقط، شريطة التزام كل منهم بالتزامات سرية مماثلة. ويُقر العميل بأن تطوير الملابس لا يمكن أن يتم دون هذا الإفصاح، وأنه لا يشكّل خرقاً لهذه الاتفاقية."),

    ("5. Exclusions",
     "Confidential Information does not include information that the Recipient can demonstrate: was already lawfully in its possession before disclosure; is or becomes publicly available through no act or omission of the Recipient; was lawfully received from a third party free of any confidentiality obligation; or was independently developed without use of or reference to the Discloser's Confidential Information.",
     "٥. الاستثناءات",
     "لا تشمل المعلومات السرية المعلومات التي يمكن للطرف المتلقي إثبات: أنها كانت في حيازته قانونياً قبل الإفصاح؛ أو أنها أصبحت متاحة للعامة دون فعله أو تقصيره؛ أو أنه تلقاها قانونياً من طرف ثالث دون التزام بالسرية؛ أو أنه طورها بشكل مستقل دون استخدام معلومات الطرف المُفصِح أو الرجوع إليها."),

    ("6. Residual Knowledge",
     "Nothing in this Agreement restricts either Party from using, in the ordinary course of its business, the general skills, know-how, techniques, industry knowledge and experience retained in the unaided memory of its personnel, including general knowledge of garment construction, pattern-making methods, fabric behaviour, sewing and finishing processes. This Clause does not permit any use or disclosure of the other Party's Confidential Information itself, nor any infringement of its Intellectual Property Rights.",
     "٦. المعرفة المتبقية",
     "لا يقيّد أي حكم في هذه الاتفاقية أياً من الطرفين من استخدام المهارات العامة والخبرة الفنية والتقنيات والمعرفة الصناعية المحتفظ بها في الذاكرة غير المعززة لموظفيه، بما في ذلك المعرفة العامة بتركيب الملابس وطرق إعداد الأنماط وسلوك الأقمشة وعمليات الخياطة والتشطيب. ولا تجيز هذه المادة استخدام أو الإفصاح عن المعلومات السرية للطرف الآخر بحد ذاتها، ولا أي انتهاك لحقوق الملكية الفكرية الخاصة به."),

    ("7. Non-Circumvention",
     "During the Term and for twenty-four (24) months thereafter, the Client shall not, directly or indirectly (whether through affiliates, agents, employees, representatives or any intermediary), contact, solicit, engage, purchase from or transact with any factory, mill, supplier or other sourcing channel that was introduced, identified or disclosed to the Client by SourceToGulf in connection with the Purpose, without SourceToGulf's prior written consent.",
     "٧. عدم التحايل",
     "خلال مدة هذه الاتفاقية ولمدة أربعة وعشرين (٢٤) شهراً بعد انتهائها، لا يجوز للعميل، بشكل مباشر أو غير مباشر (سواء من خلال الشركات التابعة أو الوكلاء أو الموظفين أو الممثلين أو أي وسيط)، الاتصال بأي مصنع أو مصنع أقمشة أو مورد أو قناة توريد تم تقديمها أو تحديدها أو الإفصاح عنها للعميل من قبل سورس تو جلف فيما يتعلق بالغرض، أو التحريض عليها أو التعاقد معها أو الشراء منها أو التعامل معها، دون موافقة كتابية مسبقة من سورس تو جلف."),

    ("8. Intellectual Property and Client Warranty",
     "(a) All Intellectual Property Rights in the Client's designs, sketches, tech packs, artwork, logos and brand assets remain the exclusive property of the Client. (b) Any patterns, grading, technical drawings, tech packs, samples, prototypes, tooling, moulds, process improvements or know-how created by SourceToGulf or its manufacturing partners in performing the Purpose shall be the property of the Client upon full payment of all amounts due; provided that SourceToGulf retains a perpetual, irrevocable, worldwide, royalty-free, non-exclusive right to use the general techniques, methods, processes, construction knowledge and professional skill embodied therein for any other client or project, and shall not use or disclose the Client's Confidential Information or reproduce the Client's specific designs. (c) The Client warrants that it owns, or is duly licensed to use, all Intellectual Property Rights in the designs and materials it provides, and that they do not infringe any third party's rights. (d) The Client shall indemnify and hold harmless SourceToGulf, its affiliates and manufacturing partners against all claims, damages, fines, seizure of goods, costs and legal fees arising from any allegation that the Client's designs infringe third party rights. (e) SourceToGulf may decline, suspend or terminate any work if it reasonably believes the Client's designs may infringe third party rights, without liability.",
     "٨. حقوق الملكية الفكرية وضمانات العميل",
     "(أ) تظل جميع حقوق الملكية الفكرية في تصاميم العميل ورسوماته وحزم المعلومات التقنية وأعماله الفنية وشعاراته وأصول علامته التجارية ملكاً خالصاً للعميل. (ب) تكون أي أنماط أو تدرج أو رسومات فنية أو حزم معلومات تقنية أو عينات أو نماذج أولية أو أدوات أو قوالب أو تحسينات في العمليات أو معرفة تقنية يتم إنشاؤها من قبل سورس تو جلف أو شركائها في التصنيع ملكاً للعميل عند السداد الكامل لجميع المبالغ المستحقة؛ على أن تحتفظ سورس تو جلف بحق دائم وغير قابل للإلغاء وعالمي وخالي من الرسوم وغير حصري في استخدام التقنيات العامة والأساليب والعمليات ومعرفة التركيب والمهارة المهنية المتجسدة فيها لأي عميل أو مشروع آخر، وألا تستخدم أو تُفصح عن المعلومات السرية للعميل أو تعيد إنتاج تصاميمه المحددة. (ج) يقر العميل ويضمن بملكيته أو ترخيصه القانوني لجميع حقوق الملكية الفكرية في التصاميم والمواد التي يقدمها، وبأنها لا تنتهك حقوق أي طرف ثالث. (د) يلتزم العميل بتعويض وحماية وإبراء ذمة سورس تو جلف وشركاتها التابعة وشركائها في التصنيع من جميع المطالبات والأضرار والغرامات ومصادرة البضائع والتكاليف والأتعاب القانونية الناشئة عن أي ادعاء بانتهاك تصاميمه لحقوق أطراف ثالثة. (هـ) يجوز لسورس تو جلف رفض أو تعليق أو إنهاء أي عمل إذا اعتقدت بشكل معقول أن تصاميم العميل قد تنتهك حقوق أطراف ثالثة، دون أي مسؤولية."),

    ("9. Term",
     "This Agreement commences on the Effective Date and continues for two (2) years, unless earlier terminated by either Party on thirty (30) days' written notice. Clauses 2-8 and 10-16 survive expiry or termination. Clause 7 (Non-Circumvention) survives for the period stated in that Clause.",
     "٩. المدة",
     "تبدأ هذه الاتفاقية من تاريخ النفاذ وتستمر لمدة سنتين (٢)، ما لم يتم إنهاؤها بموجب إشعار كتابي مدته ثلاثون (٣٠) يوماً. وتظل المواد من ٢ إلى ٨ والمواد من ١٠ إلى ١٦ سارية بعد الانتهاء أو الإنهاء. وتظل المادة ٧ سارية للمدة المبينة فيها."),

    ("10. Return or Destruction",
     "Upon written request or on expiry/termination, the Recipient shall return or destroy the Discloser's Confidential Information, except that it may retain one archival copy as required by law or professional record-keeping obligations, and copies stored in routine backups not readily accessible in the ordinary course of business. Retained copies remain subject to this Agreement.",
     "١٠. الإعادة أو الإتلاف",
     "عند الطلب الكتابي أو عند الانتهاء أو الإنهاء، يلتزم الطرف المتلقي بإعادة أو إتلاف المعلومات السرية، باستثناء الاحتفاظ بنسخة أرشيفية واحدة بالقدر الذي يقتضيه القانون أو التزامات حفظ السجلات، والنسخ المخزنة في النسخ الاحتياطية الروتينية غير المتاحة بسهولة. وتظل النسخ المحتفظ بها خاضعة لهذه الاتفاقية."),

    ("11. No Obligation",
     "This Agreement does not oblige either Party to enter into any purchase, supply, manufacturing or other commercial agreement, nor does it create any exclusivity, agency, partnership, joint venture or employment relationship. Any order is governed solely by its own separate written contract.",
     "١١. عدم الالتزام",
     "لا تُلزم هذه الاتفاقية أياً من الطرفين بإبرام أي اتفاقية شراء أو توريد أو تصنيع أو أي اتفاقية تجارية أخرى، ولا تنشئ أي حصرية أو وكالة أو شراكة أو مشروع مشترك أو علاقة عمل. ويخضع أي طلب شراء لعقده الكتابي المستقل فقط."),

    ("12. No Warranty",
     "All Confidential Information is provided \"as is\". Neither Party makes any representation or warranty as to its accuracy, completeness or fitness for any purpose, except as expressly stated in Clause 8(c).",
     "١٢. إخلاء المسؤولية من الضمانات",
     "تُقدَّم جميع المعلومات السرية \"كما هي\". ولا يقدم أي من الطرفين أي إقرار أو ضمان بشأن دقتها أو اكتمالها أو ملاءمتها لأي غرض، باستثناء ما هو منصوص عليه صراحةً في المادة ٨(ج)."),

    ("13. Remedies",
     "The Parties acknowledge that a breach may cause irreparable harm for which monetary damages would be inadequate, and that the non-breaching Party is entitled to seek injunctive relief in addition to any other remedies available at law.",
     "١٣. سبل الانتصاف",
     "يقر الطرفان بأن الخرق قد يتسبب في ضرر لا يمكن إصلاحه وتكون التعويضات المالية غير كافية بشأنه، وأن للطرف غير المُخالِق الحق في طلب الإنصاف الزجري بالإضافة إلى أي سبل انتصاف أخرى متاحة بموجب القانون."),

    ("14. Governing Law and Dispute Resolution",
     "This Agreement is governed by the laws of the People's Republic of China. The Parties shall first attempt to resolve any dispute amicably within thirty (30) days. Failing that, the dispute shall be submitted to the Guangzhou Arbitration Commission for arbitration in Guangzhou, in English. The arbitral award is final and binding on both Parties.",
     "١٤. القانون الواجب التطبيق وتسوية المنازعات",
     "تخضع هذه الاتفاقية لقوانين جمهورية الصين الشعبية. ويحاول الطرفان أولاً التسوية الودية خلال ثلاثين (٣٠) يوماً. وفي حال التعذر، تُحال المنازعة إلى لجنة التحكيم في قوانغتشو للتحكيم في مدينة قوانغتشو باللغة الإنجليزية. ويكون قرار التحكيم نهائياً وملزماً للطرفين."),

    ("15. Language",
     "This Agreement is executed in English and Arabic. In the event of any inconsistency or conflict between the two versions, the English version shall prevail.",
     "١٥. اللغة",
     "تُبرم هذه الاتفاقية باللغتين الإنجليزية والعربية. وفي حال وجود أي تعارض أو اختلاف بين النسختين، تُعتبر النسخة الإنجليزية هي السائدة."),

    ("16. Entire Agreement",
     "This Agreement constitutes the entire agreement between the Parties as to the confidentiality of information exchanged for the Purpose, and supersedes all prior understandings on that subject. Amendments must be in writing and signed by both Parties.",
     "١٦. الاتفاقية الكاملة",
     "تشكل هذه الاتفاقية كامل الاتفاق بين الطرفين فيما يتعلق بسرية المعلومات المتبادلة لتحقيق الغرض، وتلغي جميع التفاهمات السابقة بشأن هذا الموضوع. ويجب أن تكون أي تعديلات كتابية وموقعة من الطرفين."),
]


def clauses_html():
    out = []
    for (et, eb, at, ab) in CLAUSES:
        out.append(
            '<div class="nda-cl" data-lang="en">'
            '<h3>' + et + '</h3><p>' + eb + '</p></div>'
            '<div class="nda-cl" data-lang="ar" dir="rtl" lang="ar" hidden>'
            '<h3>' + at + '</h3><p>' + ab + '</p></div>'
        )
    return '\n'.join(out)


def body_inner():
    return '''
<section class="nda-wrap">
  <div class="nda-head">
    <h1>Mutual Non-Disclosure Agreement</h1>
    <p class="nda-sub">اتفاقية السرية المتبادلة</p>
    <p class="nda-intro">
      SourceToGulf (Papa Claw Marketing Technology Co., Ltd., Guangzhou, China) and the Client
      below. Please read the agreement, fill in your details, sign in the box, and submit.
      You will receive a confirmation on screen, and we will countersign and return a copy to you.
    </p>
    <div class="nda-lang">
      <button type="button" id="btnEn" class="nda-lb is-on">English</button>
      <button type="button" id="btnAr" class="nda-lb">العربية</button>
    </div>
  </div>

  <div class="nda-body" id="ndaBody">
    __CLAUSES__
  </div>

  <form class="nda-form" id="ndaForm" action="__FORM_ENDPOINT__" method="POST" novalidate>
    <input type="hidden" name="_subject" value="NDA signed online — SourceToGulf" />
    <input type="hidden" name="_captcha" value="false" />
    <input type="hidden" name="signature_png_base64" id="sigData" value="" />
    <input type="hidden" name="signed_at" id="signedAt" value="" />
    <input type="hidden" name="page_url" id="pageUrl" value="" />

    <h2 class="nda-h2">Your details</h2>
    <div class="nda-grid">
      <label>Full name *
        <input type="text" name="full_name" required autocomplete="name" />
      </label>
      <label>Company / Trading name *
        <input type="text" name="company" required autocomplete="organization" />
      </label>
      <label>Trade licence no.
        <input type="text" name="trade_licence" />
      </label>
      <label>Email *
        <input type="email" name="email" required autocomplete="email" />
      </label>
    </div>

    <h2 class="nda-h2">Signature *</h2>
    <p class="nda-hint">Sign with your mouse, finger or stylus inside the box below.</p>
    <div class="sig-wrap">
      <canvas id="sigPad" width="1200" height="360" aria-label="Signature pad"></canvas>
    </div>
    <div class="sig-actions">
      <button type="button" id="sigClear" class="nda-btnghost">Clear</button>
      <span id="sigState" class="nda-hint">Not signed yet</span>
    </div>
    <label class="nda-check">
      <input type="checkbox" id="agreeChk" required />
      <span>I have read and agree to the terms of this Mutual Non-Disclosure Agreement.</span>
    </label>

    <button type="submit" id="ndaSubmit" class="nda-btn" disabled>Sign and submit</button>
    <p id="ndaMsg" class="nda-msg" role="status"></p>
  </form>

  <div class="nda-done" id="ndaDone" hidden>
    <h2>Thank you — your signature has been recorded.</h2>
    <p>We will countersign and email you a completed copy. You can now send your designs safely.</p>
    <p><a class="nda-btn" href="https://wa.me/971585854194">Message us on WhatsApp</a></p>
  </div>
</section>

<style>
.nda-wrap{max-width:920px;margin:0 auto;padding:24px 20px 64px}
.nda-head h1{font-size:26px;line-height:1.25;margin:0 0 4px}
.nda-sub{dir:rtl;text-align:right;font-size:16px;color:#C9A24B;margin:0 0 14px}
.nda-intro{font-size:14px;line-height:1.65;color:#444;margin:0 0 16px}
.nda-lang{display:flex;gap:8px;margin:0 0 18px}
.nda-lb{font:inherit;font-size:13px;padding:6px 16px;border:0.5px solid #D9D2C5;background:#fff;border-radius:999px;cursor:pointer;color:#0B2B4D}
.nda-lb.is-on{background:#0B2B4D;color:#fff;border-color:#0B2B4D}
.nda-body{background:#fff;border:0.5px solid #E0D9CC;border-radius:12px;padding:20px 22px;max-height:520px;overflow:auto;margin-bottom:28px}
.nda-cl{margin-bottom:18px}
.nda-cl:last-child{margin-bottom:0}
.nda-cl h3{font-size:14px;font-weight:500;color:#0B2B4D;margin:0 0 6px}
.nda-cl p{font-size:13px;line-height:1.7;color:#333;margin:0}
.nda-h2{font-size:17px;font-weight:500;color:#0B2B4D;margin:0 0 12px}
.nda-form{background:#fff;border:0.5px solid #E0D9CC;border-radius:12px;padding:22px}
.nda-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:24px}
.nda-grid label{display:flex;flex-direction:column;font-size:12px;color:#6B6B6B;gap:5px}
.nda-grid input{font:inherit;font-size:14px;padding:9px 11px;border:0.5px solid #D9D2C5;border-radius:8px;background:#FBF9F5;color:#1A1A1A}
.nda-grid input:focus{outline:2px solid #C9A24B;outline-offset:1px}
.nda-hint{font-size:12px;color:#6B6B6B;margin:0 0 8px}
.sig-wrap{border:0.5px solid #D9D2C5;border-radius:10px;background:#FBF9F5;overflow:hidden;touch-action:none}
#sigPad{display:block;width:100%;height:auto;cursor:crosshair}
.sig-actions{display:flex;align-items:center;gap:14px;margin:10px 0 18px}
.nda-btnghost{font:inherit;font-size:13px;padding:6px 14px;border:0.5px solid #D9D2C5;background:#fff;border-radius:8px;cursor:pointer;color:#0B2B4D}
.nda-check{display:flex;gap:9px;align-items:flex-start;font-size:13px;line-height:1.55;color:#333;margin-bottom:18px}
.nda-check input{margin-top:3px}
.nda-btn{display:inline-block;font:inherit;font-size:15px;font-weight:500;padding:11px 26px;background:#0B2B4D;color:#fff;border:none;border-radius:10px;cursor:pointer;text-decoration:none}
.nda-btn:disabled{opacity:.45;cursor:not-allowed}
.nda-msg{font-size:13px;margin:12px 0 0;min-height:20px}
.nda-msg.err{color:#A32D2D}
.nda-done{background:#fff;border:0.5px solid #E0D9CC;border-radius:12px;padding:28px 24px;text-align:center}
.nda-done h2{font-size:19px;font-weight:500;color:#0B2B4D;margin:0 0 10px}
.nda-done p{font-size:14px;color:#444;margin:0 0 14px}
@media(max-width:640px){.nda-wrap{padding:16px 14px 48px}.nda-body{padding:16px;max-height:440px}}
</style>

<script>
(function(){
  var body=document.getElementById('ndaBody');
  var btnEn=document.getElementById('btnEn'), btnAr=document.getElementById('btnAr');
  function setLang(l){
    var cls=body.querySelectorAll('.nda-cl');
    for(var i=0;i<cls.length;i++){
      cls[i].hidden = (cls[i].getAttribute('data-lang')!==l);
    }
    btnEn.className='nda-lb'+(l==='en'?' is-on':'');
    btnAr.className='nda-lb'+(l==='ar'?' is-on':'');
  }
  if(btnEn) btnEn.onclick=function(){setLang('en');};
  if(btnAr) btnAr.onclick=function(){setLang('ar');};

  var cv=document.getElementById('sigPad');
  if(!cv) return;
  var ctx=cv.getContext('2d'), drawing=false, hasInk=false;
  var state=document.getElementById('sigState');
  var submit=document.getElementById('ndaSubmit');
  var chk=document.getElementById('agreeChk');
  var form=document.getElementById('ndaForm');
  var msg=document.getElementById('ndaMsg');

  function fit(){
    var r=window.devicePixelRatio||1;
    var w=cv.clientWidth||600, h=Math.round(w*0.3);
    if(!w) return;
    cv.width=Math.round(w*r); cv.height=Math.round(h*r);
    cv.style.height=h+'px';
    // 不 scale ctx：pos() 直接返回 canvas 内部像素坐标，线宽按 DPR 放大即可
    ctx.setTransform(1,0,0,1,0,0);
    ctx.lineWidth=2.2*r; ctx.lineCap='round'; ctx.lineJoin='round'; ctx.strokeStyle='#0B2B4D';
  }
  fit();
  // 不监听 resize 重设 canvas：改 cv.width 会清空已画内容，
  // 移动端键盘弹出或转屏会触发 resize，导致签名丢失。
  // 自适应由 CSS width:100% + pos() 的缩放换算负责。

  function pos(e){
    var r=cv.getBoundingClientRect();
    var p=(e.touches&&e.touches[0])?e.touches[0]:e;
    // CSS 显示尺寸 -> canvas 内部像素坐标 的缩放换算（不可省）
    var sx=cv.width/(r.width||1), sy=cv.height/(r.height||1);
    return {x:(p.clientX-r.left)*sx, y:(p.clientY-r.top)*sy};
  }
  function start(e){ e.preventDefault(); drawing=true; var q=pos(e); ctx.beginPath(); ctx.moveTo(q.x,q.y); }
  function move(e){ if(!drawing) return; e.preventDefault(); var q=pos(e); ctx.lineTo(q.x,q.y); ctx.stroke(); hasInk=true; sync(); }
  function end(){ drawing=false; }
  cv.addEventListener('mousedown',start); cv.addEventListener('mousemove',move);
  window.addEventListener('mouseup',end);
  cv.addEventListener('touchstart',start,{passive:false});
  cv.addEventListener('touchmove',move,{passive:false});
  cv.addEventListener('touchend',end);

  function sync(){
    if(state) state.textContent = hasInk?'Signed':'Not signed yet';
    if(submit) submit.disabled = !(hasInk && chk && chk.checked);
  }
  if(chk) chk.addEventListener('change',sync);
  document.getElementById('sigClear').onclick=function(){
    ctx.clearRect(0,0,cv.width,cv.height); hasInk=false; sync();
  };
  sync();

  form.addEventListener('submit', function(e){
    e.preventDefault();
    if(!hasInk){ msg.className='nda-msg err'; msg.textContent='Please sign in the box first.'; return; }
    document.getElementById('sigData').value = cv.toDataURL('image/png');
    document.getElementById('signedAt').value = new Date().toISOString();
    document.getElementById('pageUrl').value = location.href;
    submit.disabled=true; msg.textContent='Submitting…';
    var fd=new FormData(form);
    fetch(form.action,{method:'POST',body:fd,headers:{'Accept':'application/json'}})
      .then(function(r){
        if(!r.ok) throw new Error('http '+r.status);
        // 不能只看 content-type：FormSubmit 的 /ajax/ 端点返回 JSON body
        // 但 content-type 标的是 text/html。必须解析 body 本身判断成败，
        // 否则要么把失败当成功（危险），要么把成功当失败（当前这个坑）。
        return r.text();
      })
      .then(function(txt){
        var j=null;
        try{ j=JSON.parse(txt); }catch(e){}
        var ok = !!(j && (j.success==='true' || j.success===true));
        if(!ok) throw new Error('server rejected: '+txt.slice(0,80));
        document.getElementById('ndaDone').hidden=false;
        form.style.display='none';
      })
      .catch(function(err){
        msg.className='nda-msg err';
        msg.textContent='Submission did not go through. Please try again, or message us on WhatsApp: +971 58 585 4194';
        submit.disabled=false;
      });
  });
})();
</script>
'''


def main():
    html = page_shell(
        title='Sign our Mutual NDA | SourceToGulf',
        description='Read and sign the SourceToGulf mutual non-disclosure agreement online before sharing your apparel designs with us.',
        canonical=CANONICAL,
        body_inner=body_inner().replace('__CLAUSES__', clauses_html())
                              .replace('__FORM_ENDPOINT__', FORM_ENDPOINT),
        # NDA 页不需要 SEO，也不应被公开检索
        extra_head='<meta name="robots" content="noindex, nofollow" />\n',
        # 不做阿语版页面，因此不传 alt_ar（避免 hreflang 指向不存在的 URL）
    )
    out = os.path.join(APP, 'nda.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    print('OK wrote nda.html (%d bytes, %d clauses)' % (len(html), len(CLAUSES)))


if __name__ == '__main__':
    main()
