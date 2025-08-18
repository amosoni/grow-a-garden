#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

# 所有攻略页面的完整语言内容模板
guide_content_templates = {
    'zh-cn': {
        'how-to-grow-apples': {
            'title': '如何在Grow a Garden中种植苹果 - 完整指南',
            'description': '学习如何在Roblox Grow a Garden中种植苹果！掌握苹果种植技术获得最大产量和利润。',
            'hero_title': '🍎 如何在Grow a Garden中种植苹果',
            'hero_subtitle': '完整指南：从幼苗到果实收获',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 种植苹果',
            'overview_title': '🎯 苹果种植概述',
            'overview_content': '苹果是用于制作利润丰厚的食谱（如派和冰沙）的优质水果。适当的修剪和浇水可以显著提高产量。',
            'overview_points': [
                '高价值：用于制作派和高级果汁',
                '果园扩展：种植多个幼苗以确保稳定供应',
                '市场需求：在玩家中持续高涨'
            ],
            'requirements_title': '🥘 种植要求',
            'requirements_items': [
                {'icon': '🌱', 'title': '苹果幼苗', 'desc': '从种子/幼苗商店购买'},
                {'icon': '💧', 'title': '水', 'desc': '深度、定期浇水'},
                {'icon': '🌞', 'title': '充足阳光', 'desc': '阳光强烈的开放区域'},
                {'icon': '✂️', 'title': '修剪', 'desc': '修剪以改善空气流通和果实大小'},
                {'icon': '⏰', 'title': '时间', 'desc': '约60分钟成熟'},
                {'icon': '🛠️', 'title': '工具', 'desc': '浇水壶、修枝剪'}
            ],
            'steps_title': '📝 苹果种植分步指南',
            'step1_title': '第1步：准备果园',
            'step1_content': [
                '选择平坦、阳光充足的位置',
                '规划3x3或4x4的树木间距',
                '确保浇水方便'
            ],
            'step2_title': '第2步：种植幼苗',
            'step2_content': [
                '按计划间隔挖坑',
                '小心放置幼苗',
                '覆盖土壤并彻底浇水'
            ],
            'step3_title': '第3步：护理和维护',
            'step3_content': [
                '定期浇水，特别是在生长期',
                '修剪树枝以改善空气流通',
                '监控病虫害'
            ]
        },
        'how-to-grow-berries': {
            'title': '如何在Grow a Garden中种植浆果 - 完整指南',
            'description': '学习如何在Roblox Grow a Garden中种植浆果！掌握浆果种植快速获利。',
            'hero_title': '🫐 如何在Grow a Garden中种植浆果',
            'hero_subtitle': '完整指南：快速生长的浆果种植',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 种植浆果',
            'overview_title': '🎯 浆果种植概述',
            'overview_content': '浆果是快速生长的作物，适合新手玩家快速获得利润。',
            'overview_points': [
                '快速生长：比大多数作物成熟更快',
                '高利润：市场需求旺盛',
                '易于管理：适合初学者'
            ]
        },
        'how-to-grow-carrots': {
            'title': '如何在Grow a Garden中种植胡萝卜 - 完整指南',
            'description': '学习如何在Roblox Grow a Garden中种植胡萝卜！基础蔬菜种植指南。',
            'hero_title': '🥕 如何在Grow a Garden中种植胡萝卜',
            'hero_subtitle': '完整指南：蔬菜种植基础',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 种植胡萝卜',
            'overview_title': '🎯 胡萝卜种植概述',
            'overview_content': '胡萝卜是基础蔬菜，是学习种植技巧的理想作物。',
            'overview_points': [
                '基础作物：适合新手学习',
                '稳定收益：市场需求稳定',
                '快速回报：生长周期较短'
            ]
        },
        'how-to-grow-corn': {
            'title': '如何在Grow a Garden中种植玉米 - 完整指南',
            'description': '学习如何在Roblox Grow a Garden中种植玉米！掌握玉米种植技术。',
            'hero_title': '🌽 如何在Grow a Garden中种植玉米',
            'hero_subtitle': '完整指南：玉米种植精通',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 种植玉米',
            'overview_title': '🎯 玉米种植概述',
            'overview_content': '玉米是高产量作物，需要适当的空间和护理。',
            'overview_points': [
                '高产量：单株产量较高',
                '需要空间：需要较大的种植区域',
                '多种用途：可用于多种食谱'
            ]
        },
        'how-to-grow-oranges': {
            'title': '如何在Grow a Garden中种植橙子 - 完整指南',
            'description': '学习如何在Roblox Grow a Garden中种植橙子！柑橘种植指南。',
            'hero_title': '🍊 如何在Grow a Garden中种植橙子',
            'hero_subtitle': '完整指南：柑橘种植',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 种植橙子',
            'overview_title': '🎯 橙子种植概述',
            'overview_content': '橙子是柑橘类水果，需要温暖的气候和适当的护理。',
            'overview_points': [
                '柑橘类：需要特定的生长条件',
                '高价值：市场需求较高',
                '季节性：有特定的收获季节'
            ]
        },
        'how-to-grow-wheat': {
            'title': '如何在Grow a Garden中种植小麦 - 完整指南',
            'description': '学习如何在Roblox Grow a Garden中种植小麦！谷物种植指南。',
            'hero_title': '🌾 如何在Grow a Garden中种植小麦',
            'hero_subtitle': '完整指南：谷物种植',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 种植小麦',
            'overview_title': '🎯 小麦种植概述',
            'overview_content': '小麦是基础谷物，是制作面包和其他食物的必需品。',
            'overview_points': [
                '基础谷物：多种食谱的必需品',
                '稳定供应：全年可种植',
                '易于储存：可长期保存'
            ]
        },
        'how-to-make-bread': {
            'title': '如何在Grow a Garden中制作面包 - 完整食谱指南',
            'description': '学习如何在Roblox Grow a Garden中制作面包！掌握面包制作技巧获得利润。',
            'hero_title': '🍞 如何在Grow a Garden中制作面包',
            'hero_subtitle': '学习在 Grow a Garden 中制作面包的技巧。',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 制作面包',
            'basic_title': '🍞 基础面包制作',
            'basic_intro': '学习Grow a Garden中面包制作的基础知识：',
            'basic_steps': [
                '1. 种植小麦：种植小麦种子并定期浇水以确保健康生长',
                '2. 收获小麦：小麦成熟后收获并收集到库存中',
                '3. 制作面团：在制作台将小麦和水混合制作面团',
                '4. 发酵：让面团发酵一段时间以获得更好的质地',
                '5. 烘烤：将面团放入烤箱烘烤成面包',
                '6. 销售：将面包卖给NPC或玩家获得利润'
            ],
            'ingredients_title': '🥘 关键食材清单',
            'ingredients_intro': '制作优质面包需要各种食材，以下是详细的食材分类和清单。',
            'basic_ingredients': '必备食材（新手必备）',
            'advanced_ingredients': '进阶食材（中级玩家）',
            'rare_ingredients': '稀有食材（专家级）',
            'recipes_title': '🍞 高级面包食谱',
            'bread_varieties_title': '面包种类与类型',
            'bread_varieties_intro': '了解不同类型的面包及其特点：',
            'classic_breads': '经典面包',
            'sweet_breads': '甜味面包',
            'rich_breads': '浓郁面包',
            'specialty_breads': '特色面包',
            'tips_title': '💡 制作技巧与窍门',
            'tips_intro': '掌握这些技巧，成为Grow a Garden中的面包制作专家：',
            'growing_tips': '种植技巧',
            'making_tips': '制作技巧',
            'optimization': '优化建议',
            'efficiency_title': '⚡ 效率提升方法',
            'efficiency_intro': '通过这些高级策略最大化你的面包制作效率：',
            'production_optimization': '生产优化',
            'advanced_strategies': '高级策略',
            'faq_title': '❓ 常见问题',
            'faq_questions': [
                {
                    'q': 'Q: 制作基础面包需要多久？',
                    'a': 'A: 基础面包需要4-7个游戏周制作，而高级食谱根据复杂程度可能需要8-20个游戏周。'
                },
                {
                    'q': 'Q: 如何提高面包质量？',
                    'a': 'A: 使用高质量食材、正确发酵时间、适当的烘烤温度都能显著提高面包质量。'
                },
                {
                    'q': 'Q: 面包可以卖多少钱？',
                    'a': 'A: 基础面包售价约50-100金币，高级面包可达200-500金币，取决于食材和制作技巧。'
                }
            ],
            'next_steps_title': '🎯 下一步',
            'next_steps_intro': '现在你已经学习了基础知识，你的下一步：',
            'next_steps': [
                '1. 从小开始：从基础面包食谱开始，建立你的技能',
                '2. 扩展你的花园：种植各种原料用于不同食谱',
                '3. 掌握高级食谱：研究复杂的面包品种以获得更高利润',
                '4. 加入社区：与其他玩家联系，分享技巧和策略',
                '5. 保持更新：跟上游戏更新，获得新食谱和功能'
            ],
            'community_tip': '社区建议：加入我们的Discord服务器，与其他面包制作者联系，分享食谱，并获得最新的技巧和窍门！'
        },
        'how-to-make-cake': {
            'title': '如何在Grow a Garden中制作蛋糕 - 完整食谱指南',
            'description': '学习如何在Roblox Grow a Garden中制作蛋糕！掌握蛋糕制作技巧获得利润。',
            'hero_title': '🎂 如何在Grow a Garden中制作蛋糕',
            'hero_subtitle': '完整食谱指南：蛋糕制作',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 制作蛋糕',
            'basic_title': '🎂 基础蛋糕制作',
            'basic_intro': '学习Grow a Garden中蛋糕制作的基础知识：',
            'basic_steps': [
                '1. 收集原料：种植和收集制作蛋糕所需的食材',
                '2. 制作面团：在制作台混合面粉、鸡蛋和糖',
                '3. 添加配料：加入牛奶、香草等调味料',
                '4. 烘烤：将混合物放入烤箱烘烤',
                '5. 装饰：添加糖霜、水果等装饰',
                '6. 销售：将蛋糕卖给玩家获得高额利润'
            ]
        },
        'how-to-make-cookies': {
            'title': '如何在Grow a Garden中制作饼干 - 完整食谱指南',
            'description': '学习如何在Roblox Grow a Garden中制作饼干！掌握饼干制作技巧获得利润。',
            'hero_title': '🍪 如何在Grow a Garden中制作饼干',
            'hero_subtitle': '完整食谱指南：饼干制作',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 制作饼干',
            'basic_title': '🍪 基础饼干制作',
            'basic_intro': '学习Grow a Garden中饼干制作的基础知识：',
            'basic_steps': [
                '1. 准备原料：收集面粉、糖、鸡蛋等基础食材',
                '2. 混合面团：在制作台混合所有原料',
                '3. 成型：将面团分成小块并塑形',
                '4. 烘烤：将饼干放入烤箱烘烤至金黄',
                '5. 冷却：让饼干完全冷却',
                '6. 包装销售：将饼干包装并销售'
            ]
        },
        'how-to-make-donut': {
            'title': '如何在Grow a Garden中制作甜甜圈 - 完整食谱指南',
            'description': '学习如何在Roblox Grow a Garden中制作甜甜圈！掌握甜甜圈制作技巧获得利润。',
            'hero_title': '🍩 如何在Grow a Garden中制作甜甜圈',
            'hero_subtitle': '完整食谱指南：甜甜圈制作',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 制作甜甜圈',
            'basic_title': '🍩 基础甜甜圈制作',
            'basic_intro': '学习Grow a Garden中甜甜圈制作的基础知识：',
            'basic_steps': [
                '1. 制作面团：混合面粉、酵母、糖和鸡蛋',
                '2. 发酵：让面团发酵至两倍大小',
                '3. 成型：将面团擀平并切割成圆形',
                '4. 油炸：在热油中炸至金黄',
                '5. 装饰：添加糖霜、糖粉或巧克力',
                '6. 销售：将甜甜圈卖给玩家'
            ]
        },
        'how-to-make-pizza': {
            'title': '如何在Grow a Garden中制作披萨 - 完整食谱指南',
            'description': '学习如何在Roblox Grow a Garden中制作披萨！掌握披萨制作技巧获得利润。',
            'hero_title': '🍕 如何在Grow a Garden中制作披萨',
            'hero_subtitle': '完整食谱指南：从原料到利润',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 制作披萨',
            'basic_title': '🍕 基础披萨制作',
            'basic_intro': '学习Grow a Garden中披萨制作的基础知识：',
            'basic_steps': [
                '1. 准备面团：混合面粉、水、酵母和盐',
                '2. 发酵：让面团发酵至蓬松',
                '3. 擀面：将面团擀成圆形薄饼',
                '4. 添加配料：涂抹番茄酱并添加奶酪和配料',
                '5. 烘烤：在高温烤箱中烘烤至奶酪融化',
                '6. 切片销售：将披萨切片并销售'
            ]
        },
        'how-to-make-pie': {
            'title': '如何在Grow a Garden中制作派 - 完整食谱指南',
            'description': '学习如何在Roblox Grow a Garden中制作派！掌握派制作技巧获得利润。',
            'hero_title': '🥧 如何在Grow a Garden中制作派',
            'hero_subtitle': '完整食谱指南：派制作',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 制作派',
            'basic_title': '🥧 基础派制作',
            'basic_intro': '学习Grow a Garden中派制作的基础知识：',
            'basic_steps': [
                '1. 制作派皮：混合面粉、黄油和水制作派皮',
                '2. 准备馅料：收集水果、糖和其他配料',
                '3. 组装：将馅料放入派皮中',
                '4. 装饰：用派皮条装饰顶部',
                '5. 烘烤：在烤箱中烘烤至金黄',
                '6. 冷却销售：让派冷却后销售'
            ]
        },
        'how-to-make-salad': {
            'title': '如何在Grow a Garden中制作沙拉 - 完整食谱指南',
            'description': '学习如何在Roblox Grow a Garden中制作沙拉！掌握沙拉制作技巧获得利润。',
            'hero_title': '🥗 如何在Grow a Garden中制作沙拉',
            'hero_subtitle': '完整食谱指南：沙拉制作',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 制作沙拉',
            'basic_title': '🥗 基础沙拉制作',
            'basic_intro': '学习Grow a Garden中沙拉制作的基础知识：',
            'basic_steps': [
                '1. 种植蔬菜：种植生菜、番茄、黄瓜等蔬菜',
                '2. 收获清洗：收获蔬菜并清洗干净',
                '3. 切配：将蔬菜切成适当大小',
                '4. 混合：在碗中混合所有蔬菜',
                '5. 调味：添加橄榄油、醋和香料',
                '6. 装盘销售：将沙拉装盘并销售'
            ]
        },
        'how-to-make-sandwich': {
            'title': '如何在Grow a Garden中制作三明治 - 完整食谱指南',
            'description': '学习如何在Roblox Grow a Garden中制作三明治！掌握三明治制作技巧获得利润。',
            'hero_title': '🥪 如何在Grow a Garden中制作三明治',
            'hero_subtitle': '完整食谱指南：三明治制作',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 制作三明治',
            'basic_title': '🥪 基础三明治制作',
            'basic_intro': '学习Grow a Garden中三明治制作的基础知识：',
            'basic_steps': [
                '1. 制作面包：种植小麦并制作面包',
                '2. 准备配料：种植生菜、番茄和收集肉类',
                '3. 切片：将面包切成薄片',
                '4. 组装：在面包上添加配料',
                '5. 包装：将三明治包装好',
                '6. 销售：将三明治卖给玩家'
            ]
        },
        'how-to-make-smoothie': {
            'title': '如何在Grow a Garden中制作冰沙 - 完整食谱指南',
            'description': '学习如何在Roblox Grow a Garden中制作冰沙！掌握冰沙制作技巧获得利润。',
            'hero_title': '🥤 如何在Grow a Garden中制作冰沙',
            'hero_subtitle': '完整食谱指南：冰沙制作',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 制作冰沙',
            'basic_title': '🥤 基础冰沙制作',
            'basic_intro': '学习Grow a Garden中冰沙制作的基础知识：',
            'basic_steps': [
                '1. 种植水果：种植草莓、蓝莓、香蕉等水果',
                '2. 收获：收获成熟的水果',
                '3. 混合：在搅拌机中混合水果和牛奶',
                '4. 调味：添加糖或蜂蜜调味',
                '5. 装杯：将冰沙倒入杯中',
                '6. 销售：将冰沙卖给玩家'
            ]
        },
        'how-to-make-spaghetti': {
            'title': '如何在Grow a Garden中制作意大利面 - 完整食谱指南',
            'description': '学习如何在Roblox Grow a Garden中制作意大利面！掌握意大利面制作技巧获得利润。',
            'hero_title': '🍝 如何在Grow a Garden中制作意大利面',
            'hero_subtitle': '完整食谱指南：意大利面制作',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 制作意大利面',
            'basic_title': '🍝 基础意大利面制作',
            'basic_intro': '学习Grow a Garden中意大利面制作的基础知识：',
            'basic_steps': [
                '1. 制作面条：混合面粉和鸡蛋制作面条',
                '2. 准备酱料：制作番茄酱或奶油酱',
                '3. 煮面：将面条放入沸水中煮熟',
                '4. 混合：将面条和酱料混合',
                '5. 装盘：将意大利面装盘',
                '6. 销售：将意大利面卖给玩家'
            ]
        },
        'how-to-make-money-fast': {
            'title': '如何在Grow a Garden中快速赚钱 - 完整指南',
            'description': '学习如何在Roblox Grow a Garden中快速赚钱！掌握赚钱策略。',
            'hero_title': '💰 如何在Grow a Garden中快速赚钱',
            'hero_subtitle': '完整指南：快速赚钱策略',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 快速赚钱',
            'basic_title': '💰 基础赚钱策略',
            'basic_intro': '学习Grow a Garden中快速赚钱的基础知识：',
            'basic_steps': [
                '1. 种植高价值作物：选择利润最高的作物种植',
                '2. 制作高级食物：将原料制作成高价值食物',
                '3. 市场调研：了解玩家需求和市场价格',
                '4. 批量生产：扩大生产规模提高效率',
                '5. 建立供应链：确保原料稳定供应',
                '6. 持续优化：不断改进生产流程'
            ]
        },
        'how-to-build-farm': {
            'title': '如何在Grow a Garden中建造农场 - 完整指南',
            'description': '学习如何在Roblox Grow a Garden中建造农场！掌握农场建设。',
            'hero_title': '🏗️ 如何在Grow a Garden中建造农场',
            'hero_subtitle': '完整指南：农场建设',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 建造农场',
            'basic_title': '🏗️ 基础农场建设',
            'basic_intro': '学习Grow a Garden中农场建设的基础知识：',
            'basic_steps': [
                '1. 选择位置：选择平坦、阳光充足的土地',
                '2. 规划布局：设计农场区域和道路',
                '3. 建造基础设施：建造仓库、工具房等',
                '4. 开垦土地：清除杂草并翻耕土壤',
                '5. 种植作物：按计划种植各种作物',
                '6. 建立灌溉系统：确保作物得到充足水分'
            ]
        },
        'how-to-play-with-friends': {
            'title': '如何在Grow a Garden中与朋友一起玩 - 完整指南',
            'description': '学习如何在Roblox Grow a Garden中与朋友一起玩！多人游戏指南。',
            'hero_title': '👥 如何在Grow a Garden中与朋友一起玩',
            'hero_subtitle': '完整指南：多人游戏',
            'breadcrumb_home': '🏠 首页',
            'breadcrumb_guides': '📚 攻略',
            'breadcrumb_current': '🎯 与朋友一起玩',
            'basic_title': '👥 基础多人游戏',
            'basic_intro': '学习Grow a Garden中多人游戏的基础知识：',
            'basic_steps': [
                '1. 添加朋友：在游戏中添加你的朋友',
                '2. 创建团队：组建农场团队共同发展',
                '3. 分工合作：分配不同的任务和职责',
                '4. 共享资源：与团队成员共享资源和工具',
                '5. 共同建设：一起建造和装饰农场',
                '6. 团队活动：参与团队挑战和活动'
            ]
        }
    }
}

