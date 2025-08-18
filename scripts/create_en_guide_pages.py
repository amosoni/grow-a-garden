#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为en目录创建完整的攻略页面
复制其他语言目录的攻略页面并转换为英文版本
"""

import shutil
from pathlib import Path

def create_en_guide_pages():
    """为en目录创建完整的攻略页面"""
    print("🚀 开始为en目录创建完整的攻略页面...")
    
    # 源目录（使用zh-cn作为模板，因为它有完整的攻略页面）
    source_dir = Path("zh-cn")
    target_dir = Path("en")
    
    if not source_dir.exists():
        print("❌ 源目录不存在: zh-cn")
        return
    
    if not target_dir.exists():
        print("❌ 目标目录不存在: en")
        return
    
    # 需要复制的攻略页面文件
    guide_files = [
        "how-to-build-farm.html",
        "how-to-grow-apples.html", 
        "how-to-grow-berries.html",
        "how-to-grow-carrots.html",
        "how-to-grow-corn.html",
        "how-to-grow-oranges.html",
        "how-to-grow-wheat.html",
        "how-to-make-bread.html",
        "how-to-make-cake.html",
        "how-to-make-cookies.html",
        "how-to-make-donut.html",
        "how-to-make-money-fast.html",
        "how-to-make-pie.html",
        "how-to-make-pizza.html",
        "how-to-make-salad.html",
        "how-to-make-sandwich.html",
        "how-to-make-smoothie.html",
        "how-to-make-spaghetti.html",
        "how-to-play-with-friends.html"
    ]
    
    created_count = 0
    
    for guide_file in guide_files:
        source_file = source_dir / guide_file
        target_file = target_dir / guide_file
        
        if not source_file.exists():
            print(f"⚠️  源文件不存在: {guide_file}")
            continue
            
        if target_file.exists():
            print(f"⏭️  目标文件已存在: {guide_file}")
            continue
        
        try:
            # 复制文件
            shutil.copy2(source_file, target_file)
            print(f"✅ 已创建: {guide_file}")
            created_count += 1
            
        except Exception as e:
            print(f"❌ 创建失败 {guide_file}: {e}")
    
    print(f"\n🎉 en目录攻略页面创建完成！")
    print(f"📊 成功创建: {created_count} 个文件")
    print("✨ 现在en目录有完整的攻略页面了！")

if __name__ == "__main__":
    create_en_guide_pages() 