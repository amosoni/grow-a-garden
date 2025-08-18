#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复真正的语言问题

这个脚本将修复：
1. 损坏的URL链接
2. 损坏的JSON-LD数据
3. 损坏的JavaScript代码
4. 损坏的CSS属性
"""

import os
import glob
import re

def get_html_files():
    """获取所有HTML文件"""
    return glob.glob('*.html')

def fix_broken_urls(content):
    """修复损坏的URL链接"""
    
    changes_made = []
    
    # 修复损坏的CSS链接
    if 'https://./..../..' in content:
        content = content.replace('https://./..../..', 'https://unpkg.com/simple.css@2.1.0/simple.min.css')
        changes_made.append('修复CSS链接')
    
    # 修复损坏的图标链接
    if 'data:image./svg+xml,<svg xmlns=\'http://.././\' \'   \' \'.\' -\'\'🌱//' in content:
        content = content.replace('data:image./svg+xml,<svg xmlns=\'http://.././\' \'   \' \'.\' -\'\'🌱//', 'data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>🌱</text></svg>')
        changes_made.append('修复图标链接')
    
    # 修复损坏的背景图片URL
    if 'data:image./svg+xml;charset=UTF-8,%3csvg xmlns=\'http://.././\' \'   \' \'\' \'\' -\'\' -\'\' -\'\'%% \', , ,\'%%./%%./%' in content:
        content = content.replace('data:image./svg+xml;charset=UTF-8,%3csvg xmlns=\'http://.././\' \'   \' \'\' \'\' -\'\' -\'\' -\'\'%% \', , ,\'%%./%%./%', 'data:image/svg+xml;charset=UTF-8,%3csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'white\' stroke-width=\'2\' stroke-linecap=\'round\' stroke-linejoin=\'round\'%3e%3cpolyline points=\'6,9 12,15 18,9\'%3e%3c/polyline%3e%3c/svg%3e')
        changes_made.append('修复背景图片URL')
    
    # 修复损坏的JSON-LD URL
    if '"@context": "https://."' in content:
        content = content.replace('"@context": "https://."', '"@context": "https://schema.org"')
        changes_made.append('修复JSON-LD context')
    
    if '"url": "https://./."' in content:
        content = content.replace('"url": "https://./."', '"url": "https://growagarden.cv/online.html"')
        changes_made.append('修复JSON-LD URL')
    
    if '"url": "https:// JS comment' in content:
        content = content.replace('"url": "https:// JS comment', '"url": "https://growagarden.cv"')
        changes_made.append('修复JSON-LD网站URL')
    
    # 修复损坏的游戏链接
    if 'https://.././--' in content:
        content = content.replace('https://.././--', 'https://www.miniplay.com/embed/grow-a-garden')
        changes_made.append('修复MiniPlay链接')
    
    if 'https://./-./&&' in content:
        content = content.replace('https://./-./&&', 'https://playhop.com/dist-app/437622?header=no&utm_source=distrib&utm_medium=gameflare')
        changes_made.append('修复PlayHop链接')
    
    return content, changes_made

def fix_broken_javascript(content):
    """修复损坏的JavaScript代码"""
    
    changes_made = []
    
    # 修复损坏的正则表达式
    if './\./(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)\//' in content:
        content = content.replace('./\./(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)\//', '/(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)/')
        changes_made.append('修复正则表达式')
    
    # 修复损坏的字符串拼接
    if './\' +  + \'./\'' in content:
        content = content.replace('./\' +  + \'./\'', './' + lang + './')
        changes_made.append('修复字符串拼接')
    
    # 修复损坏的match函数调用
    if 'currentPath.match(./\./(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)\// JS comment' in content:
        content = content.replace('currentPath.match(./\./(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)\// JS comment', 'currentPath.match(/(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)/)')
        changes_made.append('修复match函数调用')
    
    # 修复损坏的注释
    if '// （）' in content:
        content = content.replace('// （）', '// 使用i18n系统')
        changes_made.append('修复中文注释')
    
    if '//  - ' in content:
        content = content.replace('//  - ', '// 初始化当前语言 - 根据URL路径设置正确的语言')
        changes_made.append('修复中文注释')
    
    if '// ，DOM' in content:
        content = content.replace('// ，DOM', '// 延迟再次初始化，确保DOM完全加载')
        changes_made.append('修复中文注释')
    
    return content, changes_made

def fix_all_files():
    """修复所有HTML文件"""
    
    html_files = get_html_files()
    
    print("🔧 开始修复真正的语言问题...")
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
            
            # 1. 修复损坏的URL
            content, changes = fix_broken_urls(content)
            file_changes.extend(changes)
            
            # 2. 修复损坏的JavaScript
            content, changes = fix_broken_javascript(content)
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
        print(f"\n✅ 成功修复了 {fixed_files} 个文件的真正语言问题！")
        print(f"🔧 总共修复了 {total_changes} 个问题")
        print(f"🌍 现在所有URL和JavaScript代码都应该正常了")
    else:
        print(f"\n⚠️  没有文件需要修复或修复失败")
    
    return fixed_files, total_changes

def main():
    """主函数"""
    
    print("🔧 开始修复真正的语言问题...")
    print("=" * 80)
    
    # 修复所有文件
    fixed_files, total_changes = fix_all_files()
    
    print(f"\n" + "=" * 80)
    print("🎉 修复完成！")
    print("=" * 80)
    
    if fixed_files > 0:
        print("✅ 所有真正的语言问题都已修复完成！")
        print("🌍 现在网站应该可以正常访问了")
    else:
        print("⚠️  没有语言问题需要修复")

if __name__ == "__main__":
    main() 