const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

function read(file){ return fs.existsSync(file) ? fs.readFileSync(file,'utf8') : null; }
function write(file, content){ fs.mkdirSync(path.dirname(file), {recursive:true}); fs.writeFileSync(file, content, 'utf8'); }
const norm = (h)=>{ if(!h) return ''; return h.startsWith('/') ? h : ('/' + h); };

const LANGS = ["zh-cn","ja","es","pt-br","fr","de","ru","ar","hi","id","vi"];

const nouns = {
  'salad': { 'zh-cn':'沙拉', 'ja':'サラダ', 'es':'Ensalada', 'pt-br':'Salada', 'fr':'Salade', 'de':'Salat', 'ru':'Салат', 'ar':'سلطة', 'hi':'सलाद', 'id':'Salad', 'vi':'Salad' },
  'pizza': { 'zh-cn':'披萨', 'ja':'ピザ', 'es':'Pizza', 'pt-br':'Pizza', 'fr':'Pizza', 'de':'Pizza', 'ru':'Пицца', 'ar':'بيتزا', 'hi':'पिज़्ज़ा', 'id':'Pizza', 'vi':'Pizza' },
  'bread': { 'zh-cn':'面包', 'ja':'パン', 'es':'Pan', 'pt-br':'Pão', 'fr':'Pain', 'de':'Brot', 'ru':'Хлеб', 'ar':'خبز', 'hi':'ब्रेड', 'id':'Roti', 'vi':'Bánh mì' },
  'cake': { 'zh-cn':'蛋糕', 'ja':'ケーキ', 'es':'Pastel', 'pt-br':'Bolo', 'fr':'Gâteau', 'de':'Kuchen', 'ru':'Торт', 'ar':'كيك', 'hi':'केक', 'id':'Kue', 'vi':'Bánh kem' },
  'pie': { 'zh-cn':'馅饼', 'ja':'パイ', 'es':'Pastel', 'pt-br':'Torta', 'fr':'Tarte', 'de':'Kuchen', 'ru':'Пирог', 'ar':'فطيرة', 'hi':'पाई', 'id':'Pai', 'vi':'Bánh pie' },
  'cookie': { 'zh-cn':'饼干', 'ja':'クッキー', 'es':'Galleta', 'pt-br':'Biscoito', 'fr':'Cookie', 'de':'Keks', 'ru':'Печенье', 'ar':'بسكويت', 'hi':'कुकी', 'id':'Kue kering', 'vi':'Bánh quy' },
  'smoothie': { 'zh-cn':'冰沙', 'ja':'スムージー', 'es':'Batido', 'pt-br':'Smoothie', 'fr':'Smoothie', 'de':'Smoothie', 'ru':'Смузи', 'ar':'سموذي', 'hi':'स्मूदी', 'id':'Smoothie', 'vi':'Sinh tố' },
  'sandwich': { 'zh-cn':'三明治', 'ja':'サンドイッチ', 'es':'Sándwich', 'pt-br':'Sanduíche', 'fr':'Sandwich', 'de':'Sandwich', 'ru':'Сэндвич', 'ar':'شطيرة', 'hi':'सैंडविच', 'id':'Roti lapis', 'vi':'Bánh mì kẹp' },
  'wheat': { 'zh-cn':'小麦', 'ja':'小麦', 'es':'Trigo', 'pt-br':'Trigo', 'fr':'Blé', 'de':'Weizen', 'ru':'Пшеница', 'ar':'قمح', 'hi':'गेहूं', 'id':'Gandum', 'vi':'Lúa mì' },
  'carrot': { 'zh-cn':'胡萝卜', 'ja':'ニンジン', 'es':'Zanahoria', 'pt-br':'Cenoura', 'fr':'Carotte', 'de':'Karotte', 'ru':'Морковь', 'ar':'جزر', 'hi':'गाजर', 'id':'Wortel', 'vi':'Cà rốt' },
  'apple': { 'zh-cn':'苹果', 'ja':'リンゴ', 'es':'Manzana', 'pt-br':'Maçã', 'fr':'Pomme', 'de':'Apfel', 'ru':'Яблоко', 'ar':'تفاح', 'hi':'सेब', 'id':'Apel', 'vi':'Táo' },
  'orange': { 'zh-cn':'橙子', 'ja':'オレンジ', 'es':'Naranja', 'pt-br':'Laranja', 'fr':'Orange', 'de':'Orange', 'ru':'Апельсин', 'ar':'برتقال', 'hi':'संतरा', 'id':'Jeruk', 'vi':'Cam' },
  'berries': { 'zh-cn':'莓果', 'ja':'ベリー', 'es':'Bayas', 'pt-br':'Frutas vermelhas', 'fr':'Baies', 'de':'Beeren', 'ru':'Ягоды', 'ar':'توت', 'hi':'बेरी', 'id':'Beri', 'vi':'Dâu' },
  'corn': { 'zh-cn':'玉米', 'ja':'トウモロコシ', 'es':'Maíz', 'pt-br':'Milho', 'fr':'Maïs', 'de':'Mais', 'ru':'Кукуруза', 'ar':'ذرة', 'hi':'मकई', 'id':'Jagung', 'vi':'Ngô' },
  'farm': { 'zh-cn':'农场', 'ja':'農場', 'es':'Granja', 'pt-br':'Fazenda', 'fr':'Ferme', 'de':'Farm', 'ru':'Ферма', 'ar':'مزرعة', 'hi':'फ़ार्म', 'id':'Pertanian', 'vi':'Trang trại' },
  'donut': {
    'zh-cn': '甜甜圈', 'ja': 'ドーナツ', 'es': 'donas', 'pt-br': 'rosquinhas', 'fr': 'beignets', 'de': 'Donut', 'ru': 'пончик', 'ar': 'دونات', 'hi': 'डोनट', 'id': 'donat', 'vi': 'bánh donut'
  },
  'doughnut': {
    'zh-cn': '甜甜圈', 'ja': 'ドーナツ', 'es': 'donas', 'pt-br': 'rosquinhas', 'fr': 'beignets', 'de': 'Donut', 'ru': 'пончик', 'ar': 'دونات', 'hi': 'डोनट', 'id': 'donat', 'vi': 'bánh donut'
  }
};

