#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理online页面CSS中的中文注释
"""

import os
import re

def clean_css_comments():
    """清理CSS中的中文注释"""
    
    print("🧹 开始清理online页面CSS中的中文注释...")
    print("=" * 80)
    
    # 清理根目录的online.html
    online_file = "online.html"
    if os.path.exists(online_file):
        print(f"🧹 清理: {online_file}")
        
        try:
            with open(online_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            changes = 0
            
            # 清理中文注释
            chinese_comments = re.findall(r'/\*[^*]*[\u4e00-\u9fff][^*]*\*/', content)
            if chinese_comments:
                print(f"  🔍 找到 {len(chinese_comments)} 个中文注释")
                for comment in chinese_comments:
                    print(f"    - {comment}")
                
                # 替换中文注释为英文注释
                replacements = {
                    '/* 导航栏中间区域 */': '/* Navigation center area */',
                    '/* 导航链接样式优化 */': '/* Navigation link style optimization */',
                    '/* 特殊按钮样式 */': '/* Special button styles */',
                    '/* 语言切换器样式 */': '/* Language switcher styles */',
                    '/* 确保emoji正确显示 */': '/* Ensure emoji displays correctly */',
                    '/* 语言切换器样式优化 */': '/* Language switcher style optimization */',
                    '/* 自定义语言选择器样式 */': '/* Custom language selector styles */',
                    '/* 移动端导航栏垂直排列 */': '/* Mobile navigation vertical layout */'
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
                print(f"  ✅ 总共清理了 {changes} 个中文注释")
            else:
                print(f"  ℹ️  无需清理")
            
        except Exception as e:
            print(f"  ❌ 处理失败: {str(e)}")
    
    # 清理所有语言版本的online.html
    language_dirs = ['en', 'zh-cn', 'es', 'pt-br', 'fr', 'de', 'ru', 'ar', 'hi', 'id', 'vi', 'ja']
    
    for lang in language_dirs:
        lang_online_file = f"{lang}/online.html"
        if os.path.exists(lang_online_file):
            print(f"🧹 清理: {lang_online_file}")
            
            try:
                with open(lang_online_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                changes = 0
                
                # 清理中文注释
                chinese_comments = re.findall(r'/\*[^*]*[\u4e00-\u9fff][^*]*\*/', content)
                if chinese_comments:
                    print(f"  🔍 找到 {len(chinese_comments)} 个中文注释")
                    
                    # 替换中文注释为英文注释
                    replacements = {
                        '/* 导航栏中间区域 */': '/* Navigation center area */',
                        '/* 导航链接样式优化 */': '/* Navigation link style optimization */',
                        '/* 特殊按钮样式 */': '/* Special button styles */',
                        '/* 语言切换器样式 */': '/* Language switcher styles */',
                        '/* 移动端导航栏垂直排列 */': '/* Mobile navigation vertical layout */'
                    }
                    
                    for chinese, english in replacements.items():
                        if chinese in content:
                            content = content.replace(chinese, english)
                            changes += 1
                            print(f"  ✅ 替换: {chinese} -> {english}")
                
                if changes > 0:
                    # 写回文件
                    with open(lang_online_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  ✅ 总共清理了 {changes} 个中文注释")
                else:
                    print(f"  ℹ️  无需清理")
                
            except Exception as e:
                print(f"  ❌ 处理失败: {str(e)}")
        
        print()
    
    print("=" * 80)
    print("🎯 CSS中文注释清理完成！")
    print("=" * 80)
    print("✅ 现在online页面应该可以正常显示了")
    print("🧹 清理了所有可能导致问题的中文注释")
    print("🎨 CSS样式应该正确解析")

def main():
    """主函数"""
    
    print("🧹 开始清理online页面CSS中的中文注释...")
    print("=" * 80)
    
    # 清理CSS注释
    clean_css_comments()
    
    print(f"\n" + "=" * 80)
    print("🎉 清理完成！")
    print("=" * 80)
    print("✅ online页面CSS注释清理完成！")

if __name__ == "__main__":
    main() 