#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有攻略页面添加标准的语言切换器

这个脚本将：
1. 为每个页面添加标准的语言切换器
2. 确保所有页面都有一致的语言切换体验
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

def add_language_switcher():
    """为所有页面添加语言切换器"""
    
    guide_pages = get_guide_pages()
    
    print("🌍 开始为所有攻略页面添加语言切换器...")
    print("=" * 60)
    
    # 标准的语言切换器HTML
    language_switcher_html = '''        <div class="language-switcher">
            <select id="lang-switcher">
                <option value="en">🇺🇸 English</option>
                <option value="zh-cn">🇨🇳 中文</option>
                <option value="es">🇪🇸 Español</option>
                <option value="pt-br">🇧🇷 Português</option>
                <option value="fr">🇫🇷 Français</option>
                <option value="de">🇩🇪 Deutsch</option>
                <option value="ru">🇷🇺 Русский</option>
                <option value="ar">🇸🇦 العربية</option>
                <option value="hi">🇮🇳 हिन्दी</option>
                <option value="id">🇮🇩 Bahasa Indonesia</option>
                <option value="vi">🇻🇳 Tiếng Việt</option>
                <option value="ja">🇯🇵 日本語</option>
            </select>
        </div>'''
    
    # 语言切换器CSS样式
    language_switcher_css = '''        .language-switcher {
            position: fixed;
            top: 100px;
            right: 20px;
            z-index: 100;
        }
        #lang-switcher {
            background: rgba(0, 0, 0, 0.7);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            cursor: pointer;
            backdrop-filter: blur(10px);
        }
        @media (max-width: 768px) {
            .language-switcher {
                position: static;
                margin: 1rem;
                display: inline-block;
            }
        }'''
    
    # 语言切换器JavaScript
    language_switcher_js = '''        // Language switcher functionality
        document.addEventListener('DOMContentLoaded', function() {
            const langSwitcher = document.getElementById('lang-switcher');
            
            if (langSwitcher) {
                langSwitcher.addEventListener('change', function() {
                    const selectedLang = this.value;
                    const currentPath = window.location.pathname;
                    let newPath;
                    
                    if (selectedLang === 'en') {
                        // Go to root directory
                        newPath = currentPath.replace(/^\/(zh-cn|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)\//, '/');
                    } else {
                        // Go to language directory
                        if (currentPath.includes('/zh-cn/') || currentPath.includes('/es/') || 
                            currentPath.includes('/pt-br/') || currentPath.includes('/fr/') || 
                            currentPath.includes('/de/') || currentPath.includes('/ru/') || 
                            currentPath.includes('/ar/') || currentPath.includes('/hi/') || 
                            currentPath.includes('/id/') || currentPath.includes('/vi/') || 
                            currentPath.includes('/ja/')) {
                            newPath = currentPath.replace(/\/(zh-cn|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)\//, '/' + selectedLang + '/');
                        } else {
                            newPath = '/' + selectedLang + currentPath;
                        }
                    }
                    
                    window.location.href = newPath;
                });
            }
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
            
            # 检查是否已经有语言切换器
            if 'id="lang-switcher"' in content:
                print(f"  ✅ 已有语言切换器，跳过")
                continue
            
            # 1. 添加语言切换器HTML到导航栏后面
            if '<nav>' in content and '</nav>' in content:
                # 在导航栏结束标签前插入语言切换器
                nav_end = content.find('</nav>')
                if nav_end != -1:
                    content = content[:nav_end] + language_switcher_html + '\n    ' + content[nav_end:]
                    changes_made.append('添加语言切换器HTML')
            
            # 2. 添加CSS样式
            if '<style>' in content and '</style>' in content:
                # 在style标签结束前插入CSS
                style_end = content.find('</style>')
                if style_end != -1:
                    content = content[:style_end] + '\n' + language_switcher_css + '\n    ' + content[style_end:]
                    changes_made.append('添加语言切换器CSS')
            
            # 3. 添加JavaScript功能
            if '<script>' in content and '</script>' in content:
                # 在最后一个script标签结束前插入JavaScript
                last_script_end = content.rfind('</script>')
                if last_script_end != -1:
                    content = content[:last_script_end] + '\n' + language_switcher_js + '\n    ' + content[last_script_end:]
                    changes_made.append('添加语言切换器JavaScript')
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(guide_page, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ 成功添加语言切换器")
                for change in changes_made:
                    print(f"    - {change}")
                fixed_count += 1
            else:
                print(f"  ⚠️  无法添加语言切换器，页面结构可能不标准")
                
        except Exception as e:
            print(f"  ❌ 处理失败: {str(e)}")
    
    print(f"\n" + "=" * 60)
    print("🎯 语言切换器添加完成总结")
    print("=" * 60)
    print(f"📊 处理结果:")
    print(f"   - 总页面数: {total_count}")
    print(f"   - 成功添加: {fixed_count}")
    print(f"   - 失败数量: {total_count - fixed_count}")
    
    if fixed_count > 0:
        print(f"\n✅ 成功为 {fixed_count} 个页面添加了语言切换器！")
        print(f"🌍 现在所有页面都支持完整的12种语言切换")
    else:
        print(f"\n⚠️  没有页面需要修复或修复失败")
    
    return fixed_count

def verify_language_switcher():
    """验证语言切换器是否添加成功"""
    
    print(f"\n🔍 验证语言切换器添加结果...")
    print("=" * 60)
    
    guide_pages = get_guide_pages()
    verified_count = 0
    
    for guide_page in guide_pages:
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含语言切换器的所有组件
            has_html = 'id="lang-switcher"' in content
            has_css = '.language-switcher' in content
            has_js = 'langSwitcher.addEventListener' in content
            
            if has_html and has_css and has_js:
                print(f"  ✅ {guide_page}: 语言切换器完整")
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
    
    print("🌍 开始为所有攻略页面添加语言切换器...")
    print("=" * 60)
    
    # 1. 添加语言切换器
    fixed_count = add_language_switcher()
    
    # 2. 验证添加结果
    if fixed_count > 0:
        verified_count = verify_language_switcher()
        
        print(f"\n" + "=" * 60)
        print("🎉 修复完成！")
        print("=" * 60)
        
        if verified_count == len(get_guide_pages()):
            print("✅ 所有页面都已成功添加语言切换器！")
            print("🌍 现在所有页面都支持完整的12种语言切换")
        else:
            print("⚠️  部分页面修复成功，建议检查失败的页面")
    else:
        print(f"\n⚠️  没有页面需要修复")

if __name__ == "__main__":
    main() 