#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补齐所有新键的翻译内容
"""

import os
import json
import re
import glob
from pathlib import Path

def create_comprehensive_translations():
    """创建全面的翻译内容"""
    translations = {
        'zh-cn': {
            # 食材名称
            'ingredient.mushroom.name': '蘑菇',
            'ingredient.chili_pepper.name': '辣椒',
            'ingredient.grape.name': '葡萄',
            'ingredient.mango.name': '芒果',
            
            # 食材用途
            'ingredient.use.making_special_salads': '用途：制作特殊沙拉',
            'ingredient.use.making_spicy_salads': '用途：制作辣味沙拉',
            'ingredient.use.making_sweet_salads': '用途：制作甜味沙拉',
            'ingredient.use.making_tropical_salads': '用途：制作热带沙拉',
            
            # 食谱标题
            'recipes.basic.title': '基本食谱',
            'recipes.advanced.title': '高级食谱',
            'recipes.luxury.title': '豪华食谱',
            
            # 沙拉名称
            'salad.basic_lemon.name': '基本柠檬沙拉',
            'salad.vegetable.name': '蔬菜沙拉',
            'salad.fresh.name': '新鲜沙拉',
            'salad.avocado.name': '牛油果沙拉',
            'salad.fruit.name': '水果沙拉',
            'salad.corn.name': '玉米沙拉',
            'salad.mushroom.name': '蘑菇沙拉',
            'salad.spicy.name': '辣味沙拉',
            'salad.tropical.name': '热带沙拉',
            
            # 食材数量
            'ingredient.lettuce.quantity': '生菜 x1',
            'ingredient.tomato.quantity': '番茄 x2',
            'ingredient.carrot.quantity': '胡萝卜 x2',
            'ingredient.cucumber.quantity': '黄瓜 x1',
            'ingredient.avocado.quantity': '牛油果 x1',
            'ingredient.strawberry.quantity': '草莓 x3',
            'ingredient.corn.quantity': '玉米 x2',
            'ingredient.broccoli.quantity': '西兰花 x1',
            
            # 时间单位
            'time.minutes': '分钟',
            
            # 货币单位
            'currency.coins': '金币',
            
            # 效果描述
            'effect.basic_nutrition': '基本营养',
            'effect.vitamin_rich': '维生素丰富',
            'effect.high_moisture': '高水分',
            'effect.healthy_body': '健康身体',
            'effect.antioxidant': '抗氧化',
            'effect.fiber_rich': '纤维丰富',
            'effect.immunity_boost': '免疫力提升',
            'effect.metabolism_boost': '新陈代谢提升',
            'effect.vitamin_c_rich': '维生素C丰富',
            
            # 提示标题
            'tip.time_management_tips.title': '时间管理技巧',
            'tip.planting_strategy.title': '种植策略',
            'tip.resource_management.title': '资源管理',
            
            # 提示标签
            'tip.staggered_planting.label': '错峰种植:',
            'tip.batch_making.label': '批量制作:',
            'tip.golden_hours.label': '黄金时段:',
            'tip.daily_login.label': '每日登录:',
            'tip.priority_planting.label': '优先种植:',
            'tip.upgrade_tools.label': '升级工具:',
            'tip.friend_cooperation.label': '好友合作:',
            'tip.event_participation.label': '参与活动:',
            
            # FAQ 问题
            'faq.how_to_quickly_earn_more_coins.question': 'Q: 如何快速赚取更多金币？',
            'faq.why_are_my_plants_growing_slowly.question': 'Q: 为什么我的植物生长缓慢？',
            'faq.where_to_get_rare_ingredients.question': 'Q: 在哪里获得稀有食材？',
            'faq.how_to_make_the_highest_level_salads.question': 'Q: 如何制作最高等级的沙拉？',
            'faq.what_if_salad_making_fails.question': 'Q: 如果沙拉制作失败怎么办？',
            'faq.how_to_cooperate_with_other_players.question': 'Q: 如何与其他玩家合作？',
            
            # FAQ 答案
            'faq.how_to_quickly_earn_more_coins.answer': 'A: 通过制作高价值沙拉和参与活动来快速赚取金币。',
            'faq.why_are_my_plants_growing_slowly.answer': 'A: 检查浇水频率和土壤质量，确保在黄金时段种植。',
            'faq.where_to_get_rare_ingredients.answer': 'A: 稀有食材通常在特殊事件或高级种子包中获得。',
            'faq.how_to_make_the_highest_level_salads.answer': 'A: 使用稀有食材组合，并确保所有食材都是最高品质。',
            'faq.what_if_salad_making_fails.question': 'A: 失败是学习的一部分，尝试不同的食材组合。',
            'faq.how_to_cooperate_with_other_players.answer': 'A: 加入玩家社区，参与合作活动和交易。',
            
            # 总结
            'summary.start_planting_basic_ingredients': '开始种植基本食材',
            'summary.learn_basic_salad_recipes': '学习基本沙拉食谱',
            'summary.join_player_communities': '加入玩家社区',
            'summary.participate_in_game_events': '参与游戏活动',
            
            # 总结要点
            'summary.bullet.start_planting_basic_ingredients': '开始种植基本食材',
            'summary.bullet.learn_basic_salad_recipes': '学习基本沙拉食谱',
            'summary.bullet.join_player_communities': '加入玩家社区',
            'summary.bullet.participate_in_game_events': '参与游戏活动',
            
            # 页脚
            'footer.copyright': '© 2023 种植花园 - 实时玩家追踪器',
            'footer.disclaimer': '非官方。数据仅供参考。'
        },
        
        'ja': {
            # 食材名称
            'ingredient.mushroom.name': 'マッシュルーム',
            'ingredient.chili_pepper.name': 'チリペッパー',
            'ingredient.grape.name': 'ブドウ',
            'ingredient.mango.name': 'マンゴー',
            
            # 食材用途
            'ingredient.use.making_special_salads': '用途：特別なサラダ作り',
            'ingredient.use.making_spicy_salads': '用途：スパイシーなサラダ作り',
            'ingredient.use.making_sweet_salads': '用途：甘いサラダ作り',
            'ingredient.use.making_tropical_salads': '用途：トロピカルなサラダ作り',
            
            # 食谱标题
            'recipes.basic.title': '基本レシピ',
            'recipes.advanced.title': '上級レシピ',
            'recipes.luxury.title': '高級レシピ',
            
            # 沙拉名称
            'salad.basic_lemon.name': '基本レモンサラダ',
            'salad.vegetable.name': '野菜サラダ',
            'salad.fresh.name': 'フレッシュサラダ',
            'salad.avocado.name': 'アボカドサラダ',
            'salad.fruit.name': 'フルーツサラダ',
            'salad.corn.name': 'コーンサラダ',
            'salad.mushroom.name': 'マッシュルームサラダ',
            'salad.spicy.name': 'スパイシーサラダ',
            'salad.tropical.name': 'トロピカルサラダ',
            
            # 食材数量
            'ingredient.lettuce.quantity': 'レタス x1',
            'ingredient.tomato.quantity': 'トマト x2',
            'ingredient.carrot.quantity': 'ニンジン x2',
            'ingredient.cucumber.quantity': 'キュウリ x1',
            'ingredient.avocado.quantity': 'アボカド x1',
            'ingredient.strawberry.quantity': 'イチゴ x3',
            'ingredient.corn.quantity': 'トウモロコシ x2',
            'ingredient.broccoli.quantity': 'ブロッコリー x1',
            
            # 时间单位
            'time.minutes': '分',
            
            # 货币单位
            'currency.coins': 'コイン',
            
            # 效果描述
            'effect.basic_nutrition': '基本栄養',
            'effect.vitamin_rich': 'ビタミン豊富',
            'effect.high_moisture': '水分多め',
            'effect.healthy_body': '健康な体',
            'effect.antioxidant': '抗酸化',
            'effect.fiber_rich': '食物繊維豊富',
            'effect.immunity_boost': '免疫力向上',
            'effect.metabolism_boost': '代謝向上',
            'effect.vitamin_c_rich': 'ビタミンC豊富',
            
            # 提示标题
            'tip.time_management_tips.title': '時間管理のコツ',
            'tip.planting_strategy.title': '植え付け戦略',
            'tip.resource_management.title': '資源管理',
            
            # 提示标签
            'tip.staggered_planting.label': '段階的植え付け:',
            'tip.batch_making.label': '一括制作:',
            'tip.golden_hours.label': 'ゴールデンアワー:',
            'tip.daily_login.label': '毎日ログイン:',
            'tip.priority_planting.label': '優先植え付け:',
            'tip.upgrade_tools.label': 'ツールアップグレード:',
            'tip.friend_cooperation.label': 'フレンド協力:',
            'tip.event_participation.label': 'イベント参加:',
            
            # FAQ 问题
            'faq.how_to_quickly_earn_more_coins.question': 'Q: より多くのコインを素早く稼ぐには？',
            'faq.why_are_my_plants_growing_slowly.question': 'Q: なぜ私の植物はゆっくり成長するの？',
            'faq.where_to_get_rare_ingredients.question': 'Q: レアな食材はどこで入手できますか？',
            'faq.how_to_make_the_highest_level_salads.question': 'Q: 最高レベルのサラダはどうやって作りますか？',
            'faq.what_if_salad_making_fails.question': 'Q: サラダ作りが失敗したらどうしますか？',
            'faq.how_to_cooperate_with_other_players.question': 'Q: 他のプレイヤーとどう協力しますか？',
            
            # FAQ 答案
            'faq.how_to_quickly_earn_more_coins.answer': 'A: 高価値のサラダを作ったり、イベントに参加したりしてコインを素早く稼ぎましょう。',
            'faq.why_are_my_plants_growing_slowly.answer': 'A: 水やりの頻度と土の質を確認し、ゴールデンアワーに植え付けましょう。',
            'faq.where_to_get_rare_ingredients.answer': 'A: レアな食材は通常、特別なイベントや上級シードパックで入手できます。',
            'faq.how_to_make_the_highest_level_salads.answer': 'A: レアな食材の組み合わせを使用し、すべての食材が最高品質であることを確認してください。',
            'faq.what_if_salad_making_fails.question': 'A: 失敗は学習の一部です。異なる食材の組み合わせを試してみてください。',
            'faq.how_to_cooperate_with_other_players.answer': 'A: プレイヤーコミュニティに参加し、協力活動や取引に参加しましょう。',
            
            # 总结
            'summary.start_planting_basic_ingredients': '基本食材の植え付けを始める',
            'summary.learn_basic_salad_recipes': '基本サラダレシピを学ぶ',
            'summary.join_player_communities': 'プレイヤーコミュニティに参加する',
            'summary.participate_in_game_events': 'ゲームイベントに参加する',
            
            # 总结要点
            'summary.bullet.start_planting_basic_ingredients': '基本食材の植え付けを始める',
            'summary.bullet.learn_basic_salad_recipes': '基本サラダレシピを学ぶ',
            'summary.bullet.join_player_communities': 'プレイヤーコミュニティに参加する',
            'summary.bullet.participate_in_game_events': 'ゲームイベントに参加する',
            
            # 页脚
            'footer.copyright': '© 2023 ガーデン栽培 - リアルタイムプレイヤートラッカー',
            'footer.disclaimer': '非公式。データは参考用です。'
        }
    }
    
    return translations

def update_language_file_with_comprehensive_translations(lang_file_path, comprehensive_translations):
    """用全面翻译更新语言文件"""
    try:
        with open(lang_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    # 获取语言代码
    lang = lang_file_path.stem
    
    if lang not in comprehensive_translations:
        print(f"⚠️ 跳过 {lang_file_path} - 未找到翻译")
        return False
    
    # 更新翻译
    updated = False
    for key, translation in comprehensive_translations[lang].items():
        if key in data and data[key].startswith('['):
            data[key] = translation
            updated = True
    
    if updated:
        # 按键排序
        sorted_data = dict(sorted(data.items()))
        
        # 写入文件
        with open(lang_file_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 全面翻译更新: {lang_file_path}")
        return True
    
    return False

def main():
    """主函数"""
    print("🚀 开始补齐所有新键的翻译内容...")
    
    # 创建全面翻译
    comprehensive_translations = create_comprehensive_translations()
    
    # 获取所有语言文件
    i18n_dir = Path("i18n")
    lang_files = list(i18n_dir.glob("*.json"))
    lang_files = [f for f in lang_files if not f.name.startswith(('en', 'fr_base', 'fr_clean', 'fr_temp', 'de_backup'))]
    
    print(f"找到 {len(lang_files)} 个语言文件")
    
    # 为每个语言文件应用全面翻译
    updated_count = 0
    for lang_file in lang_files:
        if update_language_file_with_comprehensive_translations(lang_file, comprehensive_translations):
            updated_count += 1
    
    print(f"\n🎉 完成！更新了 {updated_count} 个语言文件")
    print("现在所有攻略详情页都有了完整的本地化内容！")
    print("\n注意：目前只完成了中文和日语的翻译，其他语言需要类似处理")

if __name__ == "__main__":
    main() 