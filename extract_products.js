// extract_products.js — 把 products-data.js 求值后导出为干净 JSON，供 Python 生成脚本使用
const fs = require('fs');
const path = require('path');
const file = path.join(__dirname, 'products-data.js');
const code = fs.readFileSync(file, 'utf8');
// 在独立作用域求值，拿到 CATEGORIES / PRODUCTS / PRODUCTS_UPDATED
const fn = new Function(code + '\n;return {CATEGORIES, PRODUCTS, PRODUCTS_UPDATED};');
const out = fn();
fs.writeFileSync(
  path.join(__dirname, 'products.clean.json'),
  JSON.stringify({ cats: out.CATEGORIES, prods: out.PRODUCTS, updated: out.PRODUCTS_UPDATED })
);
console.log('exported', out.PRODUCTS.length, 'products,', out.CATEGORIES.length, 'categories');
