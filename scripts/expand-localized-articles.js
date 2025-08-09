const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const LANGS = ["zh-cn","ja","es","pt-br","fr","de","ru","ar","hi","id","vi"];

function read(file){ return fs.existsSync(file) ? fs.readFileSync(file,'utf8') : null; }
function write(file, content){ fs.mkdirSync(path.dirname(file), {recursive:true}); fs.writeFileSync(file, content, 'utf8'); }

function listRootArticles(){
  const files = fs.readdirSync(process.cwd());
  return files.filter(f=> /^(how-to-[a-z0-9-]+|ice-cream-recipe)\.html$/i.test(f));
}

function getRootMain(file){
  const html = read(path.join(process.cwd(), file));
  if (!html) return null;
  const $ = cheerio.load(html);
  const main = $('main').first();
  if (!main.length) return null;
  // Work on a wrapper to safely manipulate inner HTML
  const inner = main.html() || '';
  const $wrap = cheerio.load(`<div id="wrap">${inner}</div>`);
  const w = $wrap('#wrap');
  w.find('h1').first().remove();
  w.find('p').first().remove();
  return w.html() || '';
}

function ensureLangAttrs($, lang){
  $('html').attr('lang', lang);
  $('html').attr('dir', lang === 'ar' ? 'rtl' : 'ltr');
}

function ensureBackLink($, lang){
  const back = $('a.back-btn').first();
  const textMap = {
    'zh-cn':'← 返回攻略','ja':'← ガイドに戻る','es':'← Volver a guías','pt-br':'← Voltar para guias','fr':'← Retour aux guides','de':'← Zurück zu den Guides','ru':'← Назад к гайдам','ar':'← الرجوع إلى الإرشادات','hi':'← गाइड्स पर वापस','id':'← Kembali ke panduan','vi':'← Quay lại mục hướng dẫn'
  };
  const txt = textMap[lang] || '← Back to Guides';
  if (back.length){ back.attr('href', `/${lang}/guides.html`).text(txt); }
  else {
    const after = $('main').first();
    if (after.length){ after.append(`<a href="/${lang}/guides.html" class="back-btn">${txt}</a>`); }
  }
}

function processLang(lang){
  const articles = listRootArticles();
  for (const file of articles){
    const localPath = path.join(process.cwd(), lang, file);
    let html = read(localPath);
    if (!html) continue; // rely on other scripts to create stubs
    const $ = cheerio.load(html);
    ensureLangAttrs($, lang);

    const main = $('main').first();
    if (!main.length){
      $('body').append('<main></main>');
    }
    const rootRest = getRootMain(file) || '';
    // If localized file only has h1/p or is too short, append the rest
    const hasMore = $('main').find('*').length > 4; // heuristic
    if (!hasMore && rootRest){
      $('main').append(rootRest);
    }

    ensureBackLink($, lang);
    write(localPath, $.html());
  }
}

function main(){
  for (const lang of LANGS){ processLang(lang); }
  console.log('Localized article bodies expanded from root content where needed.');
}

main(); 