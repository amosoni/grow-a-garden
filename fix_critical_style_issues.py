#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复关键的样式问题
"""

import os
import re

def fix_css_paths(content):
    """修复CSS文件路径"""
    
    changes = 0
    
    # 修复unpkg.com链接
    old_pattern = 'href="unpkg.com/simple.css@2.1.0/simple.min.css"'
    new_pattern = 'href="https://unpkg.com/simple.css@2.1.0/simple.min.css"'
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        changes += 1
    
    # 修复leaflet CSS链接
    old_pattern = 'href="unpkg.com/leaflet@1.9.4/dist/leaflet.css"'
    new_pattern = 'href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"'
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        changes += 1
    
    # 修复绝对路径的styles.css
    old_pattern = 'href="/styles.css"'
    new_pattern = 'href="../styles.css"'
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        changes += 1
    
    # 修复相对路径的styles.css (在子目录中)
    old_pattern = 'href="styles.css"'
    new_pattern = 'href="../styles.css"'
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        changes += 1
    
    return content, changes

def fix_javascript_flags(content):
    """修复JavaScript中的国旗引用"""
    
    changes = 0
    
    # 修复JavaScript中的图片国旗引用
    old_pattern = "currentLangBtn.querySelector('.flag-img').src = `flags/${lang}.png`;"
    new_pattern = "// 国旗已改为内联SVG，无需设置src"
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        changes += 1
    
    # 修复其他可能的图片国旗引用
    old_patterns = [
        "currentLangBtn.querySelector('.flag-img').src = `flags/",
        "currentLangBtn.querySelector('.flag-img').src = 'flags/",
        "currentLangBtn.querySelector('.flag-img').src = \"flags/"
    ]
    
    for old_pattern in old_patterns:
        if old_pattern in content:
            # 找到包含这个引用的完整行并注释掉
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if old_pattern in line:
                    lines[i] = f"// {line} // 已修复：国旗改为内联SVG"
                    changes += 1
            content = '\n'.join(lines)
    
    return content, changes

def fix_page_styles(file_path):
    """修复单个页面的样式问题"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        total_changes = 0
        
        # 修复CSS路径
        content, css_changes = fix_css_paths(content)
        total_changes += css_changes
        
        # 修复JavaScript国旗引用
        content, js_changes = fix_javascript_flags(content)
        total_changes += js_changes
        
        if total_changes > 0:
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return total_changes
        
    except Exception as e:
        print(f"  ❌ 处理失败: {str(e)}")
        return 0

def fix_all_pages():
    """修复所有页面的样式问题"""
    
    print("🔧 开始修复关键的样式问题...")
    print("=" * 80)
    
    # 获取所有HTML文件
    html_files = []
    for root, dirs, files in os.walk('.'):
        # 跳过node_modules和其他不需要的目录
        if 'node_modules' in root or '.git' in root or '.next' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"📁 找到 {len(html_files)} 个HTML文件")
    print("=" * 80)
    
    total_changes = 0
    files_fixed = 0
    
    for file_path in html_files:
        print(f"🔧 修复: {file_path}")
        
        changes = fix_page_styles(file_path)
        
        if changes > 0:
            print(f"  ✅ 修复了 {changes} 个问题")
            total_changes += changes
            files_fixed += 1
        else:
            print(f"  ℹ️  无需修复")
        
        print()
    
    print("=" * 80)
    print("🎯 修复完成总结")
    print("=" * 80)
    print(f"📊 修复结果:")
    print(f"   - 处理文件: {len(html_files)}")
    print(f"   - 修复文件: {files_fixed}")
    print(f"   - 总修复数: {total_changes}")
    
    if total_changes > 0:
        print(f"\n✅ 成功修复了 {total_changes} 个样式问题！")
        print(f"🌍 现在页面应该可以正常显示了")
    else:
        print(f"\n⚠️  没有样式问题需要修复")
    
    return total_changes

def main():
    """主函数"""
    
    print("🔧 开始修复关键的样式问题...")
    print("=" * 80)
    
    # 修复所有页面
    total_changes = fix_all_pages()
    
    print(f"\n" + "=" * 80)
    print("🎉 修复完成！")
    print("=" * 80)
    
    if total_changes > 0:
        print("✅ 样式问题修复完成！")
        print("🌍 现在页面应该可以正常显示了")
    else:
        print("⚠️  没有样式问题需要修复")

if __name__ == "__main__":
    main() 