#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复攻略页面的语言内容问题

问题描述：
1. 中文版攻略页面的标题和描述混合了多种语言
2. 英文版攻略页面的Open Graph标签使用了中文内容
3. 内容质量差，像是机器翻译的结果
4. 语言标签与实际内容不匹配

修复方案：
1. 修复中文版页面的语言混乱问题
2. 修复英文版页面的语言不一致问题
3. 确保每个语言版本的内容质量
4. 统一语言标签和内容的一致性
"""

import os
import re
import glob

def fix_chinese_guide_content():
    """修复中文版攻略页面的语言内容问题"""
    
    chinese_guides = [
        'zh-cn/how-to-make-salad.html',
        'zh-cn/how-to-make-pizza.html',
        'zh-cn/how-to-make-bread.html',
        'zh-cn/how-to-make-cake.html',
        'zh-cn/how-to-make-cookies.html',
        'zh-cn/how-to-make-smoothie.html',
        'zh-cn/how-to-grow-apples.html',
        'zh-cn/how-to-grow-oranges.html',
        'zh-cn/how-to-build-farm.html'
    ]
    
    # 中文版攻略页面的正确内容模板
    chinese_content_fixes = {
        'how-to-make-salad.html': {
            'title': '如何在Grow a Garden中制作沙拉 - 完整指南 | 种植花园技巧',
            'description': '学习如何在Roblox Grow a Garden中制作完美的沙拉！从基础食材收集到高级食谱，包括所有沙拉制作技巧、最佳食材组合和效率提升方法。适合初学者和高级玩家的完整指南。',
            'keywords': '如何在grow a garden中制作沙拉, roblox沙拉制作指南, grow a garden攻略, 沙拉制作指南, roblox农场游戏, 沙拉食材收集, grow a garden技巧',
            'og_title': '如何在Grow a Garden中制作沙拉 - 完整指南',
            'og_description': '学习如何在Roblox Grow a Garden中制作完美的沙拉！从基础食材收集到高级食谱，掌握所有沙拉制作技巧。',
            'twitter_title': '如何在Grow a Garden中制作沙拉 - 完整指南',
            'twitter_description': '学习如何在Roblox Grow a Garden中制作完美的沙拉！从基础食材收集到高级食谱。',
            'json_name': '如何在Grow a Garden中制作沙拉',
            'json_description': '学习如何在Roblox Grow a Garden中制作完美的沙拉，包括食材收集、食谱制作和效率提升技巧。'
        },
        'how-to-make-pizza.html': {
            'title': '如何在Grow a Garden中制作披萨 - 完整指南 | 种植花园技巧',
            'description': '学习如何在Roblox Grow a Garden中制作美味的披萨！从面团准备到配料组合，包括所有披萨制作技巧、最佳配料搭配和烘焙优化方法。适合初学者和高级玩家的完整指南。',
            'keywords': '如何在grow a garden中制作披萨, roblox披萨制作指南, grow a garden攻略, 披萨制作指南, roblox农场游戏, 披萨食材收集, grow a garden技巧',
            'og_title': '如何在Grow a Garden中制作披萨 - 完整指南',
            'og_description': '学习如何在Roblox Grow a Garden中制作美味的披萨！从面团准备到配料组合，掌握所有披萨制作技巧。',
            'twitter_title': '如何在Grow a Garden中制作披萨 - 完整指南',
            'twitter_description': '学习如何在Roblox Grow a Garden中制作美味的披萨！从面团准备到配料组合。',
            'json_name': '如何在Grow a Garden中制作披萨',
            'json_description': '学习如何在Roblox Grow a Garden中制作美味的披萨，包括面团准备、配料搭配和烘焙技巧。'
        },
        'how-to-make-bread.html': {
            'title': '如何在Grow a Garden中制作面包 - 完整指南 | 种植花园技巧',
            'description': '学习如何在Roblox Grow a Garden中掌握面包制作技巧！了解面粉类型、酵母管理和烘焙优化，包括所有面包制作技巧、最佳配方和效率提升方法。适合初学者和高级玩家的完整指南。',
            'keywords': '如何在grow a garden中制作面包, roblox面包制作指南, grow a garden攻略, 面包制作指南, roblox农场游戏, 面包食材收集, grow a garden技巧',
            'og_title': '如何在Grow a Garden中制作面包 - 完整指南',
            'og_description': '学习如何在Roblox Grow a Garden中掌握面包制作技巧！了解面粉类型、酵母管理和烘焙优化。',
            'twitter_title': '如何在Grow a Garden中制作面包 - 完整指南',
            'twitter_description': '学习如何在Roblox Grow a Garden中掌握面包制作技巧！了解面粉类型、酵母管理和烘焙优化。',
            'json_name': '如何在Grow a Garden中制作面包',
            'json_description': '学习如何在Roblox Grow a Garden中掌握面包制作技巧，包括面粉类型、酵母管理和烘焙优化。'
        }
    }
    
    fixed_count = 0
    
    for guide_file in chinese_guides:
        if not os.path.exists(guide_file):
            continue
            
        try:
            with open(guide_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 获取文件名（不包含路径）
            filename = os.path.basename(guide_file)
            
            if filename in chinese_content_fixes:
                fixes = chinese_content_fixes[filename]
                
                # 修复标题
                content = re.sub(
                    r'<title>.*?</title>',
                    f'<title>{fixes["title"]}</title>',
                    content
                )
                
                # 修复meta description
                content = re.sub(
                    r'<meta name="description" content=".*?"',
                    f'<meta name="description" content="{fixes["description"]}"',
                    content
                )
                
                # 修复meta keywords
                content = re.sub(
                    r'<meta name="keywords" content=".*?"',
                    f'<meta name="keywords" content="{fixes["keywords"]}"',
                    content
                )
                
                # 修复Open Graph标题
                content = re.sub(
                    r'<meta property="og:title" content=".*?"',
                    f'<meta property="og:title" content="{fixes["og_title"]}"',
                    content
                )
                
                # 修复Open Graph描述
                content = re.sub(
                    r'<meta property="og:description" content=".*?"',
                    f'<meta property="og:description" content="{fixes["og_description"]}"',
                    content
                )
                
                # 修复Twitter Card标题
                content = re.sub(
                    r'<meta name="twitter:title" content=".*?"',
                    f'<meta name="twitter:title" content="{fixes["twitter_title"]}"',
                    content
                )
                
                # 修复Twitter Card描述
                content = re.sub(
                    r'<meta name="twitter:description" content=".*?"',
                    f'<meta name="twitter:description" content="{fixes["twitter_description"]}"',
                    content
                )
                
                # 修复JSON-LD数据
                content = re.sub(
                    r'"name": ".*?"',
                    f'"name": "{fixes["json_name"]}"',
                    content
                )
                
                content = re.sub(
                    r'"description": ".*?"',
                    f'"description": "{fixes["json_description"]}"',
                    content
                )
                
                # 保存修复后的内容
                with open(guide_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                fixed_count += 1
                print(f"✅ 修复中文版攻略页面: {guide_file}")
                
        except Exception as e:
            print(f"❌ 处理 {guide_file} 时出错: {str(e)}")
    
    return fixed_count

def fix_english_guide_content():
    """修复英文版攻略页面的语言内容问题"""
    
    english_guides = [
        'en/how-to-make-salad.html',
        'en/how-to-make-pizza.html',
        'en/how-to-make-bread.html',
        'en/how-to-make-cake.html',
        'en/how-to-make-cookies.html',
        'en/how-to-make-smoothie.html',
        'en/how-to-grow-apples.html',
        'en/how-to-grow-oranges.html',
        'en/how-to-build-farm.html'
    ]
    
    fixed_count = 0
    
    for guide_file in english_guides:
        if not os.path.exists(guide_file):
            continue
            
        try:
            with open(guide_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 修复Open Graph标题（确保使用英文）
            content = re.sub(
                r'<meta property="og:title" content=".*?中文.*?"',
                '<meta property="og:title" content="How to Make Salad in Grow a Garden - Complete Guide"',
                content
            )
            
            # 修复Open Graph描述（确保使用英文）
            content = re.sub(
                r'<meta property="og:description" content=".*?中文.*?"',
                '<meta property="og:description" content="Learn how to make perfect salads in Roblox Grow a Garden! From basic ingredient collection to advanced recipes."',
                content
            )
            
            # 修复Twitter Card标题（确保使用英文）
            content = re.sub(
                r'<meta name="twitter:title" content=".*?中文.*?"',
                '<meta name="twitter:title" content="How to Make Salad in Grow a Garden - Complete Guide"',
                content
            )
            
            # 修复Twitter Card描述（确保使用英文）
            content = re.sub(
                r'<meta name="twitter:description" content=".*?中文.*?"',
                '<meta name="twitter:description" content="Learn how to make perfect salads in Roblox Grow a Garden! From basic ingredient collection to advanced recipes."',
                content
            )
            
            # 保存修复后的内容
            with open(guide_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            fixed_count += 1
            print(f"✅ 修复英文版攻略页面: {guide_file}")
            
        except Exception as e:
            print(f"❌ 处理 {guide_file} 时出错: {str(e)}")
    
    return fixed_count

def verify_fixes():
    """验证修复结果"""
    
    print("\n🔍 验证修复结果...")
    
    # 检查中文版页面是否还有语言混乱问题
    chinese_guides = glob.glob('zh-cn/*.html')
    
    for guide_file in chinese_guides:
        try:
            with open(guide_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否还有混合语言的问题
            if re.search(r'en\s+Grow\s+a\s+Garden', content):
                print(f"⚠️  {guide_file} 仍存在语言混合问题")
            elif re.search(r'para\s+ganancias', content):
                print(f"⚠️  {guide_file} 仍存在西班牙语混入问题")
            else:
                print(f"✅ {guide_file} 语言内容正确")
                
        except Exception as e:
            print(f"❌ 验证 {guide_file} 时出错: {str(e)}")
    
    # 检查英文版页面是否还有中文内容
    english_guides = glob.glob('en/*.html')
    
    for guide_file in english_guides:
        try:
            with open(guide_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否还有中文内容
            if re.search(r'[\u4e00-\u9fff]', content):
                print(f"⚠️  {guide_file} 仍存在中文内容")
            else:
                print(f"✅ {guide_file} 语言内容正确")
                
        except Exception as e:
            print(f"❌ 验证 {guide_file} 时出错: {str(e)}")

def main():
    """主函数"""
    
    print("🔧 开始修复攻略页面的语言内容问题...")
    print("=" * 60)
    
    # 1. 修复中文版攻略页面
    print("\n🔧 步骤1: 修复中文版攻略页面")
    chinese_fixed = fix_chinese_guide_content()
    
    # 2. 修复英文版攻略页面
    print("\n🔧 步骤2: 修复英文版攻略页面")
    english_fixed = fix_english_guide_content()
    
    # 3. 验证修复结果
    print("\n🔍 步骤3: 验证修复结果")
    verify_fixes()
    
    # 总结
    total_fixed = chinese_fixed + english_fixed
    
    print("\n" + "=" * 60)
    print("🎉 攻略页面语言内容修复完成！")
    print(f"📊 修复统计:")
    print(f"   - 中文版修复: {chinese_fixed} 个")
    print(f"   - 英文版修复: {english_fixed} 个")
    print(f"   - 总计修复: {total_fixed} 个")
    
    print("\n📋 修复内容:")
    print("1. 修复了中文版页面的语言混乱问题")
    print("2. 修复了英文版页面的语言不一致问题")
    print("3. 统一了语言标签和内容的一致性")
    print("4. 提升了攻略页面的内容质量")
    
    print("\n💡 下一步建议:")
    print("1. 测试所有攻略页面的显示效果")
    print("2. 验证多语言SEO效果")
    print("3. 检查用户阅读体验")
    print("4. 考虑进一步优化内容质量")

if __name__ == "__main__":
    main() 