const fs = require('fs');
const path = require('path');

const LANGS = ["zh-cn","ja","es","pt-br","fr","de","ru","ar","hi","id","vi"]; 

function read(file){ return fs.existsSync(file) ? fs.readFileSync(file,'utf8') : null; }
function write(file, content){ fs.mkdirSync(path.dirname(file), {recursive:true}); fs.writeFileSync(file, content, 'utf8'); }

// Noun dictionary used for dynamic sentences
const NOUNS = {
  salad: { 'zh-cn':'沙拉', 'ja':'サラダ' },
  pizza: { 'zh-cn':'披萨', 'ja':'ピザ' },
  cake:  { 'zh-cn':'蛋糕', 'ja':'ケーキ' },
  bread: { 'zh-cn':'面包', 'ja':'パン' },
  pie:   { 'zh-cn':'馅饼', 'ja':'パイ' },
  cookies: { 'zh-cn':'饼干', 'ja':'クッキー' },
  donut: { 'zh-cn':'甜甜圈', 'ja':'ドーナツ' }
};

// Common phrases that appear in article bodies
const MAP = {
  'Table of Contents': {
    'zh-cn':'目录','ja':'目次','es':'Tabla de contenidos','pt-br':'Índice','fr':'Table des matières','de':'Inhaltsverzeichnis','ru':'Содержание','ar':'جدول المحتويات','hi':'विषय-सूची','id':'Daftar isi','vi':'Mục lục'
  },
  'Basic Salad Making': {'zh-cn':'基础沙拉制作','ja':'基本的なサラダ作り','es':'Elaboración básica de ensalada','pt-br':'Preparo básico de salada','fr':'Préparation de salade de base','de':'Grundlegende Salatzubereitung','ru':'Базовое приготовление салата','ar':'تحضير السلطة الأساسي','hi':'बेसिक सलाद बनाना','id':'Membuat salad dasar','vi':'Làm salad cơ bản'},
  'Basic Pizza Making': {'zh-cn':'基础披萨制作','ja':'基本的なピザ作り','es':'Elaboración básica de pizza','pt-br':'Preparo básico de pizza','fr':'Préparation de pizza de base','de':'Grundlegende Pizzazubereitung','ru':'Базовое приготовление пиццы','ar':'تحضير البيتزا الأساسي','hi':'बेसिक पिज्ज़ा बनाना','id':'Membuat pizza dasar','vi':'Làm pizza cơ bản'},
  'Essential Ingredient List': {'zh-cn':'关键食材清单','ja':'必須食材リスト','es':'Lista de ingredientes esenciales','pt-br':'Lista de ingredientes essenciais','fr':'Liste des ingrédients essentiels','de':'Liste der wichtigsten Zutaten','ru':'Список основных ингредиентов','ar':'قائمة المكونات الأساسية','hi':'आवश्यक सामग्री सूची','id':'Daftar bahan penting','vi':'Danh sách nguyên liệu thiết yếu'},
  'Advanced Salad Recipes': {'zh-cn':'高级沙拉食谱','ja':'上級サラダレシピ','es':'Recetas de ensalada avanzadas','pt-br':'Receitas de salada avançadas','fr':'Recettes de salade avancées','de':'Fortgeschrittene Salatrezepte','ru':'Продвинутые рецепты салатов','ar':'وصفات سلطة متقدمة','hi':'उन्नत सलाद रेसिपी','id':'Resep salad lanjutan','vi':'Công thức salad nâng cao'},
  'Advanced Pizza Recipes': {'zh-cn':'高级披萨食谱','ja':'上級ピザレシピ','es':'Recetas de pizza avanzadas','pt-br':'Receitas de pizza avançadas','fr':'Recettes de pizza avancées','de':'Fortgeschrittene Pizzarezepte','ru':'Продвинутые рецепты пиццы','ar':'وصفات بيتزا متقدمة','hi':'उन्नत पिज्ज़ा रेसिपी','id':'Resep pizza lanjutan','vi':'Công thức pizza nâng cao'},
  'Making Tips & Tricks': {'zh-cn':'制作技巧与窍门','ja':'作成のコツ','es':'Consejos y trucos','pt-br':'Dicas e truques','fr':'Astuces de réalisation','de':'Tipps & Tricks','ru':'Советы и хитрости','ar':'نصائح وحيل','hi':'टिप्स और ट्रिक्स','id':'Tips & trik','vi':'Mẹo & thủ thuật'},
  'Efficiency Improvement Methods': {'zh-cn':'效率提升方法','ja':'効率改善の方法','es':'Métodos de mejora de eficiencia','pt-br':'Métodos de melhoria de eficiência','fr':'Méthodes d’amélioration de l’efficacité','de':'Methoden zur Effizienzsteigerung','ru':'Методы повышения эффективности','ar':'طرق تحسين الكفاءة','hi':'दक्षता सुधार विधियाँ','id':'Metode peningkatan efisiensi','vi':'Phương pháp cải thiện hiệu suất'},
  'Frequently Asked Questions': {'zh-cn':'常见问题','ja':'よくある質問','es':'Preguntas frecuentes','pt-br':'Perguntas frequentes','fr':'Questions fréquentes','de':'Häufig gestellte Fragen','ru':'Часто задаваемые вопросы','ar':'أسئلة شائعة','hi':'अक्सर पूछे जाने वाले प्रश्न','id':'Pertanyaan yang sering diajukan','vi':'Câu hỏi thường gặp'},
  'Basic Recipes': {'zh-cn':'基础配方','ja':'基本レシピ','es':'Recetas básicas','pt-br':'Receitas básicas','fr':'Recettes de base','de':'Grundrezepte','ru':'Базовые рецепты','ar':'وصفات أساسية','hi':'मूल विधियाँ','id':'Resep dasar','vi':'Công thức cơ bản'},
  'Making Steps:': {'zh-cn':'制作步骤：','ja':'作り方：','es':'Pasos de elaboración:','pt-br':'Etapas de preparo:','fr':'Étapes de réalisation :','de':'Herstellungsschritte:','ru':'Этапы приготовления:','ar':'خطوات التحضير:','hi':'बनाने के चरण:','id':'Langkah pembuatan:','vi':'Các bước thực hiện:'},
  'Home': {'zh-cn':'首页','ja':'ホーム','es':'Inicio','pt-br':'Início','fr':'Accueil','de':'Startseite','ru':'Главная','ar':'الصفحة الرئيسية','hi':'होम','id':'Beranda','vi':'Trang chủ'},
  'Guides': {'zh-cn':'攻略','ja':'ガイド','es':'Guías','pt-br':'Guias','fr':'Guides','de':'Guides','ru':'Гайды','ar':'الإرشادات','hi':'गाइड्स','id':'Panduan','vi':'Hướng dẫn'},
  'Back to Guides': {'zh-cn':'← 返回攻略','ja':'← ガイドに戻る','es':'← Volver a guías','pt-br':'← Voltar para guias','fr':'← Retour aux guides','de':'← Zurück zu den Guides','ru':'← Назад к гайдам','ar':'← الرجوع إلى الإرشادات','hi':'← गाइड्स पर वापस','id':'← Kembali ke panduan','vi':'← Quay lại mục hướng dẫn'},
  // Table headers
  'Pizza Name': {'zh-cn':'披萨名称','ja':'ピザ名','es':'Nombre de la pizza','pt-br':'Nome da pizza','fr':'Nom de la pizza','de':'Pizzaname','ru':'Название пиццы','ar':'اسم البيتزا','hi':'पिज़्ज़ा का नाम','id':'Nama pizza','vi':'Tên pizza'},
  'Required Ingredients': {'zh-cn':'所需食材','ja':'必要な材料','es':'Ingredientes requeridos','pt-br':'Ingredientes necessários','fr':'Ingrédients requis','de':'Erforderliche Zutaten','ru':'Необходимые ингредиенты','ar':'المكونات المطلوبة','hi':'आवश्यक सामग्री','id':'Bahan yang dibutuhkan','vi':'Nguyên liệu cần thiết'},
  'Making Time': {'zh-cn':'制作时间','ja':'調理時間','es':'Tiempo de preparación','pt-br':'Tempo de preparo','fr':'Temps de préparation','de':'Zubereitungszeit','ru':'Время приготовления','ar':'وقت التحضير','hi':'बनाने का समय','id':'Waktu pembuatan','vi':'Thời gian thực hiện'},
  'Reward Value': {'zh-cn':'奖励价值','ja':'報酬価値','es':'Valor de recompensa','pt-br':'Valor de recompensa','fr':'Valeur de récompense','de':'Belohnungswert','ru':'Награда','ar':'قيمة المكافأة','hi':'इनाम मूल्य','id':'Nilai hadiah','vi':'Giá trị phần thưởng'},
  'Difficulty': {'zh-cn':'难度','ja':'難易度','es':'Dificultad','pt-br':'Dificuldade','fr':'Difficulté','de':'Schwierigkeit','ru':'Сложность','ar':'الصعوبة','hi':'कठिनाई','id':'Kesulitan','vi':'Độ khó'},
  'Summary': {'zh-cn':'总结','ja':'まとめ','es':'Resumen','pt-br':'Resumo','fr':'Résumé','de':'Zusammenfassung','ru':'Итоги','ar':'الملخّص','hi':'सारांश','id':'Ringkasan','vi':'Tóm tắt'},
  'Next Steps': {'zh-cn':'下一步','ja':'次のステップ','es':'Siguientes pasos','pt-br':'Próximos passos','fr':'Prochaines étapes','de':'Nächste Schritte','ru':'Дальнейшие шаги','ar':'الخطوات التالية','hi':'अगले कदम','id':'Langkah berikutnya','vi':'Bước tiếp theo'},
  'Pro Tip:': {'zh-cn':'贴士：','ja':'プロのコツ：'},
  'Important:': {'zh-cn':'重要：','ja':'重要：'},
  // ingredient tiers
  'Basic Ingredients (Beginner Essential)': {'zh-cn':'基础食材（新手必备）','ja':'基本食材（初心者向け）'},
  'Advanced Ingredients (Intermediate Players)': {'zh-cn':'进阶食材（中级玩家）','ja':'上級食材（中級者）'},
  'Rare Ingredients (Expert Level)': {'zh-cn':'稀有食材（专家级）','ja':'希少食材（上級者）'},
  // salad specific table
  'Salad Name': {'zh-cn':'沙拉名称','ja':'サラダ名'},
  'Special Effect': {'zh-cn':'特殊效果','ja':'特別効果'}
};

