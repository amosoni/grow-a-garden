const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const SUPPORTED = ["en","zh-cn","es","pt-br","fr","de","ru","ar","hi","id","vi","ja"];

function read(file){ return fs.existsSync(file) ? fs.readFileSync(file,'utf8') : null; }
function write(file, content){ fs.mkdirSync(path.dirname(file), {recursive:true}); fs.writeFileSync(file, content, 'utf8'); }
const norm = (h)=>{ if(!h) return ''; return h.startsWith('/') ? h : ('/' + h); };

function loadRoot(){
  const root = read('guides.html');
  if (!root) throw new Error('guides.html not found');
  const $ = cheerio.load(root);
  // Map href -> {anchorHtml, categoryKey}
  const map = new Map();
  $('.category-section, .guides-card').each((_,sec)=>{
    const $sec = $(sec);
    const catKey = $sec.attr('data-category') || 'trending';
    $sec.find('a.guide-item[href]').each((__,a)=>{
      const href = norm($(a).attr('href'));
      map.set(href, { catKey, html: $.html(a) });
    });
  });
  // Build quick-tips block reference and section templates by key for cloning
  const sectionsByKey = {};
  $('.category-section[data-category]').each((_,sec)=>{
    const key = $(sec).attr('data-category');
    sectionsByKey[key] = $.html(sec);
  });
  const quickTipsCard = $('h2').filter((_,el)=>/Quick Tips/i.test($(el).text())).first().closest('.guides-card');
  const quickTipsHtml = quickTipsCard.length ? $.html(quickTipsCard) : '';
  return {rootHtml: root, map, sectionsByKey, quickTipsHtml};
}

