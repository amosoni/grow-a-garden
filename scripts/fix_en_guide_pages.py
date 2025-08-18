#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正英文攻略页面的导航栏和尾部栏
使其与英文首页保持一致
"""

import re
from pathlib import Path

def get_english_homepage_content():
    """获取英文首页的导航栏和尾部栏内容"""
    try:
        with open('en/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取导航栏
        nav_match = re.search(r'<header>(.*?)</header>', content, re.DOTALL)
        if nav_match:
            navigation = nav_match.group(1)
        else:
            navigation = ""
        
        # 提取尾部栏
        footer_match = re.search(r'<footer>(.*?)</footer>', content, re.DOTALL)
        if footer_match:
            footer = footer_match.group(1)
        else:
            footer = ""
        
        return navigation, footer
    except Exception as e:
        print(f"❌ 读取英文首页失败: {e}")
        return "", ""

def fix_english_guide_page(file_path, navigation, footer):
    """修正英文攻略页面"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 修正语言标签
        content = re.sub(r'lang="zh-CN"', 'lang="en"', content)
        content = re.sub(r'lang="zh-cn"', 'lang="en"', content)
        
        # 2. 修正标题为英文
        content = re.sub(r'<title>如何在种植花园中 制作沙拉.*?</title>', 
                        '<title>How to Make Salad in Grow a Garden - Complete Guide | Grow a Garden Tips</title>', content)
        
        # 3. 修正meta描述为英文
        content = re.sub(r'<meta name="description" content="学习如何在Roblox种植花园中 制作沙拉.*?"', 
                        '<meta name="description" content="Learn how to make salad in Roblox Grow a Garden! Complete guide with techniques and efficiency improvement methods."', content)
        
        # 4. 修正meta关键词为英文
        content = re.sub(r'<meta name="keywords" content="如何在种植花园中 制作沙拉.*?"', 
                        '<meta name="keywords" content="how to make salad in grow a garden, roblox salad making guide, grow a garden guide, salad making guide, roblox farming game, salad ingredients collection, grow a garden tips"', content)
        
        # 5. 替换导航栏
        if navigation:
            old_nav_match = re.search(r'<header>(.*?)</header>', content, re.DOTALL)
            if old_nav_match:
                content = content.replace(old_nav_match.group(0), f'<header>{navigation}</header>')
        
        # 6. 替换尾部栏
        if footer:
            old_footer_match = re.search(r'<footer>(.*?)</footer>', content, re.DOTALL)
            if old_footer_match:
                content = content.replace(old_footer_match.group(0), f'<footer>{footer}</footer>')
            else:
                # 如果没有尾部栏，在body结束前添加
                content = re.sub(r'</body>', f'{footer}\n</body>', content)
        
        # 7. 修正页面内容为英文
        content = re.sub(r'<h1[^>]*>🥗 沙拉制作指南</h1>', 
                        '<h1 data-i18n="salad.guide.hero.title">🥗 Salad Making Guide</h1>', content)
        
        content = re.sub(r'<p[^>]*>学习在 Grow a Garden 中制作沙拉的技巧。</p>', 
                        '<p data-i18n="salad.guide.hero.subtitle">Learn techniques for making salad in Grow a Garden.</p>', content)
        
        # 8. 修正面包屑导航为英文
        content = re.sub(r'<a href="index.html">🏠 首页</a>', 
                        '<a href="index.html">🏠 Home</a>', content)
        content = re.sub(r'<a href="guides.html">📚 攻略</a>', 
                        '<a href="guides.html">📚 Guides</a>', content)
        content = re.sub(r'<li aria-current="page"[^>]*>🎯 制作沙拉</li>', 
                        '<li aria-current="page" data-i18n="salad.guide.breadcrumb.current">🎯 Make Salad</li>', content)
        
        # 9. 修正目录标题为英文
        content = re.sub(r'<h2[^>]*>📋 目录</h2>', 
                        '<h2 data-i18n="toc.title">📋 Table of Contents</h2>', content)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已修正英文页面: {file_path.name}")
            return True
        else:
            print(f"⏭️  无需修改: {file_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ 修正失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始修正英文攻略页面的导航栏和尾部栏...")
    
    # 获取英文首页的导航栏和尾部栏
    navigation, footer = get_english_homepage_content()
    
    if not navigation and not footer:
        print("❌ 无法获取英文首页内容")
        return
    
    print("📋 已获取英文首页的导航栏和尾部栏")
    
    # 查找英文目录下的所有攻略页面
    en_dir = Path("en")
    if not en_dir.exists():
        print("❌ 英文目录不存在")
        return
    
    guide_files = []
    for pattern in ['how-to-*.html', '*-guide.html', '*-strategies.html', '*-basics.html', '*-tips.html']:
        guide_files.extend(en_dir.glob(pattern))
    
    if not guide_files:
        print("❌ 英文目录下没有攻略页面")
        return
    
    print(f"📁 找到 {len(guide_files)} 个英文攻略页面")
    
    # 修正每个页面
    fixed_count = 0
    for file_path in guide_files:
        if fix_english_guide_page(file_path, navigation, footer):
            fixed_count += 1
    
    print(f"\n🎉 英文攻略页面修正完成！")
    print(f"📊 成功修正: {fixed_count} 个文件")
    print("✨ 现在英文攻略页面的导航栏和尾部栏与首页保持一致了！")

if __name__ == "__main__":
    main() 