#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强制修复所有HTML文件中的注释问题

这个脚本将强制替换所有中文注释为英文注释
"""

import os
import glob
import re

def get_html_files():
    """获取所有HTML文件"""
    return glob.glob('*.html')

def force_fix_comments(content):
    """强制修复所有注释"""
    
    changes_made = []
    
    # 强制替换所有CSS注释中的中文字符
    css_pattern = r'/\*[^*]*[\u4e00-\u9fff][^*]*\*/'
    def replace_css_comment(match):
        comment = match.group(0)
        # 移除所有中文字符
        cleaned = re.sub(r'[\u4e00-\u9fff]', '', comment)
        # 如果注释变得太短，用英文替代
        if len(cleaned.strip()) < 5:
            return '/* CSS comment */'
        return cleaned
    
    if re.search(css_pattern, content):
        content = re.sub(css_pattern, replace_css_comment, content)
        changes_made.append('强制清理CSS注释中的中文字符')
    
    # 强制替换所有JS注释中的中文字符
    js_pattern = r'//[^\n]*[\u4e00-\u9fff][^\n]*'
    def replace_js_comment(match):
        comment = match.group(0)
        # 移除所有中文字符
        cleaned = re.sub(r'[\u4e00-\u9fff]', '', comment)
        # 如果注释变得太短，用英文替代
        if len(cleaned.strip()) < 5:
            return '// JS comment'
        return cleaned
    
    if re.search(js_pattern, content):
        content = re.sub(js_pattern, replace_js_comment, content)
        changes_made.append('强制清理JS注释中的中文字符')
    
    return content, changes_made

def fix_all_files_force():
    """强制修复所有HTML文件"""
    
    html_files = get_html_files()
    
    print("🔧 开始强制修复所有注释问题...")
    print("=" * 80)
    
    total_files = len(html_files)
    fixed_files = 0
    total_changes = 0
    
    for html_file in html_files:
        print(f"\n📄 强制修复文件: {html_file}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 强制修复注释
            content, changes = force_fix_comments(content)
            
            if content != original_content:
                # 写回修复后的内容
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ 成功修复 {len(changes)} 个问题:")
                for change in changes:
                    print(f"    - {change}")
                
                fixed_files += 1
                total_changes += len(changes)
            else:
                print(f"  ✅ 无需修复")
                
        except Exception as e:
            print(f"  ❌ 修复失败: {str(e)}")
    
    print(f"\n" + "=" * 80)
    print("🎯 强制修复完成总结")
    print("=" * 80)
    print(f"📊 修复结果:")
    print(f"   - 总文件数: {total_files}")
    print(f"   - 成功修复: {fixed_files}")
    print(f"   - 失败数量: {total_files - fixed_files}")
    print(f"   - 总修复项: {total_changes}")
    
    if fixed_files > 0:
        print(f"\n✅ 成功强制修复了 {fixed_files} 个文件的注释问题！")
        print(f"🔧 总共修复了 {total_changes} 个问题")
        print(f"🌍 现在所有注释都不包含中文字符")
    else:
        print(f"\n⚠️  没有文件需要修复或修复失败")
    
    return fixed_files, total_changes

def main():
    """主函数"""
    
    print("🔧 开始强制修复所有注释问题...")
    print("=" * 80)
    
    # 强制修复所有文件
    fixed_files, total_changes = fix_all_files_force()
    
    print(f"\n" + "=" * 80)
    print("🎉 强制修复完成！")
    print("=" * 80)
    
    if fixed_files > 0:
        print("✅ 所有注释中的中文字符都已强制清理完成！")
        print("🌍 现在语言检测应该不会误判注释了")
    else:
        print("⚠️  没有注释需要修复")

if __name__ == "__main__":
    main() 