function getLocalArticleText(lang, href){
  const slug = href.replace(/^\//,'');
  const file = path.join(lang, slug);
  const html = read(file);
  if (!html) return null;
  const $ = cheerio.load(html);
  const title = $('h1').first().text().trim();
  const desc = ($('main p').first().text() || $('p').first().text() || '').trim();
  return {title, desc};
}

function localizeMeta($, lang){
  const DIFF = {
    'zh-cn': {Beginner:'初级', Intermediate:'中级', Advanced:'高级', Expert:'专家'},
    'ja': {Beginner:'初心者', Intermediate:'中級', Advanced:'上級', Expert:'エキスパート'},
    'es': {Beginner:'Principiante', Intermediate:'Intermedio', Advanced:'Avanzado', Expert:'Experto'},
    'pt-br': {Beginner:'Iniciante', Intermediate:'Intermediário', Advanced:'Avançado', Expert:'Especialista'},
    'fr': {Beginner:'Débutant', Intermediate:'Intermédiaire', Advanced:'Avancé', Expert:'Expert'},
    'de': {Beginner:'Anfänger', Intermediate:'Mittelstufe', Advanced:'Fortgeschritten', Expert:'Experte'},
    'ru': {Beginner:'Новичок', Intermediate:'Средний', Advanced:'Продвинутый', Expert:'Эксперт'},
    'ar': {Beginner:'مبتدئ', Intermediate:'متوسط', Advanced:'متقدم', Expert:'خبير'},
    'hi': {Beginner:'शुरुआती', Intermediate:'मध्यम', Advanced:'उन्नत', Expert:'विशेषज्ञ'},
    'id': {Beginner:'Pemula', Intermediate:'Menengah', Advanced:'Lanjutan', Expert:'Ahli'},
    'vi': {Beginner:'Mới bắt đầu', Intermediate:'Trung cấp', Advanced:'Nâng cao', Expert:'Chuyên gia'}
  };
  const RT = {
    'zh-cn': s=> s.replace(/(\d+)\s*min\s*read/i, '$1 分钟读完'),
    'ja': s=> s.replace(/(\d+)\s*min\s*read/i, '$1分読了'),
    'es': s=> s.replace(/(\d+)\s*min\s*read/i, '$1 min'),
    'pt-br': s=> s.replace(/(\d+)\s*min\s*read/i, '$1 min'),
    'fr': s=> s.replace(/(\d+)\s*min\s*read/i, '$1 min'),
    'de': s=> s.replace(/(\d+)\s*min\s*read/i, '$1 Min'),
    'ru': s=> s.replace(/(\d+)\s*min\s*read/i, '$1 мин'),
    'ar': s=> s.replace(/(\d+)\s*min\s*read/i, '$1 دقيقة قراءة'),
    'hi': s=> s.replace(/(\d+)\s*min\s*read/i, '$1 मिनट'),
    'id': s=> s.replace(/(\d+)\s*min\s*read/i, '$1 mnt'),
    'vi': s=> s.replace(/(\d+)\s*min\s*read/i, '$1 phút')
  };
  const diffMap = DIFF[lang] || {};
  $('.guide-difficulty').each((_,el)=>{
    const $el = $(el); const t = ($el.text()||'').trim(); if (diffMap[t]) $el.text(diffMap[t]);
  });
  const fmt = RT[lang];
  if (fmt){ $('.guide-read-time').each((_,el)=>{ const $el=$(el); $el.text(fmt(($el.text()||'').trim())); }); }
}

function ensureGuides(lang, rootMap, rootSections, quickTipsHtml){
  const file = path.join(lang, 'guides.html');
  let html = read(file);
  if (!html) html = read('guides.html'); // copy english if missing
  const $ = cheerio.load(html);

  // Ensure category sections exist by cloning from root when missing
  const ORDER = ['recipe','farming','co-op','profit','advanced'];
  const SEC_TITLE = {
    'recipe': {
      'zh-cn':'🍽️ 食谱攻略','ja':'🍽️ レシピガイド','es':'🍽️ Guías de recetas','pt-br':'🍽️ Guias de receitas','fr':'🍽️ Guides de recettes','de':'🍽️ Rezept-Guides','ru':'🍽️ Руководства по рецептам','ar':'🍽️ أدلة الوصفات','hi':'🍽️ रेसिपी गाइड','id':'🍽️ Panduan resep','vi':'🍽️ Hướng dẫn công thức'
    },
    'farming': {
      'zh-cn':'🌱 种植攻略','ja':'🌱 農業ガイド','es':'🌱 Guías de cultivo','pt-br':'🌱 Guias de agricultura','fr':'🌱 Guides d’agriculture','de':'🌱 Landwirtschaft-Guides','ru':'🌱 Руководства по фермерству','ar':'🌱 أدلة الزراعة','hi':'🌱 खेती गाइड','id':'🌱 Panduan bertani','vi':'🌱 Hướng dẫn nông nghiệp'
    },
    'co-op': {
      'zh-cn':'👥 协作与运营','ja':'👥 協力と運用','es':'👥 Cooperación y operaciones','pt-br':'👥 Cooperação e operações','fr':'👥 Coop & opérations','de':'👥 Kooperation & Betrieb','ru':'👥 Совместная игра и операции','ar':'👥 التعاون والتشغيل','hi':'👥 सहयोग व संचालन','id':'👥 Ko-op & Operasi','vi':'👥 Hợp tác & vận hành'
    },
    'profit': {
      'zh-cn':'💰 利润优化','ja':'💰 利益ガイド','es':'💰 Optimización de ganancias','pt-br':'💰 Otimização de lucro','fr':'💰 Optimisation du profit','de':'💰 Gewinnoptimierung','ru':'💰 Оптимизация прибыли','ar':'💰 تحسين الأرباح','hi':'💰 लाभ अनुकूलन','id':'💰 Optimasi profit','vi':'💰 Tối ưu lợi nhuận'
    },
    'advanced': {
      'zh-cn':'🎮 高级攻略','ja':'🎮 上級ガイド','es':'🎮 Guías avanzadas','pt-br':'🎮 Guias avançados','fr':'🎮 Guides avancés','de':'🎮 Fortgeschrittene Guides','ru':'🎮 Продвинутые руководства','ar':'🎮 أدلة متقدمة','hi':'🎮 उन्नत गाइड','id':'🎮 Panduan lanjutan','vi':'🎮 Hướng dẫn nâng cao'
    }
  };

  const container = $('.guides-section').first();
  ORDER.forEach(key=>{
    const has = $(`.category-section[data-category="${key}"]`).length>0;
    if (!has && rootSections[key] && container.length){
      // append clone from root and localize title
      container.append(rootSections[key]);
      const sec = $(`.category-section[data-category="${key}"]`).last();
      const h2 = sec.find('.category-title').first();
      const map = SEC_TITLE[key] || {};
      if (h2.length && map[lang]) h2.text(map[lang]);
    }
  });

  // Ensure Quick Tips exists
  const hasQuick = $('h2').filter((_,el)=>/Quick Tips|クイック|Consejos|Dicas|Astuces|Kurztipps|советы|نصائح|सुझाव|Tips cepat|Mẹo/i.test($(el).text())).length>0;
  if (!hasQuick && quickTipsHtml && container.length){
    container.append(quickTipsHtml);
  }

  // Ensure Back button exists at the end of guides-section
  const BACK = {
    'en':'← Back to Main Calculator','zh-cn':'← 返回主计算器','ja':'← メイン計算機に戻る','es':'← Volver a la calculadora principal','pt-br':'← Voltar para a calculadora principal','fr':'← Retour à la calculatrice principale','de':'← Zur Hauptkalkulation zurück','ru':'← Назад к основному калькулятору','ar':'← العودة إلى الحاسبة الرئيسية','hi':'← मुख्य कैलकुलेटर पर वापस','id':'← Kembali ke kalkulator utama','vi':'← Quay về máy tính chính'
  };
  const backBtn = $('.guides-section .back-btn').first();
  if (container.length && backBtn.length === 0){
    const txt = BACK[lang] || BACK['en'];
    container.append(`<a href="index.html" class="back-btn" data-i18n="guides.back">${txt}</a>`);
  } else if (backBtn.length) {
    const txt = BACK[lang] || BACK['en'];
    backBtn.text(txt);
    backBtn.attr('data-i18n','guides.back');
  }

  // Build section index by data-category
  function findSection(catKey){
    let sec = $(`.category-section[data-category="${catKey}"]`);
    if (sec.length===0 && catKey==='trending') sec = $('.guides-card').first();
    return sec.first();
  }

  const had = new Set();
  $('a.guide-item[href]').each((_,a)=> had.add(norm($(a).attr('href'))));

  for (const [href, rec] of rootMap.entries()){
    if (had.has(href)) continue;
    const sec = findSection(rec.catKey);
    if (sec.length===0) continue;
    const $anchor = cheerio.load(rec.html)('a');
    // Try to localize from article stub
    const t = getLocalArticleText(lang, href);
    if (t){
      const h3 = $anchor.find('h3').first(); if (t.title) h3.text(t.title);
      const p = $anchor.find('p').first(); if (t.desc) p.text(t.desc);
    }
    // Insert into section's .guides-grid or directly
    const grid = sec.find('.guides-grid').first();
    if (grid.length) grid.append($anchor);
    else sec.append($anchor);
  }

  // Localize difficulty/read-time across the file
  localizeMeta($, lang);

  // Normalize guide-item hrefs to language-prefixed paths so navigation is static and correct
  $('a.guide-item[href]').each((_,el)=>{
    const $a = $(el);
    let href = ($a.attr('href')||'').trim();
    if (!href) return;
    const bare = href.replace(/^\//,'');
    if (/^(how-to-[a-z0-9-]+\.html|ice-cream-recipe\.html)$/i.test(bare)){
      // avoid double prefix
      if (!bare.startsWith(lang + '/')){
        $a.attr('href', `/${lang}/${bare}`);
      }
    }
  });

  write(file, $.html());
}

function main(){
  const {map, sectionsByKey, quickTipsHtml} = loadRoot();
  for (const lang of SUPPORTED){
    if (lang==='en') continue;
    ensureGuides(lang, map, sectionsByKey, quickTipsHtml);
  }
  console.log('Localized guides synchronized.');
}

main(); 