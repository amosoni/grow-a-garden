#!/usr/bin/env python3
"""
翻译所有11种语言的攻略页面
"""

import os
import re

def get_all_translations():
    """获取所有语言的翻译"""
    return {
        'en': {
            'search_filter': 'Search & Filter Guides',
            'search_placeholder': 'Search guides...',
            'filter_all': 'All',
            'filter_recipe': 'Recipes',
            'filter_farming': 'Farming',
            'filter_profit': 'Profit',
            'filter_advanced': 'Advanced',
            'trending_guides': 'Trending Guides',
            'most_popular': 'Most Popular',
            'trending': 'Trending',
            'new': 'New',
            'recipe_guides': 'Recipe Guides',
            'farming_guides': 'Farming Guides',
            'profit_optimization': 'Profit Optimization',
            'cooperation_operations': 'Cooperation & Operations',
            'advanced_guides': 'Advanced Guides',
            'quick_tips': 'Quick Tips',
            'navigation': 'Navigation',
            'back_to_calc': 'Back to Main Calculator',
            'beginner': 'Beginner',
            'intermediate': 'Intermediate',
            'expert': 'Expert',
            'advanced': 'Advanced',
            'min_read': 'min read',
            'views': 'views',
            'salad_guide': 'Salad Making Guide',
            'pizza_guide': 'Pizza Making Guide',
            'bread_guide': 'Bread Making Guide',
            'cake_guide': 'Cake Making Guide',
            'ice_cream_guide': 'Ice Cream Recipe Guide',
            'donut_guide': 'Donut Making Guide',
            'pie_guide': 'Pie Making Guide',
            'cookie_guide': 'Cookie Making Guide',
            'smoothie_guide': 'Smoothie Making Guide',
            'sandwich_guide': 'Sandwich Making Guide',
            'salad_desc': 'Master the art of salad making with our comprehensive guide.',
            'pizza_desc': 'Learn how to make delicious pizza in Grow a Garden.',
            'bread_desc': 'Master bread making techniques in Grow a Garden.',
            'cake_desc': 'Learn cake making tips in Grow a Garden.',
            'ice_cream_desc': 'Learn delicious ice cream recipes and ratios to optimize profit and taste.',
            'donut_desc': 'Learn donut making tips in Grow a Garden.',
            'pie_desc': 'Learn pie making tips in Grow a Garden.',
            'cookie_desc': 'Learn cookie making tips in Grow a Garden.',
            'smoothie_desc': 'Learn smoothie making tips in Grow a Garden.',
            'sandwich_desc': 'Learn sandwich making tips in Grow a Garden.',
            'salad_full_desc': 'Complete guide to making perfect salads in Grow a Garden. From basic ingredient collection to advanced recipes.',
            'pizza_full_desc': 'Learn how to make delicious pizza in Grow a Garden. From dough preparation to topping combinations.',
            'bread_full_desc': 'Master bread making techniques. Learn about flour types, yeast management, and baking optimization.',
            'corn_guide': 'Corn Growing Guide',
            'orange_guide': 'Orange Growing Guide',
            'wheat_guide': 'Wheat Growing Guide',
            'farming_basics': 'Farming Basics',
            'watering_strategies': 'Watering Strategies',
            'crop_rotation': 'Crop Rotation Guide',
            'seed_selection': 'Seed Selection Guide',
            'carrot_guide': 'Carrot Growing Guide',
            'apple_guide': 'Apple Growing Guide',
            'berry_guide': 'Berry Growing Guide',
            'farm_building': 'Farm Building Guide',
            'fast_money': 'Fast Money Making Guide',
            'market_analysis': 'Market Analysis Guide',
            'resource_management': 'Resource Management',
            'investment': 'Investment Guide',
            'play_friends': 'Play with Friends',
            'storage_logistics': 'Storage & Logistics',
            'game_mechanics': 'Game Mechanics',
            'mutation': 'Mutation Guide',
            'special_events': 'Special Events',
            'speedrunning': 'Speedrunning',
            'corn_desc': 'Efficient corn cultivation: planting, watering, harvesting.',
            'orange_desc': 'Efficient orange cultivation: planting, watering, harvesting.',
            'wheat_desc': 'Efficient wheat cultivation: planting, watering, harvesting.',
            'farming_basics_desc': 'Basic cultivation techniques, watering, crop management points.',
            'watering_desc': 'Learn optimal watering timing, frequency, and efficiency.',
            'crop_rotation_desc': 'Maintain soil fertility and maximize yield with effective crop rotation strategies.',
            'seed_desc': 'Choose seeds that match your strategy and compare growth and profit.',
            'carrot_desc': 'Efficient carrot cultivation: planting, watering, harvesting.',
            'apple_desc': 'Efficient apple cultivation: planting, watering, harvesting.',
            'berry_desc': 'Efficient berry cultivation: planting, watering, harvesting.',
            'farm_building_desc': 'Design efficient farm layouts: optimize irrigation, storage, processing, and pathways.',
            'fast_money_desc': 'Learn long-term profit strategies, market analysis and risk management, sales optimization.',
            'market_desc': 'Analyze market trends, identify profit opportunities, optimize sales strategies.',
            'resource_desc': 'Master resource allocation, inventory management, cost optimization.',
            'investment_desc': 'Learn how to identify investment targets and maximize long-term returns.',
            'play_friends_desc': 'Collaborate with friends to build efficient farms through role division and trading.',
            'storage_desc': 'Improve logistics efficiency through storage and route design.',
            'mechanics_desc': 'Deep dive into game mechanics, mutations, special events, and advanced elements.',
            'mutation_desc': 'Understand the mutation system and combine for maximum profit.',
            'events_desc': 'Complete guide to limited-time events, special opportunities, and exclusive rewards.',
            'speed_desc': 'Speedrunning techniques to maximize efficiency and break records.',
            'golden_hour': 'Golden Hour',
            'golden_hour_desc': 'Watering at 7:00-9:00 in-game doubles growth effects.',
            'quality_matters': 'Quality Matters',
            'quality_desc': 'High-quality materials lead to better recipes and higher profits.',
            'market_timing': 'Market Timing',
            'market_timing_desc': 'Sell during peak demand to maximize profits.',
            'recipe_mastery': 'Recipe Mastery',
            'recipe_mastery_desc': 'Master basics before advanced recipes to improve efficiency.',
            'community_learning': 'Community Learning',
            'community_desc': 'Learn from other players on Discord.',
            'regular_updates': 'Regular Updates',
            'regular_desc': 'Check regularly for new guides and latest strategies.'
        },
        'es': {
            'search_filter': 'Búsqueda y Filtros',
            'search_placeholder': 'Buscar guías...',
            'filter_all': 'Todo',
            'filter_recipe': 'Recetas',
            'filter_farming': 'Agricultura',
            'filter_profit': 'Beneficios',
            'filter_advanced': 'Avanzado',
            'trending_guides': 'Guías Populares',
            'most_popular': 'Más Popular',
            'trending': 'Tendencia',
            'new': 'Nuevo',
            'recipe_guides': 'Guías de Recetas',
            'farming_guides': 'Guías de Agricultura',
            'profit_optimization': 'Optimización de Beneficios',
            'cooperation_operations': 'Cooperación y Operaciones',
            'advanced_guides': 'Guías Avanzadas',
            'quick_tips': 'Consejos Rápidos',
            'navigation': 'Navegación',
            'back_to_calc': 'Volver al Calculador Principal',
            'beginner': 'Principiante',
            'intermediate': 'Intermedio',
            'expert': 'Experto',
            'advanced': 'Avanzado',
            'min_read': 'minutos de lectura',
            'views': 'vistas',
            'salad_guide': 'Guía de Ensaladas',
            'pizza_guide': 'Guía de Pizza',
            'bread_guide': 'Guía de Pan',
            'cake_guide': 'Guía de Pasteles',
            'ice_cream_guide': 'Guía de Helados',
            'donut_guide': 'Guía de Donas',
            'pie_guide': 'Guía de Pasteles',
            'cookie_guide': 'Guía de Galletas',
            'smoothie_guide': 'Guía de Batidos',
            'sandwich_guide': 'Guía de Sándwiches',
            'salad_desc': 'Domina el arte de hacer ensaladas con nuestra guía completa.',
            'pizza_desc': 'Aprende a hacer pizza deliciosa en Grow a Garden.',
            'bread_desc': 'Domina las técnicas de panadería en Grow a Garden.',
            'cake_desc': 'Aprende consejos para hacer pasteles en Grow a Garden.',
            'ice_cream_desc': 'Aprende recetas y proporciones de helados deliciosos para optimizar ganancias y sabor.',
            'donut_desc': 'Aprende consejos para hacer donas en Grow a Garden.',
            'pie_desc': 'Aprende consejos para hacer pasteles en Grow a Garden.',
            'cookie_desc': 'Aprende consejos para hacer galletas en Grow a Garden.',
            'smoothie_desc': 'Aprende consejos para hacer batidos en Grow a Garden.',
            'sandwich_desc': 'Aprende consejos para hacer sándwiches en Grow a Garden.',
            'salad_full_desc': 'Guía completa para hacer ensaladas perfectas en Grow a Garden. Desde recolección básica de ingredientes hasta recetas avanzadas.',
            'pizza_full_desc': 'Aprende a hacer pizza deliciosa en Grow a Garden. Desde preparación de masa hasta combinaciones de ingredientes.',
            'bread_full_desc': 'Domina las técnicas de panadería. Aprende sobre tipos de harina, gestión de levadura y optimización de horneado.',
            'corn_guide': 'Guía de Cultivo de Maíz',
            'orange_guide': 'Guía de Cultivo de Naranjas',
            'wheat_guide': 'Guía de Cultivo de Trigo',
            'farming_basics': 'Básicos de Agricultura',
            'watering_strategies': 'Estrategias de Riego',
            'crop_rotation': 'Guía de Rotación de Cultivos',
            'seed_selection': 'Guía de Selección de Semillas',
            'carrot_guide': 'Guía de Cultivo de Zanahorias',
            'apple_guide': 'Guía de Cultivo de Manzanas',
            'berry_guide': 'Guía de Cultivo de Bayas',
            'farm_building': 'Guía de Construcción de Granjas',
            'fast_money': 'Guía de Ganar Dinero Rápido',
            'market_analysis': 'Guía de Análisis de Mercado',
            'resource_management': 'Gestión de Recursos',
            'investment': 'Guía de Inversión',
            'play_friends': 'Jugar con Amigos',
            'storage_logistics': 'Almacenamiento y Logística',
            'game_mechanics': 'Mecánicas del Juego',
            'mutation': 'Guía de Mutaciones',
            'special_events': 'Eventos Especiales',
            'speedrunning': 'Speedrunning',
            'corn_desc': 'Cultivo eficiente de maíz: plantación, riego, cosecha.',
            'orange_desc': 'Cultivo eficiente de naranjas: plantación, riego, cosecha.',
            'wheat_desc': 'Cultivo eficiente de trigo: plantación, riego, cosecha.',
            'farming_basics_desc': 'Técnicas básicas de cultivo, riego, puntos de gestión de cultivos.',
            'watering_desc': 'Aprende el momento óptimo de riego, frecuencia y eficiencia.',
            'crop_rotation_desc': 'Mantén la fertilidad del suelo y maximiza el rendimiento con estrategias efectivas de rotación de cultivos.',
            'seed_desc': 'Elige semillas que coincidan con tu estrategia y compara crecimiento y ganancias.',
            'carrot_desc': 'Cultivo eficiente de zanahorias: plantación, riego, cosecha.',
            'apple_desc': 'Cultivo eficiente de manzanas: plantación, riego, cosecha.',
            'berry_desc': 'Cultivo eficiente de bayas: plantación, riego, cosecha.',
            'farm_building_desc': 'Diseña diseños de granjas eficientes: optimiza riego, almacenamiento, procesamiento y caminos.',
            'fast_money_desc': 'Aprende estrategias de ganancias a largo plazo, análisis de mercado y gestión de riesgos, optimización de ventas.',
            'market_desc': 'Analiza tendencias del mercado, identifica oportunidades de ganancias, optimiza estrategias de ventas.',
            'resource_desc': 'Domina la asignación de recursos, gestión de inventario, optimización de costos.',
            'investment_desc': 'Aprende a identificar objetivos de inversión y maximizar retornos a largo plazo.',
            'play_friends_desc': 'Colabora con amigos para construir granjas eficientes a través de división de roles y comercio.',
            'storage_desc': 'Mejora la eficiencia logística a través de almacenamiento y diseño de rutas.',
            'mechanics_desc': 'Profundiza en las mecánicas del juego, mutaciones, eventos especiales y elementos avanzados.',
            'mutation_desc': 'Entiende el sistema de mutaciones y combina para máximo beneficio.',
            'events_desc': 'Guía completa de eventos de tiempo limitado, oportunidades especiales y recompensas exclusivas.',
            'speed_desc': 'Técnicas de speedrunning para maximizar eficiencia y quebrar recordes.',
            'golden_hour': 'Hora Dorada',
            'golden_hour_desc': 'Regar a las 7:00-9:00 en el juego duplica los efeitos de crescimento.',
            'quality_matters': 'La Calidad Importa',
            'quality_desc': 'Los materiales de alta calidad conducen a mejores recetas y mayores ganancias.',
            'market_timing': 'Momento del Mercado',
            'market_timing_desc': 'Vende durante la demanda máxima para maximizar ganancias.',
            'recipe_mastery': 'Dominio de Recetas',
            'recipe_mastery_desc': 'Domina los básicos antes de las recetas avanzadas para mejorar la eficiencia.',
            'community_learning': 'Aprendizaje Comunitario',
            'community_desc': 'Aprende de otros jugadores en Discord.',
            'regular_updates': 'Actualizaciones Regulares',
            'regular_desc': 'Revisa regularmente para nuevas guías y estrategias más recientes.'
        },
        'pt-br': {
            'search_filter': 'Pesquisa e Filtros',
            'search_placeholder': 'Pesquisar guias...',
            'filter_all': 'Tudo',
            'filter_recipe': 'Receitas',
            'filter_farming': 'Agricultura',
            'filter_profit': 'Lucros',
            'filter_advanced': 'Avançado',
            'trending_guides': 'Guias Populares',
            'most_popular': 'Mais Popular',
            'trending': 'Tendência',
            'new': 'Novo',
            'recipe_guides': 'Guias de Receitas',
            'farming_guides': 'Guias de Agricultura',
            'profit_optimization': 'Otimização de Lucros',
            'cooperation_operations': 'Cooperação e Operações',
            'advanced_guides': 'Guias Avançados',
            'quick_tips': 'Dicas Rápidas',
            'navigation': 'Navegação',
            'back_to_calc': 'Voltar ao Calculador Principal',
            'beginner': 'Iniciante',
            'intermediate': 'Intermediário',
            'expert': 'Especialista',
            'advanced': 'Avançado',
            'min_read': 'minutos de leitura',
            'views': 'visualizações',
            'salad_guide': 'Guia de Saladas',
            'pizza_guide': 'Guia de Pizza',
            'bread_guide': 'Guia de Pão',
            'cake_guide': 'Guia de Bolos',
            'ice_cream_guide': 'Guia de Sorvetes',
            'donut_guide': 'Guia de Donuts',
            'pie_guide': 'Guia de Tortas',
            'cookie_guide': 'Guia de Biscoitos',
            'smoothie_guide': 'Guia de Vitaminas',
            'sandwich_guide': 'Guia de Sanduíches',
            'salad_desc': 'Domine a arte de fazer saladas com nosso guia completo.',
            'pizza_desc': 'Aprenda a fazer pizza deliciosa em Grow a Garden.',
            'bread_desc': 'Domine as técnicas de panificação em Grow a Garden.',
            'cake_desc': 'Aprenda dicas para fazer bolos em Grow a Garden.',
            'ice_cream_desc': 'Aprenda receitas e proporções de sorvetes deliciosos para otimizar lucros e sabor.',
            'donut_desc': 'Aprenda dicas para fazer donuts em Grow a Garden.',
            'pie_desc': 'Aprenda dicas para fazer tortas em Grow a Garden.',
            'cookie_desc': 'Aprenda dicas para fazer biscoitos em Grow a Garden.',
            'smoothie_desc': 'Aprenda dicas para fazer vitaminas em Grow a Garden.',
            'sandwich_desc': 'Aprenda dicas para fazer sanduíches em Grow a Garden.',
            'salad_full_desc': 'Guia completo para fazer saladas perfeitas em Grow a Garden. Desde coleta básica de ingredientes até receitas avançadas.',
            'pizza_full_desc': 'Aprenda a fazer pizza deliciosa em Grow a Garden. Desde preparação de massa até combinações de ingredientes.',
            'bread_full_desc': 'Domine as técnicas de panificação. Aprenda sobre tipos de farinha, gestão de fermento e otimização de assamento.',
            'corn_guide': 'Guia de Cultivo de Milho',
            'orange_guide': 'Guia de Cultivo de Laranjas',
            'wheat_guide': 'Guia de Cultivo de Trigo',
            'farming_basics': 'Básicos de Agricultura',
            'watering_strategies': 'Estratégias de Irrigação',
            'crop_rotation': 'Guia de Rotação de Culturas',
            'seed_selection': 'Guia de Seleção de Sementes',
            'carrot_guide': 'Guia de Cultivo de Cenouras',
            'apple_guide': 'Guia de Cultivo de Maçãs',
            'berry_guide': 'Guia de Cultivo de Frutas Vermelhas',
            'farm_building': 'Guia de Construção de Fazendas',
            'fast_money': 'Guia de Ganhar Dinheiro Rápido',
            'market_analysis': 'Guia de Análise de Mercado',
            'resource_management': 'Gestão de Recursos',
            'investment': 'Guia de Investimento',
            'play_friends': 'Jogar com Amigos',
            'storage_logistics': 'Armazenamento e Logística',
            'game_mechanics': 'Mecânicas do Jogo',
            'mutation': 'Guia de Mutações',
            'special_events': 'Eventos Especiais',
            'speedrunning': 'Speedrunning',
            'corn_desc': 'Cultivo eficiente de milho: plantio, irrigação, colheita.',
            'orange_desc': 'Cultivo eficiente de laranjas: plantio, irrigação, colheita.',
            'wheat_desc': 'Cultivo eficiente de trigo: plantio, irrigação, colheita.',
            'farming_basics_desc': 'Técnicas básicas de cultivo, irrigação, pontos de gestão de culturas.',
            'watering_desc': 'Aprenda o momento ótimo de irrigação, frequência e eficiência.',
            'crop_rotation_desc': 'Mantenha a fertilidade do solo e maximize o rendimento com estratégias efetivas de rotação de culturas.',
            'seed_desc': 'Escolha sementes que coincidam com sua estratégia e compare crescimento e lucros.',
            'carrot_desc': 'Cultivo eficiente de cenouras: plantio, irrigação, colheita.',
            'apple_desc': 'Cultivo eficiente de maçãs: plantio, irrigação, colheita.',
            'berry_desc': 'Cultivo eficiente de frutas vermelhas: plantio, irrigação, colheita.',
            'farm_building_desc': 'Projete layouts de fazendas eficientes: otimize irrigação, armazenamento, processamento e caminhos.',
            'fast_money_desc': 'Aprenda estratégias de lucros a longo prazo, análise de mercado e gestão de riscos, otimização de vendas.',
            'market_desc': 'Analise tendências do mercado, identifique oportunidades de lucros, otimize estratégias de vendas.',
            'resource_desc': 'Domine a alocação de recursos, gestão de inventário, otimização de custos.',
            'investment_desc': 'Aprenda a identificar objetivos de investimento e maximizar retornos a longo prazo.',
            'play_friends_desc': 'Colabore com amigos para construir fazendas eficientes através de divisão de papéis e comércio.',
            'storage_desc': 'Melhore a eficiência logística através de armazenamento e design de rotas.',
            'mechanics_desc': 'Mergulhe nas mecânicas do jogo, mutações, eventos especiais e elementos avançados.',
            'mutation_desc': 'Entenda o sistema de mutações e combine para máximo lucro.',
            'events_desc': 'Guia completo de eventos de tempo limitado, oportunidades especiais e recompensas exclusivas.',
            'speed_desc': 'Técnicas de speedrunning para maximizar eficiência e quebrar recordes.',
            'golden_hour': 'Hora Dourada',
            'golden_hour_desc': 'Regar às 7:00-9:00 no jogo dobra os efeitos de crescimento.',
            'quality_matters': 'A Qualidade Importa',
            'quality_desc': 'Materiais de alta qualidade levam a melhores receitas e maiores lucros.',
            'market_timing': 'Momento do Mercado',
            'market_timing_desc': 'Venda durante a demanda máxima para maximizar lucros.',
            'recipe_mastery': 'Domínio de Receitas',
            'recipe_mastery_desc': 'Domine o básico antes das receitas avançadas para melhorar a eficiência.',
            'community_learning': 'Aprendizado Comunitário',
            'community_desc': 'Aprenda com outros jogadores no Discord.',
            'regular_updates': 'Atualizações Regulares',
            'regular_desc': 'Verifique regularmente para novos guias e estratégias mais recentes.'
        }
    }

