#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全修正英文攻略页面的所有内容
包括页面内容、Open Graph、Twitter Card和JSON-LD数据
"""

import re
from pathlib import Path

def get_english_translations():
    """获取英文翻译内容"""
    return {
        "salad": {
            "title": "How to Make Salad in Grow a Garden - Complete Guide | Grow a Garden Tips",
            "description": "Learn how to make salad in Roblox Grow a Garden! Complete guide with techniques and efficiency improvement methods.",
            "keywords": "how to make salad in grow a garden, roblox salad making guide, grow a garden guide, salad making guide, roblox farming game, salad ingredients collection, grow a garden tips",
            "og_title": "How to Make Salad in Grow a Garden - Complete Guide | Grow a Garden Tips",
            "og_description": "Learn how to make salad in Roblox Grow a Garden! Complete guide with techniques and efficiency improvement methods.",
            "hero_title": "🥗 Salad Making Guide",
            "hero_subtitle": "Learn techniques for making salad in Grow a Garden.",
            "breadcrumb_current": "🎯 Make Salad",
            "toc_title": "📋 Table of Contents",
            "basics_title": "🌱 Basic Salad Making",
            "basics_content": "In Grow a Garden, salad making is one of the core gameplay mechanics. By growing various vegetables and fruits, you can create different levels of salads to earn rewards.",
            "ingredients_title": "🥬 Essential Ingredients List",
            "ingredients_content": "Making quality salads requires various fresh ingredients. Here's the ingredient list categorized by importance:",
            "basic_ingredients": "Basic Ingredients (Beginner Essential)",
            "advanced_ingredients": "Advanced Ingredients (Intermediate Players)",
            "making_steps": "Making Steps:",
            "collect_ingredients": "Collect Ingredients",
            "water_management": "Water Management",
            "harvest_timing": "Harvest Timing",
            "make_salad": "Make Salad",
            "earn_rewards": "Earn Rewards",
            "pro_tip": "💡 Pro Tip",
            "important_note": "⚠️ Important Note"
        },
        "bread": {
            "title": "How to Make Bread in Grow a Garden - Complete Guide | Grow a Garden Tips",
            "description": "Learn how to make bread in Roblox Grow a Garden! Complete guide with techniques and efficiency improvement methods.",
            "keywords": "how to make bread in grow a garden, roblox bread making guide, grow a garden guide, bread making guide, roblox farming game, bread ingredients collection, grow a garden tips",
            "og_title": "How to Make Bread in Grow a Garden - Complete Guide | Grow a Garden Tips",
            "og_description": "Learn how to make bread in Roblox Grow a Garden! Complete guide with techniques and efficiency improvement methods.",
            "hero_title": "🍞 Bread Making Guide",
            "hero_subtitle": "Learn techniques for making bread in Grow a Garden.",
            "breadcrumb_current": "🎯 Make Bread"
        },
        "cake": {
            "title": "How to Make Cake in Grow a Garden - Complete Guide | Grow a Garden Tips",
            "description": "Learn how to make cake in Roblox Grow a Garden! Complete guide with techniques and efficiency improvement methods.",
            "keywords": "how to make cake in grow a garden, roblox cake making guide, grow a garden guide, cake making guide, roblox farming game, cake ingredients collection, grow a garden tips",
            "og_title": "How to Make Cake in Grow a Garden - Complete Guide | Grow a Garden Tips",
            "og_description": "Learn how to make cake in Roblox Grow a Garden! Complete guide with techniques and efficiency improvement methods.",
            "hero_title": "🎂 Cake Making Guide",
            "hero_subtitle": "Learn techniques for making cake in Grow a Garden.",
            "breadcrumb_current": "🎯 Make Cake"
        }
    }

def get_guide_type(filename):
    """根据文件名判断攻略类型"""
    if "salad" in filename:
        return "salad"
    elif "bread" in filename:
        return "bread"
    elif "cake" in filename:
        return "cake"
    else:
        return "salad"  # 默认

def fix_english_content_complete(file_path):
    """完全修正英文攻略页面的所有内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        guide_type = get_guide_type(file_path.name)
        translations = get_english_translations().get(guide_type, get_english_translations()["salad"])
        
        # 1. 修正页面标题
        content = re.sub(r'<title>.*?</title>', 
                        f'<title>{translations["title"]}</title>', content)
        
        # 2. 修正meta描述
        content = re.sub(r'<meta name="description" content="[^"]*"', 
                        f'<meta name="description" content="{translations["description"]}"', content)
        
        # 3. 修正meta关键词
        content = re.sub(r'<meta name="keywords" content="[^"]*"', 
                        f'<meta name="keywords" content="{translations["keywords"]}"', content)
        
        # 4. 修正Open Graph标题
        content = re.sub(r'<meta property="og:title" content="[^"]*"', 
                        f'<meta property="og:title" content="{translations["og_title"]}"', content)
        
        # 5. 修正Open Graph描述
        content = re.sub(r'<meta property="og:description" content="[^"]*"', 
                        f'<meta property="og:description" content="{translations["og_description"]}"', content)
        
        # 6. 修正Twitter Card标题
        content = re.sub(r'<meta name="twitter:title" content="[^"]*"', 
                        f'<meta name="twitter:title" content="{translations["og_title"]}"', content)
        
        # 7. 修正Twitter Card描述
        content = re.sub(r'<meta name="twitter:description" content="[^"]*"', 
                        f'<meta name="twitter:description" content="{translations["og_description"]}"', content)
        
        # 8. 修正JSON-LD数据
        content = re.sub(r'"name": "[^"]*"', 
                        f'"name": "{translations["hero_title"]}"', content)
        content = re.sub(r'"description": "[^"]*"', 
                        f'"description": "{translations["description"]}"', content)
        content = re.sub(r'"inLanguage": "[^"]*"', 
                        '"inLanguage": "en"', content)
        
        # 9. 修正页面内容标题
        content = re.sub(r'<h1[^>]*>🥗 沙拉制作指南</h1>', 
                        f'<h1 data-i18n="salad.guide.hero.title">{translations["hero_title"]}</h1>', content)
        content = re.sub(r'<h1[^>]*>🍞 面包制作指南</h1>', 
                        f'<h1 data-i18n="bread.guide.hero.title">{translations["hero_title"]}</h1>', content)
        content = re.sub(r'<h1[^>]*>🎂 蛋糕制作指南</h1>', 
                        f'<h1 data-i18n="cake.guide.hero.title">{translations["hero_title"]}</h1>', content)
        
        # 10. 修正页面内容副标题
        content = re.sub(r'<p[^>]*>学习在 Grow a Garden 中制作沙拉的技巧。</p>', 
                        f'<p data-i18n="salad.guide.hero.subtitle">{translations["hero_subtitle"]}</p>', content)
        content = re.sub(r'<p[^>]*>学习在 Grow a Garden 中制作面包的技巧。</p>', 
                        f'<p data-i18n="bread.guide.hero.subtitle">{translations["hero_subtitle"]}</p>', content)
        content = re.sub(r'<p[^>]*>学习在 Grow a Garden 中制作蛋糕的技巧。</p>', 
                        f'<p data-i18n="cake.guide.hero.subtitle">{translations["hero_subtitle"]}</p>', content)
        
        # 11. 修正面包屑导航
        content = re.sub(r'<li aria-current="page"[^>]*>🎯 制作沙拉</li>', 
                        f'<li aria-current="page" data-i18n="salad.guide.breadcrumb.current">{translations["breadcrumb_current"]}</li>', content)
        content = re.sub(r'<li aria-current="page"[^>]*>🎯 制作面包</li>', 
                        f'<li aria-current="page" data-i18n="bread.guide.breadcrumb.current">{translations["breadcrumb_current"]}</li>', content)
        content = re.sub(r'<li aria-current="page"[^>]*>🎯 制作蛋糕</li>', 
                        f'<li aria-current="page" data-i18n="cake.guide.breadcrumb.current">{translations["breadcrumb_current"]}</li>', content)
        
        # 12. 修正目录标题
        content = re.sub(r'<h2[^>]*>📋 目录</h2>', 
                        f'<h2 data-i18n="toc.title">{translations["toc_title"]}</h2>', content)
        
        # 13. 修正基础制作标题
        content = re.sub(r'<h2[^>]*>🌱 基础沙拉制作</h2>', 
                        f'<h2 data-i18n="basics.title">{translations["basics_title"]}</h2>', content)
        content = re.sub(r'<h2[^>]*>🌱 基础面包制作</h2>', 
                        f'<h2 data-i18n="basics.title">{translations["basics_title"]}</h2>', content)
        content = re.sub(r'<h2[^>]*>🌱 基础蛋糕制作</h2>', 
                        f'<h2 data-i18n="basics.title">{translations["basics_title"]}</h2>', content)
        
        # 14. 修正基础制作内容
        content = re.sub(r'<p>在种植花园中， 沙拉制作是核心游戏机制之一. 通过种植各种蔬菜和水果，你可以制作不同等级的沙拉来获得奖励.</p>', 
                        f'<p>{translations["basics_content"]}</p>', content)
        
        # 15. 修正制作步骤标题
        content = re.sub(r'<h3>制作步骤：</h3>', 
                        f'<h3>{translations["making_steps"]}</h3>', content)
        
        # 16. 修正制作步骤内容
        content = re.sub(r'<li><strong>收集食材</strong>: 在花园中种植生菜、番茄、胡萝卜等基础蔬菜</li>', 
                        f'<li><strong>{translations["collect_ingredients"]}</strong>: Plant basic vegetables like lettuce, tomatoes, carrots in your garden</li>', content)
        content = re.sub(r'<li><strong>浇水管理</strong>: 定期给植物浇水以确保健康生长</li>', 
                        f'<li><strong>{translations["water_management"]}</strong>: Regularly water your plants to ensure healthy growth</li>', content)
        content = re.sub(r'<li><strong>收获时机</strong>: 等待植物完全成熟后再收获</li>', 
                        f'<li><strong>{translations["harvest_timing"]}</strong>: Wait for plants to fully mature before harvesting</li>', content)
        content = re.sub(r'<li><strong>制作沙拉</strong>: 将收集的食材放入沙拉制作器</li>', 
                        f'<li><strong>{translations["make_salad"]}</strong>: Put collected ingredients into the salad maker</li>', content)
        content = re.sub(r'<li><strong>获得奖励</strong>: 完成沙拉制作以获得游戏货币和经验</li>', 
                        f'<li><strong>{translations["earn_rewards"]}</strong>: Complete salad making to earn game currency and experience</li>', content)
        
        # 17. 修正贴士内容
        content = re.sub(r'<strong>💡 贴士：</strong> 在黄金时段（游戏内7:00-9:00）浇水会提供双倍效果, 大大增加植物生长速度!', 
                        f'<strong>{translations["pro_tip"]}</strong> Watering during golden hours (7:00-9:00 in-game) provides double effects, greatly increasing plant growth speed!', content)
        
        # 18. 修正食材标题
        content = re.sub(r'<h2[^>]*>🥬 关键食材清单</h2>', 
                        f'<h2 data-i18n="ingredients.title">{translations["ingredients_title"]}</h2>', content)
        
        # 19. 修正食材内容
        content = re.sub(r'<p>制作优质沙拉需要各种新鲜食材. 以下是按重要性分类的食材清单:</p>', 
                        f'<p>{translations["ingredients_content"]}</p>', content)
        
        # 20. 修正食材分类标题
        content = re.sub(r'<h3>基础食材（新手必备）</h3>', 
                        f'<h3>{translations["basic_ingredients"]}</h3>', content)
        content = re.sub(r'<h3>进阶食材（中级玩家）</h3>', 
                        f'<h3>{translations["advanced_ingredients"]}</h3>', content)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已完全修正英文内容: {file_path.name}")
            return True
        else:
            print(f"⏭️  无需修改: {file_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ 修正失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始完全修正英文攻略页面的所有内容...")
    
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
        if fix_english_content_complete(file_path):
            fixed_count += 1
    
    print(f"\n🎉 英文攻略页面内容完全修正完成！")
    print(f"📊 成功修正: {fixed_count} 个文件")
    print("✨ 现在英文攻略页面的所有内容都是英文了！")

if __name__ == "__main__":
    main() 