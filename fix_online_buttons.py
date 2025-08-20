#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复所有语言版本的Online按钮问题
将 scrollToSection('online') 改为 scrollToSection('stats')
"""

import os
import re
import glob

def fix_online_buttons():
    """修复所有HTML文件中的Online按钮问题"""
    
    # 查找所有HTML文件
    html_files = []
    
    # 查找根目录和所有语言子目录中的HTML文件
    for pattern in ['*.html', '*/index.html', '*/*.html']:
        html_files.extend(glob.glob(pattern))
    
    # 去重
    html_files = list(set(html_files))
    
    # 过滤掉不需要的文件
    html_files = [f for f in html_files if not f.startswith('vegetable-plants-grow-a-garden.html')]
    
    print(f"找到 {len(html_files)} 个HTML文件")
    
    fixed_count = 0
    
    for file_path in html_files:
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含需要修复的内容
            if "scrollToSection('online')" in content:
                # 替换内容
                new_content = content.replace(
                    "scrollToSection('online')", 
                    "scrollToSection('stats')"
                )
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ 已修复: {file_path}")
                fixed_count += 1
            else:
                print(f"⏭️  无需修复: {file_path}")
                
        except Exception as e:
            print(f"❌ 修复失败 {file_path}: {e}")
    
    print(f"\n修复完成！共修复了 {fixed_count} 个文件")
    
    # 验证修复结果
    print("\n验证修复结果...")
    verify_fix()

def verify_fix():
    """验证修复结果"""
    
    # 查找所有HTML文件
    html_files = []
    for pattern in ['*.html', '*/index.html', '*/*.html']:
        html_files.extend(glob.glob(pattern))
    
    html_files = list(set(html_files))
    html_files = [f for f in html_files if not f.startswith('vegetable-plants-grow-a-garden.html')]
    
    remaining_online = []
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "scrollToSection('online')" in content:
                remaining_online.append(file_path)
                
        except Exception as e:
            print(f"❌ 验证失败 {file_path}: {e}")
    
    if remaining_online:
        print(f"⚠️  仍有 {len(remaining_online)} 个文件包含 'online' 引用:")
        for file_path in remaining_online:
            print(f"   - {file_path}")
    else:
        print("✅ 所有Online按钮问题已修复完成！")

if __name__ == "__main__":
    print("开始修复Online按钮问题...")
    fix_online_buttons() 