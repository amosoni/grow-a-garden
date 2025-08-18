#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终修复emoji国旗显示问题
"""

import os
import glob
import re

def get_html_files():
    """获取所有HTML文件"""
    return glob.glob('**/*.html', recursive=True)

def fix_emoji_flags(content):
    """修复emoji国旗显示问题"""
    
    changes_made = []
    
    # 修复CSS样式 - 将flag-emoji从图片样式改为文本样式
    if '.flag-emoji' in content and 'width:' in content and 'height:' in content:
        # 替换CSS样式
        old_css = r'\.flag-emoji\s*\{[^}]*width:\s*[^;]*;[^}]*height:\s*[^;]*;[^}]*object-fit:\s*[^;]*;[^}]*border-radius:\s*[^;]*;[^}]*vertical-align:\s*[^;]*;[^}]*\}'
        new_css = '''        .flag-emoji {
            font-size: 1.5rem;
            line-height: 1;
            display: inline-block;
        }'''
        
        if re.search(old_css, content, re.DOTALL):
            content = re.sub(old_css, new_css, content, flags=re.DOTALL)
            changes_made.append('修复flag-emoji CSS样式')
    
    # 修复JavaScript中的错误代码 - 移除src设置
    if "flag-emoji').src =" in content:
        content = content.replace("flag-emoji').src =", "flag-emoji').textContent =")
        changes_made.append('修复JavaScript中的src设置')
    
    # 确保HTML结构正确
    if '<span class="flag-emoji">' not in content:
        # 查找并修复HTML结构
        if 'flag-emoji' in content:
            # 替换img标签为span标签
            content = content.replace('<img src="flags/', '<span class="flag-emoji">')
            content = content.replace('" alt="', '</span><span class="code">')
            content = content.replace('" class="flag-img">', '</span>')
            changes_made.append('修复HTML结构')
    
    return content, changes_made

def fix_all_files():
    """修复所有HTML文件的emoji国旗问题"""
    
    html_files = get_html_files()
    
    print("🔧 开始最终修复emoji国旗显示问题...")
    print("=" * 80)
    
    total_files = len(html_files)
    fixed_files = 0
    total_changes = 0
    
    for html_file in html_files:
        print(f"\n📄 处理文件: {html_file}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_changes = []
            
            # 修复emoji国旗问题
            content, changes = fix_emoji_flags(content)
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
        print(f"\n✅ 成功修复了 {fixed_files} 个文件的emoji国旗问题！")
        print(f"🔧 总共修复了 {total_changes} 个问题")
        print(f"🌍 现在emoji国旗应该可以正确显示了")
    else:
        print(f"\n⚠️  没有emoji国旗问题需要修复")
    
    return fixed_files, total_changes

def main():
    """主函数"""
    
    print("🔧 开始最终修复emoji国旗显示问题...")
    print("=" * 80)
    
    # 修复所有文件
    fixed_files, total_changes = fix_all_files()
    
    print(f"\n" + "=" * 80)
    print("🎉 修复完成！")
    print("=" * 80)
    
    if fixed_files > 0:
        print("✅ 所有emoji国旗问题都已修复完成！")
        print("🌍 现在emoji国旗应该可以正确显示了")
    else:
        print("⚠️  没有emoji国旗问题需要修复")

if __name__ == "__main__":
    main() 