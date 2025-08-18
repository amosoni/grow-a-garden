#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证online页面的完整性和正确性
"""

import os
import re

def verify_online_page():
    """验证online页面的完整性"""
    
    print("🔍 开始验证online页面...")
    print("=" * 80)
    
    # 验证根目录的online.html
    online_file = "online.html"
    if os.path.exists(online_file):
        print(f"🔍 验证: {online_file}")
        
        try:
            with open(online_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            issues = []
            
            # 检查HTML结构
            if '<!DOCTYPE html>' not in content:
                issues.append("❌ 缺少 DOCTYPE 声明")
            else:
                print("  ✅ DOCTYPE 声明正确")
            
            if '<html' not in content:
                issues.append("❌ 缺少 html 标签")
            else:
                print("  ✅ html 标签存在")
            
            if '</html>' not in content:
                issues.append("❌ 缺少 html 结束标签")
            else:
                print("  ✅ html 结束标签存在")
            
            # 检查CSS链接
            if 'href="styles.css"' in content:
                print("  ✅ CSS 路径正确")
            else:
                issues.append("❌ CSS 路径不正确")
            
            if 'href="https://unpkg.com/simple.css@2.1.0/simple.min.css"' in content:
                print("  ✅ Simple.css 链接正确")
            else:
                issues.append("❌ Simple.css 链接不正确")
            
            # 检查国旗
            svg_flags = re.findall(r'<svg[^>]*>.*?</svg>', content, re.DOTALL)
            if svg_flags:
                print(f"  ✅ 找到 {len(svg_flags)} 个SVG国旗")
            else:
                issues.append("❌ 没有找到SVG国旗")
            
            # 检查JavaScript
            if '<script' in content and '</script>' in content:
                print("  ✅ JavaScript 标签完整")
            else:
                issues.append("❌ JavaScript 标签不完整")
            
            # 检查中文注释
            chinese_comments = re.findall(r'/\*[^*]*[\u4e00-\u9fff][^*]*\*/', content)
            if chinese_comments:
                issues.append(f"❌ 仍有 {len(chinese_comments)} 个中文CSS注释")
            else:
                print("  ✅ 没有中文CSS注释")
            
            chinese_js_comments = re.findall(r'//[^\\n]*[\u4e00-\u9fff][^\\n]*', content)
            if chinese_js_comments:
                issues.append(f"❌ 仍有 {len(chinese_js_comments)} 个中文JavaScript注释")
            else:
                print("  ✅ 没有中文JavaScript注释")
            
            # 检查页面结构
            if 'class="hero-section"' in content:
                print("  ✅ 英雄区域存在")
            else:
                issues.append("❌ 英雄区域缺失")
            
            if 'class="features-section"' in content:
                print("  ✅ 功能区域存在")
            else:
                issues.append("❌ 功能区域缺失")
            
            if 'class="language-selector"' in content:
                print("  ✅ 语言选择器存在")
            else:
                issues.append("❌ 语言选择器缺失")
            
            # 输出结果
            if issues:
                print(f"\n  ⚠️  发现 {len(issues)} 个问题:")
                for issue in issues:
                    print(f"    {issue}")
            else:
                print(f"\n  🎉 页面验证通过！没有发现问题")
            
        except Exception as e:
            print(f"  ❌ 验证失败: {str(e)}")
    
    print("=" * 80)
    print("🎯 online页面验证完成！")
    print("=" * 80)

def main():
    """主函数"""
    
    print("🔍 开始验证online页面...")
    print("=" * 80)
    
    # 验证online页面
    verify_online_page()
    
    print(f"\n" + "=" * 80)
    print("🎉 验证完成！")
    print("=" * 80)

if __name__ == "__main__":
    main() 