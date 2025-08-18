#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理CSS注释中的中文字符

这个脚本将清理HTML文件中CSS注释里的中文字符，避免语言检测误判
"""

import os
import glob
import re

def get_html_files():
    """获取所有HTML文件"""
    return glob.glob('*.html')

def clean_css_comments(content):
    """清理CSS注释中的中文字符"""
    
    changes_made = []
    
    # 查找CSS注释中的中文字符
    css_comment_pattern = r'/\*[^*]*[\u4e00-\u9fff][^*]*\*/'
    css_comments = re.findall(css_comment_pattern, content)
    
    if css_comments:
        # 替换中文注释为英文注释
        comment_replacements = {
            '/* 导航栏中间区域 */': '/* Navigation middle area */',
            '/* 导航链接样式优化 */': '/* Navigation link style optimization */',
            '/* 特殊按钮样式 */': '/* Special button styles */',
            '/* 语言切换器样式 */': '/* Language switcher styles */',
            '/* 确保emoji正确显示 */': '/* Ensure emoji displays correctly */',
            '/* 语言切换器样式优化 */': '/* Language switcher style optimization */',
            '/* 自定义语言选择器样式 */': '/* Custom language selector styles */',
            '/* 移动端导航栏垂直排列 */': '/* Mobile navigation vertical layout */',
            '/* 内联样式已移除，使用styles.css中的统一样式 */': '/* Inline styles removed, using unified styles from styles.css */'
        }
        
        for old_comment, new_comment in comment_replacements.items():
            if old_comment in content:
                content = content.replace(old_comment, new_comment)
                changes_made.append(f'替换CSS注释: {old_comment} -> {new_comment}')
        
        # 对于没有预定义替换的注释，直接移除中文字符
        def replace_chinese_in_comment(match):
            comment = match.group(0)
            # 移除中文字符，保留其他内容
            cleaned_comment = re.sub(r'[\u4e00-\u9fff]', '', comment)
            # 如果注释变得太短，用英文替代
            if len(cleaned_comment.strip()) < 5:
                return '/* CSS comment */'
            return cleaned_comment
        
        content = re.sub(css_comment_pattern, replace_chinese_in_comment, content)
        changes_made.append('清理其他CSS注释中的中文字符')
    
    return content, changes_made

def clean_js_comments(content):
    """清理JavaScript注释中的中文字符"""
    
    changes_made = []
    
    # 查找JavaScript注释中的中文字符
    js_comment_pattern = r'//[^\n]*[\u4e00-\u9fff][^\n]*'
    js_comments = re.findall(js_comment_pattern, content)
    
    if js_comments:
        # 替换中文注释为英文注释
        comment_replacements = {
            '// 语言选择器功能': '// Language switcher functionality',
            '// 为每个语言选项添加点击事件': '// Add click events for each language option',
            '// 跳转到对应语言页面': '// Navigate to corresponding language page',
            '// 点击按钮显示/隐藏下拉菜单': '// Toggle dropdown menu on button click',
            '// 点击其他地方隐藏下拉菜单': '// Hide dropdown when clicking elsewhere',
            '// 设置当前语言': '// Set current language',
            '// 页面加载完成后自动应用国际化': '// Apply internationalization after page load',
            '// 如果国际化系统已准备就绪，直接应用翻译': '// If i18n system is ready, apply translations directly'
        }
        
        for old_comment, new_comment in comment_replacements.items():
            if old_comment in content:
                content = content.replace(old_comment, new_comment)
                changes_made.append(f'替换JS注释: {old_comment} -> {new_comment}')
        
        # 对于没有预定义替换的注释，直接移除中文字符
        def replace_chinese_in_js_comment(match):
            comment = match.group(0)
            # 移除中文字符，保留其他内容
            cleaned_comment = re.sub(r'[\u4e00-\u9fff]', '', comment)
            # 如果注释变得太短，用英文替代
            if len(cleaned_comment.strip()) < 5:
                return '// JS comment'
            return cleaned_comment
        
        content = re.sub(js_comment_pattern, replace_chinese_in_js_comment, content)
        changes_made.append('清理其他JS注释中的中文字符')
    
    return content, changes_made

def clean_all_files():
    """清理所有HTML文件中的CSS和JS注释"""
    
    html_files = get_html_files()
    
    print("🧹 开始清理CSS和JS注释中的中文字符...")
    print("=" * 80)
    
    total_files = len(html_files)
    cleaned_files = 0
    total_changes = 0
    
    for html_file in html_files:
        print(f"\n📄 清理文件: {html_file}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_changes = []
            
            # 1. 清理CSS注释
            content, changes = clean_css_comments(content)
            file_changes.extend(changes)
            
            # 2. 清理JS注释
            content, changes = clean_js_comments(content)
            file_changes.extend(changes)
            
            if content != original_content:
                # 写回清理后的内容
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ 成功清理 {len(file_changes)} 个问题:")
                for change in file_changes:
                    print(f"    - {change}")
                
                cleaned_files += 1
                total_changes += len(file_changes)
            else:
                print(f"  ✅ 无需清理")
                
        except Exception as e:
            print(f"  ❌ 清理失败: {str(e)}")
    
    print(f"\n" + "=" * 80)
    print("🎯 注释清理完成总结")
    print("=" * 80)
    print(f"📊 清理结果:")
    print(f"   - 总文件数: {total_files}")
    print(f"   - 成功清理: {cleaned_files}")
    print(f"   - 失败数量: {total_files - cleaned_files}")
    print(f"   - 总清理项: {total_changes}")
    
    if cleaned_files > 0:
        print(f"\n✅ 成功清理了 {cleaned_files} 个文件的注释问题！")
        print(f"🧹 总共清理了 {total_changes} 个问题")
        print(f"🌍 现在所有注释都使用英文，避免语言检测误判")
    else:
        print(f"\n⚠️  没有文件需要清理或清理失败")
    
    return cleaned_files, total_changes

def main():
    """主函数"""
    
    print("🧹 开始清理CSS和JS注释中的中文字符...")
    print("=" * 80)
    
    # 清理所有文件
    cleaned_files, total_changes = clean_all_files()
    
    print(f"\n" + "=" * 80)
    print("🎉 注释清理完成！")
    print("=" * 80)
    
    if cleaned_files > 0:
        print("✅ 所有注释中的中文字符都已清理完成！")
        print("🌍 现在语言检测应该不会误判CSS和JS注释了")
    else:
        print("⚠️  没有注释需要清理")

if __name__ == "__main__":
    main() 