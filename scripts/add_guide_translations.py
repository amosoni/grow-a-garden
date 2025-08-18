#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为英文语言包添加攻略页面的翻译key
"""

def add_guide_translations():
    """添加攻略页面的翻译key到英文语言包"""
    
    # 要添加的翻译内容
    new_translations = '''
  // 攻略页面通用翻译
  "guide.toc.title": "📋 Table of Contents",
  "guide.basics.title": "🌱 Basic Making",
  "guide.ingredients.title": "🥬 Essential Ingredients",
  "guide.recipes.title": "🍳 Advanced Recipes",
  "guide.tips.title": "💡 Making Tips & Tricks",
  "guide.efficiency.title": "⚡ Efficiency Improvement",
  "guide.faq.title": "❓ Frequently Asked Questions",
  
  // 沙拉攻略专用翻译
  "salad.guide.hero.title": "🥗 Salad Making Guide",
  "salad.guide.hero.subtitle": "Learn techniques for making salad in Grow a Garden",
  "salad.guide.breadcrumb.current": "🎯 Make Salad",
  "salad.guide.basics.title": "🌱 Basic Salad Making",
  "salad.guide.ingredients.title": "🥬 Essential Ingredients List",
  "salad.guide.recipes.title": "🍳 Advanced Salad Recipes",
  "salad.guide.tips.title": "💡 Making Tips & Tricks",
  "salad.guide.efficiency.title": "⚡ Efficiency Improvement",
  "salad.guide.faq.title": "❓ Frequently Asked Questions",
  
  // 面包攻略专用翻译
  "bread.guide.hero.title": "🍞 Bread Making Guide",
  "bread.guide.hero.subtitle": "Learn techniques for making bread in Grow a Garden",
  "bread.guide.breadcrumb.current": "🎯 Make Bread",
  "bread.guide.basics.title": "🌱 Basic Bread Making",
  "bread.guide.ingredients.title": "🌾 Essential Ingredients List",
  "bread.guide.recipes.title": "🍞 Advanced Bread Recipes",
  
  // 蛋糕攻略专用翻译
  "cake.guide.hero.title": "🎂 Cake Making Guide",
  "cake.guide.hero.subtitle": "Learn techniques for making cake in Grow a Garden",
  "cake.guide.breadcrumb.current": "🎯 Make Cake",
  "cake.guide.basics.title": "🌱 Basic Cake Making",
  "cake.guide.ingredients.title": "🥚 Essential Ingredients List",
  "cake.guide.recipes.title": "🎂 Advanced Cake Recipes",
  
  // 制作步骤翻译
  "guide.making_steps.title": "Making Steps:",
  "guide.step.collect_ingredients": "Collect Ingredients",
  "guide.step.water_management": "Water Management",
  "guide.step.harvest_timing": "Harvest Timing",
  "guide.step.make_food": "Make Food",
  "guide.step.earn_rewards": "Earn Rewards",
  
  // 食材相关翻译
  "ingredient.use": "Essential ingredient for all recipes",
  "ingredient.lettuce.quantity": "Lettuce x2",
  "ingredient.tomato.quantity": "Tomato x1",
  "ingredient.carrot.quantity": "Carrot x1",
  "ingredient.cucumber.quantity": "Cucumber x1",
  
  // 效果相关翻译
  "effect.basic_nutrition": "Basic Nutrition",
  "effect.vitamin_rich": "Vitamin Rich",
  "effect.high_moisture": "High Moisture",
  "effect.antioxidant": "Antioxidant",
  "effect.fiber_rich": "Fiber Rich",
  "effect.immunity_boost": "Immunity Boost",
  "effect.metabolism_boost": "Metabolism Boost",
  "effect.vitamin_c_rich": "Vitamin C Rich",
  
  // 食谱相关翻译
  "recipes.basic_salad.title": "Basic Salad Recipes",
  "recipes.luxury_salad.title": "Luxury Salad Recipes",
  
  // 技巧相关翻译
  "tips.time_management.title": "Time Management Tips",
  "strategy.planting.title": "Planting Strategy",
  
  // 总结相关翻译
  "summary.bullet.learn_basic_making_techniques": "Learn basic making techniques",
  "summary.bullet.start_planting_advanced_ingredients": "Start planting advanced ingredients",
  "summary.bullet.participate_in_advanced_game_events": "Participate in advanced game events",
  "summary.bullet.start_planting_basic_ingredients": "Start planting basic ingredients",
  "summary.bullet.learn_basic_salad_recipes": "Learn basic salad recipes",
  "summary.bullet.join_player_communities": "Join player communities",
  "summary.bullet.participate_in_game_events": "Participate in game events",
  
  // 强调文本翻译
  "strong.time_investment": "Time Investment",
  
  // 长文本翻译
  "making_salads_is_the_core_gameplay_of_grow_a_garden._through_reasonable_planting_planning,_mastering_making_techniques,_and_participating_in_community_events,_you_can_become_a_salad_making_master": "Making salads is the core gameplay of Grow a Garden. Through reasonable planting planning, mastering making techniques, and participating in community events, you can become a salad making master!",
  
  // 货币和单位翻译
  "currency.coins": "Coins",
  "unit.kg": "kg",
  "unit.minutes": "minutes"
'''
    
    try:
        # 读取英文语言包
        with open('i18n/en.json', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 在最后一个大括号前插入新内容
        content = content.replace('}', new_translations + '\n}')
        
        # 写回文件
        with open('i18n/en.json', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ 已成功添加攻略页面翻译key到英文语言包")
        return True
        
    except Exception as e:
        print(f"❌ 添加翻译key失败: {e}")
        return False

if __name__ == "__main__":
    add_guide_translations() 