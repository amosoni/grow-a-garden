(function(){
  const supported = ["en","zh-cn","es","pt-br","fr","de","ru","ar","hi","id","vi","ja"];
  const storageKey = "gag_lang";
  const cardsModeKey = "gag_cards_mode"; // 'local' or 'root'

  function getCardsMode(){
    try{
      const url = new URL(location.href);
      const q = (url.searchParams.get('cards') || '').toLowerCase();
      if (q === 'local' || q === 'root') { localStorage.setItem(cardsModeKey, q); return q; }
    }catch(_e){}
    try{
      const saved = localStorage.getItem(cardsModeKey);
      if (saved === 'local' || saved === 'root') return saved;
    }catch(_e){}
    return 'root';
  }

  // Early redirect disabled: keep localized files accessible at /{lang}/...
  // (Previously redirected /{lang}/how-to-*.html → /how-to-*.html and /{lang}/guides.html → /guides.html?lang=lang)

  function getQueryLang(){
    try{
      const url = new URL(location.href);
      const lang = (url.searchParams.get('lang') || '').toLowerCase();
      return supported.includes(lang) ? lang : null;
    }catch(_e){ return null; }
  }

  function getLangFromUrl(){
    const seg = location.pathname.split("/")[1]?.toLowerCase();
    return supported.includes(seg) ? seg : null;
  }
  
  function detectLang(){
    const fromQuery = getQueryLang();
    if (fromQuery) return fromQuery;
    const fromUrl = getLangFromUrl();
    if (fromUrl) return fromUrl;
    
    const saved = localStorage.getItem(storageKey);
    if (saved && supported.includes(saved)) return saved;
    
    const nav = (navigator.language || navigator.userLanguage || "en").toLowerCase();
    if (supported.includes(nav)) return nav;
    const matched = supported.find(l => nav.startsWith(l));
    if (matched) return matched;
    if (nav.startsWith("zh")) return "zh-cn";
    return "en";
  }
  
  function setDocumentLang(lang){
    try{
      const html = document.documentElement;
      html.setAttribute("lang", lang);
      html.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");
    }catch(_e){}
  }

  function rewriteLocalLinks(lang){
    try{
      const anchors = Array.from(document.querySelectorAll('a[href]'));
      anchors.forEach(a => {
        const href = a.getAttribute('href');
        if (!href) return;
        if (/^(https?:)?\/\//i.test(href) || href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('javascript:') || href.startsWith('#')) return;

        const isHomeLink = /(^\/index\.html$)|(^index\.html$)|(^\/$)|(^#$)/i.test(href) || a.classList.contains('logo');
        if (isHomeLink) { a.setAttribute('href', `/${lang}/index.html`); return; }

        // Guides → prefer localized path
        if (/^\/?guides\.html(?:#.*)?$/i.test(href)) { a.setAttribute('href', `/${lang}/guides.html`); return; }

        // Articles → prefer localized path (/lang/how-to-*.html)
        if (/^\/?how-to-[a-z0-9-]+\.html(?:#.*)?$/i.test(href)){
          const normalizedPath = href.startsWith('/') ? href.replace(/^\//,'') : href;
          const [pathOnly, hash] = normalizedPath.split('#');
          a.setAttribute('href', `/${lang}/${pathOnly}${hash ? '#' + hash : ''}`);
          return;
        }

        const normalizedPath = href.startsWith('/') ? href : ('/' + href);
        const fileName = normalizedPath.replace(/^\//,'');

        if (/^[a-z0-9-]+\.html(?:#.*)?$/i.test(fileName) && !/^index\.html$/i.test(fileName) && !/^guides\.html$/i.test(fileName)) {
          // other single pages – keep relative
          a.setAttribute('href', normalizedPath);
          return;
        }

        const firstSeg = normalizedPath.split('/')[1]?.toLowerCase();
        if (supported.includes(firstSeg)) return;
        const newHref = '/' + lang + normalizedPath;
        a.setAttribute('href', newHref);
      });
    }catch(_e){}
  }
  
  async function applyI18n(lang){
    try{
      const dict = await fetch(`/i18n/${lang}.json`, {cache: "no-cache"}).then(r=>r.json());
      try { localStorage.setItem(storageKey, lang); } catch(_e) {}
      try { window.__gagI18n = { lang, dict }; window.__gagTranslate = function(key){ return (window.__gagI18n && window.__gagI18n.dict && window.__gagI18n.dict[key]) || null; }; } catch(_e) {}
      setDocumentLang(lang);
      document.querySelectorAll("[data-i18n]").forEach(el=>{ const key = el.getAttribute("data-i18n"); if (dict[key]) el.textContent = dict[key]; });
      document.querySelectorAll("[data-i18n-placeholder]").forEach(el=>{ const key = el.getAttribute("data-i18n-placeholder"); if (dict[key]) el.placeholder = dict[key]; });
      try { const nav = document.querySelector('header nav'); if (nav) { const links = nav.querySelectorAll('a'); links.forEach(a => { const text = (s)=>{ if (s) a.textContent = s; }; if (a.classList.contains('logo')) { text(dict['nav.logo']); return; } const href = a.getAttribute('href') || ''; const onClick = a.getAttribute('onclick') || ''; if (href.includes('guides.html')) { text(dict['nav.guides']); return; } if (onClick.includes("scrollToSection('stats')")) { text(dict['nav.live']); return; } if (onClick.includes("scrollToSection('map')")) { text(dict['nav.map']); return; } if (onClick.includes("scrollToSection('tips')")) { text(dict['nav.tips']); return; } if (onClick.includes("scrollToSection('community')") || a.classList.contains('discord-btn')) { text(dict['nav.discord']); return; } }); } } catch(_e) {}
      try { const footer = document.querySelector('footer .footer-content'); if (footer) { const ps = footer.querySelectorAll('p'); if (ps[0] && dict['footer.copyright']) ps[0].textContent = dict['footer.copyright']; if (ps[1] && dict['footer.disclaimer']) ps[1].textContent = dict['footer.disclaimer']; } } catch(_e) {}
      const sel = document.getElementById("lang-switcher"); if (sel) sel.value = lang;
      rewriteLocalLinks(lang);

      // Inject SEO metadata for article pages
      injectArticleStructuredData(lang);

      // Hydrate Guides page with localized content when needed
      await hydrateGuidesFromLocalized(lang);

      // Hydrate Article pages content (body text) when localized exists
      await hydrateArticleFromLocalized(lang);

      // Re-run link rewriting to ensure injected links also carry ?lang
      rewriteLocalLinks(lang);
    }catch(e){ console.warn("i18n load failed", e); }
  }

  async function hydrateGuidesFromLocalized(lang){
    try{
      const isGuides = /\/guides\.html$/i.test(location.pathname);
      if (!isGuides) return;
      if (lang === 'en') return; // root already English
      const res = await fetch(`/${lang}/guides.html`, {cache: 'no-cache'});
      if (!res.ok) return;
      const html = await res.text();
      const tmp = document.implementation.createHTMLDocument('x');
      tmp.documentElement.innerHTML = html;
      const staticOverridden = new Set();
      const LOCALIZE_CARD_TEXT = true;

      // Hard replace the entire guides section so the landing page always shows the selected language
      try{
        const guidesLocal = tmp.querySelector('.guides-section');
        const guidesCur = document.querySelector('.guides-section');
        if (guidesLocal && guidesCur) {
          guidesCur.innerHTML = guidesLocal.innerHTML;
        }
      }catch(_e){}

      // 1) Hero texts
      const heroLocal = tmp.querySelector('.guides-hero');
      if (heroLocal) {
        const h1Local = heroLocal.querySelector('h1');
        const pLocal = heroLocal.querySelector('p');
        const heroCur = document.querySelector('.guides-hero');
        if (heroCur) {
          const h1Cur = heroCur.querySelector('h1');
          const pCur = heroCur.querySelector('p');
          if (h1Cur && h1Local) h1Cur.textContent = h1Local.textContent;
          if (pCur && pLocal) pCur.textContent = pLocal.textContent;
        }
      }

      // 2) Breadcrumb last label
      const crumbLocal = tmp.querySelector('.breadcrumb-container');
      if (crumbLocal) {
        const lastLocal = crumbLocal.querySelector('[aria-current="page"]');
        const lastCur = document.querySelector('.breadcrumb-container [aria-current="page"]');
        if (lastLocal && lastCur) lastCur.textContent = lastLocal.textContent;
      }

      // 3) Filter buttons labels by data-filter
      const filterLocal = [...tmp.querySelectorAll('.filter-btn[data-filter]')];
      filterLocal.forEach(btnL => {
        const key = btnL.getAttribute('data-filter');
        const btnC = document.querySelector(`.filter-btn[data-filter="${key}"]`);
        if (btnC) btnC.textContent = btnL.textContent;
      });

      // 4) Category titles by data-category
      const catLocal = [...tmp.querySelectorAll('.category-section[data-category]')];
      catLocal.forEach(secL => {
        const key = secL.getAttribute('data-category');
        const titleL = secL.querySelector('.category-title');
        const secC = document.querySelector(`.category-section[data-category="${key}"]`);
        const titleC = secC && secC.querySelector('.category-title');
        if (titleC && titleL) titleC.textContent = titleL.textContent;
      });

      // 4b) Quick Tips block (title and 6 items)
      try{
        const quickLocal = [...tmp.querySelectorAll('.guides-card h2')]
          .map(h=>({h, text:(h.textContent||'').trim()}))
          .find(x=>/Quick Tips|クイック|Consejos|Dicas|Astuces|Kurztipps|советы|نصائح|सुझाव|Tips cepat|Mẹo/i.test(x.text));
        if (quickLocal){
          const cardL = quickLocal.h.closest('.guides-card');
          const cardC = [...document.querySelectorAll('.guides-card h2')]
            .map(h=>({h, text:(h.textContent||'').trim()}))
            .find(x=>/Quick Tips/i.test(x.text))?.h?.closest('.guides-card');
          if (cardL && cardC){
            const h2C = cardC.querySelector('h2'); const h2L = cardL.querySelector('h2');
            if (h2C && h2L) h2C.textContent = h2L.textContent;
            const itemsL = cardL.querySelectorAll('.tips-grid .tip-item');
            const itemsC = cardC.querySelectorAll('.tips-grid .tip-item');
            itemsC.forEach((elC, i)=>{
              const elL = itemsL[i]; if (!elL) return;
              const h4C = elC.querySelector('h4'); const pC = elC.querySelector('p');
              const h4L = elL.querySelector('h4'); const pL = elL.querySelector('p');
              if (h4C && h4L) h4C.textContent = h4L.textContent;
              if (pC && pL) pC.textContent = pL.textContent;
            });
          }
        }
      }catch(_e){}

      // 4c) Section titles fallback (when localized file lacks these sections)
      try{
        const SEC = {
          'co-op': {
            'zh-cn':'👥 协作与运营','ja':'👥 協力と運用','es':'👥 Cooperación y operaciones','pt-br':'👥 Cooperação e operações','fr':'👥 Coop & opérations','de':'👥 Kooperation & Betrieb','ru':'👥 Совместная игра и операции','ar':'👥 التعاون والتشغيل','hi':'👥 सहयोग व संचालन','id':'👥 Ko-op & Operasi','vi':'👥 Hợp tác & vận hành'
          },
          'advanced': {
            'zh-cn':'🎮 高级攻略','ja':'🎮 上級ガイド','es':'🎮 Guías avanzadas','pt-br':'🎮 Guias avançados','fr':'🎮 Guides avancés','de':'🎮 Fortgeschrittene Guides','ru':'🎮 Продвинутые руководства','ar':'🎮 أدلة متقدمة','hi':'🎮 उन्नत गाइड','id':'🎮 Panduan lanjutan','vi':'🎮 Hướng dẫn nâng cao'
          },
          'profit': {
            'zh-cn':'💰 利润优化','ja':'💰 利益ガイド','es':'💰 Optimización de ganancias','pt-br':'💰 Otimização de lucro','fr':'💰 Optimisation du profit','de':'💰 Gewinnoptimierung','ru':'💰 Оптимизация прибыли','ar':'💰 تحسين الأرباح','hi':'💰 लाभ अनुकूलन','id':'💰 Optimasi profit','vi':'💰 Tối ưu lợi nhuận'
          }
        };
        document.querySelectorAll('.category-section').forEach(sec=>{
          const key = sec.getAttribute('data-category');
          const map = SEC[key];
          if (!map) return;
          const h2 = sec.querySelector('.category-title');
          if (h2 && map[lang]) h2.textContent = map[lang];
        });
      }catch(_e){}

      // 4d) Static cards fallback (advanced/co-op/non-how-to)
      try{
        const CARD = {
          'ice-cream-recipe.html': {
            title:{'zh-cn':'🍦 冰淇淋食谱指南','ja':'🍦 アイスクリームレシピガイド','es':'🍦 Guía de recetas de helado','pt-br':'🍦 Guia de receitas de sorvete','fr':'🍦 Guide des recettes de glace','de':'🍦 Leitfaden für Eisrezepte','ru':'🍦 Руководство по рецептам мороженого','ar':'🍦 دليل وصفات الآيس كريم','hi':'🍦 आइसक्रीमレシピガイド','id':'🍦 Panduan resep es krim','vi':'🍦 Hướng dẫn công thức kem'},
            desc:{'zh-cn':'探索制作美味冰淇淋的配方与比例，提升利润与口感。','ja':'美味しいアイスクリームの配合と比率を学び、利益と味を最適化。','es':'Aprende combinaciones y proporciones para hacer helado delicioso y optimizar ganancias.','pt-br':'Aprenda combinações e proporções para sorvetes deliciosos e mais lucro.','fr':'Découvrez les combinaisons et proportions pour une glace délicieuse et rentable.','de':'Lerne Mischungen und Verhältnisse für leckeres Eis und mehr Profit.','ru':'Изучите рецептуры и пропорции для вкусного и прибыльного мороженого.','ar':'تعرّف على التركيبات والنِسَب لصنع آيس كريم لذيذ وتحسين الربح.','hi':'स्वादिष्ट आइसक्रीम के संयोजन व अनुपात सीखें; लाभ अनुकूलित करें।','id':'Pelajari kombinasi & komposisi untuk es krim lezat dan lebih untung.','vi':'Tìm hiểu tỉ lệ công thức kem ngon và tối ưu lợi nhuận.'}
          },
          'storage-and-logistics.html': {
            title:{'zh-cn':'📦 存储与物流','ja':'📦 ストレージと物流','es':'📦 Almacenamiento y logística','pt-br':'📦 Armazenamento e logística','fr':'📦 Stockage et logistique','de':'📦 Lagerung & Logistik','ru':'📦 Хранение и логистика','ar':'📦 التخزين واللوجستيات','hi':'📦 भंडारण और लॉजिस्टिक्स','id':'📦 Penyimpanan & Logistik','vi':'📦 Lưu trữ & hậu cần'},
            desc:{'zh-cn':'设计仓储枢纽、标记库存、规划路线与批量配送，提升效率。','ja':'倉庫拠点の設計、在庫ラベル付け、ルート計画、バッチ配送で効率化。','es':'Diseña centros de almacenamiento, etiqueta inventario y planifica rutas para máxima eficiencia.','pt-br':'Projete hubs de armazenamento, rotule estoque, planeje rotas e entregas em lote.','fr':'Concevez des hubs de stockage, étiquetez l’inventaire et planifiez les routes.','de':'Plane Lager-Hubs, bestandslabels, Routen und Bündel-Lieferungen.','ru':'Проектируйте склады, маркируйте запасы и планируйте маршруты.','ar':'صمّم مراكز التخزين، ضع بطاقات على المخزون وخطط المسارات والتسليمات.','hi':'स्टोरेज हब, इन्वेंट्री लेबलिंग, रूट व बैच डिलीवरी से दक्षता बढ़ाएँ।','id':'Rancang hub penyimpanan, label inventori, rencanakan rute & pengiriman.','vi':'Thiết kế kho, gắn nhãn tồn, lên tuyến & giao theo lô.'}
          },
          'profit-strategies.html': { title:{'ja':'✅ 利益戦略ガイド','zh-cn':'✅ 利润策略指南'}, desc:{'ja':'長期的な利益戦略、市場分析とリスク管理、販売の最適化を学ぶ。','zh-cn':'掌握长期盈利策略，市场分析与风险控制，优化销售节奏。'} },
          'market-analysis.html': { title:{'ja':'📊 マーケット分析','zh-cn':'📊 市场分析'}, desc:{'ja':'市場動向を分析し、利益機会を見極め、販売戦略を最適化。','zh-cn':'学习分析市场趋势、识别高利润机会并优化售卖策略。'} },
          'resource-management.html': { title:{'ja':'⚙️ リソース管理','zh-cn':'⚙️ 资源管理'}, desc:{'ja':'資源配分、在庫管理、コスト最適化などを習得。','zh-cn':'掌握资源分配、库存与成本优化等管理技巧。'} },
          'investment-guide.html': { title:{'ja':'💎 投資ガイド','zh-cn':'💎 投资指南'}, desc:{'ja':'投資先の見極めと長期リターン最大化の方法を学ぶ。','zh-cn':'了解投资方向，获取长期收益最大化的方法。'} },
          'game-mechanics.html': { title:{'ja':'🎮 ゲームメカニクス','zh-cn':'🎮 游戏机制'}, desc:{'ja':'ゲームメカニクス、変異、特別イベント、上級要素を深掘り。','zh-cn':'深入游戏机制、变异、特殊事件与高级玩法。'} },
          'mutation-guide.html': { title:{'ja':'🧬 ミューテーションガイド','zh-cn':'🧬 变异系统指南'}, desc:{'ja':'ミューテーションシステムを理解し、最大利益のために組み合わせる。','zh-cn':'掌握变异系统，在 Grow a Garden 中组合变异以获取最大收益。'} },
          'special-events.html': { title:{'ja':'🎉 スペシャルイベント','zh-cn':'🎉 特别活动'}, desc:{'ja':'期間限定イベント、特別なチャンス、限定報酬の完全ガイド。','zh-cn':'全面指南：限时活动、机会与独家奖励。'} },
          'speed-running.html': { title:{'ja':'⚡ スピードランニング','zh-cn':'⚡ 速通技巧'}, desc:{'ja':'効率を最大化し記録更新を目指すスピードラン技術。','zh-cn':'高效速通技巧：最大化效率并刷新纪录。'} },
          'how-to-build-farm.html': {
            title:{'ja':'🏗️ 農場づくりのガイド','zh-cn':'🏗️ 农场建设指南','es':'🏗️ Guía para construir granja','pt-br':'🏗️ Guia de construção da fazenda','fr':'🏗️ Guide de construction de ferme','de':'🏗️ Leitfaden zum Farmbau','ru':'🏗️ Руководство по строительству фермы','ar':'🏗️ دليل بناء المزرعة','hi':'🏗️ फार्म बनाने कीガイド','id':'🏗️ Panduan membangun pertanian','vi':'🏗️ Hướng dẫn xây dựng nông trại'},
            desc:{'ja':'効率的な農場レイアウトの設計：灌漑、保管、加工、導線を最適化。','zh-cn':'设计高效农场布局：灌溉、仓储、加工与动线优化。'}
          }
        };
        document.querySelectorAll('a.guide-item[href] h3').forEach(h3=>{
          const a = h3.closest('a');
          const href = (a && a.getAttribute('href')) || '';
          const key = href.replace(/^\//,'');
          const rec = CARD[key];
          if (!rec) return;
          if (rec.title && rec.title[lang]) h3.textContent = rec.title[lang];
          const p = a.querySelector('p');
          if (p && rec.desc && rec.desc[lang]) p.textContent = rec.desc[lang];
          staticOverridden.add('/' + key);
        });
      }catch(_e){}

      // 4e) Quick Tips hard fallback translations
      try{
        const tips = {
          'zh-cn': {
            title: '💡 快速提示', items:[
              {t:'⏰ 黄金时段', d:'在游戏时间 7:00-9:00 浇水，享受双倍生长效果。'},
              {t:'🎯 质量更重要', d:'高品质原料能提升配方效果并获得更高利润。'},
              {t:'📈 市场时机', d:'在高需求时段出售产品以获取最大利润。'},
              {t:'📚 食谱熟练度', d:'先掌握基础食谱，再挑战高级配方以提高效率。'},
              {t:'🤝 社区学习', d:'加入我们的 Discord，与经验玩家一起学习。'},
              {t:'🔄 定期更新', d:'经常回访以获取新攻略与最新策略。'}
            ]
          },
          'ja': {
            title: '💡 クイックヒント', items:[
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
        if (map){
          const block = [...document.querySelectorAll('.guides-card h2')].map(h=>h.closest('.guides-card')).find(card=>/Quick Tips/i.test(card?.querySelector('h2')?.textContent||''));
          if (block){
            const h2 = block.querySelector('h2'); if (h2) h2.textContent = map.title;
            const items = block.querySelectorAll('.tips-grid .tip-item');
            items.forEach((el, i)=>{
              const conf = map.items[i]; if (!conf) return;
              const h4 = el.querySelector('h4'); const p = el.querySelector('p');
              if (h4) h4.textContent = conf.t; if (p) p.textContent = conf.d;
            });
          }
        }
      }catch(_e){}

      // 5) Guide cards: match by href, copy h3/p/difficulty/read-time
      const cardsLocal = tmp.querySelectorAll('.guide-item[href]');
      const mapLocal = new Map();
      const norm = (h)=>{ if(!h) return ''; return h.startsWith('/') ? h : ('/' + h); };
      cardsLocal.forEach(a => mapLocal.set(norm(a.getAttribute('href')), a));
      const cardNodes = Array.from(document.querySelectorAll('.guide-item[href]'));
      cardNodes.forEach(aC => {
        const href = norm(aC.getAttribute('href'));
        if (staticOverridden.has(href)) return; // keep static override
        const aL = mapLocal.get(href);
        if (!aL) return; // fallback to English if not localized
        const h3L = aL.querySelector('h3');
        const pL = aL.querySelector('p');
        const diffL = aL.querySelector('.guide-difficulty');
        const h3C = aC.querySelector('h3');
        const pC = aC.querySelector('p');
        const diffC = aC.querySelector('.guide-difficulty');
        if (h3C && h3L) h3C.textContent = h3L.textContent;
        if (pC && pL) pC.textContent = pL.textContent;
        if (diffC && diffL) diffC.textContent = diffL.textContent;
        // also localize read-time if exists
        const rtC = aC.querySelector('.guide-read-time');
        const rtL = aL.querySelector('.guide-read-time');
        if (rtC && rtL) rtC.textContent = rtL.textContent;
      });

      // localize difficulty/read-time if still English
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
      try{
        const map = DIFF[lang] || {};
        document.querySelectorAll('.guide-difficulty').forEach(el=>{
          const t = el.textContent.trim();
          if (map[t]) el.textContent = map[t];
        });
        const fmt = RT[lang];
        if (fmt){
          document.querySelectorAll('.guide-read-time').forEach(el=>{
            const t = el.textContent.trim();
            el.textContent = fmt(t);
          });
        }
      }catch(_e){}
    }catch(_e){}
  }

  async function hydrateArticleFromLocalized(lang){
    try{
      const m = location.pathname.match(/^\/(how-to-[a-z0-9-]+\.html)$/i);
      if (!m) return;
      if (lang === 'en') return;
      const file = m[1];
      const res = await fetch(`/${lang}/${file}`, {cache:'no-cache'});
      const mainCur = document.querySelector('main');
      if (!res.ok) {
        // show localized notice that content falls back to English
        try{
          if (mainCur) {
            const wrap = document.createElement('div');
            wrap.style.background = 'rgba(255,230,150,0.3)';
            wrap.style.border = '1px solid rgba(200,150,50,0.6)';
            wrap.style.padding = '0.75rem 1rem';
            wrap.style.borderRadius = '8px';
            wrap.style.margin = '1rem 0';
            const t = (k)=> (window.__gagTranslate && window.__gagTranslate(k)) || '';
            const title = t('notice.missingTitle') || 'Not yet localized';
            const body = t('notice.missingBody') || 'This article is shown in English until the localized version is ready.';
            wrap.innerHTML = `<strong>${title}</strong><div style="font-size:0.95em;">${body}</div>`;
            mainCur.prepend(wrap);
          }
        }catch(_e){}
        return; // keep English content
      }
      const html = await res.text();
      const tmp = document.implementation.createHTMLDocument('x');
      tmp.documentElement.innerHTML = html;
      const mainLocal = tmp.querySelector('main');
      if (mainLocal && mainCur) {
        mainCur.replaceWith(mainLocal);
      } else if (mainLocal) {
        const h1C = document.querySelector('h1');
        if (h1C) h1C.textContent = (mainLocal.querySelector('h1')?.textContent || h1C.textContent);
      }
      // Localize breadcrumb labels if present
      try{
        const dict = (window.__gagI18n && window.__gagI18n.dict) || {};
        const crumb = document.querySelector('.breadcrumb');
        if (crumb){
          const links = crumb.querySelectorAll('a, span');
          links.forEach(el=>{
            const txt = (el.textContent||'').trim().toLowerCase();
            if (/^home|首页|ホーム$/i.test(txt) && dict['breadcrumb.home']) el.textContent = dict['breadcrumb.home'];
            if (/^guides|攻略|ガイド$/i.test(txt) && dict['breadcrumb.guides']) el.textContent = dict['breadcrumb.guides'];
          });
        }
      }catch(_e){}
    }catch(_e){}
  }

  function injectArticleStructuredData(lang){
    try{
      const m = location.pathname.match(/\/how-to-[a-z0-9-]+\.html$/i);
      if (!m) return;
      const canonHref = location.pathname;
      if (!document.querySelector('link[rel="canonical"]')){
        const link = document.createElement('link');
        link.setAttribute('rel','canonical');
        link.setAttribute('href', canonHref);
        document.head.appendChild(link);
      }
      const titleEl = document.querySelector('h1');
      const headline = (titleEl && titleEl.textContent.trim()) || document.title;
      const origin = location.origin || '';
      const pageUrl = origin + canonHref;
      const imageUrl = origin + '/grow-bg.jpg';
      const inLang = lang || (document.documentElement.getAttribute('lang') || 'en');
      const article = {
        "@context":"https://schema.org",
        "@type":"Article",
        "headline": headline,
        "mainEntityOfPage": {"@type":"WebPage","@id": pageUrl},
        "author": {"@type":"Organization","name":"Grow a Garden"},
        "publisher": {"@type":"Organization","name":"Grow a Garden","logo":{"@type":"ImageObject","url": imageUrl}},
        "image": [imageUrl],
        "inLanguage": inLang
      };
      const breadcrumb = {
        "@context":"https://schema.org",
        "@type":"BreadcrumbList",
        "itemListElement":[
          {"@type":"ListItem","position":1,"name":"Home","item": origin + "/index.html"},
          {"@type":"ListItem","position":2,"name":"Guides","item": origin + "/guides.html"},
          {"@type":"ListItem","position":3,"name": headline, "item": pageUrl}
        ]
      };
      const s1 = document.createElement('script'); s1.type='application/ld+json'; s1.textContent = JSON.stringify(article);
      const s2 = document.createElement('script'); s2.type='application/ld+json'; s2.textContent = JSON.stringify(breadcrumb);
      document.head.appendChild(s1); document.head.appendChild(s2);
    }catch(_e){}
  }
  
  function switchLang(lang){
    if (!supported.includes(lang)) return;
    localStorage.setItem(storageKey, lang);
    const isHome = /(^|\/)index\.html$/i.test(location.pathname) || location.pathname === '/';
    if (isHome) { location.assign(`/${lang}/index.html` + location.hash); return; }
    const base = (location.pathname.split('/').pop() || '').toLowerCase();
    const isSingleFile = /^[a-z0-9-]+\.html$/i.test(base);
    if (isSingleFile) {
      if (base === 'index.html') { location.assign(`/${lang}/index.html` + location.hash); return; }
      if (base === 'guides.html') { location.assign(`/${lang}/guides.html` + location.hash); return; }
      // For articles and other single pages, go to localized path
      location.assign(`/${lang}/` + base + location.hash); return;
    }
    const parts = location.pathname.split("/");
    if (supported.includes(parts[1])) { parts[1] = lang; } else { parts.splice(1, 0, lang); }
    const newPath = parts.join("/");
    location.assign(newPath + location.search + location.hash);
  }
  
  document.addEventListener("DOMContentLoaded",()=>{
    const lang = detectLang();
    applyI18n(lang);
    const sel = document.getElementById("lang-switcher"); if (sel) { sel.addEventListener("change", e=> switchLang(e.target.value)); }
    document.addEventListener('gag:i18n-refresh', ()=>{ const current = (window.__gagI18n && window.__gagI18n.lang) || lang; applyI18n(current); });
  });
})(); 