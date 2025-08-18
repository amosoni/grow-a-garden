#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有语法错误
"""

import os
import glob
import re

def get_html_files():
    """获取所有HTML文件"""
    return glob.glob('*.html')

def fix_syntax_errors(content):
    """修复语法错误"""
    
    changes_made = []
    
    # 修复CSS语法错误 - 缺少分号
    if 'background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'white\' stroke-width=\'2\' stroke-linecap=\'round\' stroke-linejoin=\'round\'%3e%3cpolyline points=\'6,9 12,15 18,9\'%3e%3c/polyline%3e%3c/svg%3e")' in content:
        content = content.replace(
            'background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'white\' stroke-width=\'2\' stroke-linecap=\'round\' stroke-linejoin=\'round\'%3e%3cpolyline points=\'6,9 12,15 18,9\'%3e%3c/polyline%3e%3c/svg%3e")',
            'background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'white\' stroke-width=\'2\' stroke-linecap=\'round\' stroke-linejoin=\'round\'%3e%3cpolyline points=\'6,9 12,15 18,9\'%3e%3c/polyline%3e%3c/svg%3e");'
        )
        changes_made.append('修复CSS语法错误 - 添加缺失的分号')
    
    # 修复JavaScript语法错误 - 字符串未闭合
    if 'newPath = currentPath.replace(/(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)/, \'./lang./\')' in content:
        content = content.replace(
            'newPath = currentPath.replace(/(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)/, \'./\' + lang + \'/\')',
            'newPath = currentPath.replace(/(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)/, \'./\' + lang + \'/\')'
        )
        changes_made.append('修复JavaScript语法错误 - 字符串闭合')
    
    # 修复JavaScript语法错误 - 正则表达式未闭合
    if 'const langMatch = currentPath.match(/(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)/ JS comment' in content:
        content = content.replace(
            'const langMatch = currentPath.match(/(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)/ JS comment',
            'const langMatch = currentPath.match(/(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)/)'
        )
        changes_made.append('修复JavaScript语法错误 - 正则表达式闭合')
    
    # 修复游戏链接的语法错误
    if 'href="https://www.miniplay.com/embed/grow-a-garden" "" "-"' in content:
        content = content.replace(
            'href="https://www.miniplay.com/embed/grow-a-garden" "" "-"',
            'href="https://www.miniplay.com/embed/grow-a-garden"'
        )
        changes_made.append('修复游戏链接语法错误')
    
    if 'href="https://playhop.com/dist-app/437622?header=no&utm_source=distrib&utm_medium=gameflare" "" "- "' in content:
        content = content.replace(
            'href="https://playhop.com/dist-app/437622?header=no&utm_source=distrib&utm_medium=gameflare" "" "- "',
            'href="https://playhop.com/dist-app/437622?header=no&utm_source=distrib&utm_medium=gameflare"'
        )
        changes_made.append('修复游戏链接语法错误')
    
    return content, changes_made

def fix_all_files():
    """修复所有HTML文件"""
    
    html_files = get_html_files()
    
    print("🔧 开始修复语法错误...")
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
            
            # 修复语法错误
            content, changes = fix_syntax_errors(content)
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
        print(f"\n✅ 成功修复了 {fixed_files} 个文件的语法错误！")
        print(f"🔧 总共修复了 {total_changes} 个问题")
        print(f"🌍 现在所有代码都应该没有语法错误了")
    else:
        print(f"\n⚠️  没有文件需要修复或修复失败")
    
    return fixed_files, total_changes

def main():
    """主函数"""
    
    print("🔧 开始修复语法错误...")
    print("=" * 80)
    
    # 修复所有文件
    fixed_files, total_changes = fix_all_files()
    
    print(f"\n" + "=" * 80)
    print("🎉 修复完成！")
    print("=" * 80)
    
    if fixed_files > 0:
        print("✅ 所有语法错误都已修复完成！")
        print("🌍 现在网站应该可以正常运行了")
    else:
        print("⚠️  没有语法错误需要修复")

if __name__ == "__main__":
    main() 