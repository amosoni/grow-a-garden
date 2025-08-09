const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const LANGS = ["zh-cn","ja","es","pt-br","fr","de","ru","ar","hi","id","vi"];

function read(file){ return fs.existsSync(file) ? fs.readFileSync(file,'utf8') : null; }
function write(file, content){ fs.mkdirSync(path.dirname(file), {recursive:true}); fs.writeFileSync(file, content, 'utf8'); }

function listRootArticles(){
  return fs.readdirSync(process.cwd()).filter(f => /^(how-to-[a-z0-9-]+|ice-cream-recipe)\.html$/i.test(f));
}

function localizeLinks($, lang){
  $('a[href]').each((_,el)=>{
    const $a = $(el); const href = ($a.attr('href')||'').trim(); if (!href) return;
    if (/^guides\.html(?:#.*)?$/i.test(href)) $a.attr('href', `/${lang}/guides.html`);
    if (/^index\.html(?:#.*)?$/i.test(href)) $a.attr('href', `/${lang}/index.html`);
  });
}

function mergeArticle(lang, file){
  const rootHtml = read(path.join(process.cwd(), file));
  if (!rootHtml) return;
  const localPath = path.join(process.cwd(), lang, file);
  const locHtml = read(localPath) || '';

  const $root = cheerio.load(rootHtml);
  const $loc = cheerio.load(locHtml);

  // extract localized h1/p (if present)
  const locH1 = ($loc('h1').first().text()||'').trim();
  const locP  = ($loc('p').first().text()||'').trim();

  // set html lang
  $root('html').attr('lang', lang).attr('dir', lang==='ar'?'rtl':'ltr');

  // replace first h1/p in body with localized
  const firstH1 = $root('h1').first(); if (firstH1.length && locH1) firstH1.text(locH1);
  const firstP  = $root('p').first();  if (firstP.length && locP)  firstP.text(locP);

  // ensure back button points to localized guides
  const back = $root('a.back-btn').first();
  const backText = {
    'zh-cn':'← 返回攻略','ja':'← ガイドに戻る','es':'← Volver a guías','pt-br':'← Voltar para guias','fr':'← Retour aux guides','de':'← Zurück zu den Guides','ru':'← Назад к гайдам','ar':'← الرجوع إلى الإرشادات','hi':'← गाइड्स पर वापस','id':'← Kembali ke panduan','vi':'← Quay lại mục hướng dẫn'
  }[lang] || '← Back to Guides';
  if (back.length){ back.attr('href', `/${lang}/guides.html`).text(backText); }

  // localize common nav links
  localizeLinks($root, lang);

  write(localPath, $root.html());
}

function main(){
  const files = listRootArticles();
  for (const lang of LANGS){
    for (const f of files){ mergeArticle(lang, f); }
  }
  console.log('Localized articles composed from root with localized headings and links.');
}

main(); 