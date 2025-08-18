#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复最终剩余的语言问题
"""

import os
import glob
import re

def get_html_files():
    """获取所有HTML文件"""
    return glob.glob('*.html')

def fix_final_issues(content):
    """修复最终剩余的问题"""
    
    changes_made = []
    
    # 修复所有剩余的损坏URL模式
    final_fixes = [
        # 修复复杂的URL模式
        ('"url": "https://./-.",', '"url": "https://growagarden.cv",'),
        ('"url":"https://./-.",', '"url": "https://growagarden.cv",'),
        ('"url": "https://./---.",', '"url": "https://growagarden.cv",'),
        ('"url":"https://./---.",', '"url": "https://growagarden.cv",'),
        ('"url": "https://./----.",', '"url": "https://growagarden.cv",'),
        ('"url":"https://./----.",', '"url": "https://growagarden.cv",'),
        
        # 修复复杂的hreflang URL
        ('href="https://././---."', 'href="https://growagarden.cv"'),
        ('href="https://./-./---."', 'href="https://growagarden.cv"'),
        ('href="https://././."', 'href="https://growagarden.cv"'),
        ('href="https://./-./."', 'href="https://growagarden.cv"'),
        ('href="https://./----." ./', 'href="https://growagarden.cv"'),
        ('content="https://./----." ./', 'content="https://growagarden.cv"'),
        
        # 修复复杂的Open Graph URL
        ('content="https://./."', 'content="https://growagarden.cv"'),
        ('content="https://./---."', 'content="https://growagarden.cv"'),
        
        # 修复复杂的JSON-LD URL
        ('"url": "https://./---."', '"url": "https://growagarden.cv"'),
        ('"url":"https://./---."', '"url": "https://growagarden.cv"'),
        
        # 修复复杂的链接
        ('<a href="https://./" "" "-"', '<a href="https://growagarden.cv"'),
        ('<a href="https://./" ""./', '<a href="https://growagarden.cv"'),
        ('<a href="https://./" ""  /', '<a href="https://growagarden.cv"'),
        ('<a href="https://./" "" //', '<a href="https://growagarden.cv"'),
        ('<p>🎮 Playing on <a href="https://./" ""./', '<p>🎮 Playing on <a href="https://growagarden.cv"'),
        ('📊 <a href="https://./" ""  /', '📊 <a href="https://growagarden.cv"'),
        ('🧮 <a href="https://./" "" //', '🧮 <a href="https://growagarden.cv"'),
    ]
    
    for old_text, new_text in final_fixes:
        if old_text in content:
            content = content.replace(old_text, new_text)
            changes_made.append(f'修复: {old_text[:30]}...')
    
    return content, changes_made

def fix_all_files():
    """修复所有HTML文件"""
    
    html_files = get_html_files()
    
    print("🔧 开始修复最终剩余的语言问题...")
    print("=" * 80)
    
    total_files = len(html_files)
    fixed_files = 0
    total_changes = 0
    
    for html_file in html_files:
        print(f"\n📄 修复文件: {html_file}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_changes = []
            
            # 修复最终问题
            content, changes = fix_final_issues(content)
            file_changes.extend(changes)
            
            if content != original_content:
                # 写回修复后的内容
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ 成功修复 {len(file_changes)} 个问题:")
                for change in file_changes:
                    print(f"    - {change}")
                
                fixed_files += 1
                total_changes += len(file_changes)
            else:
                print(f"  ✅ 无需修复")
                
        except Exception as e:
            print(f"  ❌ 修复失败: {str(e)}")
    
    print(f"\n" + "=" * 80)
    print("🎯 修复完成总结")
    print("=" * 80)
    print(f"📊 修复结果:")
    print(f"   - 总文件数: {total_files}")
    print(f"   - 成功修复: {fixed_files}")
    print(f"   - 失败数量: {total_files - fixed_files}")
    print(f"   - 总修复项: {total_changes}")
    
    if fixed_files > 0:
        print(f"\n✅ 成功修复了 {fixed_files} 个文件的最终语言问题！")
        print(f"🔧 总共修复了 {total_changes} 个问题")
        print(f"🌍 现在所有URL和代码都应该正常了")
    else:
        print(f"\n⚠️  没有文件需要修复或修复失败")
    
    return fixed_files, total_changes

def main():
    """主函数"""
    
    print("🔧 开始修复最终剩余的语言问题...")
    print("=" * 80)
    
    # 修复所有文件
    fixed_files, total_changes = fix_all_files()
    
    print(f"\n" + "=" * 80)
    print("🎉 修复完成！")
    print("=" * 80)
    
    if fixed_files > 0:
        print("✅ 所有最终语言问题都已修复完成！")
        print("🌍 现在网站应该可以正常访问了")
    else:
        print("⚠️  没有语言问题需要修复")

if __name__ == "__main__":
    main() 