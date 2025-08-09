const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const LANGS = ["zh-cn","es","pt-br","fr","de","ru","ar","hi","id","vi","ja"]; // exclude 'en'

function read(p){ return fs.existsSync(p) ? fs.readFileSync(p,'utf8') : null; }
function write(p, c){ fs.mkdirSync(path.dirname(p), {recursive:true}); fs.writeFileSync(p, c, 'utf8'); }

function applyDict($, dict, lang){
  $('html').attr('lang', lang).attr('dir', lang==='ar'?'rtl':'ltr');
  $('[data-i18n]').each((_,el)=>{ const key = $(el).attr('data-i18n'); if (dict[key]) $(el).text(dict[key]); });
  $('[data-i18n-placeholder]').each((_,el)=>{ const key = $(el).attr('data-i18n-placeholder'); if (dict[key]) $(el).attr('placeholder', dict[key]); });
}

function rewriteLinks($, lang){
  $('a[href]').each((_,a)=>{
    const $a = $(a); const href = ($a.attr('href')||'').trim(); if (!href) return;
    if (/^(https?:)?\/\//i.test(href) || href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('#')) return;
    if (/^guides\.html$/i.test(href)) { $a.attr('href', `/${lang}/guides.html`); return; }
    if (/^index\.html$/i.test(href)) { $a.attr('href', `/${lang}/index.html`); return; }
    if (/^how-to-[a-z0-9-]+\.html$/i.test(href)) { $a.attr('href', `/${lang}/${href}`); return; }
  });
}

function localizeIndex(lang){
  const dictPath = path.join('i18n', `${lang}.json`);
  const dictRaw = read(dictPath); if (!dictRaw) return;
  const dict = JSON.parse(dictRaw);
  const root = read('index.html'); if (!root) return;
  const $ = cheerio.load(root);
  applyDict($, dict, lang);
  rewriteLinks($, lang);
  write(path.join(lang, 'index.html'), $.html());
}

function localizeGuides(lang){
  const dictPath = path.join('i18n', `${lang}.json`);
  const dictRaw = read(dictPath); if (!dictRaw) return;
  const dict = JSON.parse(dictRaw);
  // Prefer localized file produced by sync-guides
  const base = read(path.join(lang, 'guides.html')) || read('guides.html');
  if (!base) return;
  const $ = cheerio.load(base);
  applyDict($, dict, lang);
  rewriteLinks($, lang);
  write(path.join(lang, 'guides.html'), $.html());
}

function main(){
  for (const lang of LANGS){
    localizeIndex(lang);
    localizeGuides(lang);
  }
  console.log('Staticized index and guides for all languages.');
}

main(); 