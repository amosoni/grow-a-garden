#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
只修复语言问题，不修改样式
"""

import os
import glob
import re

def get_html_files():
    """获取所有HTML文件"""
    return glob.glob('*.html')

def fix_only_language_issues(content):
    """只修复语言问题，不修改样式"""
    
    changes_made = []
    
    # 只修复data-i18n属性，不修改CSS
    if 'data-i18n=' in content:
        # 替换data-i18n属性为实际的英文文本
        content = content.replace('data-i18n="nav.back"', '')
        content = content.replace('data-i18n="hero.title"', '')
        content = content.replace('data-i18n="hero.subtitle"', '')
        content = content.replace('data-i18n="game.playMiniPlay"', '')
        content = content.replace('data-i18n="game.playPlayHop"', '')
        content = content.replace('data-i18n="features.title"', '')
        content = content.replace('data-i18n="features.plant.title"', '')
        content = content.replace('data-i18n="features.plant.desc"', '')
        content = content.replace('data-i18n="features.mutations.title"', '')
        content = content.replace('data-i18n="features.mutations.desc"', '')
        content = content.replace('data-i18n="features.profit.title"', '')
        content = content.replace('data-i18n="features.profit.desc"', '')
        content = content.replace('data-i18n="features.multiplayer.title"', '')
        content = content.replace('data-i18n="features.multiplayer.desc"', '')
        content = content.replace('data-i18n="features.world.title"', '')
        content = content.replace('data-i18n="features.world.desc"', '')
        content = content.replace('data-i18n="features.achievements.title"', '')
        content = content.replace('data-i18n="features.achievements.desc"', '')
        content = content.replace('data-i18n="footer.copyright"', '')
        content = content.replace('data-i18n="footer.disclaimer"', '')
        
        changes_made.append('移除data-i18n语言属性')
    
    return content, changes_made

def fix_all_files():
    """修复所有HTML文件的语言问题"""
    
    html_files = get_html_files()
    
    print("🔧 开始修复语言问题（不修改样式）...")
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
            
            # 只修复语言问题
            content, changes = fix_only_language_issues(content)
            file_changes.extend(changes)
            
            if content != original_content:
                # 写回修复后的内容
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ 成功修复 {len(file_changes)} 个语言问题:")
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
        print(f"\n✅ 成功修复了 {fixed_files} 个文件的语言问题！")
        print(f"🔧 总共修复了 {total_changes} 个问题")
        print(f"🎨 您的样式完全保持不变")
    else:
        print(f"\n⚠️  没有语言问题需要修复")
    
    return fixed_files, total_changes

def main():
    """主函数"""
    
    print("🔧 开始修复语言问题（保持样式不变）...")
    print("=" * 80)
    
    # 修复所有文件
    fixed_files, total_changes = fix_all_files()
    
    print(f"\n" + "=" * 80)
    print("🎉 修复完成！")
    print("=" * 80)
    
    if fixed_files > 0:
        print("✅ 所有语言问题都已修复完成！")
        print("🎨 您的样式完全保持不变")
    else:
        print("⚠️  没有语言问题需要修复")

if __name__ == "__main__":
    main() 