const patterns = {
  make: { 'zh-cn':'{noun}制作指南', 'ja':'{noun}作りのガイド', 'es':'Guía de {noun}', 'pt-br':'Guia de {noun}', 'fr':'Guide {noun}', 'de':'{noun}-Guide', 'ru':'Гайд по {noun}', 'ar':'دليل صنع {noun}', 'hi':'{noun} बनाने की गाइड', 'id':'Panduan {noun}', 'vi':'Hướng dẫn làm {noun}' },
  grow: { 'zh-cn':'{noun}栽培指南', 'ja':'{noun}栽培ガイド', 'es':'Guía de cultivo de {noun}', 'pt-br':'Guia de cultivo de {noun}', 'fr':'Guide de culture de {noun}', 'de':'{noun}-Anbau-Guide', 'ru':'Гайд по выращиванию {noun}', 'ar':'دليل زراعة {noun}', 'hi':'{noun} उगाने की गाइड', 'id':'Panduan menanam {noun}', 'vi':'Hướng dẫn trồng {noun}' },
  money: { 'zh-cn':'快速赚钱指南', 'ja':'早くお金を稼ぐガイド', 'es':'Guía para ganar dinero rápido', 'pt-br':'Guia para ganhar dinheiro rápido', 'fr':'Guide pour gagner de l’argent rapidement', 'de':'Schnell Geld verdienen – Guide', 'ru':'Гайд по быстрому заработку', 'ar':'دليل كسب المال بسرعة', 'hi':'जल्दी पैसे कमाने की गाइड', 'id':'Panduan menghasilkan uang cepat', 'vi':'Hướng dẫn kiếm tiền nhanh' },
  friends: { 'zh-cn':'与好友一起玩', 'ja':'友達と遊ぶ', 'es':'Jugar con amigos', 'pt-br':'Jogar com amigos', 'fr':'Jouer avec des amis', 'de':'Mit Freunden spielen', 'ru':'Играть с друзьями', 'ar':'اللعب مع الأصدقاء', 'hi':'दोस्तों के साथ खेलें', 'id':'Bermain dengan teman', 'vi':'Chơi với bạn bè' },
  storage: { 'zh-cn':'存储与物流', 'ja':'保管と物流', 'es':'Almacenamiento y logística', 'pt-br':'Armazenamento e logística', 'fr':'Stockage et logistique', 'de':'Lagerung & Logistik', 'ru':'Хранение и логистика', 'ar':'التخزين واللوجستيات', 'hi':'भंडारण और लॉजिस्टिक्स', 'id':'Penyimpanan & Logistik', 'vi':'Lưu trữ & hậu cần' }
};

