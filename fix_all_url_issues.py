#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有URL问题
"""

import os
import glob
import re

def get_html_files():
    """获取所有HTML文件"""
    return glob.glob('**/*.html', recursive=True)

def fix_all_url_issues(content):
    """修复所有URL问题"""
    
    changes_made = []
    
    # 修复错误的语言路径
    if './en./' in content:
        content = content.replace('./en./', './en/')
        changes_made.append('修复en路径')
    
    if './zh-cn./' in content:
        content = content.replace('./zh-cn./', './zh-cn/')
        changes_made.append('修复zh-cn路径')
    
    if './es./' in content:
        content = content.replace('./es./', './es/')
        changes_made.append('修复es路径')
    
    if './pt-br./' in content:
        content = content.replace('./pt-br./', './pt-br/')
        changes_made.append('修复pt-br路径')
    
    if './fr./' in content:
        content = content.replace('./fr./', './fr/')
        changes_made.append('修复fr路径')
    
    if './de./' in content:
        content = content.replace('./de./', './de/')
        changes_made.append('修复de路径')
    
    if './ru./' in content:
        content = content.replace('./ru./', './ru/')
        changes_made.append('修复ru路径')
    
    if './ar./' in content:
        content = content.replace('./ar./', './ar/')
        changes_made.append('修复ar路径')
    
    if './hi./' in content:
        content = content.replace('./hi./', './hi/')
        changes_made.append('修复hi路径')
    
    if './id./' in content:
        content = content.replace('./id./', './id/')
        changes_made.append('修复id路径')
    
    if './vi./' in content:
        content = content.replace('./vi./', './vi/')
        changes_made.append('修复vi路径')
    
    if './ja./' in content:
        content = content.replace('./ja./', './ja/')
        changes_made.append('修复ja路径')
    
    # 修复错误的script src
    if 'https://.././-' in content:
        content = content.replace('https://.././-', 'https://www.googletagmanager.com/gtag/js')
        changes_made.append('修复Google Analytics脚本路径')
    
    if 'https://..././.' in content:
        content = content.replace('https://..././.', 'https://www.googletagmanager.com/gtag/js')
        changes_made.append('修复Google Analytics脚本路径')
    
    # 修复错误的link标签
    if 'href="./styles.css" ./>' in content:
        content = content.replace('href="./styles.css" ./>', 'href="./styles.css">')
        changes_made.append('修复CSS链接路径')
    
    return content, changes_made

def fix_all_files():
    """修复所有HTML文件的URL问题"""
    
    html_files = get_html_files()
    
    print("🔧 开始修复所有URL问题...")
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
            
            # 修复所有URL问题
            content, changes = fix_all_url_issues(content)
            file_changes.extend(changes)
            
            if content != original_content:
                # 写回修复后的内容
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ 成功修复 {len(file_changes)} 个URL问题:")
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
        print(f"\n✅ 成功修复了 {fixed_files} 个文件的URL问题！")
        print(f"🔧 总共修复了 {total_changes} 个问题")
        print(f"🌍 现在页面应该可以正常访问了")
    else:
        print(f"\n⚠️  没有URL问题需要修复")
    
    return fixed_files, total_changes

def main():
    """主函数"""
    
    print("🔧 开始修复所有URL问题...")
    print("=" * 80)
    
    # 修复所有文件
    fixed_files, total_changes = fix_all_files()
    
    print(f"\n" + "=" * 80)
    print("🎉 修复完成！")
    print("=" * 80)
    
    if fixed_files > 0:
        print("✅ 所有URL问题都已修复完成！")
        print("🌍 现在页面应该可以正常访问了")
    else:
        print("⚠️  没有URL问题需要修复")

if __name__ == "__main__":
    main() 