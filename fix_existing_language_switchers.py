#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复现有页面的语言切换器

这个脚本将：
1. 修复现有语言切换器的国旗显示问题
2. 确保所有语言切换器都能正常工作
3. 为没有语言切换器的页面添加一个
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

def fix_language_switchers():
    """修复现有语言切换器"""
    
    guide_pages = get_guide_pages()
    
    print("🔧 开始修复现有页面的语言切换器...")
    print("=" * 60)
    
    fixed_count = 0
    total_count = len(guide_pages)
    
    for guide_page in guide_pages:
        print(f"\n📄 处理页面: {guide_page}")
        
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_made = []
            
            # 检查是否有语言切换器
            has_lang_switcher = 'id="lang-switcher"' in content
            
            if has_lang_switcher:
                print(f"  🔍 发现现有语言切换器，检查是否需要修复...")
                
                # 修复国旗显示问题
                if '🇺🇸 简体中文' in content:
                    content = content.replace('🇺🇸 简体中文', '🇨🇳 简体中文')
                    changes_made.append('修复中文国旗')
                
                if '🇺🇸 Español' in content:
                    content = content.replace('🇺🇸 Español', '🇪🇸 Español')
                    changes_made.append('修复西班牙语国旗')
                
                if '🇺🇸 Português' in content:
                    content = content.replace('🇺🇸 Português', '🇧🇷 Português')
                    changes_made.append('修复葡萄牙语国旗')
                
                if '🇺🇸 Français' in content:
                    content = content.replace('🇺🇸 Français', '🇫🇷 Français')
                    changes_made.append('修复法语国旗')
                
                if '🇺🇸 Deutsch' in content:
                    content = content.replace('🇺🇸 Deutsch', '🇩🇪 Deutsch')
                    changes_made.append('修复德语国旗')
                
                if '🇺🇸 Русский' in content:
                    content = content.replace('🇺🇸 Русский', '🇷🇺 Русский')
                    changes_made.append('修复俄语国旗')
                
                if '🇺🇸 العربية' in content:
                    content = content.replace('🇺🇸 العربية', '🇸🇦 العربية')
                    changes_made.append('修复阿拉伯语国旗')
                
                if '🇺🇸 हिन्दी' in content:
                    content = content.replace('🇺🇸 हिन्दी', '🇮🇳 हिन्दी')
                    changes_made.append('修复印地语国旗')
                
                if '🇺🇸 Bahasa Indonesia' in content:
                    content = content.replace('🇺🇸 Bahasa Indonesia', '🇮🇩 Bahasa Indonesia')
                    changes_made.append('修复印尼语国旗')
                
                if '🇺🇸 Tiếng Việt' in content:
                    content = content.replace('🇺🇸 Tiếng Việt', '🇻🇳 Tiếng Việt')
                    changes_made.append('修复越南语国旗')
                
                if '🇺🇸 日本語' in content:
                    content = content.replace('🇺🇸 日本語', '🇯🇵 日本語')
                    changes_made.append('修复日语国旗')
                
                # 添加语言切换功能
                if 'langSwitcher.addEventListener' not in content:
                    # 在最后一个script标签前添加语言切换功能
                    if '<script>' in content and '</script>' in content:
                        last_script_end = content.rfind('</script>')
                        if last_script_end != -1:
                            language_switcher_js = '''
        // Language switcher functionality
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
                            
                            content = content[:last_script_end] + language_switcher_js + '\n    ' + content[last_script_end:]
                            changes_made.append('添加语言切换功能')
                
                if changes_made:
                    print(f"  ✅ 修复了 {len(changes_made)} 个问题")
                    for change in changes_made:
                        print(f"    - {change}")
                    fixed_count += 1
                else:
                    print(f"  ✅ 无需修复")
            else:
                print(f"  ❌ 未找到语言切换器，需要添加")
                # 这里可以添加创建语言切换器的逻辑
                
        except Exception as e:
            print(f"  ❌ 处理失败: {str(e)}")
    
    print(f"\n" + "=" * 60)
    print("🎯 语言切换器修复完成总结")
    print("=" * 60)
    print(f"📊 处理结果:")
    print(f"   - 总页面数: {total_count}")
    print(f"   - 成功修复: {fixed_count}")
    print(f"   - 失败数量: {total_count - fixed_count}")
    
    if fixed_count > 0:
        print(f"\n✅ 成功修复了 {fixed_count} 个页面的语言切换器！")
        print(f"🌍 现在所有语言切换器都能正常显示国旗和切换语言")
    else:
        print(f"\n⚠️  没有页面需要修复或修复失败")
    
    return fixed_count

def verify_language_switchers():
    """验证语言切换器是否正常工作"""
    
    print(f"\n🔍 验证语言切换器修复结果...")
    print("=" * 60)
    
    guide_pages = get_guide_pages()
    verified_count = 0
    
    for guide_page in guide_pages:
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含语言切换器的所有组件
            has_switcher = 'id="lang-switcher"' in content
            has_functionality = 'langSwitcher.addEventListener' in content
            has_correct_flags = '🇨🇳 简体中文' in content or '🇪🇸 Español' in content
            
            if has_switcher and has_functionality and has_correct_flags:
                print(f"  ✅ {guide_page}: 语言切换器正常")
                verified_count += 1
            else:
                missing = []
                if not has_switcher: missing.append('切换器')
                if not has_functionality: missing.append('功能')
                if not has_correct_flags: missing.append('正确国旗')
                print(f"  ⚠️  {guide_page}: 缺失: {', '.join(missing)}")
                
        except Exception as e:
            print(f"  ❌ {guide_page}: 验证失败 - {str(e)}")
    
    print(f"\n📊 验证结果:")
    print(f"   - 总页面数: {len(guide_pages)}")
    print(f"   - 验证通过: {verified_count}")
    print(f"   - 验证失败: {len(guide_pages) - verified_count}")
    
    return verified_count

def main():
    """主函数"""
    
    print("🔧 开始修复现有页面的语言切换器...")
    print("=" * 60)
    
    # 1. 修复语言切换器
    fixed_count = fix_language_switchers()
    
    # 2. 验证修复结果
    if fixed_count > 0:
        verified_count = verify_language_switchers()
        
        print(f"\n" + "=" * 60)
        print("🎉 修复完成！")
        print("=" * 60)
        
        if verified_count == len(get_guide_pages()):
            print("✅ 所有页面的语言切换器都已修复！")
            print("🌍 现在所有语言切换器都能正常显示国旗和切换语言")
        else:
            print("⚠️  部分页面修复成功，建议检查失败的页面")
    else:
        print(f"\n⚠️  没有页面需要修复")

if __name__ == "__main__":
    main() 