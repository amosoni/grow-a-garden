const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const SUPPORTED = ["en","zh-cn","es","pt-br","fr","de","ru","ar","hi","id","vi","ja"];

function read(file){ return fs.existsSync(file) ? fs.readFileSync(file,'utf8') : null; }
function write(file, content){ fs.mkdirSync(path.dirname(file), {recursive:true}); fs.writeFileSync(file, content, 'utf8'); }

function extractHrefs(html){
  const $ = cheerio.load(html||'');
  const set = new Set();
  $('a.guide-item[href]').each((_,el)=>{
    let href = $(el).attr('href')||'';
    if (!href) return; if (!href.startsWith('/')) href = '/' + href;
    set.add(href);
  });
  return Array.from(set);
}

function buildStubArticle(title){
  return `<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <title>${title}</title>\n  <link rel="stylesheet" href="/styles.css">\n</head>\n<body>\n  <main>\n    <h1>${title}</h1>\n    <p>Placeholder content. Please localize this article.</p>\n  </main>\n  <script src="/i18n/i18n.js"></script>\n</body>\n</html>`;
}

function main(){
  const rootGuides = read(path.join(process.cwd(), 'guides.html'));
  if (!rootGuides) { console.error('guides.html not found'); process.exit(1); }
  const allHrefs = extractHrefs(rootGuides);
  const report = {};

  for (const lang of SUPPORTED){
    if (lang==='en') continue;
    const localizedFile = path.join(process.cwd(), lang, 'guides.html');
    const html = read(localizedFile);
    const hrefsLocal = extractHrefs(html||'');
    const missingInLocalized = allHrefs.filter(h=> !hrefsLocal.includes(h));
    report[lang] = { missing: missingInLocalized };

    // 1) Generate stubs for ALL canonical hrefs (root list)
    allHrefs.forEach(h=>{
      const slug = h.replace(/^\//,'');
      if (!/^how-to-/.test(slug) && slug !== 'ice-cream-recipe.html') return;
      const target = path.join(process.cwd(), lang, slug);
      if (!fs.existsSync(target)){
        const title = slug.replace(/-/g,' ').replace(/\.html$/,'');
        write(target, buildStubArticle(title));
      }
    });

    // 2) Also generate for any extra hrefs that exist only in localized guides
    hrefsLocal.forEach(h=>{
      const slug = h.replace(/^\//,'');
      if (!/^how-to-/.test(slug) && slug !== 'ice-cream-recipe.html') return;
      const target = path.join(process.cwd(), lang, slug);
      if (!fs.existsSync(target)){
        const title = slug.replace(/-/g,' ').replace(/\.html$/,'');
        write(target, buildStubArticle(title));
      }
    });

    // Ensure localized guides.html exists; if missing, copy English as base
    if (!html){
      write(localizedFile, rootGuides);
    }
  }

  // Write report
  write(path.join(process.cwd(), 'missing.i18n.report.json'), JSON.stringify(report, null, 2));
  console.log('Missing i18n report written to missing.i18n.report.json');
}

main(); 