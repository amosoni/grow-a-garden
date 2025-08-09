const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const LANGS = ["zh-cn","ja","es","pt-br","fr","de","ru","ar","hi","id","vi"]; 

function read(file){ return fs.existsSync(file) ? fs.readFileSync(file,'utf8') : null; }
function listHowTos(dir){
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir).filter(f=> /^(how-to-[a-z0-9-]+|ice-cream-recipe)\.html$/i.test(f));
}

function asciiRatio(text){
  const letters = (text||'').replace(/\s+/g,'');
  if (!letters.length) return 0;
  const ascii = letters.split('').filter(c=> c.charCodeAt(0) <= 127).length;
  return ascii / letters.length;
}

function containsEnglishPhrases(text){
  const patterns = [
    /Table of Contents/i, /Basic /i, /Advanced /i, /Making Steps/i, /Tips & Tricks/i,
    /Efficiency Improvement/i, /Frequently Asked Questions/i, /Next Steps/i,
    /minutes/i, /coins/i, /Guide/i
  ];
  return patterns.some(re=> re.test(text||''));
}

function auditFile(html){
  const $ = cheerio.load(html || '');
  const result = { asciiRatio: 0, englishHits: 0, sectionAscii: [] };
  const bodyText = $('body').text();
  result.asciiRatio = asciiRatio(bodyText);
  $('h1,h2,h3,p,li,th,td').each((_,el)=>{
    const t = $(el).text();
    const r = asciiRatio(t);
    if (r > 0.6) result.sectionAscii.push({ tag: el.tagName, sample: t.slice(0,120), ratio: +r.toFixed(2) });
    if (containsEnglishPhrases(t)) result.englishHits += 1;
  });
  return result;
}

function main(){
  const report = {};
  for (const lang of LANGS){
    report[lang] = {};
    const dir = path.join(process.cwd(), lang);
    const files = listHowTos(dir);
    for (const f of files){
      const html = read(path.join(dir, f));
      const res = auditFile(html);
      report[lang][f] = res;
    }
  }
  fs.writeFileSync('i18n.audit.report.json', JSON.stringify(report, null, 2), 'utf8');
  console.log('i18n.audit.report.json generated');
}

main(); 