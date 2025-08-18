#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有攻略页面添加国旗语言切换器

这个脚本将：
1. 为每个页面添加您现有的国旗语言切换器
2. 保持您原有的设计风格
3. 支持完整的12种语言
"""

import os
import glob
import re

def get_guide_pages():
    """获取所有攻略页面列表"""
    root_guides = glob.glob('*.html')
    guide_pages = []
    
    for page in root_guides:
        if page.startswith('how-to-') or page.startswith('ice-cream-') or page in ['guides.html', 'index.html', 'online.html']:
            guide_pages.append(page)
    
    return guide_pages

def add_flag_language_switcher():
    """为所有页面添加国旗语言切换器"""
    
    guide_pages = get_guide_pages()
    
    print("🏁 开始为所有攻略页面添加国旗语言切换器...")
    print("=" * 60)
    
    # 国旗语言切换器HTML (基于您现有的设计)
    flag_language_switcher_html = '''            <div class="language-selector">
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
    
    # 国旗语言切换器CSS样式 (基于您现有的设计)
    flag_language_switcher_css = '''        /* 自定义语言选择器样式 */
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
    
    # 国旗语言切换器JavaScript功能
    flag_language_switcher_js = '''        // 国旗语言切换器功能
        document.addEventListener('DOMContentLoaded', function() {
            const langOptions = document.querySelectorAll('.lang-option');
            const currentLangBtn = document.querySelector('.lang-btn');
            const langDropdown = document.querySelector('.lang-dropdown');
            
            if (!currentLangBtn || !langDropdown || langOptions.length === 0) {
                return;
            }
            
            // 为每个语言选项添加点击事件
            langOptions.forEach((option) => {
                option.addEventListener('click', function(e) {
                    e.stopPropagation();
                    const lang = this.getAttribute('data-lang');
                    const flagElement = this.querySelector('.flag-img');
                    const codeElement = this.querySelector('.code');
                    
                    if (flagElement && codeElement) {
                        // 复制国旗图片到当前按钮
                        const currentFlagElement = currentLangBtn.querySelector('.flag-img');
                        const currentCodeElement = currentLangBtn.querySelector('.code');
                        
                        if (currentFlagElement && currentCodeElement) {
                            currentFlagElement.src = flagElement.src;
                            currentCodeElement.textContent = codeElement.textContent;
                            currentLangBtn.setAttribute('data-lang', lang);
                            
                            // 切换语言页面
                            const currentPath = window.location.pathname;
                            let newPath;
                            
                            if (lang === 'en') {
                                // 跳转到根目录
                                newPath = currentPath.replace(/^\/(zh-cn|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)\//, '/');
                            } else {
                                // 跳转到对应语言目录
                                if (currentPath.includes('/zh-cn/') || currentPath.includes('/es/') || 
                                    currentPath.includes('/pt-br/') || currentPath.includes('/fr/') || 
                                    currentPath.includes('/de/') || currentPath.includes('/ru/') || 
                                    currentPath.includes('/ar/') || currentPath.includes('/hi/') || 
                                    currentPath.includes('/id/') || currentPath.includes('/vi/') || 
                                    currentPath.includes('/ja/')) {
                                    newPath = currentPath.replace(/\/(zh-cn|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)\//, '/' + lang + '/');
                                } else {
                                    newPath = '/' + lang + currentPath;
                                }
                            }
                            
                            window.location.href = newPath;
                        }
                    }
                    
                    // 隐藏下拉菜单
                    langDropdown.style.display = 'none';
                });
            });
            
            // 点击按钮显示/隐藏下拉菜单
            currentLangBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                const isVisible = langDropdown.style.display === 'block';
                langDropdown.style.display = isVisible ? 'none' : 'block';
            });
            
            // 点击其他地方隐藏下拉菜单
            document.addEventListener('click', function() {
                langDropdown.style.display = 'none';
            });
            
            // 初始化当前语言
            function initializeLanguage() {
                const currentPath = window.location.pathname;
                let currentLang = 'en';
                
                const langMatch = currentPath.match(/\/(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)\//);
                if (langMatch) {
                    currentLang = langMatch[1];
                }
                
                currentLangBtn.setAttribute('data-lang', currentLang);
                
                const targetOption = document.querySelector(`.lang-option[data-lang="${currentLang}"]`);
                if (targetOption) {
                    const flagElement = targetOption.querySelector('.flag-img');
                    const codeElement = targetOption.querySelector('.code');
                    const currentFlagElement = currentLangBtn.querySelector('.flag-img');
                    const currentCodeElement = currentLangBtn.querySelector('.code');
                    
                    if (flagElement && codeElement && currentFlagElement && currentCodeElement) {
                        currentFlagElement.src = flagElement.src;
                        currentCodeElement.textContent = codeElement.textContent;
                    }
                }
            }
            
            initializeLanguage();
        });'''
    
    fixed_count = 0
    total_count = len(guide_pages)
    
    for guide_page in guide_pages:
        print(f"\n📄 处理页面: {guide_page}")
        
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_made = []
            
            # 检查是否已经有国旗语言切换器
            if 'class="language-selector"' in content:
                print(f"  ✅ 已有国旗语言切换器，跳过")
                continue
            
            # 1. 添加国旗语言切换器HTML到导航栏后面
            if '<nav>' in content and '</nav>' in content:
                # 在导航栏结束标签前插入国旗语言切换器
                nav_end = content.find('</nav>')
                if nav_end != -1:
                    content = content[:nav_end] + flag_language_switcher_html + '\n        ' + content[nav_end:]
                    changes_made.append('添加国旗语言切换器HTML')
            
            # 2. 添加CSS样式
            if '<style>' in content and '</style>' in content:
                # 在style标签结束前插入CSS
                style_end = content.find('</style>')
                if style_end != -1:
                    content = content[:style_end] + '\n' + flag_language_switcher_css + '\n    ' + content[style_end:]
                    changes_made.append('添加国旗语言切换器CSS')
            
            # 3. 添加JavaScript功能
            if '<script>' in content and '</script>' in content:
                # 在最后一个script标签结束前插入JavaScript
                last_script_end = content.rfind('</script>')
                if last_script_end != -1:
                    content = content[:last_script_end] + '\n' + flag_language_switcher_js + '\n    ' + content[last_script_end:]
                    changes_made.append('添加国旗语言切换器JavaScript')
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(guide_page, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ 成功添加国旗语言切换器")
                for change in changes_made:
                    print(f"    - {change}")
                fixed_count += 1
            else:
                print(f"  ⚠️  无法添加国旗语言切换器，页面结构可能不标准")
                
        except Exception as e:
            print(f"  ❌ 处理失败: {str(e)}")
    
    print(f"\n" + "=" * 60)
    print("🎯 国旗语言切换器添加完成总结")
    print("=" * 60)
    print(f"📊 处理结果:")
    print(f"   - 总页面数: {total_count}")
    print(f"   - 成功添加: {fixed_count}")
    print(f"   - 失败数量: {total_count - fixed_count}")
    
    if fixed_count > 0:
        print(f"\n✅ 成功为 {fixed_count} 个页面添加了国旗语言切换器！")
        print(f"🏁 现在所有页面都支持完整的12种语言切换")
    else:
        print(f"\n⚠️  没有页面需要修复或修复失败")
    
    return fixed_count

def verify_flag_language_switcher():
    """验证国旗语言切换器是否添加成功"""
    
    print(f"\n🔍 验证国旗语言切换器添加结果...")
    print("=" * 60)
    
    guide_pages = get_guide_pages()
    verified_count = 0
    
    for guide_page in guide_pages:
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含国旗语言切换器的所有组件
            has_html = 'class="language-selector"' in content
            has_css = '.language-selector' in content
            has_js = '国旗语言切换器功能' in content
            
            if has_html and has_css and has_js:
                print(f"  ✅ {guide_page}: 国旗语言切换器完整")
                verified_count += 1
            else:
                missing = []
                if not has_html: missing.append('HTML')
                if not has_css: missing.append('CSS')
                if not has_js: missing.append('JavaScript')
                print(f"  ⚠️  {guide_page}: 缺失组件: {', '.join(missing)}")
                
        except Exception as e:
            print(f"  ❌ {guide_page}: 验证失败 - {str(e)}")
    
    print(f"\n📊 验证结果:")
    print(f"   - 总页面数: {len(guide_pages)}")
    print(f"   - 验证通过: {verified_count}")
    print(f"   - 验证失败: {len(guide_pages) - verified_count}")
    
    return verified_count

def main():
    """主函数"""
    
    print("🏁 开始为所有攻略页面添加国旗语言切换器...")
    print("=" * 60)
    
    # 1. 添加国旗语言切换器
    fixed_count = add_flag_language_switcher()
    
    # 2. 验证添加结果
    if fixed_count > 0:
        verified_count = verify_flag_language_switcher()
        
        print(f"\n" + "=" * 60)
        print("🎉 修复完成！")
        print("=" * 60)
        
        if verified_count == len(get_guide_pages()):
            print("✅ 所有页面都已成功添加国旗语言切换器！")
            print("🏁 现在所有页面都支持完整的12种语言切换")
        else:
            print("⚠️  部分页面修复成功，建议检查失败的页面")
    else:
        print(f"\n⚠️  没有页面需要修复")

if __name__ == "__main__":
    main() 