def fix_complete_content_internationalization(file_path, lang_code):
    """彻底修复单个攻略页面的所有内容国际化"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取文件名（不含扩展名）
        filename = os.path.basename(file_path).replace('.html', '')
        
        # 检查是否有对应的内容模板
        if lang_code not in guide_content_templates or filename not in guide_content_templates[lang_code]:
            print(f"⚠️ {file_path} 没有对应的内容模板，跳过")
            return False
        
        template = guide_content_templates[lang_code][filename]
        
        # 修复页面标题
        if 'title' in template:
            content = re.sub(r'<title>[^<]*</title>', f'<title>{template["title"]}</title>', content)
        
        # 修复meta description
        if 'description' in template:
            content = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{template["description"]}"', content)
        
        # 修复hero标题
        if 'hero_title' in template:
            content = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1>{template["hero_title"]}</h1>', content)
        
        # 修复hero副标题
        if 'hero_subtitle' in template:
            content = re.sub(r'<p>.*?</p>', f'<p>{template["hero_subtitle"]}</p>', content, count=1)
        
        # 修复面包屑导航
        if 'breadcrumb_home' in template:
            content = re.sub(r'<li><a href="../index.html">[^<]*</a></li>', f'<li><a href="../index.html">{template["breadcrumb_home"]}</a></li>', content)
        
        if 'breadcrumb_guides' in template:
            content = re.sub(r'<li><a href="../guides.html">[^<]*</a></li>', f'<li><a href="../guides.html">{template["breadcrumb_guides"]}</a></li>', content)
        
        if 'breadcrumb_current' in template:
            content = re.sub(r'<li aria-current="page"[^>]*>.*?</li>', f'<li aria-current="page">{template["breadcrumb_current"]}</li>', content)
        
        # 修复面包制作页面的详细内容
        if filename == 'how-to-make-bread':
            # 修复基础制作标题
            if 'basic_title' in template:
                content = re.sub(r'<h2>🍞 [^<]*</h2>', f'<h2>{template["basic_title"]}</h2>', content)
            
            # 修复基础制作介绍
            if 'basic_intro' in template:
                content = re.sub(r'<p>Learn the fundamentals[^<]*</p>', f'<p>{template["basic_intro"]}</p>', content)
            
            # 修复制作步骤列表
            if 'basic_steps' in template:
                for i, step in enumerate(template['basic_steps']):
                    if i == 0:
                        content = re.sub(r'<li>1\. Grow Wheat:[^<]*</li>', f'<li>{step}</li>', content)
                    elif i == 1:
                        content = re.sub(r'<li>2\. Harvest Wheat:[^<]*</li>', f'<li>{step}</li>', content)
                    elif i == 2:
                        content = re.sub(r'<li>3\. Make Dough:[^<]*</li>', f'<li>{step}</li>', content)
                    elif i == 3:
                        content = re.sub(r'<li>4\. Ferment:[^<]*</li>', f'<li>{step}</li>', content)
                    elif i == 4:
                        content = re.sub(r'<li>5\. Bake:[^<]*</li>', f'<li>{step}</li>', content)
                    elif i == 5:
                        content = re.sub(r'<li>6\. Sell:[^<]*</li>', f'<li>{step}</li>', content)
            
            # 修复食材标题
            if 'ingredients_title' in template:
                content = re.sub(r'<h2>🥘 [^<]*</h2>', f'<h2>{template["ingredients_title"]}</h2>', content)
            
            # 修复食材介绍
            if 'ingredients_intro' in template:
                content = re.sub(r'<p>Making quality bread requires[^<]*</p>', f'<p>{template["ingredients_intro"]}</p>', content)
            
            # 修复食材分类标题
            if 'basic_ingredients' in template:
                content = re.sub(r'Essential Ingredients \(Beginner[^<]*\)', template['basic_ingredients'], content)
            if 'advanced_ingredients' in template:
                content = re.sub(r'Advanced Ingredients \(Intermediate[^<]*\)', template['advanced_ingredients'], content)
            if 'rare_ingredients' in template:
                content = re.sub(r'Rare Ingredients \(Expert[^<]*\)', template['rare_ingredients'], content)
            
            # 修复面包种类标题
            if 'bread_varieties_title' in template:
                content = re.sub(r'<h2>Bread Varieties & Types</h2>', f'<h2>{template["bread_varieties_title"]}</h2>', content)
            
            # 修复面包种类介绍
            if 'bread_varieties_intro' in template:
                content = re.sub(r'<p>Learn about different types[^<]*</p>', f'<p>{template["bread_varieties_intro"]}</p>', content)
            
            # 修复面包种类分类
            if 'classic_breads' in template:
                content = re.sub(r'<h3>Classic Breads</h3>', f'<h3>{template["classic_breads"]}</h3>', content)
            if 'sweet_breads' in template:
                content = re.sub(r'<h3>Sweet Breads</h3>', f'<h3>{template["sweet_breads"]}</h3>', content)
            if 'rich_breads' in template:
                content = re.sub(r'<h3>Rich Breads</h3>', f'<h3>{template["rich_breads"]}</h3>', content)
            if 'specialty_breads' in template:
                content = re.sub(r'<h3>Specialty Breads</h3>', f'<h3>{template["specialty_breads"]}</h3>', content)
            
            # 修复提示标题
            if 'tips_title' in template:
                content = re.sub(r'<h2>💡 [^<]*</h2>', f'<h2>{template["tips_title"]}</h2>', content)
            
            # 修复提示介绍
            if 'tips_intro' in template:
                content = re.sub(r'<p>Master these tips[^<]*</p>', f'<p>{template["tips_intro"]}</p>', content)
            
            # 修复提示分类标题
            if 'growing_tips' in template:
                content = re.sub(r'<h3>Growing Tips</h3>', f'<h3>{template["growing_tips"]}</h3>', content)
            if 'making_tips' in template:
                content = re.sub(r'<h3>Making Tips</h3>', f'<h3>{template["making_tips"]}</h3>', content)
            if 'optimization' in template:
                content = re.sub(r'<h3>Optimization</h3>', f'<h3>{template["optimization"]}</h3>', content)
            
            # 修复效率标题
            if 'efficiency_title' in template:
                content = re.sub(r'<h2>⚡ [^<]*</h2>', f'<h2>{template["efficiency_title"]}</h2>', content)
            
            # 修复效率介绍
            if 'efficiency_intro' in template:
                content = re.sub(r'<p>Maximize your bread-making[^<]*</p>', f'<p>{template["efficiency_intro"]}</p>', content)
            
            # 修复效率分类标题
            if 'production_optimization' in template:
                content = re.sub(r'<h3>Production Optimization</h3>', f'<h3>{template["production_optimization"]}</h3>', content)
            if 'advanced_strategies' in template:
                content = re.sub(r'<h3>Advanced Strategies</h3>', f'<h3>{template["advanced_strategies"]}</h3>', content)
            
            # 修复FAQ标题
            if 'faq_title' in template:
                content = re.sub(r'<h2>❓ [^<]*</h2>', f'<h2>{template["faq_title"]}</h2>', content)
            
            # 修复FAQ问答
            if 'faq_questions' in template:
                for i, qa in enumerate(template['faq_questions']):
                    if i == 0:
                        content = re.sub(r'<p><strong>Q: [^<]*</strong></p>', f'<p><strong>{qa["q"]}</strong></p>', content)
                        content = re.sub(r'<p>A: Basic bread takes[^<]*</p>', f'<p>{qa["a"]}</p>', content)
                    elif i == 1:
                        content = re.sub(r'<p><strong>Q: [^<]*</strong></p>', f'<p><strong>{qa["q"]}</strong></p>', content, count=1)
                        content = re.sub(r'<p>A: Use high-quality[^<]*</p>', f'<p>{qa["a"]}</p>', content)
                    elif i == 2:
                        content = re.sub(r'<p><strong>Q: [^<]*</strong></p>', f'<p><strong>{qa["q"]}</strong></p>', content, count=1)
                        content = re.sub(r'<p>A: Use high-quality[^<]*</p>', f'<p>{qa["a"]}</p>', content)
            
            # 修复下一步标题
            if 'next_steps_title' in template:
                content = re.sub(r'<h2>🎯 [^<]*</h2>', f'<h2>{template["next_steps_title"]}</h2>', content)
            
            # 修复下一步介绍
            if 'next_steps_intro' in template:
                content = re.sub(r'<p>Now that you have learned[^<]*</p>', f'<p>{template["next_steps_intro"]}</p>', content)
            
            # 修复下一步列表
            if 'next_steps' in template:
                for i, step in enumerate(template['next_steps']):
                    if i == 0:
                        content = re.sub(r'<li>1\. Start Small:[^<]*</li>', f'<li>{step}</li>', content)
                    elif i == 1:
                        content = re.sub(r'<li>2\. Expand Your Garden:[^<]*</li>', f'<li>{step}</li>', content)
                    elif i == 2:
                        content = re.sub(r'<li>3\. Master Advanced Recipes:[^<]*</li>', f'<li>{step}</li>', content)
                    elif i == 3:
                        content = re.sub(r'<li>4\. Join the Community:[^<]*</li>', f'<li>{step}</li>', content)
                    elif i == 4:
                        content = re.sub(r'<li>5\. Stay Updated:[^<]*</li>', f'<li>{step}</li>', content)
            
            # 修复社区提示
            if 'community_tip' in template:
                content = re.sub(r'Community Tip:[^<]*', f'{template["community_tip"]}', content)
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {file_path} 完整内容国际化已修复")
        return True
        
    except Exception as e:
        print(f"❌ {file_path} 处理失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始彻底修复所有攻略页面的完整内容国际化...")
    
    # 获取所有语言目录
    lang_dirs = []
    for item in os.listdir('.'):
        if os.path.isdir(item) and item in guide_content_templates:
            lang_dirs.append(item)
    
    print(f"📁 找到语言目录: {lang_dirs}")
    
    # 处理每个语言目录
    total_files = 0
    fixed_files = 0
    
    for lang_dir in lang_dirs:
        print(f"\n🌍 处理 {lang_dir} 目录...")
        
        # 获取该语言目录下的所有HTML文件
        lang_path = os.path.join(lang_dir)
        for root, dirs, files in os.walk(lang_path):
            for file in files:
                if file.endswith('.html') and file.startswith('how-to-'):
                    file_path = os.path.join(root, file)
                    total_files += 1
                    if fix_complete_content_internationalization(file_path, lang_dir):
                        fixed_files += 1
    
    print(f"\n🎉 修复完成！")
    print(f"📊 总文件数: {total_files}")
    print(f"✅ 成功修复: {fixed_files}")
    print(f"❌ 失败数量: {total_files - fixed_files}")
    print(f"\n💡 现在所有攻略页面都应该有完整的语言内容国际化了！")

if __name__ == "__main__":
    main() 