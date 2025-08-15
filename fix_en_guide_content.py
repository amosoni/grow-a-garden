#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接修正英文攻略页面的内容
将中文内容替换为英文
"""

import re
from pathlib import Path

def fix_english_guide_content(file_path):
    """修正英文攻略页面的内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 修正目录内容
        content = re.sub(r'<li><a href="#basics" data-i18n="basics\.toc\.basics">基础沙拉制作</a></li>', 
                        '<li><a href="#basics" data-i18n="basics.toc.basics">Basic Salad Making</a></li>', content)
        content = re.sub(r'<li><a href="#ingredients" data-i18n="ingredients\.toc\.ingredients">关键食材清单</a></li>', 
                        '<li><a href="#ingredients" data-i18n="ingredients.toc.ingredients">Essential Ingredients List</a></li>', content)
        content = re.sub(r'<li><a href="#recipes" data-i18n="recipes\.toc\.recipes">高级沙拉食谱</a></li>', 
                        '<li><a href="#recipes" data-i18n="recipes.toc.recipes">Advanced Salad Recipes</a></li>', content)
        content = re.sub(r'<li><a href="#efficiency" data-i18n="efficiency\.toc\.efficiency">效率提升方法</a></li>', 
                        '<li><a href="#efficiency" data-i18n="efficiency.toc.efficiency">Efficiency Improvement</a></li>', content)
        content = re.sub(r'<li><a href="#faq" data-i18n="faq\.toc\.faq">常见问题</a></li>', 
                        '<li><a href="#faq" data-i18n="faq.toc.faq">Frequently Asked Questions</a></li>', content)
        
        # 2. 修正基础制作标题
        content = re.sub(r'<h2 data-i18n="_基础沙拉制作\._基础沙拉制作\.title">🌱 基础沙拉制作</h2>', 
                        '<h2 data-i18n="guide.basics.title">🌱 Basic Salad Making</h2>', content)
        
        # 3. 修正基础制作内容
        content = re.sub(r'<p>在种植花园中， 沙拉制作是核心游戏机制之一. 通过种植各种蔬菜和水果，你可以制作不同等级的沙拉来获得奖励.</p>', 
                        '<p>In Grow a Garden, salad making is one of the core gameplay mechanics. By growing various vegetables and fruits, you can create different levels of salads to earn rewards.</p>', content)
        
        # 4. 修正制作步骤标题
        content = re.sub(r'<h3>制作步骤：</h3>', 
                        '<h3>Making Steps:</h3>', content)
        
        # 5. 修正制作步骤内容
        content = re.sub(r'<li><strong>收集食材</strong>: 在花园中种植生菜、番茄、胡萝卜等基础蔬菜</li>', 
                        '<li><strong>Collect Ingredients</strong>: Plant basic vegetables like lettuce, tomatoes, carrots in your garden</li>', content)
        content = re.sub(r'<li><strong>浇水管理</strong>: 定期给植物浇水以确保健康生长</li>', 
                        '<li><strong>Water Management</strong>: Regularly water your plants to ensure healthy growth</li>', content)
        content = re.sub(r'<li><strong>收获时机</strong>: 等待植物完全成熟后再收获</li>', 
                        '<li><strong>Harvest Timing</strong>: Wait for plants to fully mature before harvesting</li>', content)
        content = re.sub(r'<li><strong>制作沙拉</strong>: 将收集的食材放入沙拉制作器</li>', 
                        '<li><strong>Make Salad</strong>: Put collected ingredients into the salad maker</li>', content)
        content = re.sub(r'<li><strong>获得奖励</strong>: 完成沙拉制作以获得游戏货币和经验</li>', 
                        '<li><strong>Earn Rewards</strong>: Complete salad making to earn game currency and experience</li>', content)
        
        # 6. 修正贴士内容
        content = re.sub(r'<strong>💡 贴士：</strong> 在黄金时段（游戏内7:00-9:00）浇水会提供双倍效果, 大大增加植物生长速度!', 
                        '<strong>💡 Pro Tip</strong> Watering during golden hours (7:00-9:00 in-game) provides double effects, greatly increasing plant growth speed!', content)
        
        # 7. 修正食材标题
        content = re.sub(r'<h2 data-i18n="_关键食材清单\._关键食材清单\.title">🥬 关键食材清单</h2>', 
                        '<h2 data-i18n="guide.ingredients.title">🥬 Essential Ingredients List</h2>', content)
        
        # 8. 修正食材内容
        content = re.sub(r'<p>制作优质沙拉需要各种新鲜食材. 以下是按重要性分类的食材清单:</p>', 
                        '<p>Making quality salads requires various fresh ingredients. Here\'s the ingredient list categorized by importance:</p>', content)
        
        # 9. 修正食材分类标题
        content = re.sub(r'<h3>基础食材（新手必备）</h3>', 
                        '<h3>Basic Ingredients (Beginner Essential)</h3>', content)
        content = re.sub(r'<h3>进阶食材（中级玩家）</h3>', 
                        '<h3>Advanced Ingredients (Intermediate Players)</h3>', content)
        
        # 10. 修正食材描述
        content = re.sub(r'<p data-i18n="ingredient\.use">所有沙拉的基础食材</p>', 
                        '<p data-i18n="ingredient.use">Essential ingredient for all salads</p>', content)
        content = re.sub(r'<p data-i18n="ingredient\.use">提升沙拉营养价值</p>', 
                        '<p data-i18n="ingredient.use">Improves salad nutrition value</p>', content)
        content = re.sub(r'<p data-i18n="ingredient\.use">提升沙拉等级</p>', 
                        '<p data-i18n="ingredient.use">Improves salad level</p>', content)
        content = re.sub(r'<p data-i18n="ingredient\.use">增加水分含量</p>', 
                        '<p data-i18n="ingredient.use">Increases moisture content</p>', content)
        
        # 11. 修正食材名称
        content = re.sub(r'<h4>🥬 生菜</h4>', '<h4>🥬 Lettuce</h4>', content)
        content = re.sub(r'<h4>🍅 番茄</h4>', '<h4>🍅 Tomato</h4>', content)
        content = re.sub(r'<h4>🥕 胡萝卜</h4>', '<h4>🥕 Carrot</h4>', content)
        content = re.sub(r'<h4>🥒 黄瓜</h4>', '<h4>🥒 Cucumber</h4>', content)
        
        # 12. 修正食材描述
        content = re.sub(r'<p data-i18n="ingredient\.use"> 制作高级沙拉</p>', 
                        '<p data-i18n="ingredient.use">Making advanced salads</p>', content)
        content = re.sub(r'<p data-i18n="ingredient\.use"> 增加甜味和营养</p>', 
                        '<p data-i18n="ingredient.use">Adds sweetness and nutrition</p>', content)
        content = re.sub(r'<p data-i18n="ingredient\.use"> Making luxury salads</p>', 
                        '<p data-i18n="ingredient.use">Making luxury salads</p>', content)
        content = re.sub(r'<p data-i18n="ingredient\.use"> Improves salad quality</p>', 
                        '<p data-i18n="ingredient.use">Improves salad quality</p>', content)
        
        # 13. 修正食谱标题
        content = re.sub(r'<h3 data-i18n="recipes\.basic_salad\.title">基本沙拉食谱</h3>', 
                        '<h3 data-i18n="recipes.basic_salad.title">Basic Salad Recipes</h3>', content)
        
        # 14. 修正食材数量
        content = re.sub(r'<td data-i18n="ingredient\.lettuce\.quantity">生菜 x2</td>', 
                        '<td data-i18n="ingredient.lettuce.quantity">Lettuce x2</td>', content)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已修正英文内容: {file_path.name}")
            return True
        else:
            print(f"⏭️  无需修改: {file_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ 修正失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始直接修正英文攻略页面的内容...")
    
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
        if fix_english_guide_content(file_path):
            fixed_count += 1
    
    print(f"\n🎉 英文攻略页面内容修正完成！")
    print(f"📊 成功修正: {fixed_count} 个文件")
    print("✨ 现在英文攻略页面的内容都是英文了！")

if __name__ == "__main__":
    main() 