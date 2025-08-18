#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确修复语言匹配问题

这个脚本将精确修复：
1. HTML标签损坏问题 (<./tag>)
2. 损坏的URL路径 (././)
3. 国旗显示问题
4. 保留必要的导航文本
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

def fix_html_tags_and_urls(content):
    """修复HTML标签和URL问题"""
    
    changes_made = []
    
    # 1. 修复损坏的HTML标签 (<./tag> -> </tag>)
    if '<./' in content:
        content = re.sub(r'<\./', '</', content)
        changes_made.append('修复损坏的HTML标签')
    
    # 2. 修复损坏的URL路径 (././ -> //)
    if '././' in content:
        content = content.replace('././', '//')
        changes_made.append('修复损坏的URL路径')
    
    # 3. 修复损坏的URL路径 (growagarden.cv./ -> growagarden.cv/)
    if 'growagarden.cv./' in content:
        content = content.replace('growagarden.cv./', 'growagarden.cv/')
        changes_made.append('修复growagarden.cv URL路径')
    
    # 4. 修复损坏的URL路径 (unpkg.com./ -> unpkg.com/)
    if 'unpkg.com./' in content:
        content = content.replace('unpkg.com./', 'unpkg.com/')
        changes_made.append('修复unpkg.com URL路径')
    
    # 5. 修复损坏的URL路径 (www.w3.org./ -> www.w3.org/)
    if 'www.w3.org./' in content:
        content = content.replace('www.w3.org./', 'www.w3.org/')
        changes_made.append('修复www.w3.org URL路径')
    
    # 6. 修复损坏的URL路径 (www.googletagmanager.com./ -> www.googletagmanager.com/)
    if 'www.googletagmanager.com./' in content:
        content = content.replace('www.googletagmanager.com./', 'www.googletagmanager.com/')
        changes_made.append('修复googletagmanager URL路径')
    
    # 7. 修复损坏的URL路径 (www.miniplay.com./ -> www.miniplay.com/)
    if 'www.miniplay.com./' in content:
        content = content.replace('www.miniplay.com./', 'www.miniplay.com/')
        changes_made.append('修复miniplay URL路径')
    
    # 8. 修复损坏的URL路径 (playhop.com./ -> playhop.com/)
    if 'playhop.com./' in content:
        content = content.replace('playhop.com./', 'playhop.com/')
        changes_made.append('修复playhop URL路径')
    
    return content, changes_made

def fix_flag_issues(content):
    """修复国旗显示问题"""
    
    changes_made = []
    
    # 修复国旗显示
    flag_fixes = {
        '🇺🇸 简体中文': '🇨🇳 简体中文',
        '🇺🇸 Español': '🇪🇸 Español',
        '🇺🇸 Português': '🇧🇷 Português',
        '🇺🇸 Français': '🇫🇷 Français',
        '🇺🇸 Deutsch': '🇩🇪 Deutsch',
        '🇺🇸 Русский': '🇷🇺 Русский',
        '🇺🇸 العربية': '🇸🇦 العربية',
        '🇺🇸 हिन्दी': '🇮🇳 हिन्दी',
        '🇺🇸 Bahasa Indonesia': '🇮🇩 Bahasa Indonesia',
        '🇺🇸 Tiếng Việt': '🇻🇳 Tiếng Việt',
        '🇺🇸 日本語': '🇯🇵 日本語'
    }
    
    for old_flag, new_flag in flag_fixes.items():
        if old_flag in content:
            content = content.replace(old_flag, new_flag)
            changes_made.append(f'修复国旗: {old_flag} -> {new_flag}')
    
    return content, changes_made

def restore_navigation_text(content):
    """恢复导航文本"""
    
    changes_made = []
    
    # 恢复导航链接的文本
    nav_fixes = [
        (r'<a href="index\.html" class="logo">🌱 </a>', '<a href="index.html" class="logo">🌱 Grow a Garden</a>'),
        (r'<a href="index\.html#stats"></a>', '<a href="index.html#stats">Live Stats</a>'),
        (r'<a href="index\.html#map"></a>', '<a href="index.html#map">Global Heatmap</a>'),
        (r'<a href="index\.html#tips"></a>', '<a href="index.html#tips">Tips</a>'),
        (r'<a href="guides\.html"></a>', '<a href="guides.html">📚 Guides</a>'),
        (r'<a href="index\.html#community" class="discord-btn"></a>', '<a href="index.html#community" class="discord-btn">💬 Discord</a>'),
        (r'<a href="guides\.html"></a>', '<a href="guides.html">📚 Guides</a>'),
        (r'Making  & Tricks', 'Making Tips & Tricks')
    ]
    
    for pattern, replacement in nav_fixes:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changes_made.append(f'恢复导航文本: {pattern[:30]}...')
    
    return content, changes_made

