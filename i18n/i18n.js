(function(){
  const supported = ["en","zh-cn"];
  const storageKey = "gag_lang";

  function getLangFromUrl(){
    const seg = location.pathname.split("/")[1]?.toLowerCase();
    return supported.includes(seg) ? seg : null;
  }
  function detectLang(){
    const fromUrl = getLangFromUrl();
    if (fromUrl) return fromUrl;
    const saved = localStorage.getItem(storageKey);
    if (supported.includes(saved)) return saved;
    const nav = (navigator.language || "en").toLowerCase();
    return supported.find(l => nav.startsWith(l)) || "en";
  }
  async function applyI18n(lang){
    try{
      const dict = await fetch(`/i18n/${lang}.json`, {cache: "no-cache"}).then(r=>r.json());
      document.querySelectorAll("[data-i18n]").forEach(el=>{
        const key = el.getAttribute("data-i18n");
        if (dict[key]) el.textContent = dict[key];
      });
      const sel = document.getElementById("lang-switcher");
      if (sel) sel.value = lang;
    }catch(e){ console.warn("i18n load failed", e); }
  }
  function switchLang(lang){
    localStorage.setItem(storageKey, lang);
    const parts = location.pathname.split("/");
    if (supported.includes(parts[1])) {
      parts[1] = lang;
    } else {
      parts.splice(1, 0, lang);
    }
    const newPath = parts.join("/");
    location.assign(newPath + location.search + location.hash);
  }
  document.addEventListener("DOMContentLoaded",()=>{
    const lang = detectLang();
    applyI18n(lang);
    const sel = document.getElementById("lang-switcher");
    if (sel) sel.addEventListener("change", e=> switchLang(e.target.value));
  });
})(); 