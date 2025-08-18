#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终修复所有语言匹配问题

这个脚本将：
1. 修复所有CSS注释中的中文字符
2. 修复所有JS注释中的中文字符
3. 确保页面语言一致性
"""

import os
import glob
import re

def get_html_files():
    """获取所有HTML文件"""
    return glob.glob('*.html')

def fix_css_comments_final(content):
    """最终修复CSS注释中的中文字符"""
    
    # 定义所有需要替换的CSS注释
    css_comment_replacements = {
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
    
    changes_made = []
    
    for old_comment, new_comment in css_comment_replacements.items():
        if old_comment in content:
            content = content.replace(old_comment, new_comment)
            changes_made.append(f'替换CSS注释: {old_comment} -> {new_comment}')
    
    return content, changes_made

def fix_js_comments_final(content):
    """最终修复JS注释中的中文字符"""
    
    # 定义所有需要替换的JS注释
    js_comment_replacements = {
        '// 语言选择器功能': '// Language switcher functionality',
        '// 为每个语言选项添加点击事件': '// Add click events for each language option',
        '// 跳转到对应语言页面': '// Navigate to corresponding language page',
        '// 点击按钮显示/隐藏下拉菜单': '// Toggle dropdown menu on button click',
        '// 点击其他地方隐藏下拉菜单': '// Hide dropdown when clicking elsewhere',
        '// 设置当前语言': '// Set current language',
        '// 页面加载完成后自动应用国际化': '// Apply internationalization after page load',
        '// 如果国际化系统已准备就绪，直接应用翻译': '// If i18n system is ready, apply translations directly',
        '// 验证关键元素': '// Validate key elements',
        '// 复制国旗图片到当前按钮': '// Copy flag image to current button',
        '// 复制国旗图片的src和代码': '// Copy flag image src and code',
        '// 验证更新是否成功': '// Verify update success',
        '// 切换语言（使用现有的i18n系统）': '// Switch language (using existing i18n system)',
        '// 显示切换提示': '// Show switch notification',
        '// 调用i18n系统的语言切换': '// Call i18n system language switch',
        '// 强制跳转到对应语言页面': '// Force redirect to corresponding language page',
        '// 检查当前路径格式': '// Check current path format',
        '// 如果当前路径包含语言代码，替换它': '// If current path contains language code, replace it',
        '// 如果当前路径不包含语言代码，添加它': '// If current path doesn\'t contain language code, add it',
        '// 隐藏下拉菜单': '// Hide dropdown menu',
        '// 点击按钮显示/隐藏下拉菜单': '// Toggle dropdown menu on button click',
        '// 初始化当前语言 - 根据URL路径设置正确的语言': '// Initialize current language - set correct language based on URL path',
        '// 从URL路径提取语言代码': '// Extract language code from URL path',
        '// 更新按钮显示': '// Update button display',
        '// 根据当前语言设置正确的国旗和代码': '// Set correct flag and code based on current language',
        '// 显示语言切换成功提示': '// Show language switch success notification',
        '// 创建提示元素': '// Create notification element',
        '// 3秒后自动消失': '// Auto-disappear after 3 seconds',
        '// 添加CSS动画': '// Add CSS animations',
        '// 立即初始化一次': '// Initialize immediately once',
        '// 延迟再次初始化，确保DOM完全加载': '// Delay re-initialization to ensure DOM is fully loaded'
    }
    
    changes_made = []
    
    for old_comment, new_comment in js_comment_replacements.items():
        if old_comment in content:
            content = content.replace(old_comment, new_comment)
            changes_made.append(f'替换JS注释: {old_comment} -> {new_comment}')
    
    return content, changes_made

def fix_all_files_final():
    """最终修复所有HTML文件中的注释问题"""
    
    html_files = get_html_files()
    
    print("🔧 开始最终修复所有语言匹配问题...")
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
            
            # 1. 修复CSS注释
            content, changes = fix_css_comments_final(content)
            file_changes.extend(changes)
            
            # 2. 修复JS注释
            content, changes = fix_js_comments_final(content)
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
    print("🎯 最终修复完成总结")
    print("=" * 80)
    print(f"📊 修复结果:")
    print(f"   - 总文件数: {total_files}")
    print(f"   - 成功修复: {fixed_files}")
    print(f"   - 失败数量: {total_files - fixed_files}")
    print(f"   - 总修复项: {total_changes}")
    
    if fixed_files > 0:
        print(f"\n✅ 成功修复了 {fixed_files} 个文件的注释问题！")
        print(f"🔧 总共修复了 {total_changes} 个问题")
        print(f"🌍 现在所有注释都使用英文，语言检测应该正常了")
    else:
        print(f"\n⚠️  没有文件需要修复或修复失败")
    
    return fixed_files, total_changes

def main():
    """主函数"""
    
    print("🔧 开始最终修复所有语言匹配问题...")
    print("=" * 80)
    
    # 修复所有文件
    fixed_files, total_changes = fix_all_files_final()
    
    print(f"\n" + "=" * 80)
    print("🎉 最终修复完成！")
    print("=" * 80)
    
    if fixed_files > 0:
        print("✅ 所有注释中的中文字符都已修复完成！")
        print("🌍 现在语言检测应该不会误判CSS和JS注释了")
    else:
        print("⚠️  没有注释需要修复")

if __name__ == "__main__":
    main() 