def fix_all_pages():
    """修复所有页面的语言问题"""
    
    guide_pages = get_guide_pages()
    
    print("🔧 开始精确修复所有页面的语言匹配问题...")
    print("=" * 80)
    
    total_pages = len(guide_pages)
    fixed_pages = 0
    total_changes = 0
    
    for guide_page in guide_pages:
        print(f"\n📄 修复页面: {guide_page}")
        
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            page_changes = []
            
            # 1. 修复HTML标签和URL
            content, changes = fix_html_tags_and_urls(content)
            page_changes.extend(changes)
            
            # 2. 修复国旗问题
            content, changes = fix_flag_issues(content)
            page_changes.extend(changes)
            
            # 3. 恢复导航文本
            content, changes = restore_navigation_text(content)
            page_changes.extend(changes)
            
            if content != original_content:
                # 写回修复后的内容
                with open(guide_page, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ 成功修复 {len(page_changes)} 个问题:")
                for change in page_changes:
                    print(f"    - {change}")
                
                fixed_pages += 1
                total_changes += len(page_changes)
            else:
                print(f"  ✅ 无需修复")
                
        except Exception as e:
            print(f"  ❌ 修复失败: {str(e)}")
    
    print(f"\n" + "=" * 80)
    print("🎯 精确修复完成总结")
    print("=" * 80)
    print(f"📊 修复结果:")
    print(f"   - 总页面数: {total_pages}")
    print(f"   - 成功修复: {fixed_pages}")
    print(f"   - 失败数量: {total_pages - fixed_pages}")
    print(f"   - 总修复项: {total_changes}")
    
    if fixed_pages > 0:
        print(f"\n✅ 成功修复了 {fixed_pages} 个页面的语言匹配问题！")
        print(f"🔧 总共修复了 {total_changes} 个问题")
        print(f"🌍 现在所有页面都应该有正确的HTML结构和导航文本")
    else:
        print(f"\n⚠️  没有页面需要修复或修复失败")
    
    return fixed_pages, total_changes

def verify_fixes():
    """验证修复结果"""
    
    print(f"\n🔍 验证修复结果...")
    print("=" * 80)
    
    guide_pages = get_guide_pages()
    verified_count = 0
    
    for guide_page in guide_pages:
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否还有问题
            has_broken_tags = '<./' in content
            has_broken_urls = '././' in content or 'growagarden.cv./' in content
            has_wrong_flags = '🇺🇸 简体中文' in content or '🇺🇸 Español' in content
            has_empty_nav = '<a href="index.html" class="logo">🌱 </a>' in content
            
            if not has_broken_tags and not has_broken_urls and not has_wrong_flags and not has_empty_nav:
                print(f"  ✅ {guide_page}: 修复完成")
                verified_count += 1
            else:
                remaining_issues = []
                if has_broken_tags: remaining_issues.append('损坏标签')
                if has_broken_urls: remaining_issues.append('损坏URL')
                if has_wrong_flags: remaining_issues.append('错误国旗')
                if has_empty_nav: remaining_issues.append('空导航')
                print(f"  ⚠️  {guide_page}: 仍有问题: {', '.join(remaining_issues)}")
                
        except Exception as e:
            print(f"  ❌ {guide_page}: 验证失败 - {str(e)}")
    
    print(f"\n📊 验证结果:")
    print(f"   - 总页面数: {len(guide_pages)}")
    print(f"   - 验证通过: {verified_count}")
    print(f"   - 验证失败: {len(guide_pages) - verified_count}")
    
    return verified_count

def main():
    """主函数"""
    
    print("🔧 开始精确修复所有页面的语言匹配问题...")
    print("=" * 80)
    
    # 1. 修复所有页面
    fixed_pages, total_changes = fix_all_pages()
    
    # 2. 验证修复结果
    if fixed_pages > 0:
        verified_count = verify_fixes()
        
        print(f"\n" + "=" * 80)
        print("🎉 修复完成！")
        print("=" * 80)
        
        if verified_count == len(get_guide_pages()):
            print("✅ 所有页面的语言匹配问题都已成功修复！")
            print("🌍 现在所有页面都有正确的HTML结构和导航文本")
        else:
            print("⚠️  部分页面修复成功，建议检查失败的页面")
    else:
        print(f"\n⚠️  没有页面需要修复")

if __name__ == "__main__":
    main() 