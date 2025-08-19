#!/usr/bin/env python3
"""
为所有语言创建新的攻略页面：
1. Flower Type Plants (花卉类植物种植)
2. How to Make Spaghetti (意大利面制作)
"""

import os
import re

# 网站支持的所有语言
LANGUAGES = {
    'en': 'English',
    'zh-cn': '简体中文',
    'es': 'Español',
    'pt-br': 'Português',
    'fr': 'Français',
    'de': 'Deutsch',
    'ru': 'Русский',
    'ar': 'العربية',
    'hi': 'हिन्दी',
    'id': 'Bahasa Indonesia',
    'vi': 'Tiếng Việt',
    'ja': '日本語'
}

# 页面内容模板
FLOWER_PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="{lang_code}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <link rel="canonical" href="https://growagarden.cv/{lang_path}/flower-type-plants.html">
    
    <!-- Open Graph for social sharing -->
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{og_description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://growagarden.cv/{lang_path}/flower-type-plants.html">
    <meta property="og:image" content="https://growagarden.cv/flower-guide-og.jpg">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{twitter_title}">
    <meta name="twitter:description" content="{twitter_description}">
    <meta name="twitter:image" content="https://growagarden.cv/flower-guide-og.jpg">
    
    <!-- Structured Data JSON-LD -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "HowTo",
      "name": "{json_name}",
      "description": "{json_description}",
      "image": "https://growagarden.cv/flower-guide-og.jpg",
      "url": "https://growagarden.cv/{lang_path}/flower-type-plants.html",
      "inLanguage": "{lang_code}",
      "step": [
        {{
          "@type": "HowToStep",
          "name": "{step1_name}",
          "text": "{step1_text}"
        }},
        {{
          "@type": "HowToStep", 
          "name": "{step2_name}",
          "text": "{step2_text}"
        }},
        {{
          "@type": "HowToStep",
          "name": "{step3_name}",
          "text": "{step3_text}"
        }}
      ]
    }}
    </script>
    
    <!-- Roblox-like color scheme -->
    <link rel="stylesheet" href="https://unpkg.com/simple.css@2.1.0/simple.min.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
    <link rel="stylesheet" href="../styles.css">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌸</text></svg>">
    
    <style>
        body {{
            position: relative;
            min-height: 100vh;
            overflow-x: hidden;
        }}
        .bg-blur {{
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: 0;
            background: url('../grow-bg.jpg') center center/cover no-repeat;
            opacity: 0.3;
            filter: blur(2px);
            pointer-events: none;
        }}
        .content-wrapper {{
            position: relative;
            z-index: 1;
        }}
        .flower-hero {{
            background: linear-gradient(135deg, #ff69b4, #da70d6);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
            margin-top: 60px;
            margin-bottom: 2rem;
            position: relative;
        }}
        .flower-hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.2);
            z-index: 1;
        }}
        .flower-hero h1,
        .flower-hero p {{
            position: relative;
            z-index: 2;
        }}
        .flower-hero h1 {{
            font-size: 3rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .flower-hero p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        .guide-section {{
            background: rgba(255, 255, 255, 0.95);
            margin: 2rem;
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }}
        .flower-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }}
        .flower-card {{
            background: white;
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .flower-card:hover {{
            transform: translateY(-5px);
        }}
        .flower-card h3 {{
            color: #ff69b4;
            margin-bottom: 1rem;
        }}
        .profit-info {{
            background: linear-gradient(135deg, #32cd32, #228b22);
            color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }}
        .tips-section {{
            background: linear-gradient(135deg, #ffd700, #ffa500);
            color: #333;
            padding: 1.5rem;
            border-radius: 1rem;
            margin: 2rem 0;
        }}
        .tips-section h3 {{
            color: #8b4513;
            margin-bottom: 1rem;
        }}
        .tips-list {{
            list-style: none;
            padding: 0;
        }}
        .tips-list li {{
            padding: 0.5rem 0;
            border-bottom: 1px solid rgba(139, 69, 19, 0.2);
        }}
        .tips-list li:last-child {{
            border-bottom: none;
        }}
        .tips-list li::before {{
            content: "🌸 ";
            margin-right: 0.5rem;
        }}
    </style>
</head>
<body>
    <div class="bg-blur"></div>
    <div class="content-wrapper">
        <header>
            <nav>
                <a href="#" class="logo" data-i18n="nav.logo">{nav_logo}</a>
                <a href="javascript:void(0)" onclick="scrollToSection('stats')" data-i18n="nav.live">{nav_live}</a>
                <a href="javascript:void(0)" onclick="scrollToSection('map')" data-i18n="nav.map">{nav_map}</a>
                <a href="javascript:void(0)" onclick="scrollToSection('tips')" data-i18n="nav.tips">{nav_tips}</a>
                <a href="guides.html" data-i18n="nav.guides">📚 {nav_guides}</a>
                <a href="javascript:void(0)" onclick="scrollToSection('online')" data-i18n="nav.online">🎮 {nav_online}</a>
                <a href="javascript:void(0)" onclick="scrollToSection('community')" class="discord-btn" data-i18n="nav.discord">💬 Discord</a>
                <div class="flag-language-switcher">
                    <div class="current-flag" id="current-flag">
                        <img src="{current_flag_src}" alt="{current_flag_alt}">
                    </div>
                    <div class="flag-dropdown" id="flag-dropdown">
                        {flag_options}
                    </div>
                </div>
            </nav>
        </header>

        <section class="flower-hero">
            <h1>🌸 {hero_title}</h1>
            <p>{hero_subtitle}</p>
        </section>

        <div class="guide-section">
            <h2>🌺 {why_grow_title}</h2>
            <p>{why_grow_desc}</p>
            
            <div class="profit-info">
                <h3>💰 {profit_title}</h3>
                <p>{profit_desc}</p>
            </div>

            <div class="flower-grid">
                <div class="flower-card">
                    <h3>🌹 {rose_title}</h3>
                    <p><strong>{growth_time}:</strong> {rose_growth_time}</p>
                    <p><strong>{base_value}:</strong> {rose_base_value}</p>
                    <p><strong>{best_season}:</strong> {rose_best_season}</p>
                    <p><strong>{special_features}:</strong> {rose_special}</p>
                </div>

                <div class="flower-card">
                    <h3>🌻 {sunflower_title}</h3>
                    <p><strong>{growth_time}:</strong> {sunflower_growth_time}</p>
                    <p><strong>{base_value}:</strong> {sunflower_base_value}</p>
                    <p><strong>{best_season}:</strong> {sunflower_best_season}</p>
                    <p><strong>{special_features}:</strong> {sunflower_special}</p>
                </div>

                <div class="flower-card">
                    <h3>🌷 {tulip_title}</h3>
                    <p><strong>{growth_time}:</strong> {tulip_growth_time}</p>
                    <p><strong>{base_value}:</strong> {tulip_base_value}</p>
                    <p><strong>{best_season}:</strong> {tulip_best_season}</p>
                    <p><strong>{special_features}:</strong> {tulip_special}</p>
                </div>

                <div class="flower-card">
                    <h3>🌼 {daisy_title}</h3>
                    <p><strong>{growth_time}:</strong> {daisy_growth_time}</p>
                    <p><strong>{base_value}:</strong> {daisy_base_value}</p>
                    <p><strong>{best_season}:</strong> {daisy_best_season}</p>
                    <p><strong>{special_features}:</strong> {daisy_special}</p>
                </div>

                <div class="flower-card">
                    <h3>🌺 {lily_title}</h3>
                    <p><strong>{growth_time}:</strong> {lily_growth_time}</p>
                    <p><strong>{base_value}:</strong> {lily_base_value}</p>
                    <p><strong>{best_season}:</strong> {lily_best_season}</p>
                    <p><strong>{special_features}:</strong> {lily_special}</p>
                </div>

                <div class="flower-card">
                    <h3>🌸 {cherry_blossom_title}</h3>
                    <p><strong>{growth_time}:</strong> {cherry_blossom_growth_time}</p>
                    <p><strong>{base_value}:</strong> {cherry_blossom_base_value}</p>
                    <p><strong>{best_season}:</strong> {cherry_blossom_best_season}</p>
                    <p><strong>{special_features}:</strong> {cherry_blossom_special}</p>
                </div>
            </div>
        </div>

        <div class="guide-section">
            <h2>🌱 {strategies_title}</h2>
            
            <h3>1. {soil_prep_title}</h3>
            <p>{soil_prep_desc}</p>
            
            <h3>2. {watering_title}</h3>
            <p>{watering_desc}</p>
            
            <h3>3. {spacing_title}</h3>
            <p>{spacing_desc}</p>
            
            <h3>4. {pest_title}</h3>
            <p>{pest_desc}</p>
        </div>

        <div class="tips-section">
            <h3>💡 {pro_tips_title}</h3>
            <ul class="tips-list">
                {tips_list}
            </ul>
        </div>

        <div class="guide-section">
            <h2>🎯 {advanced_title}</h2>
            
            <h3>{mutation_title}</h3>
            <p>{mutation_desc}</p>
            
            <h3>{seasonal_title}</h3>
            <p>{seasonal_desc}</p>
            
            <h3>{market_title}</h3>
            <p>{market_desc}</p>
        </div>

        <div class="guide-section">
            <h2>🚀 {getting_started_title}</h2>
            <ol>
                {getting_started_steps}
            </ol>
        </div>
    </div>

    <script src="../script.js"></script>
    <script src="../i18n/i18n.js"></script>
    <script>
        // 国旗语言切换器功能
        document.addEventListener('DOMContentLoaded', function() {{
            const currentFlag = document.getElementById('current-flag');
            const flagDropdown = document.getElementById('flag-dropdown');
            const flagOptions = document.querySelectorAll('.flag-option');
            
            // 点击当前国旗显示/隐藏下拉菜单
            if (currentFlag) {{
                currentFlag.addEventListener('click', function() {{
                    flagDropdown.classList.toggle('open');
                }});
            }}
            
            // 点击国旗选项切换语言
            flagOptions.forEach(option => {{
                option.addEventListener('click', function() {{
                    const lang = this.getAttribute('data-lang');
                    const flagImg = this.querySelector('img').src;
                    const flagName = this.querySelector('.flag-name').textContent;
                    
                    // 更新当前显示的国旗
                    const currentFlagImg = currentFlag.querySelector('img');
                    currentFlagImg.src = flagImg;
                    
                    // 关闭下拉菜单
                    flagDropdown.classList.remove('open');
                    
                    // 重定向到对应语言页面
                    if (lang === 'en') {{
                        window.location.href = '/en/flower-type-plants.html';
                    }} else {{
                        window.location.href = '/' + lang + '/flower-type-plants.html';
                    }}
                }});
            }}
            
            // 点击外部关闭下拉菜单
            document.addEventListener('click', function(event) {{
                if (!event.target.closest('.flag-language-switcher')) {{
                    flagDropdown.classList.remove('open');
                }}
            }});
        }});
    </script>
</body>
</html>'''

def get_flag_options():
    """获取所有国旗选项的HTML"""
    flag_options = []
    for lang_code, lang_name in LANGUAGES.items():
        # 这里需要根据实际的文件路径调整
        flag_src = f"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5MDAgNjAwIj4KICAgICAgICAgICAgPHJlY3Qgd2lkdGg9IjkwMCIgaGVpZ2h0PSI2MDAiIGZpbGw9IiNmZmYiLz4KICAgICAgICA8L3N2Zz4="
        
        flag_option = f'''<div class="flag-option" data-lang="{lang_code}" title="{lang_name}">
            <img src="{flag_src}" alt="{lang_code} Flag">
            <span class="flag-name">{lang_name}</span>
        </div>'''
        flag_options.append(flag_option)
    
    return '\n                        '.join(flag_options)

def get_translations(lang_code):
    """获取指定语言的翻译"""
    if lang_code == 'en':
        return {
            'title': 'Flower Type Plants in Grow a Garden - Complete Growing Guide | Grow a Garden Tips',
            'description': 'Master flower type plants in Roblox Grow a Garden! Learn about rose cultivation, sunflower farming, tulip growing, and all flower plant strategies for maximum profit and beauty.',
            'keywords': 'flower type plants grow a garden, roblox flower farming, grow a garden flower guide, rose cultivation, sunflower farming, tulip growing, flower plant strategies, roblox gardening tips',
            'og_title': 'Flower Type Plants in Grow a Garden - Complete Growing Guide',
            'og_description': 'Master flower type plants in Roblox Grow a Garden! Learn about rose cultivation, sunflower farming, tulip growing, and all flower plant strategies.',
            'twitter_title': 'Flower Type Plants in Grow a Garden - Complete Growing Guide',
            'twitter_description': 'Master flower type plants in Roblox Grow a Garden! Learn about rose cultivation, sunflower farming, tulip growing.',
            'json_name': 'Flower Type Plants in Grow a Garden',
            'json_description': 'Master flower type plants in Roblox Grow a Garden, including rose cultivation, sunflower farming, tulip growing, and all flower plant strategies for maximum profit.',
            'step1_name': 'Choose Flower Types',
            'step1_text': 'Select the best flower types for your garden based on climate and profit potential',
            'step2_name': 'Prepare Soil',
            'step2_text': 'Ensure proper soil conditions and fertilization for optimal flower growth',
            'step3_name': 'Plant and Care',
            'step3_text': 'Plant flowers with proper spacing and maintain regular watering and care',
            'nav_logo': '🌱 Grow a Garden',
            'nav_live': 'Live Stats',
            'nav_map': 'Global Heatmap',
            'nav_tips': 'Tips',
            'nav_guides': 'Guides',
            'nav_online': 'Online',
            'hero_title': 'Flower Type Plants in Grow a Garden',
            'hero_subtitle': 'Master the art of growing beautiful and profitable flowers in Roblox\'s most popular farming game!',
            'why_grow_title': 'Why Grow Flower Type Plants?',
            'why_grow_desc': 'Flower type plants in Grow a Garden offer unique advantages that make them essential for any serious farmer:',
            'profit_title': 'High Profit Potential',
            'profit_desc': 'Flowers often have higher base values and can fetch premium prices in the market, especially during special events and seasonal demand.',
            'growth_time': 'Growth Time',
            'base_value': 'Base Value',
            'best_season': 'Best Season',
            'special_features': 'Special Features',
            'rose_title': 'Roses',
            'rose_growth_time': '2-3 hours',
            'rose_base_value': '$150-300',
            'rose_best_season': 'Spring/Summer',
            'rose_special': 'High demand for romantic events, can be used in bouquets',
            'sunflower_title': 'Sunflowers',
            'sunflower_growth_time': '1-2 hours',
            'sunflower_base_value': '$100-200',
            'sunflower_best_season': 'Summer',
            'sunflower_special': 'Fast growth, high yield, attracts bees',
            'tulip_title': 'Tulips',
            'tulip_growth_time': '2-4 hours',
            'tulip_base_value': '$120-250',
            'tulip_best_season': 'Spring',
            'tulip_special': 'Multiple color variants, seasonal bonus',
            'daisy_title': 'Daisies',
            'daisy_growth_time': '1-1.5 hours',
            'daisy_base_value': '$80-150',
            'daisy_best_season': 'Spring/Summer',
            'daisy_special': 'Very fast growth, beginner-friendly',
            'lily_title': 'Lilies',
            'lily_growth_time': '3-4 hours',
            'lily_base_value': '$200-400',
            'lily_best_season': 'Summer',
            'lily_special': 'High-end market, luxury item',
            'cherry_blossom_title': 'Cherry Blossoms',
            'cherry_blossom_growth_time': '4-6 hours',
            'cherry_blossom_base_value': '$300-600',
            'cherry_blossom_best_season': 'Spring',
            'cherry_blossom_special': 'Rare, extremely high value, event-exclusive',
            'strategies_title': 'Growing Strategies for Flower Type Plants',
            'soil_prep_title': 'Soil Preparation',
            'soil_prep_desc': 'Flowers require well-draining, nutrient-rich soil. Use premium fertilizer and ensure proper pH levels for optimal growth.',
            'watering_title': 'Watering Schedule',
            'watering_desc': 'Flowers need consistent moisture but avoid overwatering. Implement a drip irrigation system for best results.',
            'spacing_title': 'Spacing and Layout',
            'spacing_desc': 'Proper spacing prevents disease and ensures adequate sunlight. Use grid patterns for efficient harvesting.',
            'pest_title': 'Pest Management',
            'pest_desc': 'Flowers attract beneficial insects but can also attract pests. Use natural pest control methods when possible.',
            'pro_tips_title': 'Pro Tips for Flower Farming',
            'tips_list': '''<li>Plant flowers in batches to ensure continuous harvest throughout the season</li>
                <li>Use companion planting with herbs to naturally repel pests</li>
                <li>Save your highest-quality flowers for special events and premium markets</li>
                <li>Experiment with different flower combinations for unique bouquets</li>
                <li>Monitor market trends to plant the most profitable flowers</li>
                <li>Use greenhouses to extend the growing season for high-value flowers</li>
                <li>Network with other players to learn about rare flower varieties</li>
                <li>Keep detailed records of growth times and yields for optimization</li>''',
            'advanced_title': 'Advanced Flower Farming Techniques',
            'mutation_title': 'Mutation Breeding',
            'mutation_desc': 'Cross-pollinate different flower varieties to create rare mutations with unique colors and higher values.',
            'seasonal_title': 'Seasonal Optimization',
            'seasonal_desc': 'Plan your flower planting calendar to maximize profits during peak demand periods.',
            'market_title': 'Market Timing',
            'market_desc': 'Study market patterns to sell flowers when demand is highest and prices are at their peak.',
            'getting_started_title': 'Getting Started with Flower Farming',
            'getting_started_steps': '''<li><strong>Choose Your Flowers:</strong> Start with fast-growing, high-demand flowers like daisies and sunflowers</li>
                <li><strong>Prepare Your Garden:</strong> Set up proper soil, irrigation, and pest control systems</li>
                <li><strong>Plant in Stages:</strong> Stagger your planting to ensure continuous harvest</li>
                <li><strong>Monitor Growth:</strong> Keep track of growth times and adjust your schedule accordingly</li>
                <li><strong>Harvest and Sell:</strong> Time your harvests for maximum profit and market demand</li>
                <li><strong>Expand Gradually:</strong> As you gain experience, add more complex and valuable flower varieties</li>''',
            'current_flag_src': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NDAgNDgwIj4KICAgICAgICAgICAgPGRlZnM+PGNsaXBQYXRoIGlkPSJhIj48cGF0aCBkPSJNLTg1LjMgMGg2ODIuNnY1MTJILTg1LjN6Ii8+PC9jbGlwUGF0aD48L2RlZnM+CiAgICAgICAgICAgIDxjbGlwUGF0aCBpZD0iYiI+PHVzZSBocmVmPSIjYSIvPjwvY2xpcFBhdGg+CiAgICAgICAgICAgIDxnIGNsaXAtcGF0aD0idXJsKCNiKSIgdHJhbnNmb3JtPSJzY2FsZSguOTM3NSkiPgogICAgICAgICAgICAgICAgPGcgZmlsbC1ydWxlPSJldmVub2RkIiBzdHJva2Utd2lkdGg9IjFwdCI+CiAgICAgICAgICAgICAgICAgICAgPHBhdGggZD0iTS0yNTYgMEg3Njh2NTEySC0yNTZ6IiBmaWxsPSIjYmQzZDQ0Ii8+CiAgICAgICAgICAgICAgICAgICAgPHBhdGggZD0iTS0yNTYgMEg3Njh2MTAyLjRILTI1NnoiIGZpbGw9IiNmZmYiLz4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBkPSJNLTI1NiAxMDIuNEg3Njh2MTAyLjRILTI1NnoiIGZpbGw9IiNmZmYiLz4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBkPSJNLTI1NiAyMDQuOEg3Njh2MTAyLjRILTI1NnoiIGZpbGw9IiNmZmYiLz4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBkPSJNLTI1NiAzMDcuMkg3Njh2MTAyLjRILTI1NnoiIGZpbGw9IiNmZmYiLz4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBkPSJNLTI1NiA0MDkuNkg3NjhWNTEySC0yNTZ6IiBmaWxsPSIjZmZmIi8+CiAgICAgICAgICAgICAgICA8L2c+CiAgICAgICAgICAgICAgICA8ZyBmaWxsPSIjMTkyZjVkIj4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBkPSJNLTI1NiAwdjUxMmwyNTYtMjU2eiIvPgogICAgICAgICAgICAgICAgPC9nPgogICAgICAgICAgICA8L2c+CiAgICAgICAgPC9zdmc+',
            'current_flag_alt': 'en Flag'
        }
    elif lang_code == 'zh-cn':
        return {
            'title': 'Grow a Garden 花卉类植物种植完全指南 | 种植花园攻略',
            'description': '掌握Roblox Grow a Garden中花卉类植物的种植技巧！学习玫瑰栽培、向日葵种植、郁金香培育等所有花卉植物策略，实现最大利润和美观效果。',
            'keywords': 'flower type plants grow a garden, roblox花卉种植, grow a garden花卉指南, 玫瑰栽培, 向日葵种植, 郁金香培育, 花卉植物策略, roblox园艺技巧',
            'og_title': 'Grow a Garden 花卉类植物种植完全指南',
            'og_description': '掌握Roblox Grow a Garden中花卉类植物的种植技巧！学习玫瑰栽培、向日葵种植、郁金香培育等所有花卉植物策略。',
            'twitter_title': 'Grow a Garden 花卉类植物种植完全指南',
            'twitter_description': '掌握Roblox Grow a Garden中花卉类植物的种植技巧！学习玫瑰栽培、向日葵种植、郁金香培育。',
            'json_name': 'Grow a Garden 花卉类植物种植完全指南',
            'json_description': '掌握Roblox Grow a Garden中花卉类植物的种植技巧，包括玫瑰栽培、向日葵种植、郁金香培育等所有花卉植物策略，实现最大利润。',
            'step1_name': '选择花卉类型',
            'step1_text': '根据气候和利润潜力选择最适合您花园的花卉类型',
            'step2_name': '准备土壤',
            'step2_text': '确保适当的土壤条件和施肥，实现最佳花卉生长',
            'step3_name': '种植和护理',
            'step3_text': '以适当的间距种植花卉，保持定期浇水和护理',
            'nav_logo': '🌱 种植花园',
            'nav_live': '实时统计',
            'nav_map': '全球热力图',
            'nav_tips': '技巧',
            'nav_guides': '攻略',
            'nav_online': '在线',
            'hero_title': 'Grow a Garden 花卉类植物种植完全指南',
            'hero_subtitle': '掌握Roblox最受欢迎的农场游戏中美丽且有利可图的花卉种植艺术！',
            'why_grow_title': '为什么要种植花卉类植物？',
            'why_grow_desc': 'Grow a Garden中的花卉类植物为任何认真的农民提供独特的优势，使它们成为必不可少的：',
            'profit_title': '高利润潜力',
            'profit_desc': '花卉通常具有更高的基础价值，在市场上可以获得溢价，特别是在特殊活动和季节性需求期间。',
            'growth_time': '生长时间',
            'base_value': '基础价值',
            'best_season': '最佳季节',
            'special_features': '特殊功能',
            'rose_title': '玫瑰',
            'rose_growth_time': '2-3小时',
            'rose_base_value': '$150-300',
            'rose_best_season': '春季/夏季',
            'rose_special': '浪漫活动需求高，可用于制作花束',
            'sunflower_title': '向日葵',
            'sunflower_growth_time': '1-2小时',
            'sunflower_base_value': '$100-200',
            'sunflower_best_season': '夏季',
            'sunflower_special': '生长快速，产量高，吸引蜜蜂',
            'tulip_title': '郁金香',
            'tulip_growth_time': '2-4小时',
            'tulip_base_value': '$120-250',
            'tulip_best_season': '春季',
            'tulip_special': '多种颜色变体，季节性奖励',
            'daisy_title': '雏菊',
            'daisy_growth_time': '1-1.5小时',
            'daisy_base_value': '$80-150',
            'daisy_best_season': '春季/夏季',
            'daisy_special': '生长非常快速，适合初学者',
            'lily_title': '百合',
            'lily_growth_time': '3-4小时',
            'lily_base_value': '$200-400',
            'lily_best_season': '夏季',
            'lily_special': '高端市场，奢侈品',
            'cherry_blossom_title': '樱花',
            'cherry_blossom_growth_time': '4-6小时',
            'cherry_blossom_base_value': '$300-600',
            'cherry_blossom_best_season': '春季',
            'cherry_blossom_special': '稀有，极高价值，活动专属',
            'strategies_title': '花卉类植物种植策略',
            'soil_prep_title': '土壤准备',
            'soil_prep_desc': '花卉需要排水良好、营养丰富的土壤。使用优质肥料并确保适当的pH值以实现最佳生长。',
            'watering_title': '浇水时间表',
            'watering_desc': '花卉需要持续的水分，但要避免过度浇水。实施滴灌系统以获得最佳效果。',
            'spacing_title': '间距和布局',
            'spacing_desc': '适当的间距可以防止疾病并确保充足的阳光。使用网格模式进行高效收获。',
            'pest_title': '害虫管理',
            'pest_desc': '花卉吸引有益昆虫，但也可能吸引害虫。尽可能使用自然害虫控制方法。',
            'pro_tips_title': '花卉种植专业技巧',
            'tips_list': '''<li>分批种植花卉，确保整个季节的连续收获</li>
                <li>与草药一起种植，自然驱除害虫</li>
                <li>保存最高质量的花卉用于特殊活动和高端市场</li>
                <li>尝试不同的花卉组合制作独特花束</li>
                <li>监控市场趋势，种植最有利可图的花卉</li>
                <li>使用温室延长高价值花卉的生长季节</li>
                <li>与其他玩家建立联系，了解稀有花卉品种</li>
                <li>详细记录生长时间和产量以进行优化</li>''',
            'advanced_title': '高级花卉种植技术',
            'mutation_title': '突变育种',
            'mutation_desc': '交叉授粉不同的花卉品种，创造具有独特颜色和更高价值的稀有突变。',
            'seasonal_title': '季节性优化',
            'seasonal_desc': '规划您的花卉种植日历，在需求高峰期实现利润最大化。',
            'market_title': '市场时机',
            'market_desc': '研究市场模式，在需求最高、价格达到峰值时销售花卉。',
            'getting_started_title': '开始花卉种植',
            'getting_started_steps': '''<li><strong>选择您的花卉：</strong> 从快速生长、高需求的花卉开始，如雏菊和向日葵</li>
                <li><strong>准备您的花园：</strong> 设置适当的土壤、灌溉和害虫控制系统</li>
                <li><strong>分阶段种植：</strong> 错开您的种植以确保连续收获</li>
                <li><strong>监控生长：</strong> 跟踪生长时间并相应调整您的计划</li>
                <li><strong>收获和销售：</strong> 为最大利润和市场需求安排您的收获时间</li>
                <li><strong>逐步扩展：</strong> 随着您获得经验，添加更复杂和有价值的花卉品种</li>''',
            'current_flag_src': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5MDAgNjAwIj4KICAgICAgICAgICAgPHJlY3Qgd2lkdGg9IjkwMCIgaGVpZ2h0PSI2MDAiIGZpbGw9IiNkZTI5MTAiLz4KICAgICAgICAgICAgPGcgZmlsbD0iI2ZmZGUwMCI+CiAgICAgICAgICAgICAgICA8cGF0aCBkPSJNNDUwIDEyMGwtNDUuNyAxNDAuNy0xMTkuMyAwaDE1NGwtMTE5LjMgMHoiLz4KICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik00NTAgMzAwbC00NS43IDE0MC43LTExOS4zIDBoMTU0bC0xMTkuMyAweiIvPgogICAgICAgICAgICAgICAgPHBhdGggZD0iTTQ1MCA0ODBsLTQ1LjcgMTQwLjctMTE5LjMgMGgxNTRsLTExOS4zIDB6Ii8+CiAgICAgICAgICAgIDwvZz4KICAgICAgICA8L3N2Zz4=',
            'current_flag_alt': 'zh-cn Flag'
        }
    else:
        # 其他语言暂时使用英文内容，后续可以添加翻译
        return get_translations('en')

def create_flower_pages():
    """为所有语言创建花卉种植页面"""
    flag_options = get_flag_options()
    
    for lang_code in LANGUAGES.keys():
        # 创建语言目录（如果不存在）
        lang_dir = f"{lang_code}"
        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)
        
        # 获取翻译
        translations = get_translations(lang_code)
        
        # 填充模板
        content = FLOWER_PAGE_TEMPLATE.format(
            lang_code=lang_code,
            lang_path=lang_dir,
            flag_options=flag_options,
            **translations
        )
        
        # 写入文件
        file_path = f"{lang_dir}/flower-type-plants.html"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已创建: {file_path}")

def main():
    """主函数"""
    print("🌸 开始创建花卉类植物种植攻略页面...")
    create_flower_pages()
    print("🎉 所有语言的花卉种植页面创建完成！")

if __name__ == "__main__":
    main() 