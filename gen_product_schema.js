// gen_product_schema.js
// 读取 products-data.js，按 products.html 完全相同的价格公式，
// 生成静态 ItemList + Product/Offer JSON-LD，注入 products.html（位于 </body> 前）。
// 用法：node gen_product_schema.js   （在 app 目录下运行）
// 重跑幂等：用标记 <!--PRODUCT-LD-START--> ... <!--PRODUCT-LD-END--> 包裹，已存在则替换。

const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const DATA_FILE = path.join(ROOT, 'products-data.js');
const HTML_FILE = path.join(ROOT, 'products.html');
const SITE = 'https://sourcetogulf.com';
const CNY_TO_USD = 7.15;

function cainiaoShipUSD(kg) {
  const cny = (kg <= 0.5) ? 68 : 68 + (kg - 0.5) * 45.6;
  return cny / CNY_TO_USD;
}

// 在隔离函数作用域内执行数据文件，取回变量
const code = fs.readFileSync(DATA_FILE, 'utf8');
const fn = new Function(code + '\n; return { PRODUCTS, CATEGORIES, PRODUCTS_UPDATED };');
const { PRODUCTS, CATEGORIES, PRODUCTS_UPDATED } = fn();

const catEn = {};
CATEGORIES.forEach(c => { catEn[c.key] = c.en; });

function priceOf(p) {
  const fob = p.fob_cny / CNY_TO_USD;
  const shipPerUnit = cainiaoShipUSD(p.moq * p.weight_kg) / p.moq;
  return { fob: fob, landed: fob + shipPerUnit };
}

const itemListElement = PRODUCTS.map((p, i) => {
  const pr = priceOf(p);
  return {
    '@type': 'ListItem',
    'position': i + 1,
    'item': {
      '@type': 'Product',
      'name': p.name_en,
      'image': SITE + p.img,
      'category': catEn[p.cat] || p.cat,
      'offers': {
        '@type': 'Offer',
        'priceCurrency': 'USD',
        'price': Number(pr.landed.toFixed(2)),
        'availability': 'https://schema.org/InStock',
        'minOrderQuantity': p.moq
      }
    }
  };
});

const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'ItemList',
  'name': 'SourceToGulf Hot Picks — Ready-to-Order Products with Landed Prices to the Gulf',
  'url': SITE + '/products.html',
  'numberOfItems': PRODUCTS.length,
  'itemListElement': itemListElement
};

const block = '<!--PRODUCT-LD-START-->\n<script type="application/ld+json">\n'
  + JSON.stringify(jsonLd, null, 2)
  + '\n</script>\n<!--PRODUCT-LD-END-->';

let html = fs.readFileSync(HTML_FILE, 'utf8');
const re = /<!--PRODUCT-LD-START-->[\s\S]*?<!--PRODUCT-LD-END-->/;
if (re.test(html)) {
  html = html.replace(re, block);
  console.log('已替换现有 JSON-LD 块');
} else {
  html = html.replace('</body>', block + '\n</body>');
  console.log('已新增强 JSON-LD 块');
}

fs.writeFileSync(HTML_FILE, html, 'utf8');
console.log('PRODUCTS=' + PRODUCTS.length + '  CATEGORIES=' + CATEGORIES.length + '  updated=' + PRODUCTS_UPDATED);
console.log('JSON-LD 字节数≈' + JSON.stringify(jsonLd).length);
