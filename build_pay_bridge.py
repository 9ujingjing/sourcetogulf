# -*- coding: utf-8 -*-
"""
收银入口桥接页 /pay.html（2026-11-06）

业务前提：SourceToGulf 是 sourcing agent，不是零售商。每笔 $125 sourcing
engagement 由人在 Ziina 生成一条专属定额链接；本页把那条链接包装成品牌域名下的
入口，客户在 sourcetogulf.com 上看到金额、参考号与付款方式，点击后跳到
Ziina 托管结账页完成付款。本页不收款、不自动扣款、不是结账接口。

URL：/pay.html?link=<Ziina 链接 ID>&ref=<STG 参考号>

工程约束：
  - 站点是静态 GitHub Pages；无后端、无 API key。
  - 主体内容全部 SSR（AI 与人都不依赖 JS），JS 只做参数校验、href 拼接、
    货币展示换算与语言切换（复用站点 MINI_JS 的 data-en/data-ar 机制）。
  - 🔴 页面专属 CSS 必须放第二个 <style> 块；sync_header_footer.py 只替换第一个。
  - 🔴 汇率来自 pricing.json 单一真相源，不硬编码；无汇率的币种不编造数字。
  - 🔴 不接受完整 URL 参数，只接受 ID 并拼到固定前缀，防开放重定向/钓鱼。
  - 🔴 noindex,nofollow；不进 sitemap。
  - 支付方式用自绘的简化品牌标记（品牌色 + 文字/几何），不抓取官方 logo 文件。
"""
import json
import os

from tpl_common import BASE, STYLE, HEADER, FOOTER, FLOAT_BTN, MINI_JS, GA4_SNIPPET

APP = os.path.dirname(os.path.abspath(__file__))
PRICING = json.load(open(os.path.join(APP, 'pricing.json'), encoding='utf-8'))

# 每 USD 兑本币；pricing.json 是唯一真相源
RATE_BY_CUR = {v['cur']: v['rate'] for v in PRICING['local_currency'].values()}
RATE_BY_CUR['USD'] = 1.0

CURRENCIES = ['AED', 'USD', 'EUR', 'GBP', 'INR', 'SAR', 'QAR', 'BHD', 'KWD', 'OMR']
RATES = {c: RATE_BY_CUR.get(c) for c in CURRENCIES}  # EUR/GBP/INR -> None，不编造
RATES_JSON = json.dumps(RATES, ensure_ascii=False)

ZINA_PURPLE = '#9B28EB'  # 实测自 pay.ziina.com 付款页源码
ZINA_PURPLE_DARK = '#8220C7'

OPTIONS = '\n'.join('          <option value="' + c + '">' + c + '</option>' for c in CURRENCIES)

