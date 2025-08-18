#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复CSS代码位置错误
"""

import os
import glob
import re

def get_html_files():
    """获取所有HTML文件"""
    return glob.glob('**/*.html', recursive=True)

def fix_css_misplaced(content):
    """修复CSS代码位置错误"""
    
    changes_made = []
    
    # 检查是否有CSS代码被放在了</script>标签之后
    if '</script>' in content and '<style>' in content:
        # 找到</script>标签的位置
        script_end = content.find('</script>')
        style_start = content.find('<style>')
        
        # 如果<style>在</script>之后，说明CSS位置错误
        if style_start > script_end:
            changes_made.append('CSS位置错误，需要移动到head标签内')
            
            # 找到</style>标签
            style_end = content.find('</style>')
            if style_end != -1:
                # 提取CSS代码
                css_code = content[style_start:style_end + 8]
                
                # 从原位置删除CSS代码
                content = content[:style_start] + content[style_end + 8:]
                
                # 找到</head>标签
                head_end = content.find('</head>')
                if head_end != -1:
                    # 在</head>之前插入CSS代码
                    content = content[:head_end] + '\n    ' + css_code + '\n' + content[head_end:]
                    changes_made.append('CSS代码已移动到head标签内')
                else:
                    changes_made.append('未找到</head>标签，无法移动CSS代码')
    
    return content, changes_made

def fix_all_files():
    """修复所有HTML文件的CSS位置错误"""
    
    html_files = get_html_files()
    
    print("🔧 开始修复CSS位置错误...")
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
            
            # 修复CSS位置错误
            content, changes = fix_css_misplaced(content)
            file_changes.extend(changes)
            
            if content != original_content:
                # 写回修复后的内容
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ 成功修复 {len(file_changes)} 个CSS位置问题:")
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
        print(f"\n✅ 成功修复了 {fixed_files} 个文件的CSS位置问题！")
        print(f"🔧 总共修复了 {total_changes} 个问题")
        print(f"🎨 您的样式完全保持不变，只是移动了位置")
    else:
        print(f"\n⚠️  没有CSS位置问题需要修复")
    
    return fixed_files, total_changes

def main():
    """主函数"""
    
    print("🔧 开始修复CSS位置错误...")
    print("=" * 80)
    
    # 修复所有文件
    fixed_files, total_changes = fix_all_files()
    
    print(f"\n" + "=" * 80)
    print("🎉 修复完成！")
    print("=" * 80)
    
    if fixed_files > 0:
        print("✅ 所有CSS位置问题都已修复完成！")
        print("🎨 您的样式完全保持不变")
    else:
        print("⚠️  没有CSS位置问题需要修复")

if __name__ == "__main__":
    main() 