function translateTitle(lang, slug){
  const s = slug.replace(/^\//,'').replace(/\.html$/,'');
  if (s.startsWith('how-to-make-')){
    let key = s.replace('how-to-make-','');
    if (!nouns[key]){
      if (key === 'cookies') key = 'cookie';
      else if (key.endsWith('ies')) key = key.slice(0,-3)+'y';
      else if (key.endsWith('s')) key = key.slice(0,-1);
      if (!nouns[key] && key.endsWith('ughnut')) key = 'doughnut';
    }
    const noun = nouns[key] && nouns[key][lang];
    if (noun) return patterns.make[lang].replace('{noun}', noun);
  }
  if (s.startsWith('how-to-grow-')){
    let key = s.replace('how-to-grow-','');
    if (!nouns[key]){
      if (key === 'cookies') key = 'cookie';
      else if (key.endsWith('ies')) key = key.slice(0,-3)+'y';
      else if (key.endsWith('s')) key = key.slice(0,-1);
      if (!nouns[key] && key.endsWith('ughnut')) key = 'doughnut';
    }
    const noun = nouns[key] && nouns[key][lang];
    if (noun) return patterns.grow[lang].replace('{noun}', noun);
  }
  const staticMap = {
    'how-to-make-money-fast': 'money',
    'how-to-play-with-friends': 'friends',
    'storage-and-logistics': 'storage'
  };
  if (staticMap[s]) return patterns[staticMap[s]][lang];
  // static guides
  const staticTitles = {
    'farming-basics': { 'zh-cn':'种植基础', 'ja':'栽培の基礎', 'es':'Conceptos básicos de cultivo', 'pt-br':'Noções básicas de agricultura', 'fr':'Bases de l’agriculture', 'de':'Grundlagen der Landwirtschaft', 'ru':'Основы земледелия', 'ar':'أساسيات الزراعة', 'hi':'खेती की बुनियादी बातें', 'id':'Dasar-dasar pertanian', 'vi':'Cơ bản về canh tác' },
    'watering-strategies': { 'zh-cn':'浇水策略', 'ja':'水やり戦略', 'es':'Estrategias de riego', 'pt-br':'Estratégias de rega', 'fr':'Stratégies d’arrosage', 'de':'Bewässerungsstrategien', 'ru':'Стратегии полива', 'ar':'استراتيجيات الري', 'hi':'सिंचाई रणनीतियाँ', 'id':'Strategi penyiraman', 'vi':'Chiến lược tưới nước' },
    'crop-rotation': { 'zh-cn':'轮作指南', 'ja':'輪作ガイド', 'es':'Guía de rotación de cultivos', 'pt-br':'Guia de rotação de culturas', 'fr':'Guide de rotation des cultures', 'de':'Leitfaden zur Fruchtfolge', 'ru':'Руководство по севообороту', 'ar':'دليل تناوب المحاصيل', 'hi':'फसल चक्र मार्गदर्शिका', 'id':'Panduan rotasi tanaman', 'vi':'Hướng dẫn luân canh' },
    'seed-selection': { 'zh-cn':'种子选择指南', 'ja':'種子選びガイド', 'es':'Guía de selección de semillas', 'pt-br':'Guia de seleção de sementes', 'fr':'Guide de choix des graines', 'de':'Leitfaden zur Samenauswahl', 'ru':'Выбор семян – руководство', 'ar':'دليل اختيار البذور', 'hi':'बीज चयन गाइड', 'id':'Panduan pemilihan benih', 'vi':'Hướng dẫn chọn hạt giống' },
    'ice-cream-recipe': { 'zh-cn':'冰淇淋食谱指南', 'ja':'アイスクリームレシピガイド', 'es':'Guía de recetas de helado', 'pt-br':'Guia de receitas de sorvete', 'fr':'Guide des recettes de glace', 'de':'Leitfaden für Eisrezepte', 'ru':'Руководство по рецептам мороженого', 'ar':'دليل وصفات الآيس كريم', 'hi':'आइसक्रीम रेसिपीガイド', 'id':'Panduan resep es krim', 'vi':'Hướng dẫn công thức kem' },
    'profit-strategies': { 'zh-cn':'利润策略指南', 'ja':'利益戦略ガイド', 'es':'Guía de estrategias de beneficio', 'pt-br':'Guia de estratégias de lucro', 'fr':'Guide des stratégies de profit', 'de':'Leitfaden für Gewinnstrategien', 'ru':'Стратегии прибыли', 'ar':'دليل استراتيجيات الربح', 'hi':'लाभ रणनीति गाइड', 'id':'Panduan strategi keuntungan', 'vi':'Hướng dẫn chiến lược lợi nhuận' },
    'market-analysis': { 'zh-cn':'市场分析', 'ja':'マーケット分析', 'es':'Análisis de mercado', 'pt-br':'Análise de mercado', 'fr':'Analyse de marché', 'de':'Marktanalyse', 'ru':'Анализ рынка', 'ar':'تحليل السوق', 'hi':'बाज़ार विश्लेषण', 'id':'Analisis pasar', 'vi':'Phân tích thị trường' },
    'resource-management': { 'zh-cn':'资源管理', 'ja':'リソース管理', 'es':'Gestión de recursos', 'pt-br':'Gestão de recursos', 'fr':'Gestion des ressources', 'de':'Ressourcenmanagement', 'ru':'Управление ресурсами', 'ar':'إدارة الموارد', 'hi':'संसाधन प्रबंधन', 'id':'Manajemen sumber daya', 'vi':'Quản lý tài nguyên' },
    'investment-guide': { 'zh-cn':'投资指南', 'ja':'投資ガイド', 'es':'Guía de inversión', 'pt-br':'Guia de investimento', 'fr':'Guide d’investissement', 'de':'Investitionsleitfaden', 'ru':'Инвестиционный гайд', 'ar':'دليل الاستثمار', 'hi':'निवेश गाइड', 'id':'Panduan investasi', 'vi':'Hướng dẫn đầu tư' },
    'game-mechanics': { 'zh-cn':'游戏机制', 'ja':'ゲームメカニクス', 'es':'Mecánicas del juego', 'pt-br':'Mecânicas do jogo', 'fr':'Mécaniques de jeu', 'de':'Spielmechaniken', 'ru':'Механики игры', 'ar':'آليات اللعبة', 'hi':'गेम मैकेनिक्स', 'id':'Mekanika permainan', 'vi':'Cơ chế trò chơi' },
    'mutation-guide': { 'zh-cn':'变异系统指南', 'ja':'ミューテーションガイド', 'es':'Guía de mutaciones', 'pt-br':'Guia de mutações', 'fr':'Guide des mutations', 'de':'Mutations-Guide', 'ru':'Руководство по мутациям', 'ar':'دليل الطفرات', 'hi':'म्यूटेशन गाइड', 'id':'Panduan mutasi', 'vi':'Hướng dẫn đột biến' },
    'special-events': { 'zh-cn':'特别活动', 'ja':'スペシャルイベント', 'es':'Eventos especiales', 'pt-br':'Eventos especiais', 'fr':'Événements spéciaux', 'de':'Spezielle Events', 'ru':'Особые события', 'ar':'فعاليات خاصة', 'hi':'विशेष इवेंट', 'id':'Acara khusus', 'vi':'Sự kiện đặc biệt' },
    'speed-running': { 'zh-cn':'速通技巧', 'ja':'スピードランニング', 'es':'Speed running', 'pt-br':'Speed running', 'fr':'Speed running', 'de':'Speedrunning', 'ru':'Скоростное прохождение', 'ar':'العب السريع', 'hi':'स्पीड रनिंग', 'id':'Speed running', 'vi':'Speed running' },
    'how-to-build-farm': { 'zh-cn':'农场建设指南', 'ja':'農場づくりのガイド', 'es':'Guía para construir granja', 'pt-br':'Guia de construção da fazenda', 'fr':'Guide de construction de ferme', 'de':'Leitfaden zum Farmbau', 'ru':'Руководство по строительству фермы', 'ar':'دليل بناء المزرعة', 'hi':'फार्म बनाने की गाइड', 'id':'Panduan membangun pertanian', 'vi':'Hướng dẫn xây dựng nông trại' }
  };
  if (staticTitles[s]) return staticTitles[s][lang];
  return null;
}

function translateDesc(lang, slug){
  const s = slug.replace(/^\//,'').replace(/\.html$/,'');
  if (s.startsWith('how-to-make-')){
    let key = s.replace('how-to-make-','');
    if (key === 'cookies') key = 'cookie';
    else if (key.endsWith('ies')) key = key.slice(0,-3)+'y'; else if (key.endsWith('s')) key = key.slice(0,-1);
    if (!nouns[key] && key.endsWith('ughnut')) key = 'doughnut';
    const tmpl = { 'zh-cn':'学习在 Grow a Garden 中制作{noun}的技巧。', 'ja':'Grow a Gardenで{noun}を作るコツを学びましょう。', 'es':'Aprende a hacer {noun} en Grow a Garden.', 'pt-br':'Aprenda a fazer {noun} no Grow a Garden.', 'fr':'Apprenez à faire {noun} dans Grow a Garden.', 'de':'Lerne {noun} in Grow a Garden herzustellen.', 'ru':'Научитесь готовить {noun} в Grow a Garden.', 'ar':'تعلم صنع {noun} في Grow a Garden.', 'hi':'Grow a Garden में {noun} बनाना सीखें।', 'id':'Pelajari cara membuat {noun} di Grow a Garden.', 'vi':'Học cách làm {noun} trong Grow a Garden.' }[lang];
    const noun = nouns[key] && nouns[key][lang];
    return noun ? tmpl.replace('{noun}', noun) : tmpl;
  }
  if (s.startsWith('how-to-grow-')){
    let key = s.replace('how-to-grow-','');
    if (key === 'cookies') key = 'cookie';
    else if (key.endsWith('ies')) key = key.slice(0,-3)+'y'; else if (key.endsWith('s')) key = key.slice(0,-1);
    if (!nouns[key] && key.endsWith('ughnut')) key = 'doughnut';
    const tmpl = { 'zh-cn':'高效种植{noun}：播种、浇水、施肥与收获。', 'ja':'効率的な{noun}の栽培：播種・水やり・収穫。', 'es':'Cultivo eficiente de {noun}: siembra, riego y cosecha.', 'pt-br':'Cultivo eficiente de {noun}: plantio, rega e colheita.', 'fr':'Culture efficace de {noun} : semis, arrosage et récolte.', 'de':'Effizienter Anbau von {noun}: Aussaat, Bewässerung, Ernte.', 'ru':'Эффективное выращивание {noun}: посадка, полив, сбор.', 'ar':'زراعة فعالة لـ{noun}: البذر والري والحصاد.', 'hi':'{noun} की कुशल खेती: बोना, सिंचाई, फसल।', 'id':'Budidaya {noun} yang efisien: tanam, siram, panen.', 'vi':'Trồng {noun} hiệu quả: gieo, tưới, thu hoạch.' }[lang];
    const noun = nouns[key] && nouns[key][lang];
    return noun ? tmpl.replace('{noun}', noun) : tmpl;
  }
  const staticDesc = {
    'money': { 'zh-cn':'掌握高效耕作与销售，快速提升收入。', 'ja':'効率的な栽培と販売で素早く稼ぐ方法。', 'es':'Aprende a ganar dinero rápido con cultivo y ventas.', 'pt-br':'Ganhe dinheiro rápido com cultivo e vendas.', 'fr':'Gagnez rapidement grâce à la culture et la vente.', 'de':'Schnell Geld verdienen durch Anbau und Verkauf.', 'ru':'Быстрый заработок с помощью фермы и продаж.', 'ar':'اكسب المال بسرعة عبر الزراعة والبيع.', 'hi':'कृषि और बिक्री से तेजी से कमाएं।', 'id':'Hasilkan uang cepat dengan bertani & menjual.', 'vi':'Kiếm tiền nhanh nhờ trồng trọt và bán hàng.' },
    'friends': { 'zh-cn':'邀请好友协作、分工与交易，共建高效农场。', 'ja':'友達と協力し、役割分担と取引で効率的な農場を。', 'es':'Colabora con amigos y gestiona roles y comercio.', 'pt-br':'Colabore com amigos, papéis e trocas.', 'fr':'Collaborez entre amis : rôles et échanges.', 'de':'Mit Freunden zusammenarbeiten – Rollen & Handel.', 'ru':'Играйте с друзьями: роли и обмен.', 'ar':'تعاون مع الأصدقاء: أدوار وتداول.', 'hi':'दोस्तों के साथ सहयोग, भूमिकाएँ और व्यापार।', 'id':'Berkolaborasi dengan teman: peran & perdagangan.', 'vi':'Hợp tác với bạn bè: vai trò và giao dịch.' },
    'storage': { 'zh-cn':'设计仓储与路线，提升物流效率。', 'ja':'保管とルート設計で物流効率を上げる。', 'es':'Diseña almacenamiento y rutas para optimizar logística.', 'pt-br':'Otimize logística com armazenamento e rotas.', 'fr':'Optimisez la logistique : stockage & itinéraires.', 'de':'Logistik optimieren: Lager & Routen.', 'ru':'Оптимизируйте логистику: склад и маршруты.', 'ar':'حسن اللوجستيات: التخزين والمسارات.', 'hi':'भंडारण व मार्ग से लॉजिस्टिक्स कुशल बनाएं।', 'id':'Optimalkan logistik: penyimpanan & rute.', 'vi':'Tối ưu hậu cần: lưu trữ & lộ trình.' },
    'farming-basics': { 'zh-cn':'基础的种植技巧、浇水策略与作物管理要点。', 'ja':'基本的な栽培技術・水やり・作物管理のポイント。', 'es':'Técnicas básicas de cultivo, riego y manejo de cultivos.', 'pt-br':'Técnicas básicas de cultivo, rega e manejo de culturas.', 'fr':'Techniques de base, arrosage et gestion des cultures.', 'de':'Grundtechniken, Bewässerung und Pflanzenmanagement.', 'ru':'Базовые техники: полив и управление культурами.', 'ar':'تقنيات أساسية للزراعة والري وإدارة المحاصيل.', 'hi':'बुनियादी खेती, सिंचाई और फसल प्रबंधन।', 'id':'Teknik dasar bertani, penyiraman & manajemen tanaman.', 'vi':'Kỹ thuật cơ bản, tưới nước & quản lý cây trồng.' },
    'watering-strategies': { 'zh-cn':'掌握最佳浇水时机、频率与效率。', 'ja':'最適な水やりのタイミング・頻度・効率を学ぶ。', 'es':'Aprende el momento, la frecuencia y eficiencia de riego.', 'pt-br':'Aprenda tempo, frequência e eficiência da rega.', 'fr':'Moments, fréquences et efficacité de l’arrosage.', 'de':'Zeitpunkte, Häufigkeit und Effizienz der Bewässerung.', 'ru':'Время, частота и эффективность полива.', 'ar':'تعلم توقيت وتكرار وكفاءة الري.', 'hi':'सिंचाई का समय, आवृत्ति और दक्षता सीखें।', 'id':'Pelajari waktu, frekuensi & efisiensi penyiraman.', 'vi':'Thời điểm, tần suất và hiệu quả tưới.' },
    'crop-rotation': { 'zh-cn':'有效的轮作策略，保持土壤肥力并最大化产量。', 'ja':'効果的な輪作戦略で土壌肥沃度を維持し収量を最大化。', 'es':'Estrategias de rotación eficaces para mantener la fertilidad.', 'pt-br':'Estratégias de rotação para manter a fertilidade.', 'fr':'Stratégies de rotation pour maintenir la fertilité.', 'de':'Strategien zur Fruchtfolge für Bodenfruchtbarkeit.', 'ru':'Эффективный севооборот для плодородия.', 'ar':'استراتيجيات تدوير المحاصيل للحفاظ على خصوبة التربة.', 'hi':'फसल चक्र रणनीतियाँ मिट्टी की उर्वरता बनाए रखें।', 'id':'Strategi rotasi untuk kesuburan tanah.', 'vi':'Chiến lược luân canh giữ độ phì & tăng năng suất.' },
    'seed-selection': { 'zh-cn':'根据策略选择合适的种子，比较生长周期与收益。', 'ja':'戦略に合う種を選び、成長と利益を比較。', 'es':'Elige semillas adecuadas y compara tiempos y rendimientos.', 'pt-br':'Escolha sementes adequadas e compare prazos e rendimentos.', 'fr':'Choisissez des graines et comparez durées/rendements.', 'de':'Wähle geeignete Samen; vergleiche Zeiten & Erträge.', 'ru':'Выбирайте семена; сравнивайте сроки и урожайность.', 'ar':'اختر البذور المناسبة وقارن الزمن والعائد.', 'hi':'उपयुक्त बीज चुनें, समय व लाभ तुलना करें।', 'id':'Pilih benih yang sesuai; bandingkan waktu & hasil.', 'vi':'Chọn hạt giống phù hợp; so sánh thời gian & năng suất.' },
    'ice-cream-recipe': { 'zh-cn':'探索制作美味冰淇淋的配方与比例，提升利润与口感。', 'ja':'美味しいアイスクリームの配合と比率を学び、利益と味を最適化。', 'es':'Aprende combinaciones y proporciones para hacer helado delicioso y optimizar ganancias.', 'pt-br':'Aprenda combinações e proporções para sorvetes deliciosos e mais lucro.', 'fr':'Découvrez les combinaisons et proportions pour une glace délicieuse et rentable.', 'de':'Lerne Mischungen und Verhältnisse für leckeres Eis und mehr Profit.', 'ru':'Изучите рецептуры и пропорции для вкусного и прибыльного мороженого.', 'ar':'تعرّف على التركيبات والنِسَب لصنع آيس كريم لذيذ وتحسين الربح.', 'hi':'स्वादिष्ट आइसक्रीम के संयोजन व अनुपात सीखें; लाभ अनुकूलित करें।', 'id':'Pelajari kombinasi & komposisi untuk es krim lezat dan lebih untung.', 'vi':'Tìm hiểu tỉ lệ công thức kem ngon và tối ưu lợi nhuận.' },
    'profit-strategies': { 'zh-cn':'掌握长期盈利策略，市场分析与风险控制，优化销售节奏。', 'ja':'長期的な利益戦略、市場分析とリスク管理、販売の最適化を学ぶ。', 'es':'Aprende estrategias de beneficio a largo plazo, análisis de mercado y control de riesgos.', 'pt-br':'Aprenda estratégias de lucro de longo prazo, análise de mercado e controle de riscos.', 'fr':'Apprenez des stratégies de profit à long terme, analyse de marché et gestion des risques.', 'de':'Lerne langfristige Gewinnstrategien, Marktanalyse und Risikokontrolle.', 'ru':'Освойте долгосрочные стратегии прибыли, анализ рынка и управление рисками.', 'ar':'تعلّم استراتيجيات ربح طويلة الأجل وتحليل السوق وإدارة المخاطر.', 'hi':'दीर्घकालीन लाभ रणनीतियाँ, बाज़ार विश्लेषण व जोखिम नियंत्रण सीखें।', 'id':'Pelajari strategi laba jangka panjang, analisis pasar, dan kontrol risiko.', 'vi':'Học chiến lược lợi nhuận dài hạn, phân tích thị trường và kiểm soát rủi ro.' },
    'market-analysis': { 'zh-cn':'学习分析市场趋势、识别高利润机会并优化售卖策略。', 'ja':'市場動向を分析し、利益機会を見極め、販売戦略を最適化。', 'es':'Aprende a analizar tendencias de mercado e identificar oportunidades rentables.', 'pt-br':'Aprenda a analisar tendências de mercado e identificar oportunidades lucrativas.', 'fr':'Apprenez à analyser les tendances du marché et identifier les opportunités rentables.', 'de':'Lerne Markttrends zu analysieren und profitable Chancen zu erkennen.', 'ru':'Научитесь анализировать тренды и находить выгодные возможности.', 'ar':'تعلّم تحليل اتجاهات السوق وتحديد الفرص المربحة.', 'hi':'बाजार रुझानों का विश्लेषण करें और लाभदायक अवसर पहचानें।', 'id':'Analisis tren pasar dan identifikasi peluang menguntungkan.', 'vi':'Phân tích xu hướng thị trường và nhận diện cơ hội có lợi.' },
    'resource-management': { 'zh-cn':'掌握资源分配、库存与成本优化等管理技巧。', 'ja':'資源配分、在庫管理、コスト最適化などを習得。', 'es':'Domina la asignación de recursos, inventario y optimización de costos.', 'pt-br':'Domine alocação de recursos, inventário e otimização de custos.', 'fr':'Maîtrisez l’allocation des ressources, l’inventaire et l’optimisation des coûts.', 'de':'Beherrsche Ressourcenallokation, Bestände und Kostenoptimierung.', 'ru':'Освойте распределение ресурсов, запасы и оптимизацию затрат.', 'ar':'أتقن تخصيص الموارد والمخزون وتحسين التكاليف.', 'hi':'संसाधन आवंटन, इन्वेंट्री व लागत अनुकूलन में महारत पाएं।', 'id':'Kuasai alokasi sumber daya, inventaris, dan optimasi biaya.', 'vi':'Thành thạo phân bổ tài nguyên, tồn kho và tối ưu chi phí.' },
    'investment-guide': { 'zh-cn':'了解投资方向，获取长期收益最大化的方法。', 'ja':'投資先の見極めと長期リターン最大化の方法を学ぶ。', 'es':'Aprende dónde invertir para maximizar retornos a largo plazo.', 'pt-br':'Saiba onde investir para maximizar retornos de longo prazo.', 'fr':'Apprenez où investir pour maximiser les rendements à long terme.', 'de':'Lerne, wo du für maximale Langfristerträge investierst.', 'ru':'Узнайте, куда инвестировать для максимальной доходности.', 'ar':'تعرف أين تستثمر لتحقيق عوائد طويلة الأجل.', 'hi':'लंबी अवधि में अधिकतम रिटर्न हेतु कहाँ निवेश करें सीखें।', 'id':'Pelajari tempat berinvestasi untuk hasil jangka panjang maksimal.', 'vi':'Học nơi đầu tư để tối đa hóa lợi nhuận dài hạn.' },
    'game-mechanics': { 'zh-cn':'深入游戏机制、变异、特殊事件与高级玩法。', 'ja':'ゲームメカニクス、変異、特別イベント、上級要素を深掘り。', 'es':'Explora mecánicas, mutaciones, eventos especiales y juego avanzado.', 'pt-br':'Aprofunde-se em mecânicas, mutações, eventos e jogabilidade avançada.', 'fr':'Approfondissez mécaniques, mutations, événements et gameplay avancé.', 'de':'Tiefer Einblick in Mechaniken, Mutationen, Events und fortgeschrittenes Gameplay.', 'ru':'Погружение в механики, мутации, события и продвинутый геймплей.', 'ar':'تعمق في الآليات والطفرات والفعاليات واللعب المتقدم.', 'hi':'गेम मेकॅनिक्स, म्यूटेशन्स और उन्नत玩法 में गहराई से जाएँ।', 'id':'Selami mekanik, mutasi, event, dan gameplay lanjutan.', 'vi':'Đào sâu cơ chế, đột biến, sự kiện và lối chơi nâng cao.' },
    'mutation-guide': { 'zh-cn':'掌握变异系统，在 Grow a Garden 中组合变异以获取最大收益。', 'ja':'ミューテーションシステムを理解し、最大利益のために組み合わせる。', 'es':'Domina el sistema de mutaciones para maximizar beneficios.', 'pt-br':'Domine o sistema de mutações para maximizar lucros.', 'fr':'Maîtrisez les mutations pour un profit maximal.', 'de':'Meistere das Mutationssystem für maximalen Gewinn.', 'ru':'Освойте систему мутаций для максимальной выгоды.', 'ar':'أتقن نظام الطفرات لتحقيق أقصى ربح.', 'hi':'अधिकतम लाभ के लिए म्यूटेशन सिस्टम में महारत पाएं।', 'id':'Kuasai sistem mutasi demi keuntungan maksimum.', 'vi':'Làm chủ hệ thống đột biến để tối đa lợi nhuận.' },
    'special-events': { 'zh-cn':'全面指南：限时活动、机会与独家奖励。', 'ja':'期間限定イベント、特別なチャンス、限定報酬の完全ガイド。', 'es':'Guía completa de eventos especiales, oportunidades y recompensas exclusivas.', 'pt-br':'Guia completo de eventos especiais, oportunidades e recompensas exclusivas.', 'fr':'Guide complet des événements spéciaux, opportunités et récompenses exclusives.', 'de':'Vollständiger Leitfaden zu Sonderevents, Chancen und exklusiven Belohnungen.', 'ru':'Полное руководство по спецсобытиям, возможностям и наградам.', 'ar':'دليل متكامل للفعاليات الخاصة والفرص والمكافآت الحصرية.', 'hi':'विशेष इवेंट, अवसर और विशेष पुरस्कारों की पूरी गाइड।', 'id':'Panduan lengkap acara khusus, peluang & hadiah eksklusif.', 'vi':'Hướng dẫn đầy đủ về sự kiện đặc biệt, cơ hội và phần thưởng độc quyền.' },
    'speed-running': { 'zh-cn':'高效速通技巧：最大化效率并刷新纪录。', 'ja':'効率を最大化し記録更新を目指すスピードラン技術。', 'es':'Técnicas de speed running para máxima eficiencia y récords.', 'pt-br':'Técnicas de speed running para máxima eficiência e recordes.', 'fr':'Techniques de speed running pour une efficacité maximale et des records.', 'de':'Speedrunning-Techniken für maximale Effizienz und Rekorde.', 'ru':'Техники спидрана для максимальной эффективности и рекордов.', 'ar':'تقنيات لعب سريع لتحقيق أعلى كفاءة وأرقام قياسية.', 'hi':'उच्च दक्षता व रिकॉर्ड के लिए स्पीड रनिंग तकनीकें।', 'id':'Teknik speed running untuk efisiensi & rekor.', 'vi':'Kỹ thuật speed running để tối ưu hiệu suất & kỷ lục.' },
    'how-to-build-farm': { 'zh-cn':'设计高效农场布局：灌溉、仓储、加工与动线优化。', 'ja':'効率的な農場レイアウトの設計：灌漑、保管、加工、導線を最適化。', 'es':'Diseñar una granja eficiente: riego, almacenamiento, procesamiento y rutas.', 'pt-br':'Projetar uma fazenda eficiente: irrigação, armazenamento, processamento e fluxo.', 'fr':'Concevoir une ferme efficace : irrigation, stockage, transformation et flux.', 'de':'Effizientes Farm-Layout: Bewässerung, Lager, Verarbeitung & Wege.', 'ru':'Проектирование эффективной фермы: орошение, склад, переработка и потоки.', 'ar':'تصميم مزرعة فعّالة: ريّ، تخزين، معالجة وتدفق حركات.', 'hi':'कुशल फार्म लेआउट: सिंचाई, भंडारण, प्रसंस्करण व मार्ग।', 'id':'Rancang tata letak pertanian efisien: irigasi, penyimpanan, pemrosesan & jalur.', 'vi':'Thiết kế trang trại hiệu quả: tưới, lưu trữ, chế biến & luồng di chuyển.' }
  };
  if (staticDesc['money'] && s==='how-to-make-money-fast') return staticDesc['money'][lang];
  if (staticDesc['friends'] && s==='how-to-play-with-friends') return staticDesc['friends'][lang];
  if (staticDesc['storage'] && s==='storage-and-logistics') return staticDesc['storage'][lang];
  if (staticDesc[s]) return staticDesc[s][lang];
  return '';
}

function updateArticle(lang, href){
  const slug = href.replace(/^\//,'');
  const file = path.join(lang, slug);
  const html = read(file);
  if (!html) return;
  const $ = cheerio.load(html);
  const title = translateTitle(lang, href);
  if (title) $('h1').first().text(title);
  const descTmpl = translateDesc(lang, href);
  if (descTmpl){
    const key = slug.replace(/\.html$/,'').replace(/^how-to-(make|grow)-/,'');
    const noun = nouns[key] && nouns[key][lang];
    const desc = noun ? descTmpl.replace('{noun}', noun) : descTmpl;
    const p = $('main p').first();
    if (p.length) p.text(desc); else $('main').prepend(`<p>${desc}</p>`);
  }
  write(file, $.html());
}

function updateGuidesCard(lang, href){
  const file = path.join(lang, 'guides.html');
  const html = read(file);
  if (!html) return;
  const $ = cheerio.load(html);
  const a = $(`a.guide-item[href="${href.replace(/^\//,'')}"] , a.guide-item[href="${href}"]`).first();
  if (a.length===0) return;
  const title = translateTitle(lang, href);
  if (title) a.find('h3').first().text(title);
  const descTmpl = translateDesc(lang, href);
  if (descTmpl){
    const key = href.replace(/^\//,'').replace(/\.html$/,'').replace(/^how-to-(make|grow)-/,'');
    const noun = nouns[key] && nouns[key][lang];
    const desc = noun ? descTmpl.replace('{noun}', noun) : descTmpl;
    a.find('p').first().text(desc);
  }
  write(file, $.html());
}

function updateQuickTips(lang){
  const file = path.join(lang, 'guides.html');
  const html = read(file);
  if (!html) return;
  const $ = cheerio.load(html);
  const tips = {
    'zh-cn': {
      title: '💡 快速提示',
      items: [
        {t:'⏰ 黄金时段', d:'在游戏时间 7:00-9:00 浇水，享受双倍生长效果。'},
        {t:'🎯 质量更重要', d:'高品质原料能提升配方效果并获得更高利润。'},
        {t:'📈 市场时机', d:'在高需求时段出售产品以获取最大利润。'},
        {t:'📚 食谱熟练度', d:'先掌握基础食谱，再挑战高级配方以提高效率。'},
        {t:'🤝 社区学习', d:'加入我们的 Discord，与经验玩家一起学习。'},
        {t:'🔄 定期更新', d:'经常回访以获取新攻略与最新策略。'}
      ]
    },
    'ja': {
      title: '💡 クイックヒント',
      items: [
        {t:'⏰ ゴールデンアワー', d:'ゲーム内 7:00〜9:00 に水やりすると成長効果が2倍。'},
        {t:'🎯 品質が重要', d:'高品質の材料はより良いレシピと高い利益につながります。'},
        {t:'📈 マーケットタイミング', d:'需要が高い時間に販売して利益を最大化。'},
        {t:'📚 レシピ習熟', d:'上級レシピの前に基本を習得して効率アップ。'},
        {t:'🤝 コミュニティ学習', d:'Discordで他のプレイヤーから学びましょう。'},
        {t:'🔄 定期的な更新', d:'新しいガイドと最新戦略のために定期的に確認。'}
      ]
    },
    'es': { title:'💡 Consejos rápidos', items:[
      {t:'⏰ Horas doradas', d:'Riega de 7:00 a 9:00 para efecto de crecimiento doble.'},
      {t:'🎯 La calidad importa', d:'Mejores ingredientes dan mejores recetas y más ganancias.'},
      {t:'📈 Momento del mercado', d:'Vende en picos de demanda para máximo beneficio.'},
      {t:'📚 Maestría de recetas', d:'Domina recetas básicas antes de las avanzadas.'},
      {t:'🤝 Aprendizaje comunitario', d:'Únete a Discord para aprender de jugadores expertos.'},
      {t:'🔄 Actualizaciones regulares', d:'Vuelve seguido para nuevas guías y estrategias.'}
    ]},
    'pt-br': { title:'💡 Dicas rápidas', items:[
      {t:'⏰ Horas de ouro', d:'Regue entre 7:00-9:00 no jogo para efeito duplo.'},
      {t:'🎯 Qualidade importa', d:'Ingredientes melhores rendem receitas e lucros maiores.'},
      {t:'📈 Momento de mercado', d:'Venda nos picos de demanda para máximo lucro.'},
      {t:'📚 Domínio de receitas', d:'Domine as básicas antes das avançadas.'},
      {t:'🤝 Aprendizado em comunidade', d:'Entre no Discord para aprender com jogadores experientes.'},
      {t:'🔄 Atualizações regulares', d:'Volte sempre para novas guias e estratégias.'}
    ]},
    'fr': { title:'💡 Astuces rapides', items:[
      {t:'⏰ Heures dorées', d:'Arrosez entre 7h et 9h pour un double effet de croissance.'},
      {t:'🎯 La qualité compte', d:'De meilleurs ingrédients donnent de meilleures recettes et profits.'},
      {t:'📈 Timing du marché', d:'Vendez aux heures de forte demande pour un profit maximal.'},
      {t:'📚 Maîtrise des recettes', d:'Maîtrisez les bases avant les recettes avancées.'},
      {t:'🤝 Apprentissage communautaire', d:'Rejoignez Discord pour apprendre des joueurs expérimentés.'},
      {t:'🔄 Mises à jour régulières', d:'Revenez souvent pour de nouveaux guides et stratégies.'}
    ]},
    'de': { title:'💡 Kurztipps', items:[
      {t:'⏰ Goldene Stunden', d:'Bewässere 7:00–9:00 für doppelten Wachstumseffekt.'},
      {t:'🎯 Qualität zählt', d:'Bessere Zutaten ergeben bessere Rezepte und mehr Profit.'},
      {t:'📈 Markt-Timing', d:'Verkaufe bei hoher Nachfrage für maximalen Gewinn.'},
      {t:'📚 Rezept-Meisterschaft', d:'Erst Grundlagen beherrschen, dann Fortgeschrittenes.'},
      {t:'🤝 Lernen in der Community', d:'Tritt Discord bei und lerne von erfahrenen Spielern.'},
      {t:'🔄 Regelmäßige Updates', d:'Schau regelmäßig für neue Guides und Strategien vorbei.'}
    ]},
    'ru': { title:'💡 Быстрые советы', items:[
      {t:'⏰ Золотые часы', d:'Поливайте с 7:00 до 9:00 — двойной эффект роста.'},
      {t:'🎯 Качество важно', d:'Лучшие ингредиенты — лучшие рецепты и прибыль.'},
      {t:'📈 Тайминг рынка', d:'Продавайте в пик спроса для максимальной прибыли.'},
      {t:'📚 Мастерство рецептов', d:'Освойте базовые рецепты перед сложными.'},
      {t:'🤝 Обучение в сообществе', d:'Вступайте в Discord и учитесь у опытных игроков.'},
      {t:'🔄 Регулярные обновления', d:'Чаще заглядывайте за новыми гайдами и стратегиями.'}
    ]},
    'ar': { title:'💡 نصائح سريعة', items:[
      {t:'⏰ الساعات الذهبية', d:'اسقِ بين 7:00 و9:00 لتأثير نمو مضاعف.'},
      {t:'🎯 الجودة مهمة', d:'مكونات أفضل تعطي وصفات وأرباحًا أعلى.'},
      {t:'📈 توقيت السوق', d:'بِع خلال ذروة الطلب لتحقيق أقصى ربح.'},
      {t:'📚 إتقان الوصفات', d:'أتقن الأساسيات قبل الوصفات المتقدمة.'},
      {t:'🤝 التعلّم المجتمعي', d:'انضم إلى ديسكورد لتتعلم من اللاعبين الخبراء.'},
      {t:'🔄 تحديثات منتظمة', d:'عد بانتظام للحصول على أدلة واستراتيجيات جديدة.'}
    ]},
    'hi': { title:'💡 त्वरित सुझाव', items:[
      {t:'⏰ गोल्डन घंटे', d:'गेम में 7:00-9:00 बजे पानी दें – डबल प्रभाव।'},
      {t:'🎯 गुणवत्ता मायने रखती है', d:'बेहतर सामग्री से बेहतर रेसिपी और ज़्यादा मुनाफा मिलता है।'},
      {t:'📈 बाज़ार समय', d:'मांग के शिखर पर बेचें ताकि अधिकतम लाभ हो।'},
      {t:'📚 रेसिपी महारत', d:'उन्नत से पहले बुनियादी रेसिपी पर महारत पाएं।'},
      {t:'🤝 सामुदायिक सीख', d:'Discord से अनुभवी खिलाड़ियों से सीखें।'},
      {t:'🔄 नियमित अपडेट', d:'नई गाइड और रणनीतियों के लिए नियमित रूप से देखें।'}
    ]},
    'id': { title:'💡 Tips cepat', items:[
      {t:'⏰ Jam emas', d:'Siram 07.00–09.00 untuk efek pertumbuhan ganda.'},
      {t:'🎯 Kualitas penting', d:'Bahan lebih baik memberi resep dan profit lebih baik.'},
      {t:'📈 Timing pasar', d:'Jual saat permintaan puncak untuk untung maksimal.'},
      {t:'📚 Penguasaan resep', d:'Kuasai dasar sebelum resep tingkat lanjut.'},
      {t:'🤝 Belajar komunitas', d:'Gabung Discord untuk belajar dari pemain berpengalaman.'},
      {t:'🔄 Pembaruan rutin', d:'Sering kembali untuk panduan dan strategi baru.'}
    ]},
    'vi': { title:'💡 Mẹo nhanh', items:[
      {t:'⏰ Giờ vàng', d:'Tưới cây 7:00–9:00 để hiệu ứng tăng trưởng x2.'},
      {t:'🎯 Chất lượng quan trọng', d:'Nguyên liệu tốt hơn cho công thức và lợi nhuận cao hơn.'},
      {t:'📈 Thời điểm thị trường', d:'Bán lúc nhu cầu cao để tối đa lợi nhuận.'},
      {t:'📚 Thành thạo công thức', d:'Nắm vững cơ bản trước khi làm công thức nâng cao.'},
      {t:'🤝 Học cùng cộng đồng', d:'Tham gia Discord để học từ người chơi giàu kinh nghiệm.'},
      {t:'🔄 Cập nhật thường xuyên', d:'Thường xuyên quay lại để xem hướng dẫn và chiến lược mới.'}
    ]}
  };
  const map = tips[lang];
  if (!map) return;
  // title
  const h2 = $('h2').filter((_,el)=>/Quick Tips|クイック|Consejos|Dicas|Astuces|Kurztipps|советы|نصائح|सुझाव|Tips cepat|Mẹo/i.test($(el).text())).first();
  if (h2.length) h2.text(map.title);
  // items in order
  const items = $('.tips-grid .tip-item');
  items.each((i,el)=>{
    const conf = map.items[i];
    if (!conf) return;
    const h4 = $(el).find('h4').first();
    const p = $(el).find('p').first();
    if (h4.length) h4.text(conf.t);
    if (p.length) p.text(conf.d);
  });
  write(file, $.html());
}

function main(){
  const reportPath = 'missing.i18n.report.json';
  const report = JSON.parse(read(reportPath) || '{}');
  const allLangs = LANGS;
  for (const lang of allLangs){
    // Update all cards found in this localized guides.html
    const gfile = path.join(lang, 'guides.html');
    const ghtml = read(gfile);
    if (ghtml){
      const $ = cheerio.load(ghtml);
      $('a.guide-item[href]').each((_,a)=>{
        const href = ($(a).attr('href')||'').trim();
        if (!href) return;
        updateGuidesCard(lang, href);
        const h = href.replace(/^\//,'');
        if (/^how-to-/.test(h) || h === 'ice-cream-recipe.html'){
          updateArticle(lang, href);
        }
      });
    }
    // still handle previously generated missing list
    const miss = (report[lang] && report[lang].missing) || [];
    miss.forEach(href => {
      updateArticle(lang, href);
      updateGuidesCard(lang, href);
    });
    // Quick Tips localization inside localized guides
    updateQuickTips(lang);
  }
  console.log('Auto-translation applied to stubs, guide cards, and quick tips.');
}

main(); 