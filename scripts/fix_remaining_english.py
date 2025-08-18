#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译攻略页面中剩余的英文内容
确保所有内容都使用对应语言
"""

import re
from pathlib import Path

def get_remaining_translations():
    """获取剩余需要翻译的内容"""
    return {
        "zh-cn": {
            "Making Tips & Tricks": "制作技巧与窍门",
            "salad making is one of the core gameplay mechanics": "沙拉制作是核心游戏机制之一",
            "By growing various vegetables and fruits, you can create different levels of salads to earn rewards": "通过种植各种蔬菜和水果，你可以制作不同等级的沙拉来获得奖励",
            "Plant basic vegetables like lettuce, tomatoes, carrots in your garden": "在花园中种植生菜、番茄、胡萝卜等基础蔬菜",
            "Regularly water your plants to ensure healthy growth": "定期给植物浇水以确保健康生长",
            "Wait for plants to fully mature before harvesting": "等待植物完全成熟后再收获",
            "Put collected ingredients into the salad maker": "将收集的食材放入沙拉制作器",
            "Complete salad making to earn game currency and experience": "完成沙拉制作以获得游戏货币和经验",
            "Watering during golden hours (7:00-9:00 in-game) provides double effects": "在黄金时段（游戏内7:00-9:00）浇水会提供双倍效果",
            "greatly increasing plant growth speed": "大大增加植物生长速度",
            "Making quality salads requires various fresh ingredients": "制作优质沙拉需要各种新鲜食材",
            "Here's the ingredient list categorized by importance": "以下是按重要性分类的食材清单",
            "基础食材（新手必备）": "基础食材（新手必备）",
            "进阶食材（中级玩家）": "进阶食材（中级玩家）",
            "Making advanced salads": "制作高级沙拉",
            "Adds sweetness and nutrition": "增加甜味和营养",
            "Lettuce": "生菜",
            "Tomato": "番茄",
            "Carrot": "胡萝卜",
            "Cucumber": "黄瓜",
            "Avocado": "牛油果",
            "Strawberry": "草莓",
            "Corn": "玉米"
        },
        "ja": {
            "Making Tips & Tricks": "制作のコツとテクニック",
            "salad making is one of the core gameplay mechanics": "サラダ作りはコアゲームプレイメカニクスの一つです",
            "By growing various vegetables and fruits, you can create different levels of salads to earn rewards": "様々な野菜や果物を育てることで、異なるレベルのサラダを作って報酬を獲得できます",
            "Plant basic vegetables like lettuce, tomatoes, carrots in your garden": "庭にレタス、トマト、ニンジンなどの基本的な野菜を植えましょう",
            "Regularly water your plants to ensure healthy growth": "植物の健康な成長のために定期的に水やりをしましょう",
            "Wait for plants to fully mature before harvesting": "収穫する前に植物が完全に成熟するまで待ちましょう",
            "Put collected ingredients into the salad maker": "収集した材料をサラダメーカーに入れましょう",
            "Complete salad making to earn game currency and experience": "サラダ作りを完了してゲーム通貨と経験値を獲得しましょう",
            "Watering during golden hours (7:00-9:00 in-game) provides double effects": "ゴールデンアワー（ゲーム内7:00-9:00）に水やりすると二倍の効果があります",
            "greatly increasing plant growth speed": "植物の成長速度が大幅に向上します",
            "Making quality salads requires various fresh ingredients": "質の高いサラダを作るには様々な新鮮な材料が必要です",
            "Here's the ingredient list categorized by importance": "重要性別に分類された材料リストは以下の通りです",
            "Basic Ingredients (Beginner Essential)": "基本材料（初心者必須）",
            "Advanced Ingredients (Intermediate Players)": "上級材料（中級プレイヤー）",
            "Making advanced salads": "上級サラダの制作",
            "Adds sweetness and nutrition": "甘さと栄養を追加",
            "Lettuce": "レタス",
            "Tomato": "トマト", 
            "Carrot": "ニンジン",
            "Cucumber": "キュウリ",
            "Avocado": "アボカド",
            "Strawberry": "イチゴ",
            "Corn": "トウモロコシ"
        }
    }

def apply_remaining_translations(file_path, language_code):
    """应用剩余的翻译"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        translations = get_remaining_translations()
        
        if language_code not in translations:
            return False
        
        translation = translations[language_code]
        
        # 应用所有翻译
        for english, translated in translation.items():
            content = content.replace(english, translated)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已应用 {language_code} 剩余翻译: {file_path.name}")
            return True
        else:
            print(f"⏭️  无需修改: {file_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ 应用翻译失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始翻译攻略页面中剩余的英文内容...")
    
    language_mapping = {"zh-cn": "zh-cn", "ja": "ja"}
    total_translated = 0
    
    for lang_dir, lang_code in language_mapping.items():
        lang_path = Path(lang_dir)
        if not lang_path.exists():
            continue
            
        print(f"\n🔧 正在处理语言目录: {lang_dir}")
        
        guide_files = []
        for pattern in ['how-to-*.html', '*-guide.html', '*-strategies.html', '*-basics.html', '*-tips.html']:
            guide_files.extend(lang_path.glob(pattern))
        
        if not guide_files:
            continue
        
        print(f"   📁 找到 {len(guide_files)} 个攻略页面")
        
        for file_path in guide_files:
            if apply_remaining_translations(file_path, lang_code):
                total_translated += 1
    
    print(f"\n🎉 剩余英文内容翻译完成！")
    print(f"📊 成功翻译: {total_translated} 个文件")

if __name__ == "__main__":
    main() 