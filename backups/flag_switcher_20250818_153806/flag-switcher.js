// 国旗语言切换器功能
document.addEventListener('DOMContentLoaded', function() {
    const currentFlag = document.getElementById('current-flag');
    const flagDropdown = document.getElementById('flag-dropdown');

    // 语言到两字母代码映射（展示用）
    const langToCode = {
        'en': 'US',
        'zh-cn': 'CN',
        'es': 'ES',
        'pt-br': 'BR',
        'fr': 'FR',
        'de': 'DE',
        'ru': 'RU',
        'ar': 'SA',
        'hi': 'IN',
        'id': 'ID',
        'vi': 'VN',
        'ja': 'JP'
    };

    function getCode(lang){
        return langToCode[lang] || (lang || '').toUpperCase();
    }

    // 用更清晰的英文(US)国旗替换，避免小尺寸下不可见
    (function replaceEnFlag(){
        const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">\n' +
                    '<rect width="900" height="600" fill="#b22234"/>\n' +
                    // 6 条白色条纹
                    '<g fill="#fff">\n' +
                    '<rect y="46" width="900" height="46"/>\n' +
                    '<rect y="138" width="900" height="46"/>\n' +
                    '<rect y="230" width="900" height="46"/>\n' +
                    '<rect y="322" width="900" height="46"/>\n' +
                    '<rect y="414" width="900" height="46"/>\n' +
                    '<rect y="506" width="900" height="46"/>\n' +
                    '</g>\n' +
                    // 蓝色星区（不画星以保证小尺寸清晰）
                    '<rect width="360" height="322" fill="#3c3b6e"/>\n' +
                    '</svg>';
        const dataUrl = 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(svg);
        document.querySelectorAll('.flag-option[data-lang="en"] img').forEach(img=>{ img.src = dataUrl; img.alt = 'en Flag'; });
    })();

    // 将下拉中每个选项的文字替换为两字母代码
    document.querySelectorAll('.flag-option').forEach(option => {
        const lang = option.getAttribute('data-lang');
        const nameEl = option.querySelector('.flag-name');
        if (nameEl) nameEl.textContent = getCode(lang);
    });
    
    if (currentFlag && flagDropdown) {
        // 设置当前语言的国旗
        const currentLang = document.documentElement.getAttribute('lang') || 'en';
        updateCurrentFlag(currentLang);

        // 为每个国旗选项添加点击事件
        document.querySelectorAll('.flag-option').forEach(option => {
            option.addEventListener('click', function() {
                const lang = this.getAttribute('data-lang');
                if (lang) {
                    // 调用现有的语言切换函数
                    if (typeof switchLang === 'function') {
                        switchLang(lang);
                    } else if (typeof window.__gagI18n !== 'undefined' && window.__gagI18n.switchLang) {
                        window.__gagI18n.switchLang(lang);
                    }
                }
            });
        });
    }
});

function updateCurrentFlag(lang) {
    const currentFlag = document.getElementById('current-flag');
    if (currentFlag) {
        const flagOptions = document.querySelectorAll('.flag-option');
        flagOptions.forEach(option => {
            if (option.getAttribute('data-lang') === lang) {
                // 复制对应选项（包含图片与两字母代码）到按钮
                const flagContent = option.innerHTML;
                currentFlag.innerHTML = flagContent;
                return;
            }
        });
    }
} 