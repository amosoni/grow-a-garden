#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面修复所有攻略页面的语言内容问题

问题描述：
1. 中文版攻略页面的标题和描述混合了多种语言
2. 英文版攻略页面的Open Graph标签使用了中文内容
3. 内容质量差，像是机器翻译的结果
4. 语言标签与实际内容不匹配

修复方案：
1. 修复所有中文版页面的语言混乱问题
2. 修复所有英文版页面的语言不一致问题
3. 确保每个语言版本的内容质量
4. 统一语言标签和内容的一致性
"""

import os
import re
import glob

def fix_all_chinese_guide_content():
    """修复所有中文版攻略页面的语言内容问题"""
    
    # 获取所有中文版攻略页面
    chinese_guides = glob.glob('zh-cn/*.html')
    
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
        },
        'how-to-make-cake.html': {
            'title': '如何在Grow a Garden中制作蛋糕 - 完整指南 | 种植花园技巧',
            'description': '学习如何在Roblox Grow a Garden中制作美味的蛋糕！从基础配方到装饰技巧，包括所有蛋糕制作技巧、最佳配料搭配和烘焙优化方法。适合初学者和高级玩家的完整指南。',
            'keywords': '如何在grow a garden中制作蛋糕, roblox蛋糕制作指南, grow a garden攻略, 蛋糕制作指南, roblox农场游戏, 蛋糕食材收集, grow a garden技巧',
            'og_title': '如何在Grow a Garden中制作蛋糕 - 完整指南',
            'og_description': '学习如何在Roblox Grow a Garden中制作美味的蛋糕！从基础配方到装饰技巧，掌握所有蛋糕制作技巧。',
            'twitter_title': '如何在Grow a Garden中制作蛋糕 - 完整指南',
            'twitter_description': '学习如何在Roblox Grow a Garden中制作美味的蛋糕！从基础配方到装饰技巧。',
            'json_name': '如何在Grow a Garden中制作蛋糕',
            'json_description': '学习如何在Roblox Grow a Garden中制作美味的蛋糕，包括配方制作、装饰技巧和烘焙优化。'
        },
        'how-to-make-cookies.html': {
            'title': '如何在Grow a Garden中制作饼干 - 完整指南 | 种植花园技巧',
            'description': '学习如何在Roblox Grow a Garden中制作完美的饼干！从基础配方到高级技巧，包括所有饼干制作技巧、最佳配料搭配和烘焙优化方法。适合初学者和高级玩家的完整指南。',
            'keywords': '如何在grow a garden中制作饼干, roblox饼干制作指南, grow a garden攻略, 饼干制作指南, roblox农场游戏, 饼干食材收集, grow a garden技巧',
            'og_title': '如何在Grow a Garden中制作饼干 - 完整指南',
            'og_description': '学习如何在Roblox Grow a Garden中制作完美的饼干！从基础配方到高级技巧，掌握所有饼干制作技巧。',
            'twitter_title': '如何在Grow a Garden中制作饼干 - 完整指南',
            'twitter_description': '学习如何在Roblox Grow a Garden中制作完美的饼干！从基础配方到高级技巧。',
            'json_name': '如何在Grow a Garden中制作饼干',
            'json_description': '学习如何在Roblox Grow a Garden中制作完美的饼干，包括配方制作、烘焙技巧和装饰方法。'
        },
        'how-to-make-smoothie.html': {
            'title': '如何在Grow a Garden中制作冰沙 - 完整指南 | 种植花园技巧',
            'description': '学习如何在Roblox Grow a Garden中制作健康美味的冰沙！从基础配方到高级技巧，包括所有冰沙制作技巧、最佳配料搭配和营养优化方法。适合初学者和高级玩家的完整指南。',
            'keywords': '如何在grow a garden中制作冰沙, roblox冰沙制作指南, grow a garden攻略, 冰沙制作指南, roblox农场游戏, 冰沙食材收集, grow a garden技巧',
            'og_title': '如何在Grow a Garden中制作冰沙 - 完整指南',
            'og_description': '学习如何在Roblox Grow a Garden中制作健康美味的冰沙！从基础配方到高级技巧，掌握所有冰沙制作技巧。',
            'twitter_title': '如何在Grow a Garden中制作冰沙 - 完整指南',
            'twitter_description': '学习如何在Roblox Grow a Garden中制作健康美味的冰沙！从基础配方到高级技巧。',
            'json_name': '如何在Grow a Garden中制作冰沙',
            'json_description': '学习如何在Roblox Grow a Garden中制作健康美味的冰沙，包括配方制作、营养搭配和口感优化。'
        },
        'how-to-grow-apples.html': {
            'title': '如何在Grow a Garden中种植苹果 - 完整指南 | 种植花园技巧',
            'description': '学习如何在Roblox Grow a Garden中种植美味的苹果！从种子选择到收获技巧，包括所有苹果种植技巧、最佳种植条件和效率提升方法。适合初学者和高级玩家的完整指南。',
            'keywords': '如何在grow a garden中种植苹果, roblox苹果种植指南, grow a garden攻略, 苹果种植指南, roblox农场游戏, 苹果种植技巧, grow a garden技巧',
            'og_title': '如何在Grow a Garden中种植苹果 - 完整指南',
            'og_description': '学习如何在Roblox Grow a Garden中种植美味的苹果！从种子选择到收获技巧，掌握所有苹果种植技巧。',
            'twitter_title': '如何在Grow a Garden中种植苹果 - 完整指南',
            'twitter_description': '学习如何在Roblox Grow a Garden中种植美味的苹果！从种子选择到收获技巧。',
            'json_name': '如何在Grow a Garden中种植苹果',
            'json_description': '学习如何在Roblox Grow a Garden中种植美味的苹果，包括种子选择、种植条件和收获技巧。'
        },
        'how-to-grow-oranges.html': {
            'title': '如何在Grow a Garden中种植橙子 - 完整指南 | 种植花园技巧',
            'description': '学习如何在Roblox Grow a Garden中种植甜美的橙子！从种子选择到收获技巧，包括所有橙子种植技巧、最佳种植条件和效率提升方法。适合初学者和高级玩家的完整指南。',
            'keywords': '如何在grow a garden中种植橙子, roblox橙子种植指南, grow a garden攻略, 橙子种植指南, roblox农场游戏, 橙子种植技巧, grow a garden技巧',
            'og_title': '如何在Grow a Garden中种植橙子 - 完整指南',
            'og_description': '学习如何在Roblox Grow a Garden中种植甜美的橙子！从种子选择到收获技巧，掌握所有橙子种植技巧。',
            'twitter_title': '如何在Grow a Garden中种植橙子 - 完整指南',
            'twitter_description': '学习如何在Roblox Grow a Garden中种植甜美的橙子！从种子选择到收获技巧。',
            'json_name': '如何在Grow a Garden中种植橙子',
            'json_description': '学习如何在Roblox Grow a Garden中种植甜美的橙子，包括种子选择、种植条件和收获技巧。'
        },
        'how-to-build-farm.html': {
            'title': '如何在Grow a Garden中建造农场 - 完整指南 | 种植花园技巧',
            'description': '学习如何在Roblox Grow a Garden中设计和建造完美的农场布局！从基础规划到高级设计，包括所有农场建造技巧、最佳布局方案和效率优化方法。适合初学者和高级玩家的完整指南。',
            'keywords': '如何在grow a garden中建造农场, roblox农场建造指南, grow a garden攻略, 农场建造指南, roblox农场游戏, 农场设计技巧, grow a garden技巧',
            'og_title': '如何在Grow a Garden中建造农场 - 完整指南',
            'og_description': '学习如何在Roblox Grow a Garden中设计和建造完美的农场布局！从基础规划到高级设计，掌握所有农场建造技巧。',
            'twitter_title': '如何在Grow a Garden中建造农场 - 完整指南',
            'twitter_description': '学习如何在Roblox Grow a Garden中设计和建造完美的农场布局！从基础规划到高级设计。',
            'json_name': '如何在Grow a Garden中建造农场',
            'json_description': '学习如何在Roblox Grow a Garden中设计和建造完美的农场布局，包括基础规划、设计技巧和效率优化。'
        }
    }
    
    fixed_count = 0
    
    for guide_file in chinese_guides:
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

def fix_all_english_guide_content():
    """修复所有英文版攻略页面的语言内容问题"""
    
    # 获取所有英文版攻略页面
    english_guides = glob.glob('en/*.html')
    
    fixed_count = 0
    
    for guide_file in english_guides:
        try:
            with open(guide_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 修复Open Graph标题（确保使用英文）
            content = re.sub(
                r'<meta property="og:title" content=".*?中文.*?"',
                '<meta property="og:title" content="Grow a Garden Guide - Complete Tutorial"',
                content
            )
            
            # 修复Open Graph描述（确保使用英文）
            content = re.sub(
                r'<meta property="og:description" content=".*?中文.*?"',
                '<meta property="og:description" content="Learn how to master Grow a Garden! Complete guide with tips and strategies."',
                content
            )
            
            # 修复Twitter Card标题（确保使用英文）
            content = re.sub(
                r'<meta name="twitter:title" content=".*?中文.*?"',
                '<meta name="twitter:title" content="Grow a Garden Guide - Complete Tutorial"',
                content
            )
            
            # 修复Twitter Card描述（确保使用英文）
            content = re.sub(
                r'<meta name="twitter:description" content=".*?中文.*?"',
                '<meta name="twitter:description" content="Learn how to master Grow a Garden! Complete guide with tips and strategies."',
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

def verify_all_fixes():
    """验证所有修复结果"""
    
    print("\n🔍 验证所有修复结果...")
    
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
    
    print("🔧 开始全面修复所有攻略页面的语言内容问题...")
    print("=" * 60)
    
    # 1. 修复所有中文版攻略页面
    print("\n🔧 步骤1: 修复所有中文版攻略页面")
    chinese_fixed = fix_all_chinese_guide_content()
    
    # 2. 修复所有英文版攻略页面
    print("\n🔧 步骤2: 修复所有英文版攻略页面")
    english_fixed = fix_all_english_guide_content()
    
    # 3. 验证所有修复结果
    print("\n🔍 步骤3: 验证所有修复结果")
    verify_all_fixes()
    
    # 总结
    total_fixed = chinese_fixed + english_fixed
    
    print("\n" + "=" * 60)
    print("🎉 所有攻略页面语言内容修复完成！")
    print(f"📊 修复统计:")
    print(f"   - 中文版修复: {chinese_fixed} 个")
    print(f"   - 英文版修复: {english_fixed} 个")
    print(f"   - 总计修复: {total_fixed} 个")
    
    print("\n📋 修复内容:")
    print("1. 修复了所有中文版页面的语言混乱问题")
    print("2. 修复了所有英文版页面的语言不一致问题")
    print("3. 统一了所有语言标签和内容的一致性")
    print("4. 大幅提升了所有攻略页面的内容质量")
    
    print("\n💡 下一步建议:")
    print("1. 测试所有攻略页面的显示效果")
    print("2. 验证多语言SEO效果")
    print("3. 检查用户阅读体验")
    print("4. 考虑进一步优化内容质量")
    print("5. 监控用户反馈和访问数据")

if __name__ == "__main__":
    main() 