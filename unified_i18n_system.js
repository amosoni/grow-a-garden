// 统一的国际化管理系统
class UnifiedI18nSystem {
    constructor() {
        this.currentLanguage = this.detectLanguage();
        this.translations = {};
        this.initialized = false;
        this.init();
    }

    // 检测当前语言
    detectLanguage() {
        // 从URL路径检测语言
        const path = window.location.pathname;
        const langMatch = path.match(/^\/([a-z]{2}(?:-[a-z]{2})?)\//);
        if (langMatch) {
            return langMatch[1];
        }
        
        // 从HTML lang属性检测
        const htmlLang = document.documentElement.lang;
        if (htmlLang && htmlLang !== 'en') {
            return htmlLang;
        }
        
        // 从localStorage检测
        const savedLang = localStorage.getItem('preferred-language');
        if (savedLang) {
            return savedLang;
        }
        
        // 默认返回英文
        return 'en';
    }

    // 初始化系统
    async init() {
        try {
            await this.loadTranslations(this.currentLanguage);
            this.applyTranslations();
            this.setupLanguageSwitcher();
            this.initialized = true;
            console.log(`🌐 国际化系统已初始化，当前语言: ${this.currentLanguage}`);
        } catch (error) {
            console.error('❌ 国际化系统初始化失败:', error);
        }
    }

    // 加载翻译文件
    async loadTranslations(langCode) {
        try {
            const response = await fetch(`/i18n/${langCode}.json`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            this.translations = await response.json();
            console.log(`✅ 已加载 ${langCode} 语言包，共 ${Object.keys(this.translations).length} 个翻译项`);
        } catch (error) {
            console.warn(`⚠️ 无法加载 ${langCode} 语言包，使用英文作为后备:`, error);
            // 如果无法加载指定语言，尝试加载英文
            if (langCode !== 'en') {
                await this.loadTranslations('en');
            }
        }
    }

    // 应用翻译到页面
    applyTranslations() {
        const elements = document.querySelectorAll('[data-i18n]');
        let translatedCount = 0;

        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.translations[key];
            
            if (translation) {
                // 根据元素类型应用翻译
                if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                    element.placeholder = translation;
                } else if (element.tagName === 'IMG') {
                    element.alt = translation;
                } else {
                    element.textContent = translation;
                }
                translatedCount++;
            } else {
                // 如果没有找到翻译，保持原内容
                console.warn(`⚠️ 未找到翻译键: ${key}`);
            }
        });

        console.log(`✅ 已应用 ${translatedCount} 个翻译项`);
    }

    // 设置语言切换器
    setupLanguageSwitcher() {
        // 查找所有语言切换按钮
        const langButtons = document.querySelectorAll('.lang-btn, .language-selector button, [data-lang]');
        
        langButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const langCode = button.getAttribute('data-lang') || 
                               button.textContent.trim().toLowerCase() ||
                               this.detectLanguageFromButton(button);
                
                if (langCode && langCode !== this.currentLanguage) {
                    this.switchLanguage(langCode);
                }
            });
        });

        // 设置语言选择下拉菜单
        const langOptions = document.querySelectorAll('.lang-option, .language-dropdown a');
        langOptions.forEach(option => {
            option.addEventListener('click', (e) => {
                e.preventDefault();
                const href = option.getAttribute('href');
                const langCode = this.extractLanguageFromHref(href);
                
                if (langCode && langCode !== this.currentLanguage) {
                    this.switchLanguage(langCode);
                }
            });
        });
    }

    // 从按钮检测语言代码
    detectLanguageFromButton(button) {
        const text = button.textContent.trim();
        const langMap = {
            '🇺🇸': 'en', '🇨🇳': 'zh-cn', '🇪🇸': 'es', '🇫🇷': 'fr',
            '🇩🇪': 'de', '🇷🇺': 'ru', '🇸🇦': 'ar', '🇮🇳': 'hi',
            '🇮🇩': 'id', '🇻🇳': 'vi', '🇯🇵': 'ja', '🇧🇷': 'pt-br'
        };
        
        for (const [flag, lang] of Object.entries(langMap)) {
            if (text.includes(flag)) {
                return lang;
            }
        }
        
        return null;
    }

    // 从href提取语言代码
    extractLanguageFromHref(href) {
        const match = href.match(/^\/([a-z]{2}(?:-[a-z]{2})?)\//);
        return match ? match[1] : null;
    }

    // 切换语言
    async switchLanguage(newLangCode) {
        if (newLangCode === this.currentLanguage) {
            return;
        }

        console.log(`🔄 正在切换语言: ${this.currentLanguage} → ${newLangCode}`);
        
        try {
            // 加载新语言的翻译
            await this.loadTranslations(newLangCode);
            
            // 更新当前语言
            this.currentLanguage = newLangCode;
            
            // 保存用户偏好
            localStorage.setItem('preferred-language', newLangCode);
            
            // 应用新翻译
            this.applyTranslations();
            
            // 更新页面语言属性
            document.documentElement.lang = newLangCode;
            
            // 更新URL（如果可能）
            this.updateURL(newLangCode);
            
            console.log(`✅ 语言切换完成: ${newLangCode}`);
            
        } catch (error) {
            console.error('❌ 语言切换失败:', error);
        }
    }

    // 更新URL
    updateURL(newLangCode) {
        const currentPath = window.location.pathname;
        const newPath = currentPath.replace(/^\/([a-z]{2}(?:-[a-z]{2})?)\//, `/${newLangCode}/`);
        
        if (newPath !== currentPath) {
            // 使用history API更新URL，不刷新页面
            window.history.pushState({}, '', newPath);
        }
    }

    // 获取翻译文本
    getText(key, defaultValue = '') {
        return this.translations[key] || defaultValue || key;
    }

    // 获取当前语言
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    // 检查是否已初始化
    isReady() {
        return this.initialized;
    }
}

// 全局国际化系统实例
window.i18nSystem = new UnifiedI18nSystem();

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    if (!window.i18nSystem.isReady()) {
        window.i18nSystem.init();
    }
});

// 导出到全局作用域
window.UnifiedI18nSystem = UnifiedI18nSystem; 