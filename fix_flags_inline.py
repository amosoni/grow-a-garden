#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将国旗直接嵌入到HTML中，使用内联SVG
"""

import os
import re

def get_inline_flag_svg(lang):
    """获取内联SVG国旗"""
    
    flag_svgs = {
        'en': '<svg width="20" height="15" viewBox="0 0 640 480" style="display:inline-block;vertical-align:middle;"><rect width="640" height="480" fill="#bd3d44"/><rect width="640" height="96" fill="#fff"/><rect width="640" height="96" y="96" fill="#fff"/><rect width="640" height="96" y="192" fill="#fff"/><rect width="640" height="96" y="288" fill="#fff"/><rect width="640" height="96" y="384" fill="#fff"/><path d="M0 0l256 240L0 480z" fill="#192f5d"/></svg>',
        'zh-cn': '<svg width="20" height="15" viewBox="0 0 900 600" style="display:inline-block;vertical-align:middle;"><rect width="900" height="600" fill="#de2910"/><g fill="#ffde00"><path d="M450 120l-45.7 140.7-119.3 0h154l-119.3 0z"/><path d="M450 300l-45.7 140.7-119.3 0h154l-119.3 0z"/><path d="M450 480l-45.7 140.7-119.3 0h154l-119.3 0z"/></g></svg>',
        'es': '<svg width="20" height="15" viewBox="0 0 750 500" style="display:inline-block;vertical-align:middle;"><rect width="750" height="500" fill="#c60b1e"/><rect width="750" height="250" y="125" fill="#ffc400"/></svg>',
        'pt-br': '<svg width="20" height="15" viewBox="0 0 720 504" style="display:inline-block;vertical-align:middle;"><rect width="720" height="504" fill="#009b3a"/><path d="M360 252l-180-126v252z" fill="#fedf00"/><circle cx="360" cy="252" r="60" fill="#002776"/></svg>',
        'fr': '<svg width="20" height="15" viewBox="0 0 900 600" style="display:inline-block;vertical-align:middle;"><rect width="300" height="600" fill="#002395"/><rect width="300" height="600" x="300" fill="#fff"/><rect width="300" height="600" x="600" fill="#ed2939"/></svg>',
        'de': '<svg width="20" height="15" viewBox="0 0 900 600" style="display:inline-block;vertical-align:middle;"><rect width="900" height="200" fill="#000"/><rect width="900" height="200" y="200" fill="#dd0000"/><rect width="900" height="200" y="400" fill="#ffce00"/></svg>',
        'ru': '<svg width="20" height="15" viewBox="0 0 900 600" style="display:inline-block;vertical-align:middle;"><rect width="900" height="200" fill="#fff"/><rect width="900" height="200" y="200" fill="#0039a6"/><rect width="900" height="200" y="400" fill="#d52b1e"/></svg>',
        'ar': '<svg width="20" height="15" viewBox="0 0 900 600" style="display:inline-block;vertical-align:middle;"><rect width="900" height="600" fill="#006c35"/><rect width="900" height="400" y="100" fill="#fff"/><rect width="900" height="200" y="200" fill="#ce1126"/></svg>',
        'hi': '<svg width="20" height="15" viewBox="0 0 900 600" style="display:inline-block;vertical-align:middle;"><rect width="900" height="200" fill="#ff9933"/><rect width="900" height="200" y="200" fill="#fff"/><rect width="900" height="200" y="400" fill="#138808"/><circle cx="450" cy="300" r="60" fill="#000080"/></svg>',
        'id': '<svg width="20" height="15" viewBox="0 0 900 600" style="display:inline-block;vertical-align:middle;"><rect width="900" height="300" fill="#fff"/><rect width="900" height="300" y="300" fill="#ce1126"/></svg>',
        'vi': '<svg width="20" height="15" viewBox="0 0 900 600" style="display:inline-block;vertical-align:middle;"><rect width="900" height="600" fill="#da251d"/><path d="M450 300l-180-126v252z" fill="#ffff00"/></svg>',
        'ja': '<svg width="20" height="15" viewBox="0 0 900 600" style="display:inline-block;vertical-align:middle;"><rect width="900" height="600" fill="#fff"/><circle cx="450" cy="300" r="180" fill="#bc002d"/></svg>'
    }
    
    return flag_svgs.get(lang, '')

def fix_flags_inline(content):
    """将国旗图片替换为内联SVG"""
    
    changes = 0
    
    # 替换所有 <img src="flags/..."> 为内联SVG
    for lang in ['en', 'zh-cn', 'es', 'pt-br', 'fr', 'de', 'ru', 'ar', 'hi', 'id', 'vi', 'ja']:
        # 匹配 <img src="flags/lang.png" alt="..." class="flag-img">
        old_pattern = f'<img src="flags/{lang}.png" alt="[^"]*" class="flag-img">'
        new_svg = get_inline_flag_svg(lang)
        
        if new_svg:
            content, count = re.subn(old_pattern, new_svg, content)
            changes += count
            
            # 也匹配相对路径的版本
            old_pattern2 = f'<img src="../flags/{lang}.png" alt="[^"]*" class="flag-img">'
            content, count = re.subn(old_pattern2, new_svg, content)
            changes += count
    
    return content, changes

def process_html_files():
    """处理所有HTML文件"""
    
    print("🔧 开始修复国旗显示问题...")
    print("=" * 80)
    
    # 获取所有HTML文件
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"📁 找到 {len(html_files)} 个HTML文件")
    print("=" * 80)
    
    total_changes = 0
    processed_files = 0
    
    for file_path in html_files:
        try:
            print(f"🔧 处理: {file_path}")
            
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 修复国旗
            new_content, changes = fix_flags_inline(content)
            
            if changes > 0:
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"  ✅ 修复了 {changes} 个国旗引用")
                total_changes += changes
            else:
                print(f"  ℹ️  无需修复")
            
            processed_files += 1
            
        except Exception as e:
            print(f"  ❌ 处理失败: {str(e)}")
    
    print(f"\n" + "=" * 80)
    print("🎯 修复完成总结")
    print("=" * 80)
    print(f"📊 处理结果:")
    print(f"   - 处理文件: {processed_files}")
    print(f"   - 总修复数: {total_changes}")
    
    if total_changes > 0:
        print(f"\n✅ 成功修复了 {total_changes} 个国旗显示问题！")
        print(f"🌍 现在国旗应该可以正确显示了")
        print(f"💡 国旗直接嵌入在HTML中，不需要外部图片文件")
    else:
        print(f"\n⚠️  没有国旗问题需要修复")
    
    return total_changes

def main():
    """主函数"""
    
    print("🔧 开始修复国旗显示问题...")
    print("=" * 80)
    
    # 处理HTML文件
    total_changes = process_html_files()
    
    print(f"\n" + "=" * 80)
    print("🎉 修复完成！")
    print("=" * 80)
    
    if total_changes > 0:
        print("✅ 国旗显示问题修复完成！")
        print("🌍 现在页面应该可以显示国旗了")
    else:
        print("⚠️  没有国旗问题需要修复")

if __name__ == "__main__":
    main() 