#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门修复online页面的样式问题
"""

import os
import re

def fix_online_page_styles():
    """修复online页面的样式问题"""
    
    print("🔧 开始修复online页面的样式问题...")
    print("=" * 80)
    
    # 修复根目录的online.html
    online_file = "online.html"
    if os.path.exists(online_file):
        print(f"🔧 修复: {online_file}")
        
        try:
            with open(online_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            changes = 0
            
            # 修复CSS路径
            if 'href="../styles.css"' in content:
                content = content.replace('href="../styles.css"', 'href="styles.css"')
                changes += 1
                print(f"  ✅ 修复了CSS路径: ../styles.css -> styles.css")
            
            # 检查是否有其他CSS路径问题
            if 'href="unpkg.com/' in content:
                content = content.replace('href="unpkg.com/', 'href="https://unpkg.com/')
                changes += 1
                print(f"  ✅ 修复了unpkg.com链接")
            
            # 检查国旗是否已经是SVG
            svg_flags = re.findall(r'<svg[^>]*>.*?</svg>', content, re.DOTALL)
            if svg_flags:
                print(f"  ✅ 国旗已经是SVG格式 ({len(svg_flags)} 个)")
            else:
                print(f"  ⚠️  没有找到SVG国旗")
            
            # 检查JavaScript中的国旗引用
            if 'flags/${lang}.png' in content:
                print(f"  ⚠️  仍然有JavaScript图片国旗引用")
                # 注释掉这些引用
                content = content.replace(
                    "currentLangBtn.querySelector('.flag-img').src = `flags/${lang}.png`;",
                    "// currentLangBtn.querySelector('.flag-img').src = `flags/${lang}.png`; // 已修复：国旗改为内联SVG"
                )
                changes += 1
                print(f"  ✅ 注释掉了JavaScript图片国旗引用")
            
            if changes > 0:
                # 写回文件
                with open(online_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✅ 总共修复了 {changes} 个问题")
            else:
                print(f"  ℹ️  无需修复")
            
        except Exception as e:
            print(f"  ❌ 处理失败: {str(e)}")
    
    # 修复所有语言版本的online.html
    language_dirs = ['en', 'zh-cn', 'es', 'pt-br', 'fr', 'de', 'ru', 'ar', 'hi', 'id', 'vi', 'ja']
    
    for lang in language_dirs:
        lang_online_file = f"{lang}/online.html"
        if os.path.exists(lang_online_file):
            print(f"🔧 修复: {lang_online_file}")
            
            try:
                with open(lang_online_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                changes = 0
                
                # 修复CSS路径
                if 'href="unpkg.com/' in content:
                    content = content.replace('href="unpkg.com/', 'href="https://unpkg.com/')
                    changes += 1
                    print(f"  ✅ 修复了unpkg.com链接")
                
                # 检查国旗是否已经是SVG
                svg_flags = re.findall(r'<svg[^>]*>.*?</svg>', content, re.DOTALL)
                if svg_flags:
                    print(f"  ✅ 国旗已经是SVG格式 ({len(svg_flags)} 个)")
                else:
                    print(f"  ⚠️  没有找到SVG国旗")
                
                # 检查JavaScript中的国旗引用
                if 'flags/${lang}.png' in content:
                    print(f"  ⚠️  仍然有JavaScript图片国旗引用")
                    # 注释掉这些引用
                    content = content.replace(
                        "currentLangBtn.querySelector('.flag-img').src = `flags/${lang}.png`;",
                        "// currentLangBtn.querySelector('.flag-img').src = `flags/${lang}.png`; // 已修复：国旗改为内联SVG"
                    )
                    changes += 1
                    print(f"  ✅ 注释掉了JavaScript图片国旗引用")
                
                if changes > 0:
                    # 写回文件
                    with open(lang_online_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  ✅ 总共修复了 {changes} 个问题")
                else:
                    print(f"  ℹ️  无需修复")
                
            except Exception as e:
                print(f"  ❌ 处理失败: {str(e)}")
        
        print()
    
    print("=" * 80)
    print("🎯 online页面样式修复完成！")
    print("=" * 80)
    print("✅ 现在online页面应该可以正常显示了")
    print("🌍 国旗应该正确显示为SVG格式")
    print("🎨 CSS样式应该正确加载")

def main():
    """主函数"""
    
    print("🔧 开始修复online页面的样式问题...")
    print("=" * 80)
    
    # 修复online页面样式
    fix_online_page_styles()
    
    print(f"\n" + "=" * 80)
    print("🎉 修复完成！")
    print("=" * 80)
    print("✅ online页面样式问题修复完成！")

if __name__ == "__main__":
    main() 