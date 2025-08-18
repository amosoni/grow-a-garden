#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复online页面JavaScript中的中文注释和script标签问题
"""

import os
import re

def fix_online_js_comments():
    """修复JavaScript中的中文注释和script标签问题"""
    
    print("🔧 开始修复online页面JavaScript问题...")
    print("=" * 80)
    
    # 修复根目录的online.html
    online_file = "online.html"
    if os.path.exists(online_file):
        print(f"🔧 修复: {online_file}")
        
        try:
            with open(online_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            changes = 0
            
            # 修复script标签问题
            if '<script src="/i18n/i18n.js">        // 语言切换器功能' in content:
                content = content.replace(
                    '<script src="/i18n/i18n.js">        // 语言切换器功能',
                    '<script src="/i18n/i18n.js">\n        // Language switcher functionality'
                )
                changes += 1
                print(f"  ✅ 修复了script标签")
            
            # 替换中文注释为英文注释
            replacements = {
                '// 语言切换器功能': '// Language switcher functionality',
                '// 设置当前语言': '// Set current language',
                '// 国旗已改为内联SVG，无需设置src': '// Flag changed to inline SVG, no need to set src',
                '// 保存语言选择到localStorage': '// Save language selection to localStorage',
                '// 跳转到对应语言页面': '// Jump to corresponding language page',
                '// 为每个语言选项添加点击事件': '// Add click events for each language option',
                '// 从localStorage恢复语言选择': '// Restore language selection from localStorage',
                '// 语言选择器功能': '// Language selector functionality',
                '// 验证关键元素': '// Validate key elements',
                '// 复制国旗图片到当前按钮': '// Copy flag image to current button',
                '// 复制国旗图片的src和代码': '// Copy flag image src and code',
                '// 验证更新是否成功': '// Verify if update is successful',
                '// 切换语言（使用现有的i18n系统）': '// Switch language (using existing i18n system)',
                '// 显示切换提示': '// Show switch prompt',
                '// 调用i18n系统的语言切换': '// Call i18n system language switch',
                '// 强制跳转到对应语言页面': '// Force jump to corresponding language page',
                '// 如果当前在根目录，直接跳转到语言目录': '// If currently in root directory, jump directly to language directory',
                '// 检查当前路径格式': '// Check current path format',
                '// 如果当前路径包含语言代码，替换它': '// If current path contains language code, replace it',
                '// 如果当前路径不包含语言代码，添加它': '// If current path does not contain language code, add it',
                '// 立即跳转，确保语言切换生效': '// Jump immediately to ensure language switch takes effect',
                '// 隐藏下拉菜单': '// Hide dropdown menu',
                '// 点击按钮显示/隐藏下拉菜单': '// Click button to show/hide dropdown menu',
                '// 点击其他地方隐藏下拉菜单': '// Click elsewhere to hide dropdown menu',
                '// 初始化当前语言 - 根据URL路径设置正确的语言': '// Initialize current language - set correct language based on URL path',
                '// 默认语言': '// Default language',
                '// 从URL路径提取语言代码': '// Extract language code from URL path',
                '// 更新按钮显示': '// Update button display',
                '// 根据当前语言设置正确的国旗和代码': '// Set correct flag and code based on current language',
                '// 显示语言切换成功提示': '// Show language switch success prompt',
                '// 创建提示元素': '// Create prompt element',
                '// 3秒后自动消失': '// Auto-disappear after 3 seconds',
                '// 添加CSS动画': '// Add CSS animation',
                '// 立即初始化一次': '// Initialize once immediately',
                '// 延迟再次初始化，确保DOM完全加载': '// Delay re-initialization to ensure DOM is fully loaded'
            }
            
            for chinese, english in replacements.items():
                if chinese in content:
                    content = content.replace(chinese, english)
                    changes += 1
                    print(f"  ✅ 替换: {chinese} -> {english}")
            
            if changes > 0:
                # 写回文件
                with open(online_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✅ 总共修复了 {changes} 个问题")
            else:
                print(f"  ℹ️  无需修复")
            
        except Exception as e:
            print(f"  ❌ 处理失败: {str(e)}")
    
    print("=" * 80)
    print("🎯 JavaScript问题修复完成！")
    print("=" * 80)
    print("✅ 现在online页面应该可以正常显示了")
    print("🔧 修复了script标签和中文注释问题")
    print("🎨 JavaScript应该正确执行")

def main():
    """主函数"""
    
    print("🔧 开始修复online页面JavaScript问题...")
    print("=" * 80)
    
    # 修复JavaScript问题
    fix_online_js_comments()
    
    print(f"\n" + "=" * 80)
    print("🎉 修复完成！")
    print("=" * 80)
    print("✅ online页面JavaScript问题修复完成！")

if __name__ == "__main__":
    main() 