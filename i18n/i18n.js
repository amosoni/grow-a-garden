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
      const anchors = Array.from(document.querySelectorAll('a[href], a[onclick]'));
      const isHomeNow = /(^|\/)index\.html$/i.test(location.pathname) || location.pathname === '/';
      anchors.forEach(a => {
        const href = a.getAttribute('href');
        const onClick = (a.getAttribute('onclick') || '');
        // 将带有 scrollToSection 的导航，在非首页时改为去首页对应锚点；在首页使用本页锚点
        const m = onClick.match(/scrollToSection\('([a-z0-9-]+)'\)/i);
        if (m) {
          const sec = (m[1] || '').toLowerCase();
          a.setAttribute('href', isHomeNow ? `#${sec}` : `/${lang}/index.html#${sec}`);
          a.removeAttribute('onclick');
          return;
        }
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
  
  // Helper: only use a translation value if it looks valid (non-empty, not an echo of the key or [key])
  function isUsableTranslation(val, key){
    if (val == null) return false;
    const t = String(val).trim();
    if (!t) return false;
    if (t === key) return false;
    if (t === `[${key}]`) return false;
    if (/^\[[^\]]+\]$/.test(t)) return false;
    return true;
  }

  // Heuristic: remove/disable any floating right-side flags bar overlaying clicks
  function disableFloatingFlagSidebar(){
    try{
      const scan = ()=>{
        const nodes = Array.from(document.querySelectorAll('body *'));
        const toHide = [];
        nodes.forEach(el=>{
          const cs = getComputedStyle(el);
          if (cs.position !== 'fixed') return;
          const rect = el.getBoundingClientRect();
          if (rect.width > 180) return; // narrow column
          if (rect.right < window.innerWidth - 20) return; // must be near right edge
          // many small images stacked vertically
          const imgs = el.querySelectorAll('img');
          if (imgs.length >= 6) {
            let stacked = 0;
            imgs.forEach(img=>{ const r = img.getBoundingClientRect(); if (r.width <= 40 && r.height <= 30) stacked++; });
            if (stacked >= 5) toHide.push(el);
          }
        });
        toHide.forEach(el=>{ el.style.pointerEvents = 'none'; el.style.opacity = '0'; el.style.display = 'none'; el.setAttribute('data-gag-hidden', 'true'); });
      };
      scan();
      // Keep it suppressed if some script re-inserts it later
      if (!window.__gagFlagSidebarObserver){
        const obs = new MutationObserver(()=> scan());
        obs.observe(document.body, { childList: true, subtree: true });
        window.__gagFlagSidebarObserver = obs;
      }
    }catch(_e){}
  }

  async function applyI18n(lang){
    try{
      const dict = await fetch(`/i18n/${lang}.json`, {cache: "no-cache"}).then(r=>r.json());
      try { localStorage.setItem(storageKey, lang); } catch(_e) {}
      try { window.__gagI18n = { lang, dict }; window.__gagTranslate = function(key){ return (window.__gagI18n && window.__gagI18n.dict && window.__gagI18n.dict[key]) || null; }; } catch(_e) {}
      setDocumentLang(lang);
      document.querySelectorAll("[data-i18n]").forEach(el=>{ const key = el.getAttribute("data-i18n"); const v = dict[key]; if (isUsableTranslation(v, key)) el.textContent = v; });
      document.querySelectorAll("[data-i18n-placeholder]").forEach(el=>{ const key = el.getAttribute("data-i18n-placeholder"); const v = dict[key]; if (isUsableTranslation(v, key)) el.placeholder = v; });
      try { const nav = document.querySelector('header nav'); if (nav) { const links = nav.querySelectorAll('a'); links.forEach(a => {
        const text = (s)=>{ if (s) a.textContent = s; };
        if (a.classList.contains('logo')) { text(dict['nav.logo']); return; }
        const href = (a.getAttribute('href') || '').toLowerCase();
        if (href.includes('guides.html')) { text(dict['nav.guides']); return; }
        if (href.includes('#stats') || /scrolltosection\('stats'\)/i.test(a.getAttribute('onclick')||'')) { text(dict['nav.live']); return; }
        if (href.includes('#map') || /scrolltosection\('map'\)/i.test(a.getAttribute('onclick')||'')) { text(dict['nav.map']); return; }
        if (href.includes('#tips') || /scrolltosection\('tips'\)/i.test(a.getAttribute('onclick')||'')) { text(dict['nav.tips']); return; }
        if (a.classList.contains('discord-btn')) { text(dict['nav.discord']); return; }
      }); } } catch(_e) {}
      try { const footer = document.querySelector('footer .footer-content'); if (footer) { const ps = footer.querySelectorAll('p'); if (ps[0] && dict['footer.copyright']) ps[0].textContent = dict['footer.copyright']; if (ps[1] && dict['footer.disclaimer']) ps[1].textContent = dict['footer.disclaimer']; } } catch(_e) {}
      const sel = document.getElementById("lang-switcher"); if (sel) sel.value = lang;
      rewriteLocalLinks(lang);

      // Inject SEO metadata for article pages
      injectArticleStructuredData(lang);

      // Hydrate Guides page with localized content when needed
      await hydrateGuidesFromLocalized(lang);

      // Hydrate Article pages content (body text) when localized exists
      await hydrateArticleFromLocalized(lang);

      // NEW: Localize article labels via keys (works on both root and localized paths)
      localizeArticleLabels(lang, dict);

      // Re-run link rewriting to ensure injected links also carry ?lang
      rewriteLocalLinks(lang);

      // Disable any floating flag sidebar that could block clicks
      disableFloatingFlagSidebar();
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
            desc:{'zh-cn':'设计仓储枢纽、标记库存、规划路线与批量配送，提升效率。','ja':'倉庫拠点の設計、在庫ラベル付け、ルート計画、バッチ配送で効率化。','es':'Diseña centros de almacenamiento, etiqueta inventario y planifica rutas para máxima eficiencia.','pt-br':'Projete hubs de armazenamento, rotule estoque, planeje rotas e entregas em lote.','fr':'Concevez des hubs de stockage, étiquetez l\'inventaire et planifiez les routes.','de':'Plane Lager-Hubs, bestandslabels, Routen und Bündel-Lieferungen.','ru':'Проектируйте склады, маркируйте запасы и планируйте маршруты.','ar':'صمّم مراكز التخزين، ضع بطاقات على المخزون وخطط المسارات والتسليمات.','hi':'स्टोरेज हब, इन्वेंट्री लेबलिंग, रूट व बैच डिलीवरी से दक्षता बढ़ाएँ।','id':'Rancang hub penyimpanan, label inventori, rencanakan rute & pengiriman.','vi':'Thiết kế kho, gắn nhãn tồn, lên tuyến & giao theo lô.'}
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
      const mainCur2 = document.querySelector('main');
      if (mainLocal && mainCur2) {
        mainCur2.replaceWith(mainLocal);
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
  
  // NEW: Localize article labels via keys and basic pattern rules
  function localizeArticleLabels(lang, dict){
    try{
      const base = (location.pathname.split('/').pop() || '').toLowerCase();
      if (!/^[a-z0-9-]+\.html$/.test(base)) return;
      if (!/^how-to-[a-z0-9-]+\.html$/.test(base)) return; // only how-to pages
      const t = (k)=> (dict && dict[k]) || null;

      // Generic table headers mapping (by language)
      const TABLE_MAP = {
        'en':   { name:'Name', ingredients:'Ingredients', time:'Time', rewards:'Rewards', difficulty:'Difficulty' },
        'zh-cn':{ name:'名称', ingredients:'所需材料', time:'时间', rewards:'奖励', difficulty:'难度' },
        'ja':   { name:'名前', ingredients:'必要な材料', time:'調理時間', rewards:'報酬価値', difficulty:'難易度' },
        'es':   { name:'Nombre', ingredients:'Ingredientes', time:'Tiempo', rewards:'Recompensas', difficulty:'Dificultad' },
        'pt-br':{ name:'Nome', ingredients:'Ingredientes', time:'Tempo', rewards:'Recompensas', difficulty:'Dificuldade' },
        'fr':   { name:'Nom', ingredients:'Ingrédients', time:'Temps', rewards:'Récompenses', difficulty:'Difficulté' },
        'de':   { name:'Name', ingredients:'Zutaten', time:'Zeit', rewards:'Belohnungen', difficulty:'Schwierigkeit' },
        'ru':   { name:'Название', ingredients:'Ингредиенты', time:'Время', rewards:'Награды', difficulty:'Сложность' },
        'ar':   { name:'الاسم', ingredients:'المكونات', time:'الوقت', rewards:'المكافآت', difficulty:'الصعوبة' },
        'hi':   { name:'नाम', ingredients:'आवश्यक सामग्री', time:'समय', rewards:'इनाम', difficulty:'कठिनाई' },
        'id':   { name:'Nama', ingredients:'Bahan', time:'Waktu', rewards:'Hadiah', difficulty:'Kesulitan' },
        'vi':   { name:'Tên', ingredients:'Nguyên liệu', time:'Thời gian', rewards:'Phần thưởng', difficulty:'Độ khó' }
      };
      const TABLE = TABLE_MAP[lang] || TABLE_MAP['en'];

      // Headings common terms per language
      const HEADINGS_MAP = {
        'ja': {
          'Basic Salad Recipes':'基本サラダレシピ',
          'Luxury Salad Recipes':'高級サラダレシピ',
          'Basic Pizza Recipes':'基本ピザレシピ',
          'Advanced Pizza Recipes':'上級ピザレシピ',
          'Premium Recipes':'プレミアムレシピ',
          'Pizza Varieties & Types':'ピザの種類',
          'Making Tips & Tricks':'作りのコツとテクニック',
          'Growing Tips':'栽培のコツ',
          'Making Tips':'作り方のコツ',
          'Profit Optimization':'利益最適化',
          'Production Optimization':'生産最適化',
          'Advanced Strategies':'高度な戦略',
          'Next Steps':'次のステップ',
          'Basic Bread Making':'基本的なパン作り',
          'Basic Bread Recipes':'基本パンレシピ',
          'Advanced Bread Recipes':'上級パンレシピ',
          'Premium Bread Recipes':'プレミアムパンレシピ',
          'Bread Varieties & Types':'パンの種類'
        },
        'zh-cn': {
          'Basic Salad Recipes':'基础沙拉配方',
          'Luxury Salad Recipes':'高阶沙拉配方',
          'Basic Pizza Recipes':'基础披萨配方',
          'Advanced Pizza Recipes':'进阶披萨配方',
          'Premium Recipes':'高级配方',
          'Pizza Varieties & Types':'披萨种类',
          'Making Tips & Tricks':'制作技巧',
          'Growing Tips':'种植技巧',
          'Making Tips':'制作要点',
          'Profit Optimization':'收益优化',
          'Production Optimization':'生产优化',
          'Advanced Strategies':'高级策略',
          'Next Steps':'下一步',
          'Basic Bread Making':'基础面包制作',
          'Basic Bread Recipes':'基础面包配方',
          'Advanced Bread Recipes':'进阶面包配方',
          'Premium Bread Recipes':'高级面包配方',
          'Bread Varieties & Types':'面包种类'
        },
        'es': {
          'Basic Salad Recipes':'Recetas básicas de ensalada',
          'Luxury Salad Recipes':'Recetas de ensalada premium',
          'Basic Pizza Recipes':'Recetas básicas de pizza',
          'Advanced Pizza Recipes':'Recetas avanzadas de pizza',
          'Premium Recipes':'Recetas premium',
          'Pizza Varieties & Types':'Variedades de pizza',
          'Making Tips & Tricks':'Consejos y trucos',
          'Growing Tips':'Consejos de cultivo',
          'Making Tips':'Consejos de preparación',
          'Profit Optimization':'Optimización de ganancias',
          'Production Optimization':'Optimización de producción',
          'Advanced Strategies':'Estrategias avanzadas',
          'Next Steps':'Siguientes pasos',
          'Basic Bread Making':'Elaboración básica de pan',
          'Basic Bread Recipes':'Recetas básicas de pan',
          'Advanced Bread Recipes':'Recetas avanzadas de pan',
          'Premium Bread Recipes':'Recetas de pan premium',
          'Bread Varieties & Types':'Tipos de pan'
        },
        'pt-br': {
          'Basic Salad Recipes':'Receitas básicas de salada',
          'Luxury Salad Recipes':'Receitas de salada premium',
          'Basic Pizza Recipes':'Receitas básicas de pizza',
          'Advanced Pizza Recipes':'Receitas avançadas de pizza',
          'Premium Recipes':'Receitas premium',
          'Pizza Varieties & Types':'Tipos de pizza',
          'Making Tips & Tricks':'Dicas e truques',
          'Growing Tips':'Dicas de cultivo',
          'Making Tips':'Dicas de preparo',
          'Profit Optimization':'Otimização de lucro',
          'Production Optimization':'Otimização de produção',
          'Advanced Strategies':'Estratégias avançadas',
          'Next Steps':'Próximos passos',
          'Basic Bread Making':'Preparo básico de pão',
          'Basic Bread Recipes':'Receitas básicas de pão',
          'Advanced Bread Recipes':'Receitas avançadas de pão',
          'Premium Bread Recipes':'Receitas de pão premium',
          'Bread Varieties & Types':'Tipos de pão'
        },
        'fr': {
          'Basic Salad Recipes':'Recettes de salade de base',
          'Luxury Salad Recipes':'Recettes de salade haut de gamme',
          'Basic Pizza Recipes':'Recettes de pizza de base',
          'Advanced Pizza Recipes':'Recettes de pizza avancées',
          'Premium Recipes':'Recettes premium',
          'Pizza Varieties & Types':'Variétés de pizza',
          'Making Tips & Tricks':'Astuces et conseils',
          'Growing Tips':'Conseils de culture',
          'Making Tips':'Conseils de préparation',
          'Profit Optimization':'Optimisation du profit',
          'Production Optimization':'Optimisation de la production',
          'Advanced Strategies':'Stratégies avancées',
          'Next Steps':'Étapes suivantes',
          'Basic Bread Making':'Fabrication de pain de base',
          'Basic Bread Recipes':'Recettes de pain de base',
          'Advanced Bread Recipes':'Recettes de pain avancées',
          'Premium Bread Recipes':'Recettes de pain premium',
          'Bread Varieties & Types':'Variétés de pain'
        },
        'de': {
          'Basic Salad Recipes':'Grundlegende Salatrezepte',
          'Luxury Salad Recipes':'Luxus-Salatrezepte',
          'Basic Pizza Recipes':'Einfache Pizzarezepte',
          'Advanced Pizza Recipes':'Fortgeschrittene Pizzarezepte',
          'Premium Recipes':'Premium-Rezepte',
          'Pizza Varieties & Types':'Pizza-Varianten',
          'Making Tips & Tricks':'Tipps und Tricks',
          'Growing Tips':'Anbautipps',
          'Making Tips':'Zubereitungstipps',
          'Profit Optimization':'Gewinnoptimierung',
          'Production Optimization':'Produktionsoptimierung',
          'Advanced Strategies':'Fortgeschrittene Strategien',
          'Next Steps':'Nächste Schritte',
          'Basic Bread Making':'Grundlegendes Brotbacken',
          'Basic Bread Recipes':'Grundrezepte für Brot',
          'Advanced Bread Recipes':'Fortgeschrittene Brotrezepte',
          'Premium Bread Recipes':'Premium-Brotrezepte',
          'Bread Varieties & Types':'Brotarten'
        },
        'ru': {
          'Basic Salad Recipes':'Базовые рецепты салатов',
          'Luxury Salad Recipes':'Премиальные рецепты салатов',
          'Basic Pizza Recipes':'Базовые рецепты пиццы',
          'Advanced Pizza Recipes':'Продвинутые рецепты пиццы',
          'Premium Recipes':'Премиальные рецепты',
          'Pizza Varieties & Types':'Виды пиццы',
          'Making Tips & Tricks':'Советы и хитрости',
          'Growing Tips':'Советы по выращиванию',
          'Making Tips':'Советы по приготовлению',
          'Profit Optimization':'Оптимизация прибыли',
          'Production Optimization':'Оптимизация производства',
          'Advanced Strategies':'Продвинутые стратегии',
          'Next Steps':'Следующие шаги',
          'Basic Bread Making':'Основы выпечки хлеба',
          'Basic Bread Recipes':'Базовые рецепты хлеба',
          'Advanced Bread Recipes':'Продвинутые рецепты хлеба',
          'Premium Bread Recipes':'Премиальные рецепты хлеба',
          'Bread Varieties & Types':'Виды хлеба'
        },
        'ar': {
          'Basic Salad Recipes':'وصفات سلطة أساسية',
          'Luxury Salad Recipes':'وصفات سلطة فاخرة',
          'Basic Pizza Recipes':'وصفات بيتزا أساسية',
          'Advanced Pizza Recipes':'وصفات بيتزا متقدمة',
          'Premium Recipes':'وصفات مميزة',
          'Pizza Varieties & Types':'أنواع البيتزا',
          'Making Tips & Tricks':'نصائح وحيل',
          'Growing Tips':'نصائح الزراعة',
          'Making Tips':'نصائح التحضير',
          'Profit Optimization':'تحسين الأرباح',
          'Production Optimization':'تحسين الإنتاج',
          'Advanced Strategies':'استراتيجيات متقدمة',
          'Next Steps':'الخطوات التالية',
          'Basic Bread Making':'خبز أساسي',
          'Basic Bread Recipes':'وصفات خبز أساسية',
          'Advanced Bread Recipes':'وصفات خبز متقدمة',
          'Premium Bread Recipes':'وصفات خبز مميزة',
          'Bread Varieties & Types':'أنواع الخبز'
        },
        'hi': {
          'Basic Salad Recipes':'बेसिक सलाद रेसिपी',
          'Luxury Salad Recipes':'लक्ज़री सलाद रेसिपी',
          'Basic Pizza Recipes':'बेसिक पिज़्ज़ा रेसिपी',
          'Advanced Pizza Recipes':'एडवांस्ड पिज़्ज़ा रेसिपी',
          'Premium Recipes':'प्रीमियम रेसिपी',
          'Pizza Varieties & Types':'पिज़्ज़ा के प्रकार',
          'Making Tips & Tricks':'टिप्स और ट्रिक्स',
          'Growing Tips':'खेती के सुझाव',
          'Making Tips':'बनाने के सुझाव',
          'Profit Optimization':'लाभ अनुकूलन',
          'Production Optimization':'उत्पादन अनुकूलन',
          'Advanced Strategies':'उन्नत रणनीतियाँ',
          'Next Steps':'अगले कदम',
          'Basic Bread Making':'बेसिक ब्रेड बनाना',
          'Basic Bread Recipes':'बेसिक ब्रेड रेसिपी',
          'Advanced Bread Recipes':'एडवांस्ड ब्रेड रेसिपी',
          'Premium Bread Recipes':'प्रीमियम ब्रेड रेसिपी',
          'Bread Varieties & Types':'ब्रेड के प्रकार'
        },
        'id': {
          'Basic Salad Recipes':'Resep salad dasar',
          'Luxury Salad Recipes':'Resep salad premium',
          'Basic Pizza Recipes':'Resep pizza dasar',
          'Advanced Pizza Recipes':'Resep pizza lanjutan',
          'Premium Recipes':'Resep premium',
          'Pizza Varieties & Types':'Jenis pizza',
          'Making Tips & Tricks':'Tips & trik',
          'Growing Tips':'Tips budidaya',
          'Making Tips':'Tips pembuatan',
          'Profit Optimization':'Optimasi profit',
          'Production Optimization':'Optimasi produksi',
          'Advanced Strategies':'Strategi lanjutan',
          'Next Steps':'Langkah berikutnya',
          'Basic Bread Making':'Pembuatan roti dasar',
          'Basic Bread Recipes':'Resep roti dasar',
          'Advanced Bread Recipes':'Resep roti lanjutan',
          'Premium Bread Recipes':'Resep roti premium',
          'Bread Varieties & Types':'Jenis roti'
        },
        'vi': {
          'Basic Salad Recipes':'Công thức salad cơ bản',
          'Luxury Salad Recipes':'Công thức salad cao cấp',
          'Basic Pizza Recipes':'Công thức pizza cơ bản',
          'Advanced Pizza Recipes':'Công thức pizza nâng cao',
          'Premium Recipes':'Công thức cao cấp',
          'Pizza Varieties & Types':'Các loại pizza',
          'Making Tips & Tricks':'Mẹo và thủ thuật',
          'Growing Tips':'Mẹo trồng trọt',
          'Making Tips':'Mẹo chế biến',
          'Profit Optimization':'Tối ưu lợi nhuận',
          'Production Optimization':'Tối ưu sản xuất',
          'Advanced Strategies':'Chiến lược nâng cao',
          'Next Steps':'Bước tiếp theo',
          'Basic Bread Making':'Làm bánh mì cơ bản',
          'Basic Bread Recipes':'Công thức bánh mì cơ bản',
          'Advanced Bread Recipes':'Công thức bánh mì nâng cao',
          'Premium Bread Recipes':'Công thức bánh mì cao cấp',
          'Bread Varieties & Types':'Các loại bánh mì'
        }
      };
      const HEADINGS = HEADINGS_MAP[lang] || {};

      // Strong label mapping
      const STRONG_MAP = {
        'ja': {
          'Optimal Watering':'最適な水やり', 'Golden Hours':'ゴールデンアワー', 'Harvest Timing':'収穫タイミング', 'Soil Quality':'土壌品質',
          'Dough Quality':'生地の品質', 'Topping Balance':'トッピングのバランス', 'Recipe Efficiency':'レシピ効率', 'Storage Management':'在庫管理',
          'Market Timing':'市場のタイミング', 'Quality vs Quantity':'品質と量のバランス', 'Recipe Mastery':'レシピの習熟', 'Supply Chain':'サプライチェーン',
          'Automated Systems':'自動化システム', 'Batch Processing':'バッチ処理', 'Ingredient Rotation':'作物ローテーション', 'Quality Control':'品質管理',
          'Market Analysis':'市場分析', 'Recipe Optimization':'レシピ最適化', 'Resource Management':'リソース管理', 'Skill Development':'スキル向上',
          'Community Tip:':'コミュニティのヒント:'
        },
        'zh-cn': {
          'Optimal Watering':'最佳浇水', 'Golden Hours':'黄金时段', 'Harvest Timing':'收获时机', 'Soil Quality':'土壤质量',
          'Dough Quality':'面团质量', 'Topping Balance':'配料平衡', 'Recipe Efficiency':'配方效率', 'Storage Management':'库存管理',
          'Market Timing':'市场时机', 'Quality vs Quantity':'质量 vs 数量', 'Recipe Mastery':'配方熟练度', 'Supply Chain':'供应链',
          'Automated Systems':'自动化系统', 'Batch Processing':'批量处理', 'Ingredient Rotation':'轮作', 'Quality Control':'质量控制',
          'Market Analysis':'市场分析', 'Recipe Optimization':'配方优化', 'Resource Management':'资源管理', 'Skill Development':'技能提升',
          'Community Tip:':'社区提示：'
        },
        'es': {
          'Optimal Watering':'Riego óptimo', 'Golden Hours':'Horas doradas', 'Harvest Timing':'Momento de cosecha', 'Soil Quality':'Calidad del suelo',
          'Dough Quality':'Calidad de la masa', 'Topping Balance':'Equilibrio de ingredientes', 'Recipe Efficiency':'Eficiencia de recetas', 'Storage Management':'Gestión de inventario',
          'Market Timing':'Momento del mercado', 'Quality vs Quantity':'Calidad vs Cantidad', 'Recipe Mastery':'Maestría de recetas', 'Supply Chain':'Cadena de suministro',
          'Automated Systems':'Sistemas automatizados', 'Batch Processing':'Procesamiento por lotes', 'Ingredient Rotation':'Rotación de cultivos', 'Quality Control':'Control de calidad',
          'Market Analysis':'Análisis de mercado', 'Recipe Optimization':'Optimización de recetas', 'Resource Management':'Gestión de recursos', 'Skill Development':'Desarrollo de habilidades',
          'Community Tip:':'Consejo de la comunidad:'
        },
        'pt-br': {
          'Optimal Watering':'Rega ideal', 'Golden Hours':'Horas de ouro', 'Harvest Timing':'Momento da colheita', 'Soil Quality':'Qualidade do solo',
          'Dough Quality':'Qualidade da massa', 'Topping Balance':'Equilíbrio de coberturas', 'Recipe Efficiency':'Eficiência da receita', 'Storage Management':'Gestão de estoque',
          'Market Timing':'Momento de mercado', 'Quality vs Quantity':'Qualidade vs Quantidade', 'Recipe Mastery':'Domínio da receita', 'Supply Chain':'Cadeia de suprimentos',
          'Automated Systems':'Sistemas automatizados', 'Batch Processing':'Processamento em lote', 'Ingredient Rotation':'Rotação de culturas', 'Quality Control':'Controle de qualidade',
          'Market Analysis':'Análise de mercado', 'Recipe Optimization':'Otimização de receita', 'Resource Management':'Gestão de recursos', 'Skill Development':'Desenvolvimento de habilidades',
          'Community Tip:':'Dica da comunidade:'
        },
        'fr': {
          'Optimal Watering':'Arrosage optimal', 'Golden Hours':'Heures dorées', 'Harvest Timing':'Moment de récolte', 'Soil Quality':'Qualité du sol',
          'Dough Quality':'Qualité de la pâte', 'Topping Balance':'Équilibre des garnitures', 'Recipe Efficiency':'Efficacité des recettes', 'Storage Management':'Gestion du stock',
          'Market Timing':'Timing du marché', 'Quality vs Quantity':'Qualité vs Quantité', 'Recipe Mastery':'Maîtrise des recettes', 'Supply Chain':'Chaîne d\'approvisionnement',
          'Automated Systems':'Systèmes automatisés', 'Batch Processing':'Traitement par lot', 'Ingredient Rotation':'Rotation des cultures', 'Quality Control':'Contrôle qualité',
          'Market Analysis':'Analyse du marché', 'Recipe Optimization':'Optimisation des recettes', 'Resource Management':'Gestion des ressources', 'Skill Development':'Développement des compétences',
          'Community Tip:':'Astuce de la communauté :'
        },
        'de': {
          'Optimal Watering':'Optimale Bewässerung', 'Golden Hours':'Goldene Stunden', 'Harvest Timing':'Erntezeitpunkt', 'Soil Quality':'Bodenqualität',
          'Dough Quality':'Teigqualität', 'Topping Balance':'Belag-Balance', 'Recipe Efficiency':'Rezept-Effizienz', 'Storage Management':'Lagerverwaltung',
          'Market Timing':'Markt-Timing', 'Quality vs Quantity':'Qualität vs Quantität', 'Recipe Mastery':'Rezeptbeherrschung', 'Supply Chain':'Lieferkette',
          'Automated Systems':'Automatisierte Systeme', 'Batch Processing':'Batch-Verarbeitung', 'Ingredient Rotation':'Fruchtfolge', 'Quality Control':'Qualitätskontrolle',
          'Market Analysis':'Marktanalyse', 'Recipe Optimization':'Rezeptoptimierung', 'Resource Management':'Ressourcenmanagement', 'Skill Development':'Fähigkeitenentwicklung',
          'Community Tip:':'Community-Tipp:'
        },
        'ru': {
          'Optimal Watering':'Оптимальный полив', 'Golden Hours':'Золотые часы', 'Harvest Timing':'Время сбора', 'Soil Quality':'Качество почвы',
          'Dough Quality':'Качество теста', 'Topping Balance':'Баланс начинок', 'Recipe Efficiency':'Эффективность рецептов', 'Storage Management':'Управление запасами',
          'Market Timing':'Тайминг рынка', 'Quality vs Quantity':'Качество vs Количество', 'Recipe Mastery':'Мастерство рецептов', 'Supply Chain':'Цепочка поставок',
          'Automated Systems':'Автоматизированные системы', 'Batch Processing':'Пакетная обработка', 'Ingredient Rotation':'Севооборот', 'Quality Control':'Контроль качества',
          'Market Analysis':'Анализ рынка', 'Recipe Optimization':'Оптимизация рецептов', 'Resource Management':'Управление ресурсами', 'Skill Development':'Развитие навыков',
          'Community Tip:':'Совет сообщества:'
        },
        'ar': {
          'Optimal Watering':'الري الأمثل', 'Golden Hours':'الساعات الذهبية', 'Harvest Timing':'توقيت الحصاد', 'Soil Quality':'جودة التربة',
          'Dough Quality':'جودة العجين', 'Topping Balance':'توازن الإضافات', 'Recipe Efficiency':'كفاءة الوصفة', 'Storage Management':'إدارة المخزون',
          'Market Timing':'توقيت السوق', 'Quality vs Quantity':'الجودة مقابل الكمية', 'Recipe Mastery':'إتقان الوصفات', 'Supply Chain':'سلسلة الإمداد',
          'Automated Systems':'أنظمة مؤتمتة', 'Batch Processing':'المعالجة الدفعية', 'Ingredient Rotation':'دورة المحاصيل', 'Quality Control':'مراقبة الجودة',
          'Market Analysis':'تحليل السوق', 'Recipe Optimization':'تحسين الوصفات', 'Resource Management':'إدارة الموارد', 'Skill Development':'تطوير المهارات',
          'Community Tip:':'نصيحة المجتمع:'
        },
        'hi': {
          'Optimal Watering':'सर्वोत्तम सिंचाई', 'Golden Hours':'स्वर्णिम समय', 'Harvest Timing':'कटाई समय', 'Soil Quality':'मिट्टी की गुणवत्ता',
          'Dough Quality':'आटे की गुणवत्ता', 'Topping Balance':'टॉपिंग संतुलन', 'Recipe Efficiency':'रेसिपी दक्षता', 'Storage Management':'भंडारण प्रबंधन',
          'Market Timing':'बाज़ार समय', 'Quality vs Quantity':'गुणवत्ता बनाम मात्रा', 'Recipe Mastery':'रेसिपी महारत', 'Supply Chain':'आपूर्ति श्रृंखला',
          'Automated Systems':'स्वचालित प्रणालियाँ', 'Batch Processing':'बैच प्रसंस्करण', 'Ingredient Rotation':'फसल चक्र', 'Quality Control':'गुणवत्ता नियंत्रण',
          'Market Analysis':'बाज़ार विश्लेषण', 'Recipe Optimization':'रेसिपी अनुकूलन', 'Resource Management':'संसाधन प्रबंधन', 'Skill Development':'कौशल विकास',
          'Community Tip:':'समुदाय सुझाव:'
        },
        'id': {
          'Optimal Watering':'Penyiraman optimal', 'Golden Hours':'Jam emas', 'Harvest Timing':'Waktu panen', 'Soil Quality':'Kualitas tanah',
          'Dough Quality':'Kualitas adonan', 'Topping Balance':'Keseimbangan topping', 'Recipe Efficiency':'Efisiensi resep', 'Storage Management':'Manajemen persediaan',
          'Market Timing':'Timing pasar', 'Quality vs Quantity':'Kualitas vs Kuantitas', 'Recipe Mastery':'Penguasaan resep', 'Supply Chain':'Rantai pasok',
          'Automated Systems':'Sistem otomatis', 'Batch Processing':'Pemrosesan batch', 'Ingredient Rotation':'Rotasi tanaman', 'Quality Control':'Kontrol kualitas',
          'Market Analysis':'Analisis pasar', 'Recipe Optimization':'Optimasi resep', 'Resource Management':'Manajemen sumber daya', 'Skill Development':'Pengembangan keterampilan',
          'Community Tip:':'Tips komunitas:'
        },
        'vi': {
          'Optimal Watering':'Tưới nước tối ưu', 'Golden Hours':'Giờ vàng', 'Harvest Timing':'Thời điểm thu hoạch', 'Soil Quality':'Chất lượng đất',
          'Dough Quality':'Chất lượng bột', 'Topping Balance':'Cân bằng topping', 'Recipe Efficiency':'Hiệu quả công thức', 'Storage Management':'Quản lý kho',
          'Market Timing':'Thời điểm thị trường', 'Quality vs Quantity':'Chất lượng vs Số lượng', 'Recipe Mastery':'Thành thạo công thức', 'Supply Chain':'Chuỗi cung ứng',
          'Automated Systems':'Hệ thống tự động', 'Batch Processing':'Xử lý theo lô', 'Ingredient Rotation':'Luân canh', 'Quality Control':'Kiểm soát chất lượng',
          'Market Analysis':'Phân tích thị trường', 'Recipe Optimization':'Tối ưu công thức', 'Resource Management':'Quản lý tài nguyên', 'Skill Development':'Phát triển kỹ năng',
          'Community Tip:':'Mẹo cộng đồng:'
        }
      };
      const STRONG = STRONG_MAP[lang] || {};

      // Difficulty labels mapping
      const DIFF = ({
        'ja':    {Easy:'初級', Medium:'中級', Hard:'上級', Expert:'エキスパート', Master:'マスター', Legendary:'レジェンダリー'},
        'zh-cn': {Easy:'简单', Medium:'中等', Hard:'困难', Expert:'专家', Master:'大师', Legendary:'传说'},
        'es':    {Easy:'Fácil', Medium:'Medio', Hard:'Difícil', Expert:'Experto', Master:'Maestro', Legendary:'Legendario'},
        'pt-br': {Easy:'Fácil', Medium:'Médio', Hard:'Difícil', Expert:'Especialista', Master:'Mestre', Legendary:'Lendário'},
        'fr':    {Easy:'Facile', Medium:'Moyen', Hard:'Difficile', Expert:'Expert', Master:'Maître', Legendary:'Légendaire'},
        'de':    {Easy:'Leicht', Medium:'Mittel', Hard:'Schwer', Expert:'Experte', Master:'Meister', Legendary:'Legendär'},
        'ru':    {Easy:'Легко', Medium:'Средне', Hard:'Сложно', Expert:'Эксперт', Master:'Мастер', Legendary:'Легендарно'},
        'ar':    {Easy:'سهل', Medium:'متوسط', Hard:'صعب', Expert:'خبير', Master:'ماستر', Legendary:'أسطوري'},
        'hi':    {Easy:'आसान', Medium:'मध्यम', Hard:'कठिन', Expert:'विशेषज्ञ', Master:'मास्टर', Legendary:'लेजेंडरी'},
        'id':    {Easy:'Mudah', Medium:'Sedang', Hard:'Sulit', Expert:'Ahli', Master:'Master', Legendary:'Legendaris'},
        'vi':    {Easy:'Dễ', Medium:'Trung bình', Hard:'Khó', Expert:'Chuyên gia', Master:'Bậc thầy', Legendary:'Huyền thoại'}
      })[lang] || {};

      // Apply headings replacements
      document.querySelectorAll('h2, h3').forEach(h=>{
        const s = (h.textContent||'').trim();
        if (HEADINGS[s]) h.textContent = HEADINGS[s];
      });

      // Apply table headers
      document.querySelectorAll('table thead th').forEach(th=>{
        const s = (th.textContent||'').trim().toLowerCase();
        if ((/^name$|^.*name$/i.test(s)) && TABLE.name) th.textContent = TABLE.name;
        if ((/^ingredients$|^needed ingredients$/i.test(s)) && TABLE.ingredients) th.textContent = TABLE.ingredients;
        if ((/^time$|^cook time$|^prep time$|^調理時間$/i.test(s)) && TABLE.time) th.textContent = TABLE.time;
        if ((/^rewards$|^reward value$/i.test(s)) && TABLE.rewards) th.textContent = TABLE.rewards;
        if ((/^difficulty$/i.test(s)) && TABLE.difficulty) th.textContent = TABLE.difficulty;
      });

      // Apply difficulty labels
      document.querySelectorAll('.recipe-table td, .guide-difficulty, td, span').forEach(el=>{
        const v = (el.textContent||'').trim();
        if (DIFF[v]) el.textContent = DIFF[v];
      });

      // Units & simple replacements
      document.querySelectorAll('td, p, li, span').forEach(el=>{
        let txt = el.textContent;
        if (lang === 'ja')      txt = txt.replace(/(\d+)\s*minutes/gi, (m,g1)=> `${g1}分`).replace(/(\d+)\s*coins/gi, (m,g1)=> `${g1} コイン`);
        else if (lang === 'zh-cn') txt = txt.replace(/(\d+)\s*minutes/gi, (m,g1)=> `${g1} 分钟`).replace(/(\d+)\s*coins/gi, (m,g1)=> `${g1} 金币`);
        else if (lang === 'es')   txt = txt.replace(/(\d+)\s*minutes/gi, (m,g1)=> `${g1} minutos`).replace(/(\d+)\s*coins/gi, (m,g1)=> `${g1} monedas`);
        else if (lang === 'pt-br')txt = txt.replace(/(\d+)\s*minutes/gi, (m,g1)=> `${g1} min`).replace(/(\d+)\s*coins/gi, (m,g1)=> `${g1} moedas`);
        else if (lang === 'fr')   txt = txt.replace(/(\d+)\s*minutes/gi, (m,g1)=> `${g1} min`).replace(/(\d+)\s*coins/gi, (m,g1)=> `${g1} pièces`);
        else if (lang === 'de')   txt = txt.replace(/(\d+)\s*minutes/gi, (m,g1)=> `${g1} Min`).replace(/(\d+)\s*coins/gi, (m,g1)=> `${g1} Münzen`);
        else if (lang === 'ru')   txt = txt.replace(/(\d+)\s*minutes/gi, (m,g1)=> `${g1} мин`).replace(/(\d+)\s*coins/gi, (m,g1)=> `${g1} монет`);
        else if (lang === 'ar')   txt = txt.replace(/(\d+)\s*minutes/gi, (m,g1)=> `${g1} دقيقة`).replace(/(\d+)\s*coins/gi, (m,g1)=> `${g1} عملات`);
        else if (lang === 'hi')   txt = txt.replace(/(\d+)\s*minutes/gi, (m,g1)=> `${g1} मिनट`).replace(/(\d+)\s*coins/gi, (m,g1)=> `${g1} सिक्के`);
        else if (lang === 'id')   txt = txt.replace(/(\d+)\s*minutes/gi, (m,g1)=> `${g1} mnt`).replace(/(\d+)\s*coins/gi, (m,g1)=> `${g1} koin`);
        else if (lang === 'vi')   txt = txt.replace(/(\d+)\s*minutes/gi, (m,g1)=> `${g1} phút`).replace(/(\d+)\s*coins/gi, (m,g1)=> `${g1} xu`);
        el.textContent = txt;
      });

      // Strong labels
      document.querySelectorAll('strong').forEach(el=>{
        const s = (el.textContent||'').trim();
        if (STRONG[s]) el.textContent = STRONG[s];
      });

      // Ingredient cards: "Use:" label
      document.querySelectorAll('.ingredient-item p').forEach(p=>{
        const USE = {
          'en':'Use:', 'zh-cn':'用途：', 'ja':'用途：', 'es':'Uso:', 'pt-br':'Uso:', 'fr':'Utilisation :', 'de':'Verwendung:', 'ru':'Использование:', 'ar':'الاستخدام:', 'hi':'उपयोग:', 'id':'Kegunaan:', 'vi':'Cách dùng:'
        }[lang] || 'Use:';
        p.textContent = p.textContent.replace(/^\s*Use:\s*/i, USE);
      });

      // Q/A labels in FAQ blocks
      (function(){
        const QA = {
          'en': {Q:'Q:', A:'A:'},
          'zh-cn': {Q:'问：', A:'答：'},
          'ja': {Q:'Q：', A:'A：'},
          'es': {Q:'P:', A:'R:'},
          'pt-br': {Q:'P:', A:'R:'},
          'fr': {Q:'Q :', A:'R :'},
          'de': {Q:'F:', A:'A:'},
          'ru': {Q:'В:', A:'О:'},
          'ar': {Q:'س:', A:'ج:'},
          'hi': {Q:'प्र:', A:'उ:'},
          'id': {Q:'T:', A:'J:'},
          'vi': {Q:'H:', A:'Đ:'}
        }[lang] || {Q:'Q:', A:'A:'};
        document.querySelectorAll('#faq h3, #faq p').forEach(el=>{
          el.textContent = el.textContent.replace(/^\s*Q:\s*/i, QA.Q).replace(/^\s*A:\s*/i, QA.A);
        });
      })();

    }catch(_e){}
  }

  function switchLang(lang){
    if (!supported.includes(lang)) return;
    try { localStorage.setItem(storageKey, lang); } catch(_e){}

    const path = location.pathname || '/';
    const hash = location.hash || '';
    const search = location.search || '';

    const segments = path.split('/');
    const last = segments[segments.length - 1];
    let filename = (last && /.html$/i.test(last)) ? last.toLowerCase() : 'index.html';
    if (last === '' || last === null) filename = 'index.html';

    const target = `/${lang}/${filename}`;
    location.assign(target + (search || '') + hash);
  }

  // 暴露到全局，供其它组件调用
  try {
    window.__gagI18n = window.__gagI18n || {};
    window.__gagI18n.switchLang = switchLang;
    window.switchLang = switchLang;
  } catch(_e){}
  
  document.addEventListener("DOMContentLoaded",()=>{
    const lang = detectLang();
    applyI18n(lang);
    const sel = document.getElementById("lang-switcher"); if (sel) { sel.addEventListener("change", e=> switchLang(e.target.value)); }
    document.addEventListener('gag:i18n-refresh', ()=>{ const current = (window.__gagI18n && window.__gagI18n.lang) || lang; applyI18n(current); });
    disableFloatingFlagSidebar();
  });
})(); 