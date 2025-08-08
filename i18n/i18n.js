(function(){
  const supported = ["en","zh-cn","es","pt-br","fr","de","ru","ar","hi","id","vi","ja"];
  const storageKey = "gag_lang";

  function getLangFromUrl(){
    const seg = location.pathname.split("/")[1]?.toLowerCase();
    return supported.includes(seg) ? seg : null;
  }
  
  function detectLang(){
    const fromUrl = getLangFromUrl();
    if (fromUrl) return fromUrl;
    
    const saved = localStorage.getItem(storageKey);
    if (saved && supported.includes(saved)) return saved;
    
    // 改进的浏览器语言检测
    const nav = (navigator.language || navigator.userLanguage || "en").toLowerCase();
    
    // 精确匹配
    if (supported.includes(nav)) return nav;
    
    // 前缀匹配
    const matched = supported.find(l => nav.startsWith(l));
    if (matched) return matched;
    
    // 特殊处理中文
    if (nav.startsWith("zh")) return "zh-cn";
    
    return "en";
  }
  
  async function applyI18n(lang){
    try{
      const dict = await fetch(`/i18n/${lang}.json`, {cache: "no-cache"}).then(r=>r.json());
      
      // 翻译 data-i18n 元素
      document.querySelectorAll("[data-i18n]").forEach(el=>{
        const key = el.getAttribute("data-i18n");
        if (dict[key]) el.textContent = dict[key];
      });
      
      // 翻译 data-i18n-placeholder 元素
      document.querySelectorAll("[data-i18n-placeholder]").forEach(el=>{
        const key = el.getAttribute("data-i18n-placeholder");
        if (dict[key]) el.placeholder = dict[key];
      });
      
      // 设置语言切换器
      const sel = document.getElementById("lang-switcher");
      if (sel) sel.value = lang;
      
    }catch(e){ 
      console.warn("i18n load failed", e); 
    }
  }
  
  function switchLang(lang){
    if (!supported.includes(lang)) return;
    
    localStorage.setItem(storageKey, lang);
    const parts = location.pathname.split("/");
    
    // 检查当前是否在语言子目录中
    if (supported.includes(parts[1])) {
      // 在语言子目录中，替换语言代码
      parts[1] = lang;
    } else {
      // 不在语言子目录中，插入语言代码
      parts.splice(1, 0, lang);
    }
    
    const newPath = parts.join("/");
    location.assign(newPath + location.search + location.hash);
  }
  
  document.addEventListener("DOMContentLoaded",()=>{
    const lang = detectLang();
    console.log("Detected language:", lang);
    applyI18n(lang);
    
    const sel = document.getElementById("lang-switcher");
    if (sel) {
      sel.addEventListener("change", e=> switchLang(e.target.value));
    }
  });
})(); 