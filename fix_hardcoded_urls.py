#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复攻略页面中的硬编码URL问题

这个脚本将：
1. 修复硬编码的绝对路径URL
2. 将绝对路径改为相对路径
3. 确保所有链接都能正常工作
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

def fix_hardcoded_urls():
    """修复硬编码的URL问题"""
    
    guide_pages = get_guide_pages()
    
    print("🔧 开始修复攻略页面中的硬编码URL问题...")
    print("=" * 60)
    
    fixed_count = 0
    total_count = len(guide_pages)
    
    for guide_page in guide_pages:
        print(f"\n📄 修复页面: {guide_page}")
        
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_made = []
            
            # 修复 /i18n/i18n.js 路径
            if '/i18n/i18n.js' in content:
                content = content.replace('/i18n/i18n.js', 'i18n/i18n.js')
                changes_made.append('修复 /i18n/i18n.js 为相对路径')
            
            # 修复其他绝对路径
            # 将 / 开头的路径改为相对路径
            content = re.sub(r'href="/([^"]+)"', r'href="\1"', content)
            content = re.sub(r'src="/([^"]+)"', r'src="\1"', content)
            content = re.sub(r'action="/([^"]+)"', r'action="\1"', content)
            
            # 修复特定的绝对路径
            path_fixes = {
                '/': './',
                '/styles.css': 'styles.css',
                '/script.js': 'script.js',
                '/flags/': 'flags/',
                '/images/': 'images/',
            }
            
            for old_path, new_path in path_fixes.items():
                if old_path in content:
                    content = content.replace(old_path, new_path)
                    changes_made.append(f'修复 {old_path} 为 {new_path}')
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(guide_page, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ 成功修复 {len(changes_made)} 个URL问题")
                for change in changes_made:
                    print(f"    - {change}")
                fixed_count += 1
            else:
                print(f"  ✅ 无需修复")
                
        except Exception as e:
            print(f"  ❌ 修复失败: {str(e)}")
    
    print(f"\n" + "=" * 60)
    print("🎯 URL修复完成总结")
    print("=" * 60)
    print(f"📊 修复结果:")
    print(f"   - 总页面数: {total_count}")
    print(f"   - 成功修复: {fixed_count}")
    print(f"   - 失败数量: {total_count - fixed_count}")
    
    if fixed_count > 0:
        print(f"\n✅ 成功修复了 {fixed_count} 个页面的URL问题！")
        print(f"🌐 现在所有链接都使用相对路径，部署更加灵活")
    else:
        print(f"\n⚠️  没有页面需要修复或修复失败")
    
    return fixed_count

def verify_url_fixes():
    """验证URL修复结果"""
    
    print(f"\n🔍 验证URL修复结果...")
    print("=" * 60)
    
    guide_pages = get_guide_pages()
    verified_count = 0
    
    for guide_page in guide_pages:
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否还有硬编码的绝对路径
            hardcoded_patterns = [
                r'href="/[^"]+"',
                r'src="/[^"]+"',
                r'action="/[^"]+"',
            ]
            
            has_hardcoded = False
            for pattern in hardcoded_patterns:
                if re.search(pattern, content):
                    has_hardcoded = True
                    break
            
            if has_hardcoded:
                print(f"  ⚠️  {guide_page}: 仍存在硬编码URL")
            else:
                print(f"  ✅ {guide_page}: URL修复完成")
                verified_count += 1
                
        except Exception as e:
            print(f"  ❌ {guide_page}: 验证失败 - {str(e)}")
    
    print(f"\n📊 验证结果:")
    print(f"   - 总页面数: {len(guide_pages)}")
    print(f"   - 验证通过: {verified_count}")
    print(f"   - 验证失败: {len(guide_pages) - verified_count}")
    
    return verified_count

def main():
    """主函数"""
    
    print("🔧 开始修复攻略页面中的硬编码URL问题...")
    print("=" * 60)
    
    # 1. 修复硬编码URL
    fixed_count = fix_hardcoded_urls()
    
    # 2. 验证修复结果
    if fixed_count > 0:
        verified_count = verify_url_fixes()
        
        print(f"\n" + "=" * 60)
        print("🎉 修复完成！")
        print("=" * 60)
        
        if verified_count == len(get_guide_pages()):
            print("✅ 所有页面的URL问题都已成功修复！")
            print("🌐 现在所有链接都使用相对路径，部署更加灵活")
        else:
            print("⚠️  部分页面修复成功，建议检查失败的页面")
    else:
        print(f"\n⚠️  没有页面需要修复")

if __name__ == "__main__":
    main() 