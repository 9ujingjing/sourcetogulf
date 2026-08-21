// fx.js — Real-time multi-currency landed prices for SourceToGulf
// Data: Frankfurter v2 (ECB daily reference rates). Keyless, CORS-open.
// Works on any page that contains .planded b / .pfob span (category pages).
// On other pages it does nothing (no price elements -> no UI, no fetch).
(function () {
  'use strict';

  var SYMS = {
    AE: { code: 'AED', name: 'UAE Dirham' },
    SA: { code: 'SAR', name: 'Saudi Riyal' },
    QA: { code: 'QAR', name: 'Qatar Riyal' },
    KW: { code: 'KWD', name: 'Kuwait Dinar' },
    BH: { code: 'BHD', name: 'Bahrain Dinar' },
    OM: { code: 'OMR', name: 'Oman Rial' }
  };
  var ENDPOINT = 'https://api.frankfurter.dev/v2/rates?base=USD&quotes=' +
    Object.keys(SYMS).map(function (k) { return SYMS[k].code; }).join(',');

  var rates = null;
  var today = new Date().toISOString().slice(0, 10);
  var cacheKey = 'stg_fx_' + today;

  function priceEls() {
    return document.querySelectorAll('.planded b, .pfob span');
  }

  function parseUSD(el) {
    var m = el.textContent.match(/\$?\s*([\d,]+\.?\d*)/);
    return m ? parseFloat(m[1].replace(/,/g, '')) : NaN;
  }

  function loadRates(cb) {
    try {
      var cached = localStorage.getItem(cacheKey);
      if (cached) { rates = JSON.parse(cached); return cb(); }
    } catch (e) {}
    fetch(ENDPOINT, { headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
      .then(function (rows) {
        rates = {};
        if (Array.isArray(rows)) {
          rows.forEach(function (row) { rates[row.quote] = row.rate; });
        }
        try { localStorage.setItem(cacheKey, JSON.stringify(rates)); } catch (e) {}
        cb();
      })
      .catch(function () { cb(); }); // keep USD on failure
  }

  function convert() {
    var sel = document.getElementById('fx-country');
    var cc = sel ? sel.value : 'US';
    var sym = (SYMS[cc] && SYMS[cc].code) || 'USD';
    var rate = (sym === 'USD' || !rates) ? 1 : (rates[sym] || 1);
    priceEls().forEach(function (el) {
      if (el.dataset.usd === undefined) {
        var u = parseUSD(el);
        if (isNaN(u)) return;
        el.dataset.usd = u;
      }
      var usd = parseFloat(el.dataset.usd);
      el.textContent = (sym === 'USD')
        ? ('$' + usd.toFixed(2))
        : (sym + ' ' + (usd * rate).toFixed(2));
    });
    var note = document.getElementById('fx-note');
    if (note) {
      note.textContent = (sym === 'USD')
        ? 'Prices shown in US dollars'
        : ('1 USD = ' + rate.toFixed(4) + ' ' + sym + ' · ECB daily');
    }
  }

  function injectUI() {
    if (!priceEls().length) return; // not a price page

    var style = document.createElement('style');
    style.textContent =
      '#fx-bar{position:fixed;bottom:22px;inset-inline-start:22px;z-index:60;' +
      'display:flex;align-items:center;gap:8px;background:#fff;border:1px solid #e7e1d8;' +
      'border-radius:999px;padding:8px 14px;box-shadow:0 6px 20px rgba(0,0,0,.12);' +
      'font:500 13px/1 Inter,system-ui,sans-serif;color:#222;max-width:calc(100vw - 44px)}' +
      '#fx-bar select{border:1px solid #d8d2c8;border-radius:8px;padding:4px 8px;' +
      'font:inherit;background:#fff;cursor:pointer}' +
      '#fx-bar #fx-note{color:#8a8276;font-size:11px}' +
      '@media(max-width:560px){#fx-bar #fx-note{display:none}}';
    document.head.appendChild(style);

    var bar = document.createElement('div');
    bar.id = 'fx-bar';
    bar.innerHTML =
      '<span class="fx-label">Price in</span>' +
      '<select id="fx-country" aria-label="Show price in your currency">' +
        '<option value="US">USD ($)</option>' +
        '<option value="AE">UAE — AED</option>' +
        '<option value="SA">Saudi — SAR</option>' +
        '<option value="QA">Qatar — QAR</option>' +
        '<option value="KW">Kuwait — KWD</option>' +
        '<option value="BH">Bahrain — BHD</option>' +
        '<option value="OM">Oman — OMR</option>' +
      '</select>' +
      '<span id="fx-note"></span>';
    document.body.appendChild(bar);

    var sel = bar.querySelector('#fx-country');
    try {
      var saved = localStorage.getItem('stg_fx_cc');
      if (saved && sel.querySelector('option[value="' + saved + '"]')) {
        sel.value = saved;
      }
    } catch (e) {}

    sel.addEventListener('change', function () {
      try { localStorage.setItem('stg_fx_cc', this.value); } catch (e) {}
      convert();
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    injectUI();
    loadRates(convert);
  });
})();