STYLE2 = '''<style>
.pb-wrap{max-width:520px;margin:0 auto;padding:42px 18px 70px}
.pb-card{background:#fff;border:0.5px solid #e3e6ea;border-radius:16px;overflow:hidden}
.pb-strip{height:4px;background:__PURPLE__}
.pb-in{padding:28px 30px 26px}
.pb-top{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-bottom:16px;border-bottom:0.5px solid #eceef1}
.pb-brand{font-size:15px;font-weight:500;color:#17201c;letter-spacing:-.2px}
.pb-lang{font-size:12px;color:__PURPLE__;background:none;border:0.5px solid #eceef1;border-radius:8px;padding:6px 12px;cursor:pointer;font-family:inherit}
.pb-kicker{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:__PURPLE__;margin:22px 0 6px}
.pb-h1{font-size:22px;font-weight:500;line-height:1.3;color:#17201c;margin:0 0 8px}
.pb-sub{font-size:13px;line-height:1.6;color:#6b7570;margin:0 0 22px}
.pb-amount{background:#f8f5fd;border-radius:12px;padding:18px 20px;margin-bottom:14px}
.pb-amount-label{font-size:12px;color:#6b7570;margin-bottom:6px}
.pb-amount-row{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.pb-amount-num{font-size:28px;font-weight:500;color:#17201c;line-height:1.2;letter-spacing:-.5px}
.pb-cur{font-size:13px;font-family:inherit;color:#17201c;background:#fff;border:0.5px solid #d9dde2;border-radius:8px;padding:8px 10px;cursor:pointer}
.pb-amount-note{font-size:11.5px;line-height:1.55;color:#6b7570;margin:10px 0 0}
.pb-approx{font-size:11.5px;color:__PURPLE__;margin:6px 0 0;min-height:15px}
.pb-ref{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 14px;border:1px dashed #cfd6d2;border-radius:10px;margin-bottom:8px}
.pb-ref span{font-size:12px;color:#6b7570}
.pb-ref code{font-size:13px;color:#17201c;letter-spacing:.4px}
.pb-ref-note{font-size:11.5px;line-height:1.55;color:#6b7570;margin:0 0 22px}
.pb-label{font-size:12px;font-weight:500;color:#17201c;margin:0 0 10px}
.pb-methods{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px}
.pb-badge{width:62px;height:38px;border:0.5px solid #e3e6ea;border-radius:8px;display:flex;align-items:center;justify-content:center;gap:2px;font-size:10px;font-weight:500;background:#fff;flex:0 0 auto}
.pb-visa{color:#1a1f71;font-style:italic;font-size:15px;letter-spacing:-.5px}
.pb-mc{background:#fff}
.pb-mc i{width:19px;height:19px;border-radius:50%;display:block}
.pb-mc .r{background:#eb001b}
.pb-mc .o{background:#f79e1b;margin-left:-7px;opacity:.92}
.pb-amex{background:#2e77bc;color:#fff;border-color:#2e77bc;font-size:11px;letter-spacing:.3px}
.pb-apple{background:#111;color:#fff;border-color:#111;font-size:10.5px;gap:4px}
.pb-apple svg{display:block}
.pb-gpay{color:#3c4043;font-size:11px;gap:5px}
.pb-g{width:14px;height:14px;border-radius:50%;display:block;position:relative;background:conic-gradient(#ea4335 0 25%,#fbbc05 0 50%,#34a853 0 75%,#4285f4 0)}
.pb-g::after{content:"";position:absolute;inset:3px;border-radius:50%;background:#fff}
.pb-cur-line{font-size:11.5px;color:#6b7570;margin:-8px 0 22px;line-height:1.55}
.pb-btn{display:block;width:100%;box-sizing:border-box;text-align:center;padding:14px 18px;background:__PURPLE__;color:#fff;border:0.5px solid __PURPLE__;border-radius:10px;font-size:14px;font-weight:500;text-decoration:none;font-family:inherit;cursor:pointer;transition:background .15s}
.pb-btn:hover{background:__PURPLE_DARK__;border-color:__PURPLE_DARK__}
.pb-btn.is-disabled{background:#e9e2f2;border-color:#e9e2f2;color:#8b8197;cursor:not-allowed}
.pb-err{font-size:12px;color:#a32d2d;background:#fcebeb;border-radius:8px;padding:10px 12px;margin:12px 0 0;line-height:1.5}
.pb-trust{font-size:11.5px;line-height:1.6;color:#6b7570;margin:16px 0 0;padding-top:16px;border-top:0.5px solid #eceef1}
.pb-links{font-size:11.5px;margin:12px 0 0;color:#6b7570}
.pb-links a{color:__PURPLE__;text-decoration:none}
[dir="rtl"] .pb-amount-row,[dir="rtl"] .pb-ref{flex-direction:row-reverse}
[dir="rtl"] .pb-top{flex-direction:row-reverse}
@media(max-width:560px){.pb-wrap{padding:22px 12px 48px}.pb-in{padding:22px 20px}.pb-amount-num{font-size:24px}.pb-badge{width:56px}}
</style>'''.replace('__PURPLE_DARK__', ZINA_PURPLE_DARK).replace('__PURPLE__', ZINA_PURPLE)