def translate_page_content(content, lang_code, translations):
    """翻译页面内容"""
    if lang_code not in translations:
        return content
    
    trans = translations[lang_code]
    
    # 替换所有翻译项
    replacements = [
        # 搜索和筛选
        ('🔍 検索とフィルター', f"🔍 {trans['search_filter']}"),
        ('ガイドを検索...', trans['search_placeholder']),
        ('すべて', trans['filter_all']),
        ('レシピ', trans['filter_recipe']),
        ('農業', trans['filter_farming']),
        ('利益', trans['filter_profit']),
        ('上級', trans['filter_advanced']),
        
        # 热门指南
        ('🔥 人気のガイド', f"🔥 {trans['trending_guides']}"),
        ('⭐ 最も人気', f"⭐ {trans['most_popular']}"),
        ('📈 トレンド', f"📈 {trans['trending']}"),
        ('🆕 新着', f"🆕 {trans['new']}"),
        
        # 分类标题
        ('🍽️ レシピガイド', f"🍽️ {trans['recipe_guides']}"),
        ('🌾 農業ガイド', f"🌾 {trans['farming_guides']}"),
        ('💰 利益最適化', f"💰 {trans['profit_optimization']}"),
        ('👥 協力と運用', f"👥 {trans['cooperation_operations']}"),
        ('🎮 上級ガイド', f"🎮 {trans['advanced_guides']}"),
        
        # 快速提示
        ('💡 クイックヒント', f"💡 {trans['quick_tips']}"),
        ('⏰ ゴールデンアワー', f"⏰ {trans['golden_hour']}"),
        ('🎯 品質が重要', f"🎯 {trans['quality_matters']}"),
        ('📈 マーケットタイミング', f"📈 {trans['market_timing']}"),
        ('📚 レシピ習熟', f"📚 {trans['recipe_mastery']}"),
        ('🤝 コミュニティ学習', f"🤝 {trans['community_learning']}"),
        ('🔄 定期的な更新', f"🔄 {trans['regular_updates']}"),
        
        # 导航
        ('🏠 ナビゲーション', f"🏠 {trans['navigation']}"),
        ('← メイン計算機に戻る', f"← {trans['back_to_calc']}"),
        
        # 难度和阅读时间
        ('初心者', trans['beginner']),
        ('中級', trans['intermediate']),
        ('エキスパート', trans['expert']),
        ('上級', trans['advanced']),
        ('分読了', f" {trans['min_read']}"),
        
        # 浏览量
        ('🔥 2.5k 閲覧', f"🔥 2.5k {trans['views']}"),
        ('🔥 1.8k 閲覧', f"🔥 1.8k {trans['views']}"),
        ('🔥 1.2k 閲覧', f"🔥 1.2k {trans['views']}"),
        
        # 指南标题
        ('サラダ作りのガイド', trans['salad_guide']),
        ('ピザ作りのガイド', trans['pizza_guide']),
        ('パン作りのガイド', trans['bread_guide']),
        ('ケーキ作りのガイド', trans['cake_guide']),
        ('アイスクリームレシピガイド', trans['ice_cream_guide']),
        ('ドーナツ作りのガイド', trans['donut_guide']),
        ('パイ作りのガイド', trans['pie_guide']),
        ('クッキー作りのガイド', trans['cookie_guide']),
        ('スムージー作りのガイド', trans['smoothie_guide']),
        ('サンドイッチ作りのガイド', trans['sandwich_guide']),
        
        # 农业指南
        ('トウモロコシ栽培ガイド', trans['corn_guide']),
        ('オレンジ栽培ガイド', trans['orange_guide']),
        ('小麦栽培ガイド', trans['wheat_guide']),
        ('栽培の基礎', trans['farming_basics']),
        ('水やり戦略', trans['watering_strategies']),
        ('輪作ガイド', trans['crop_rotation']),
        ('種子選びガイド', trans['seed_selection']),
        ('ニンジン栽培ガイド', trans['carrot_guide']),
        ('リンゴ栽培ガイド', trans['apple_guide']),
        ('ベリー栽培ガイド', trans['berry_guide']),
        ('農場づくりのガイド', trans['farm_building']),
        
        # 利润指南
        ('早くお金を稼ぐガイド', trans['fast_money']),
        ('市場分析ガイド', trans['market_analysis']),
        ('リソース管理', trans['resource_management']),
        ('投資ガイド', trans['investment']),
        
        # 合作与运营
        ('友達と遊ぶ', trans['play_friends']),
        ('保管と物流', trans['storage_logistics']),
        
        # 高级指南
        ('ゲームメカニクス', trans['game_mechanics']),
        ('ミューテーションガイド', trans['mutation']),
        ('スペシャルイベント', trans['special_events']),
        ('スピードランニング', trans['speedrunning']),
        
        # 描述文本
        ('Grow a Gardenでサラダを作るコツを学びましょう。', trans['salad_desc']),
        ('Grow a Gardenでピザを作るコツを学びましょう。', trans['pizza_desc']),
        ('Grow a Gardenでパンを作るコツを学びましょう。', trans['bread_desc']),
        ('Grow a Gardenでケーキを作るコツを学びましょう。', trans['cake_desc']),
        ('Grow a Gardenでドーナツを作るコツを学びましょう。', trans['donut_desc']),
        ('Grow a Gardenでパイを作るコツを学びましょう。', trans['pie_desc']),
        ('Grow a Gardenでクッキーを作るコツを学びましょう。', trans['cookie_desc']),
        ('Grow a Gardenでスムージーを作るコツを学びましょう。', trans['smoothie_desc']),
        ('Grow a Gardenでサンドイッチを作るコツを学びましょう。', trans['sandwich_desc']),
        
        # 完整描述
        ('Grow a Gardenで完璧なサラダを作るための完全ガイド。基本的な材料収集から高度なレシピまで。', trans['salad_full_desc']),
        ('Grow a Gardenで美味しいピザの作り方を学びます。生地の準備からトッピングの組み合わせまで。', trans['pizza_full_desc']),
        ('パン作りの技術を習得。小麦粉の種類、酵母管理、焼成の最適化を学びます。', trans['bread_full_desc']),
        
        # 农业描述
        ('効率的なトウモロコシの栽培：播種・水やり・収穫。', trans['corn_desc']),
        ('効率的なオレンジの栽培：播種・水やり・収穫。', trans['orange_desc']),
        ('効率的な小麦の栽培：播種・水やり・収穫。', trans['wheat_desc']),
        ('基本的な栽培技術・水やり・作物管理のポイント。', trans['farming_basics_desc']),
        ('最適な水やりのタイミング・頻度・効率を学ぶ。', trans['watering_desc']),
        ('効果的な輪作戦略で土壌肥沃度を維持し収量を最大化。', trans['crop_rotation_desc']),
        ('戦略に合う種を選び、成長と利益を比較。', trans['seed_desc']),
        ('効率的な農場レイアウトの設計：灌漑、保管、加工、導線を最適化。', trans['farm_building_desc']),
        
        # 利润描述
        ('長期的な利益戦略、市場分析とリスク管理、販売の最適化を学ぶ。', trans['fast_money_desc']),
        ('市場動向を分析し、利益機会を見極め、販売戦略を最適化。', trans['market_desc']),
        ('資源配分、在庫管理、コスト最適化などを習得。', trans['resource_desc']),
        ('投資先の見極めと長期リターン最大化の方法を学ぶ。', trans['investment_desc']),
        
        # 合作描述
        ('友達と協力し、役割分担と取引で効率的な農場を。', trans['play_friends_desc']),
        ('保管とルート設計で物流効率を上げる。', trans['storage_desc']),
        
        # 高级描述
        ('ゲームメカニクス、変異、特別イベント、上級要素を深掘り。', trans['mechanics_desc']),
        ('ミューテーションシステムを理解し、最大利益のために組み合わせる。', trans['mutation_desc']),
        ('期間限定イベント、特別なチャンス、限定報酬の完全ガイド。', trans['events_desc']),
        ('効率を最大化し記録更新を目指すスピードラン技術。', trans['speed_desc']),
        
        # 快速提示描述
        ('ゲーム内 7:00〜9:00 に水やりすると成長効果が2倍。', trans['golden_hour_desc']),
        ('高品質の材料はより良いレシピと高い利益につながります。', trans['quality_desc']),
        ('需要が高い時間に販売して利益を最大化。', trans['market_timing_desc']),
        ('上級レシピの前に基本を習得して効率アップ。', trans['recipe_mastery_desc']),
        ('Discordで他のプレイヤーから学びましょう。', trans['community_desc']),
        ('新しいガイドと最新戦略のために定期的に確認。', trans['regular_desc']),
        
        # 其他
        ('Recipesガイド', trans['recipe_guides']),
        ('Profit', trans['filter_profit']),
        ('アイスクリームRecipesガイド', trans['ice_cream_guide']),
        ('美味しいアイスクリームの配合と比率を学び、Profitと味を最適化。', trans['ice_cream_desc']),
    ]
    
    # 执行替换
    for old_text, new_text in replacements:
        content = content.replace(old_text, new_text)
    
    return content