function translateBody(html, lang){
  let out = html;
  for (const [en, langs] of Object.entries(MAP)){
    const tr = langs[lang]; if (!tr) continue;
    const re = new RegExp(en.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
    out = out.replace(re, tr);
  }
  return out;
}

function applyDynamic(html, lang, file){
  const slug = (file||'').replace(/\.html$/,'');
  const nounKey = slug.replace(/^how-to-make-/,'').replace(/^how-to-grow-/,'');
  const noun = (NOUNS[nounKey] && NOUNS[nounKey][lang]) || null;
  if (!noun) return html;
  let out = html;
  // Section headings generic
  out = out.replace(/Basic\s+[A-Za-z]+\s+Making/g, lang==='zh-cn'?`基础${noun}制作`:(lang==='ja'?`基本的な${noun}作り`:`Basic ${noun} Making`));
  out = out.replace(/Advanced\s+[A-Za-z]+\s+Recipes/g, lang==='zh-cn'?`高级${noun}食谱`:(lang==='ja'?`上級${noun}レシピ`:`Advanced ${noun} Recipes`));
  out = out.replace(/Premium\s+[A-Za-z]+\s+Recipes/g, lang==='zh-cn'?`豪华${noun}食谱`:(lang==='ja'?`プレミアム${noun}レシピ`:`Premium ${noun} Recipes`));
  out = out.replace(/[A-Za-z]+\s+Varieties\s*&\s*Types/g, lang==='zh-cn'?`${noun}种类与类型`:(lang==='ja'?`${noun}の種類`:`Varieties & Types`));

  // Hero subtitle pattern
  out = out.replace(/Complete Guide: From Dough Preparation to Topping Combinations/gi, lang==='zh-cn'?`完整指南：从面团准备到配料搭配`:(lang==='ja'?`完全ガイド：生地作りからトッピングの組み合わせまで`:`Complete Guide`));
  // Intro paragraph generic
  out = out.replace(/In Grow a Garden, [a-z\- ]+ making is one of the most popular and profitable crafting activities\.[^<]+/i,
    lang==='zh-cn'?`在 Grow a Garden 中，${noun}制作是最受欢迎且极具收益的玩法之一。通过种植并收集各种食材，在加工台中组合即可制作出美味的${noun}并获得可观奖励。`:
    (lang==='ja'?`Grow a Garden では、${noun}作りは最も人気があり収益性の高いクラフト要素のひとつです。さまざまな食材を育てて集め、メーカーで組み合わせることでおいしい${noun}を作り、たくさんの報酬を得られます。`:
    out));
  // Recipes section lead-in
  out = out.replace(/Different ingredient combinations can create [a-z\- ]+s of varying levels and effects\.[^<]+/i,
    lang==='zh-cn'?`不同的食材组合可以制作出不同等级与效果的${noun}。下表给出了详细配方：`:
    (lang==='ja'?`食材の組み合わせによって、さまざまなレベルや効果の${noun}を作れます。以下の表で詳しいレシピを確認してください：`:
    out));
  // Varieties section lead-in
  out = out.replace(/Grow a Garden features various [a-z\- ]+ types[^<]+/i,
    lang==='zh-cn'?`Grow a Garden 中包含多种${noun}类型，每种都有独特特性与奖励：`:
    (lang==='ja'?`${noun}には多くの種類があり、それぞれ特徴や報酬が異なります：`:
    out));
  // Tips section intro
  out = out.replace(/Master these tips to become a [a-z\- ]+\-making expert[^<]+/i,
    lang==='zh-cn'?`掌握这些技巧，你将很快成为${noun}制作高手：`:
    (lang==='ja'?`これらのコツを身につければ、${noun}作りの達人になれます：`:
    out));
  // Efficiency section intro
  out = out.replace(/Maximize your [a-z\- ]+\-making efficiency with these advanced strategies[^<]+/i,
    lang==='zh-cn'?`使用以下进阶策略，最大化${noun}制作的效率：`:
    (lang==='ja'?`以下の上級戦略で、${noun}作りの効率を最大化しましょう：`:
    out));

  // FAQ generics
  out = out.replace(/Q:\s*How long does it take to make a basic [a-z\- ]+\?/gi, lang==='zh-cn'?`问：制作基础${noun}需要多久？`:(lang==='ja'?`Q: 基本的な${noun}はどのくらいで作れますか？`:`Q:`));
  out = out.replace(/Q:\s*What’s the most profitable [a-z\- ]+ recipe\?/gi, lang==='zh-cn'?`问：哪种${noun}配方最赚钱？`:(lang==='ja'?`Q: 最も利益の高い${noun}のレシピは？`:`Q:`));
  out = out.replace(/Q:\s*Can I sell [a-z\- ]+s to other players\?/gi, lang==='zh-cn'?`问：可以把${noun}卖给其他玩家吗？`:(lang==='ja'?`Q: ${noun}を他のプレイヤーに販売できますか？`:`Q:`));
  out = out.replace(/Q:\s*How do I unlock rare ingredient recipes\?/gi, lang==='zh-cn'?`问：如何解锁稀有食材配方？`:(lang==='ja'?`Q: レア食材のレシピはどうやって解放しますか？`:`Q:`));

  return out;
}

function processLang(lang){
  const dir = path.join(process.cwd(), lang);
  if (!fs.existsSync(dir)) return;
  const files = fs.readdirSync(dir).filter(f=> /^(how-to-[a-z0-9-]+|ice-cream-recipe)\.html$/i.test(f));
  for (const f of files){
    const p = path.join(dir, f);
    const html = read(p); if (!html) continue;
    let translated = translateBody(html, lang);
    translated = applyDynamic(translated, lang, f);
    write(p, translated);
  }
}

function main(){
  for (const lang of LANGS){ processLang(lang); }
  console.log('Article bodies translated for common headings/labels (with dynamic paragraphs for zh-cn/ja).');
}

main(); 