BODY = '''<main class="pb-wrap">
  <div class="pb-card">
    <div class="pb-strip"></div>
    <div class="pb-in">
      <div class="pb-top">
        <span class="pb-brand">SourceToGulf</span>
        <button type="button" class="lang-btn pb-lang" data-en="العربية" data-ar="English">العربية</button>
      </div>

      <p class="pb-kicker" data-en="Secure checkout" data-ar="دفع آمن">Secure checkout</p>
      <h1 class="pb-h1" data-en="Pay the sourcing deposit" data-ar="ادفع مبلغ التوريد">Pay the sourcing deposit</h1>
      <p class="pb-sub" data-en="One fixed deposit starts your sourcing project. It is credited in full against your order value." data-ar="مبلغ ثابت واحد يبدأ مشروع التوريد، ويُخصم بالكامل من قيمة طلبك.">One fixed deposit starts your sourcing project. It is credited in full against your order value.</p>

      <div class="pb-amount">
        <div class="pb-amount-label" data-en="Amount due" data-ar="المبلغ المستحق">Amount due</div>
        <div class="pb-amount-row">
          <span class="pb-amount-num" id="pbAmount">AED 459.00</span>
          <select class="pb-cur" id="pbCur" aria-label="Display currency">
__OPTIONS__
          </select>
        </div>
        <p class="pb-amount-note" data-en="Fixed at AED 459 (USD 125). Your final currency is chosen on the Ziina checkout page." data-ar="المبلغ الثابت 459 درهماً (125 دولاراً). تُختار العملة النهائية في صفحة دفع Ziina.">Fixed at AED 459 (USD 125). Your final currency is chosen on the Ziina checkout page.</p>
        <p class="pb-approx" id="pbApprox"></p>
      </div>

      <div class="pb-ref">
        <span data-en="Your reference" data-ar="مرجعك">Your reference</span>
        <code id="pbRef">—</code>
      </div>
      <p class="pb-ref-note" data-en="Quote this reference in the payment note so we can match your deposit to your request." data-ar="اذكر هذا المرجع في ملاحظة الدفع كي نطابق المبلغ بطلبك.">Quote this reference in the payment note so we can match your deposit to your request.</p>

      <p class="pb-label" data-en="Accepted payment methods" data-ar="وسائل الدفع المقبولة">Accepted payment methods</p>
      <div class="pb-methods">
        <span class="pb-badge pb-visa" title="Visa">VISA</span>
        <span class="pb-badge pb-mc" title="Mastercard"><i class="r"></i><i class="o"></i></span>
        <span class="pb-badge pb-amex" title="American Express">AMEX</span>
        <span class="pb-badge pb-apple" title="Apple Pay"><svg viewBox="0 0 24 24" width="12" height="12" fill="#fff" aria-hidden="true"><path d="M17 12.5c0-2.2 1.8-3.3 1.9-3.4-1-1.5-2.6-1.7-3.2-1.7-1.3-.1-2.6.8-3.3.8-.7 0-1.7-.8-2.9-.8-1.5 0-2.9.9-3.7 2.2-1.6 2.7-.4 6.8 1.1 9 .8 1.1 1.7 2.3 2.9 2.2 1.2 0 1.6-.7 3-.7s1.8.7 3 .7c1.2 0 2-1.1 2.8-2.2.6-.9.9-1.7 1-1.9-2.2-.9-2.6-3.3-2.6-4.2zM14.8 5.4c.6-.8 1.1-1.9 1-3-1 0-2.2.7-2.9 1.5-.6.7-1.2 1.8-1 2.9 1.1.1 2.2-.6 2.9-1.4z"/></svg><span>Pay</span></span>
        <span class="pb-badge pb-gpay" title="Google Pay"><i class="pb-g"></i><span>Pay</span></span>
      </div>

      <p class="pb-cur-line" data-en="Also available: Ziina wallet. 10 currencies in the browser, Arabic checkout, settled in AED." data-ar="متاح أيضاً: محفظة Ziina. 10 عملات في المتصفح، ودفع بالعربية، والتسوية بالدرهم.">Also available: Ziina wallet. 10 currencies in the browser, Arabic checkout, settled in AED.</p>

      <a class="pb-btn" id="pbBtn" href="#" rel="noopener" data-en="Pay securely with Ziina →" data-ar="الدفع الآمن عبر Ziina ←">Pay securely with Ziina →</a>
      <p class="pb-err" id="pbErr" hidden data-en="This payment link is missing or invalid. Please ask us for a fresh link." data-ar="رابط الدفع غير صالح أو مفقود. اطلب منا رابطاً جديداً.">This payment link is missing or invalid. Please ask us for a fresh link.</p>

      <p class="pb-trust" data-en="Checkout is completed on Ziina's secure page. No automatic charge is ever made. A person reviews every request before work starts." data-ar="يتم الدفع على صفحة Ziina الآمنة. لا يُخصم أي مبلغ تلقائياً، ويراجع شخصٌ كل طلب قبل بدء العمل.">Checkout is completed on Ziina's secure page. No automatic charge is ever made. A person reviews every request before work starts.</p>
      <p class="pb-links"><a href="/service-terms.html">Service terms</a> · <a href="/refund-policy.html">Deposit policy</a> · <a href="/privacy.html">Privacy</a> · <a href="/services/sourcing-request.html">How sourcing works</a></p>
    </div>
  </div>
</main>'''.replace('__OPTIONS__', OPTIONS)

