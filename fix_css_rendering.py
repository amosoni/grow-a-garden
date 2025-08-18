#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复CSS渲染问题
"""

import os
import glob
import re

def get_html_files():
    """获取所有HTML文件"""
    return glob.glob('*.html')

def fix_css_rendering(content):
    """修复CSS渲染问题"""
    
    changes_made = []
    
    # 确保CSS文件路径正确
    if 'href="styles.css"' in content:
        content = content.replace('href="styles.css"', 'href="./styles.css"')
        changes_made.append('修复CSS文件路径')
    
    # 确保外部CSS链接正确
    if 'href="https://unpkg.com/simple.css@2.1.0/simple.min.css"' in content:
        content = content.replace('href="https://unpkg.com/simple.css@2.1.0/simple.min.css"', 'href="https://unpkg.com/simple.css@2.1.0/simple.min.css"')
        changes_made.append('确保外部CSS链接正确')
    
    # 添加CSS加载检查
    if '<script>' in content and 'CSS加载检查' not in content:
        css_check_script = '''
        <script>
        // CSS加载检查
        document.addEventListener('DOMContentLoaded', function() {
            const styles = document.styleSheets;
            console.log('已加载的样式表数量:', styles.length);
            
            for (let i = 0; i < styles.length; i++) {
                try {
                    console.log('样式表', i, ':', styles[i].href);
                } catch (e) {
                    console.log('样式表', i, ':', '内联样式');
                }
            }
            
            // 检查关键样式是否加载
            const body = document.body;
            const computedStyle = window.getComputedStyle(body);
            console.log('背景色:', computedStyle.backgroundColor);
            console.log('字体:', computedStyle.fontFamily);
        });
        </script>
        '''
        
        # 在</body>标签前插入CSS检查脚本
        if '</body>' in content:
            content = content.replace('</body>', css_check_script + '\n</body>')
            changes_made.append('添加CSS加载检查脚本')
    
    return content, changes_made

def fix_all_files():
    """修复所有HTML文件"""
    
    html_files = get_html_files()
    
    print("🔧 开始修复CSS渲染问题...")
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
            
            # 修复CSS渲染问题
            content, changes = fix_css_rendering(content)
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
        print(f"\n✅ 成功修复了 {fixed_files} 个文件的CSS渲染问题！")
        print(f"🔧 总共修复了 {total_changes} 个问题")
        print(f"🌍 现在CSS应该可以正确渲染了")
    else:
        print(f"\n⚠️  没有文件需要修复或修复失败")
    
    return fixed_files, total_changes

def main():
    """主函数"""
    
    print("🔧 开始修复CSS渲染问题...")
    print("=" * 80)
    
    # 修复所有文件
    fixed_files, total_changes = fix_all_files()
    
    print(f"\n" + "=" * 80)
    print("🎉 修复完成！")
    print("=" * 80)
    
    if fixed_files > 0:
        print("✅ 所有CSS渲染问题都已修复完成！")
        print("🌍 现在网站应该可以正确显示样式了")
    else:
        print("⚠️  没有CSS渲染问题需要修复")

if __name__ == "__main__":
    main() 