def main():
    """主函数"""
    print("🔄 开始翻译所有语言页面的攻略内容...")
    
    # 获取翻译配置
    translations = get_all_translations()
    
    # 需要翻译的语言
    languages = ['en', 'es', 'pt-br']
    
    # 需要翻译的页面类型
    guide_pages = [
        'guides.html',
        'how-to-make-spaghetti.html',
        'how-to-make-pizza.html',
        'how-to-make-bread.html',
        'how-to-make-cake.html',
        'how-to-make-ice-cream.html',
        'how-to-make-donuts.html',
        'how-to-make-pie.html',
        'how-to-make-cookies.html',
        'how-to-make-smoothie.html',
        'how-to-make-sandwich.html',
        'how-to-make-salad.html',
        'corn-growing-guide.html',
        'orange-growing-guide.html',
        'wheat-growing-guide.html',
        'farming-basics.html',
        'watering-strategies.html',
        'crop-rotation-guide.html',
        'seed-selection-guide.html',
        'carrot-growing-guide.html',
        'apple-growing-guide.html',
        'berry-growing-guide.html',
        'farm-building-guide.html',
        'fast-money-making-guide.html',
        'market-analysis-guide.html',
        'resource-management-guide.html',
        'investment-guide.html',
        'play-with-friends.html',
        'storage-and-logistics.html',
        'game-mechanics-guide.html',
        'mutation-guide.html',
        'special-events-guide.html',
        'speedrunning-guide.html'
    ]
    
    translated_count = 0
    
    for lang_code in languages:
        if lang_code not in translations:
            continue
            
        lang_dir = lang_code
        if not os.path.isdir(lang_dir):
            continue
            
        print(f"📝 正在翻译 {lang_code} 语言页面...")
        
        for page_type in guide_pages:
            page_path = os.path.join(lang_dir, page_type)
            if not os.path.exists(page_path):
                continue
                
            try:
                # 读取文件
                with open(page_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 翻译内容
                translated_content = translate_page_content(content, lang_code, translations)
                
                # 如果内容有变化，写入文件
                if translated_content != content:
                    with open(page_path, 'w', encoding='utf-8') as f:
                        f.write(translated_content)
                    
                    print(f"  ✅ 已翻译: {page_path}")
                    translated_count += 1
                    
            except Exception as e:
                print(f"  ❌ 翻译失败 {page_path}: {e}")
    
    print(f"\n🎉 攻略内容翻译完成！共翻译了 {translated_count} 个文件")
    print("📋 已翻译的语言:")
    for lang in languages:
        if lang in translations:
            print(f"   - {lang}")

if __name__ == "__main__":
    main() 