#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复原来的图片国旗系统
"""

import os
import glob
import re

def get_html_files():
    """获取所有HTML文件"""
    return glob.glob('**/*.html', recursive=True)

def get_image_flag_language_switcher():
    """获取使用图片国旗的语言切换器HTML代码"""
    return '''            <div class="language-selector">
                <button class="lang-btn current" data-lang="en">
                    <img src="flags/en.png" alt="US Flag" class="flag-img">
                    <span class="code">US</span>
                </button>
                <div class="lang-dropdown">
                    <div class="lang-option" data-lang="en">
                        <img src="flags/en.png" alt="US Flag" class="flag-img">
                        <span class="code">US</span>
                    </div>
                    <div class="lang-option" data-lang="zh-cn">
                        <img src="flags/zh-cn.png" alt="CN Flag" class="flag-img">
                        <span class="code">CN</span>
                    </div>
                    <div class="lang-option" data-lang="es">
                        <img src="flags/es.png" alt="ES Flag" class="flag-img">
                        <span class="code">ES</span>
                    </div>
                    <div class="lang-option" data-lang="pt-br">
                        <img src="flags/pt-br.png" alt="BR Flag" class="flag-img">
                        <span class="code">BR</span>
                    </div>
                    <div class="lang-option" data-lang="fr">
                        <img src="flags/fr.png" alt="FR Flag" class="flag-img">
                        <span class="code">FR</span>
                    </div>
                    <div class="lang-option" data-lang="de">
                        <img src="flags/de.png" alt="DE Flag" class="flag-img">
                        <span class="code">DE</span>
                    </div>
                    <div class="lang-option" data-lang="ru">
                        <img src="flags/ru.png" alt="RU Flag" class="flag-img">
                        <span class="code">RU</span>
                    </div>
                    <div class="lang-option" data-lang="ar">
                        <img src="flags/ar.png" alt="SA Flag" class="flag-img">
                        <span class="code">SA</span>
                    </div>
                    <div class="lang-option" data-lang="hi">
                        <img src="flags/hi.png" alt="IN Flag" class="flag-img">
                        <span class="code">IN</span>
                    </div>
                    <div class="lang-option" data-lang="id">
                        <img src="flags/en.png" alt="ID Flag" class="flag-img">
                        <span class="code">ID</span>
                    </div>
                    <div class="lang-option" data-lang="vi">
                        <img src="flags/vi.png" alt="VN Flag" class="flag-img">
                        <span class="code">VN</span>
                    </div>
                    <div class="lang-option" data-lang="ja">
                        <img src="flags/ja.png" alt="JP Flag" class="flag-img">
                        <span class="code">JP</span>
                    </div>
                </div>
            </div>'''

def get_image_flag_css():
    """获取使用图片国旗的CSS样式"""
    return '''        /* 语言切换器统一样式 - 使用图片国旗 */
        .language-selector {
            position: relative;
            display: inline-block;
        }
        
        .lang-btn {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 0.5rem 1rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-family: inherit;
            transition: all 0.3s ease;
            min-width: 120px;
        }
        
        .lang-btn:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.3);
        }
        
        .lang-btn .flag-img {
            width: 24px;
            height: 16px;
            object-fit: cover;
            border-radius: 2px;
            vertical-align: middle;
        }
        
        .lang-btn .code {
            font-weight: 500;
        }
        
        .lang-dropdown {
            position: absolute;
            top: 100%;
            right: 0;
            background: rgba(0, 0, 0, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 0.5rem 0;
            min-width: 120px;
            display: none;
            z-index: 1000;
            backdrop-filter: blur(20px);
        }
        
        .language-selector:hover .lang-dropdown {
            display: block;
        }
        
        .lang-option {
            padding: 0.5rem 1rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: background 0.2s ease;
        }
        
        .lang-option:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        .lang-option .flag-img {
            width: 20px;
            height: 14px;
            object-fit: cover;
            border-radius: 2px;
            vertical-align: middle;
        }
        
        .lang-option .code {
            color: white;
            font-weight: 500;
        }'''

def get_image_flag_js():
    """获取使用图片国旗的JavaScript代码"""
    return '''        // 语言切换器功能 - 使用图片国旗
        document.addEventListener('DOMContentLoaded', function() {
            const langOptions = document.querySelectorAll('.lang-option');
            const currentLangBtn = document.querySelector('.lang-btn.current');
            
            // 设置当前语言
            function setCurrentLanguage(lang) {
                const langNames = {
                    'en': 'English',
                    'zh-cn': '简体中文',
                    'es': 'Español',
                    'pt-br': 'Português',
                    'fr': 'Français',
                    'de': 'Deutsch',
                    'ru': 'Русский',
                    'ar': 'العربية',
                    'hi': 'हिन्दी',
                    'id': 'Bahasa Indonesia',
                    'vi': 'Tiếng Việt',
                    'ja': '日本語'
                };
                
                const langCodes = {
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
                
                if (currentLangBtn) {
                    currentLangBtn.setAttribute('data-lang', lang);
                    currentLangBtn.querySelector('.code').textContent = langCodes[lang];
                    currentLangBtn.querySelector('.flag-img').src = `flags/${lang}.png`;
                }
                
                // 保存语言选择到localStorage
                localStorage.setItem('selectedLanguage', lang);
                
                // 跳转到对应语言页面
                const currentPath = window.location.pathname;
                const fileName = currentPath.split('/').pop() || 'index.html';
                
                if (lang === 'en') {
                    window.location.href = `./${fileName}`;
                } else {
                    window.location.href = `./${lang}/${fileName}`;
                }
            }
            
            // 为每个语言选项添加点击事件
            langOptions.forEach(option => {
                option.addEventListener('click', function() {
                    const lang = this.getAttribute('data-lang');
                    setCurrentLanguage(lang);
                });
            });
            
            // 从localStorage恢复语言选择
            const savedLang = localStorage.getItem('selectedLanguage');
            if (savedLang && savedLang !== 'en') {
                setCurrentLanguage(savedLang);
            }
        });'''

def restore_image_flags(content):
    """恢复图片国旗系统"""
    changes_made = []
    
    # 替换emoji国旗为图片国旗
    if 'flag-emoji' in content:
        # 替换HTML结构
        content = content.replace(get_emoji_flag_language_switcher(), get_image_flag_language_switcher())
        changes_made.append('恢复图片国旗HTML结构')
        
        # 替换CSS样式
        if 'flag-emoji' in content:
            content = content.replace('.flag-emoji', '.flag-img')
            changes_made.append('恢复图片国旗CSS样式')
    
    # 添加图片国旗CSS样式（如果不存在）
    if '.flag-img' not in content:
        # 在</style>标签前添加CSS
        if '</style>' in content:
            content = content.replace('</style>', get_image_flag_css() + '\n    </style>')
            changes_made.append('添加图片国旗CSS样式')
        # 如果没有style标签，在</head>前添加
        elif '</head>' in content:
            style_tag = f'    <style>\n{get_image_flag_css()}\n    </style>'
            content = content.replace('</head>', style_tag + '\n</head>')
            changes_made.append('添加style标签和图片国旗CSS样式')
    
    # 添加图片国旗JavaScript功能（如果不存在）
    if '图片国旗' not in content:
        # 在</script>标签前添加JS
        if '</script>' in content:
            content = content.replace('</script>', get_image_flag_js() + '\n    </script>')
            changes_made.append('添加图片国旗JavaScript功能')
        # 如果没有script标签，在</body>前添加
        elif '</body>' in content:
            script_tag = f'    <script>\n{get_image_flag_js()}\n    </script>'
            content = content.replace('</body>', script_tag + '\n</body>')
            changes_made.append('添加script标签和图片国旗JavaScript功能')
    
    return content, changes_made

def get_emoji_flag_language_switcher():
    """获取emoji国旗的语言切换器HTML代码（用于替换）"""
    return '''            <div class="language-selector">
                <button class="lang-btn current" data-lang="en">
                    <span class="flag-emoji">🇺🇸</span>
                    <span class="code">US</span>
                </button>
                <div class="lang-dropdown">
                    <div class="lang-option" data-lang="en">
                        <span class="flag-emoji">🇺🇸</span>
                        <span class="code">US</span>
                    </div>
                    <div class="lang-option" data-lang="zh-cn">
                        <span class="flag-emoji">🇨🇳</span>
                        <span class="code">CN</span>
                    </div>
                    <div class="lang-option" data-lang="es">
                        <span class="flag-emoji">🇪🇸</span>
                        <span class="code">ES</span>
                    </div>
                    <div class="lang-option" data-lang="pt-br">
                        <span class="flag-emoji">🇧🇷</span>
                        <span class="code">BR</span>
                    </div>
                    <div class="lang-option" data-lang="fr">
                        <span class="flag-emoji">🇫🇷</span>
                        <span class="code">FR</span>
                    </div>
                    <div class="lang-option" data-lang="de">
                        <span class="flag-emoji">🇩🇪</span>
                        <span class="code">DE</span>
                    </div>
                    <div class="lang-option" data-lang="ru">
                        <span class="flag-emoji">🇷🇺</span>
                        <span class="code">RU</span>
                    </div>
                    <div class="lang-option" data-lang="ar">
                        <span class="flag-emoji">🇸🇦</span>
                        <span class="code">SA</span>
                    </div>
                    <div class="lang-option" data-lang="hi">
                        <span class="flag-emoji">🇮🇳</span>
                        <span class="code">IN</span>
                    </div>
                    <div class="lang-option" data-lang="id">
                        <span class="flag-emoji">🇮🇩</span>
                        <span class="code">ID</span>
                    </div>
                    <div class="lang-option" data-lang="vi">
                        <span class="flag-emoji">🇻🇳</span>
                        <span class="code">VN</span>
                    </div>
                    <div class="lang-option" data-lang="ja">
                        <span class="flag-emoji">🇯🇵</span>
                        <span class="code">JP</span>
                    </div>
                </div>
            </div>'''

def restore_all_files():
    """恢复所有HTML文件的图片国旗系统"""
    
    html_files = get_html_files()
    
    print("🔧 开始恢复原来的图片国旗系统...")
    print("=" * 80)
    
    total_files = len(html_files)
    restored_files = 0
    total_changes = 0
    
    for html_file in html_files:
        print(f"\n📄 处理文件: {html_file}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_changes = []
            
            # 恢复图片国旗系统
            content, changes = restore_image_flags(content)
            file_changes.extend(changes)
            
            if content != original_content:
                # 写回恢复后的内容
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ 成功恢复 {len(file_changes)} 个组件:")
                for change in file_changes:
                    print(f"    - {change}")
                
                restored_files += 1
                total_changes += len(file_changes)
            else:
                print(f"  ✅ 无需修改")
                
        except Exception as e:
            print(f"  ❌ 处理失败: {str(e)}")
    
    print(f"\n" + "=" * 80)
    print("🎯 恢复完成总结")
    print("=" * 80)
    print(f"📊 恢复结果:")
    print(f"   - 总文件数: {total_files}")
    print(f"   - 成功恢复: {restored_files}")
    print(f"   - 失败数量: {total_files - restored_files}")
    print(f"   - 总恢复项: {total_changes}")
    
    if restored_files > 0:
        print(f"\n✅ 成功恢复了 {restored_files} 个文件的图片国旗系统！")
        print(f"🔧 总共恢复了 {total_changes} 个组件")
        print(f"🌍 现在所有页面都使用原来的图片国旗了")
    else:
        print(f"\n⚠️  没有文件需要恢复")
    
    return restored_files, total_changes

def main():
    """主函数"""
    
    print("🔧 开始恢复原来的图片国旗系统...")
    print("=" * 80)
    
    # 恢复所有文件
    restored_files, total_changes = restore_all_files()
    
    print(f"\n" + "=" * 80)
    print("🎉 恢复完成！")
    print("=" * 80)
    
    if restored_files > 0:
        print("✅ 所有页面的图片国旗系统都已恢复！")
        print("🌍 现在所有页面都使用原来的图片国旗了")
    else:
        print("⚠️  没有页面需要恢复")

if __name__ == "__main__":
    main() 