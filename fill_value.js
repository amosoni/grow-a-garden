const fs = require('fs');
const axios = require('axios');
const cheerio = require('cheerio');

// 1. 读取 plants_auto.js
const js = fs.readFileSync('plants_auto.js', 'utf-8');
const plants = eval(js.replace('const plants =', '').replace(';', ''));

// 2. 爬取 Wiki 作物价值
async function fetchValues() {
  const resp = await axios.get('https://growagarden.fandom.com/wiki/Crops', {
    headers: { 'User-Agent': 'Mozilla/5.0' }
  });
  const $ = cheerio.load(resp.data);
  const valueMap = {};
  $('tr').each((i, tr) => {
    const tds = $(tr).find('td');
    if (tds.length < 2) return;
    const name = $(tds[0]).text().trim().toLowerCase().replace(/[- _]/g, '');
    const valueText = $(tds[1]).text().trim();
    const m = valueText.match(/\$?([0-9,]+)/);
    if (m) valueMap[name] = parseInt(m[1].replace(/,/g, ''));
  });
  return valueMap;
}

(async () => {
  const valueMap = await fetchValues();
  plants.forEach(p => {
    p.value = valueMap[p.key] || 1;
  });
  fs.writeFileSync('plants_auto.js', 'const plants = ' + JSON.stringify(plants, null, 2) + ';\n', 'utf-8');
  console.log('已自动爬取Wiki并补全plants_auto.js的value字段。');
})();