PAY_JS = '''<script>
(function(){
  var PREFIX = "https://pay.ziina.com/sourcetogulf/";
  var RATES = __RATES__;
  var BASE_USD = 125;
  var ID_RE = /^[A-Za-z0-9]{6,20}$/;
  var REF_RE = /^STG-[A-Za-z0-9]{6,12}$/;
  var q = new URLSearchParams(window.location.search);
  var link = (q.get("link") || "").trim();
  var ref = (q.get("ref") || "").trim();
  var btn = document.getElementById("pbBtn");
  var err = document.getElementById("pbErr");
  var refEl = document.getElementById("pbRef");

  if (REF_RE.test(ref)) { refEl.textContent = ref; }

  if (ID_RE.test(link)) {
    btn.setAttribute("href", PREFIX + link);
    btn.setAttribute("target", "_blank");
  } else {
    btn.setAttribute("href", "#");
    btn.setAttribute("aria-disabled", "true");
    btn.classList.add("is-disabled");
    err.hidden = false;
    btn.addEventListener("click", function(e){ e.preventDefault(); });
  }

  var sel = document.getElementById("pbCur");
  var num = document.getElementById("pbAmount");
  var approx = document.getElementById("pbApprox");
  sel.addEventListener("change", function(){
    var c = sel.value, r = RATES[c];
    if (c === "AED") {
      num.textContent = "AED 459.00";
      approx.textContent = "";
    } else if (r) {
      var v = BASE_USD * r;
      num.textContent = "\\u2248 " + c + " " + v.toLocaleString("en-US", {minimumFractionDigits:2, maximumFractionDigits:2});
      approx.textContent = "Indicative only \\u2014 Ziina sets the final amount at checkout.";
    } else {
      num.textContent = c + " \\u00b7 set at checkout";
      approx.textContent = "Indicative only \\u2014 Ziina sets the final amount at checkout.";
    }
  });
})();
</script>'''.replace('__RATES__', RATES_JSON)


def main():
    head = (
        '<!doctype html>\n<html lang="en" dir="ltr">\n<head>\n'
        '<meta charset="UTF-8" />\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
        '<title>Pay the sourcing deposit | SourceToGulf</title>\n'
        '<meta name="description" content="Pay the USD 125 (AED 459) sourcing deposit securely with Ziina. Cards, Apple Pay and Google Pay accepted." />\n'
        '<meta name="robots" content="noindex,nofollow" />\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Kufi+Arabic:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n'
        '<style>' + STYLE + '</style>\n'
        + STYLE2 + '\n'
        + GA4_SNIPPET + '\n'
        '</head>\n<body>\n'
        + '<header>\n' + HEADER + '\n</header>\n'
        + BODY + '\n'
        + '<footer>\n' + FOOTER + '\n</footer>\n'
        + FLOAT_BTN + '\n'
        + '<script>' + MINI_JS + '</script>\n'
        + PAY_JS + '\n'
        '</body>\n</html>'
    )
    out = os.path.join(APP, 'pay.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(head)
    print('-> pay.html (%d bytes)' % len(head))
    print('   RATES:', RATES_JSON)


if __name__ == '__main__':
    main()
