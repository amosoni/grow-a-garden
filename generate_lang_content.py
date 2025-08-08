#!/usr/bin/env python3
import os
import json

# 语言配置
LANGUAGES = {
    'en': {
        'name': 'English',
        'guides_title': '📚 Grow a Garden Guides',
        'guides_subtitle': 'Complete Collection of Strategies, Recipes, and Gameplay Tips',
        'search_title': '🔍 Search & Filter Guides',
        'search_placeholder': 'Search guides...',
        'filter_all': 'All',
        'filter_recipe': 'Recipes',
        'filter_farming': 'Farming',
        'filter_profit': 'Profit',
        'filter_advanced': 'Advanced',
        'popular_title': '🔥 Trending Guides',
        'featured_badge': '⭐ Most Popular',
        'trending_badge': '📈 Trending',
        'new_badge': '🆕 New',
        'difficulty_beginner': 'Beginner',
        'difficulty_intermediate': 'Intermediate',
        'difficulty_advanced': 'Advanced',
        'read_time': 'min read',
        'views': 'views',
        'recipe_title': '🍽️ Recipe Guides',
        'farming_title': '🌱 Farming Guides',
        'profit_title': '💰 Profit Guides',
        'guides': {
            'salad': {
                'title': '🥗 Salad Making Guide',
                'desc': 'Master the art of salad making with our comprehensive guide. Learn ingredient collection, advanced recipes, and efficiency improvement methods.',
                'difficulty': 'beginner',
                'time': '15'
            },
            'pizza': {
                'title': '🍕 Pizza Making Guide',
                'desc': 'Learn how to make delicious pizzas in Grow a Garden. From dough preparation to topping combinations and profit strategies.',
                'difficulty': 'intermediate',
                'time': '25'
            },
            'bread': {
                'title': '🍞 Bread Making Guide',
                'desc': 'Master bread making techniques in Grow a Garden. Learn flour types, yeast management, and baking optimization.',
                'difficulty': 'beginner',
                'time': '20'
            },
            'cake': {
                'title': '🍰 Cake Making Guide',
                'desc': 'Learn to make various delicious cakes. From basic recipes to advanced decoration techniques.',
                'difficulty': 'intermediate',
                'time': '30'
            },
            'corn': {
                'title': '🌽 Corn Growing Guide',
                'desc': 'Master corn growing techniques. Learn optimal planting times, watering strategies, and harvest optimization.',
                'difficulty': 'beginner',
                'time': '18'
            },
            'oranges': {
                'title': '🍊 Orange Growing Guide',
                'desc': 'Learn orange growing techniques. Complete process from seed selection to mature harvest.',
                'difficulty': 'intermediate',
                'time': '22'
            },
            'money': {
                'title': '💸 Fast Money Making Guide',
                'desc': 'Learn the fastest money-making methods. Master market timing, crop selection, and investment strategies.',
                'difficulty': 'intermediate',
                'time': '35'
            },
            'profit': {
                'title': '📈 Profit Strategies Guide',
                'desc': 'Master long-term profit strategies. Learn market analysis, risk management, and investment portfolio.',
                'difficulty': 'advanced',
                'time': '45'
            }
        }
    },
    'zh-cn': {
        'name': '简体中文',
        'guides_title': '📚 种植花园攻略',
        'guides_subtitle': '完整的策略、食谱与玩法技巧合集',
        'search_title': '🔍 搜索与分类',
        'search_placeholder': '搜索攻略...',
        'filter_all': '全部',
        'filter_recipe': '食谱',
        'filter_farming': '种植',
        'filter_profit': '收益',
        'filter_advanced': '进阶',
        'popular_title': '🔥 热门攻略',
        'featured_badge': '⭐ 最受欢迎',
        'trending_badge': '📈 热门',
        'new_badge': '🆕 新',
        'difficulty_beginner': '新手',
        'difficulty_intermediate': '中级',
        'difficulty_advanced': '高级',
        'read_time': '分钟阅读',
        'views': '浏览',
        'recipe_title': '🍽️ 食谱攻略',
        'farming_title': '🌱 种植攻略',
        'profit_title': '💰 收益攻略',
        'guides': {
            'salad': {
                'title': '🥗 沙拉制作指南',
                'desc': '掌握沙拉制作的艺术。学习食材收集、高级食谱和效率提升方法。',
                'difficulty': 'beginner',
                'time': '15'
            },
            'pizza': {
                'title': '🍕 披萨制作指南',
                'desc': '学习在种植花园中制作美味披萨。从面团准备到配料组合和收益策略。',
                'difficulty': 'intermediate',
                'time': '25'
            },
            'bread': {
                'title': '🍞 面包制作指南',
                'desc': '掌握种植花园中的面包制作技巧。学习面粉类型、酵母管理和烘焙优化。',
                'difficulty': 'beginner',
                'time': '20'
            },
            'cake': {
                'title': '🍰 蛋糕制作指南',
                'desc': '学习制作各种美味蛋糕。从基础配方到高级装饰技巧。',
                'difficulty': 'intermediate',
                'time': '30'
            },
            'corn': {
                'title': '🌽 玉米种植指南',
                'desc': '掌握玉米种植技巧。学习最佳种植时间、浇水策略和收获优化。',
                'difficulty': 'beginner',
                'time': '18'
            },
            'oranges': {
                'title': '🍊 橙子种植指南',
                'desc': '学习橙子种植技术。从种子选择到成熟收获的完整流程。',
                'difficulty': 'intermediate',
                'time': '22'
            },
            'money': {
                'title': '💸 快速赚钱指南',
                'desc': '学习最快的赚钱方法。掌握市场时机、作物选择和投资策略。',
                'difficulty': 'intermediate',
                'time': '35'
            },
            'profit': {
                'title': '📈 收益策略指南',
                'desc': '掌握长期收益策略。学习市场分析、风险管理和投资组合。',
                'difficulty': 'advanced',
                'time': '45'
            }
        }
    },
    'es': {
        'name': 'Español',
        'guides_title': '📚 Guías de Grow a Garden',
        'guides_subtitle': 'Colección completa de estrategias, recetas y trucos de juego',
        'search_title': '🔍 Buscar y Filtrar',
        'search_placeholder': 'Buscar guías...',
        'filter_all': 'Todas',
        'filter_recipe': 'Recetas',
        'filter_farming': 'Cultivo',
        'filter_profit': 'Ganancias',
        'filter_advanced': 'Avanzado',
        'popular_title': '🔥 Guías Populares',
        'featured_badge': '⭐ Más Popular',
        'trending_badge': '📈 Tendencia',
        'new_badge': '🆕 Nuevo',
        'difficulty_beginner': 'Principiante',
        'difficulty_intermediate': 'Intermedio',
        'difficulty_advanced': 'Avanzado',
        'read_time': 'min lectura',
        'views': 'vistas',
        'recipe_title': '🍽️ Guías de Recetas',
        'farming_title': '🌱 Guías de Cultivo',
        'profit_title': '💰 Guías de Ganancias',
        'guides': {
            'salad': {
                'title': '🥗 Guía de Ensaladas',
                'desc': 'Domina el arte de hacer ensaladas. Aprende recolección de ingredientes, recetas avanzadas y métodos de mejora de eficiencia.',
                'difficulty': 'beginner',
                'time': '15'
            },
            'pizza': {
                'title': '🍕 Guía de Pizza',
                'desc': 'Aprende a hacer deliciosas pizzas en Grow a Garden. Desde preparación de masa hasta combinaciones de ingredientes.',
                'difficulty': 'intermediate',
                'time': '25'
            },
            'bread': {
                'title': '🍞 Guía de Pan',
                'desc': 'Domina las técnicas de panadería en Grow a Garden. Aprende tipos de harina, gestión de levadura y optimización de horneado.',
                'difficulty': 'beginner',
                'time': '20'
            },
            'cake': {
                'title': '🍰 Guía de Pasteles',
                'desc': 'Aprende a hacer varios pasteles deliciosos. Desde recetas básicas hasta técnicas avanzadas de decoración.',
                'difficulty': 'intermediate',
                'time': '30'
            },
            'corn': {
                'title': '🌽 Guía de Cultivo de Maíz',
                'desc': 'Domina las técnicas de cultivo de maíz. Aprende mejores tiempos de siembra, estrategias de riego y optimización de cosecha.',
                'difficulty': 'beginner',
                'time': '18'
            },
            'oranges': {
                'title': '🍊 Guía de Cultivo de Naranjas',
                'desc': 'Aprende técnicas de cultivo de naranjas. Proceso completo desde selección de semillas hasta cosecha madura.',
                'difficulty': 'intermediate',
                'time': '22'
            },
            'money': {
                'title': '💸 Guía de Ganar Dinero Rápido',
                'desc': 'Aprende los métodos más rápidos para ganar dinero. Domina el timing del mercado, selección de cultivos y estrategias de inversión.',
                'difficulty': 'intermediate',
                'time': '35'
            },
            'profit': {
                'title': '📈 Guía de Estrategias de Ganancias',
                'desc': 'Domina estrategias de ganancias a largo plazo. Aprende análisis de mercado, gestión de riesgos y portafolio de inversión.',
                'difficulty': 'advanced',
                'time': '45'
            }
        }
    }
}

def generate_guides_content(lang_code, lang_config):
    """生成攻略页面内容"""
    content = f'''  <div class="guides-section">
    <div class="guides-card">
      <h2>{lang_config['search_title']}</h2>
      <div class="search-filter-container">
        <input type="text" id="guide-search" placeholder="{lang_config['search_placeholder']}" class="guide-search-input">
        <div class="filter-buttons">
          <button class="filter-btn active" data-filter="all">{lang_config['filter_all']}</button>
          <button class="filter-btn" data-filter="recipe">{lang_config['filter_recipe']}</button>
          <button class="filter-btn" data-filter="farming">{lang_config['filter_farming']}</button>
          <button class="filter-btn" data-filter="profit">{lang_config['filter_profit']}</button>
          <button class="filter-btn" data-filter="advanced">{lang_config['filter_advanced']}</button>
        </div>
      </div>
    </div>

    <!-- 热门攻略 -->
    <div class="guides-card">
      <h2>{lang_config['popular_title']}</h2>
      <div class="guides-grid">
        <a href="/how-to-make-salad.html" class="guide-item featured-guide">
          <div class="featured-badge">{lang_config['featured_badge']}</div>
          <h3>{lang_config['guides']['salad']['title']}</h3>
          <p>{lang_config['guides']['salad']['desc']}</p>
          <div class="guide-meta">
            <span class="guide-difficulty">{lang_config[f"difficulty_{lang_config['guides']['salad']['difficulty']}"]}</span>
            <span class="guide-read-time">{lang_config['guides']['salad']['time']} {lang_config['read_time']}</span>
            <span class="guide-views">🔥 2.5k {lang_config['views']}</span>
          </div>
        </a>
        
        <a href="/how-to-make-pizza.html" class="guide-item">
          <div class="trending-badge">{lang_config['trending_badge']}</div>
          <h3>{lang_config['guides']['pizza']['title']}</h3>
          <p>{lang_config['guides']['pizza']['desc']}</p>
          <div class="guide-meta">
            <span class="guide-difficulty">{lang_config[f"difficulty_{lang_config['guides']['pizza']['difficulty']}"]}</span>
            <span class="guide-read-time">{lang_config['guides']['pizza']['time']} {lang_config['read_time']}</span>
            <span class="guide-views">🔥 1.8k {lang_config['views']}</span>
          </div>
        </a>
        
        <a href="/how-to-make-bread.html" class="guide-item">
          <div class="new-badge">{lang_config['new_badge']}</div>
          <h3>{lang_config['guides']['bread']['title']}</h3>
          <p>{lang_config['guides']['bread']['desc']}</p>
          <div class="guide-meta">
            <span class="guide-difficulty">{lang_config[f"difficulty_{lang_config['guides']['bread']['difficulty']}"]}</span>
            <span class="guide-read-time">{lang_config['guides']['bread']['time']} {lang_config['read_time']}</span>
            <span class="guide-views">🔥 1.2k {lang_config['views']}</span>
          </div>
        </a>
      </div>
    </div>
    
    <!-- 食谱攻略 -->
    <div class="category-section" data-category="recipe">
      <h2 class="category-title">{lang_config['recipe_title']}</h2>
      <div class="guides-grid">
        <a href="/how-to-make-salad.html" class="guide-item">
          <h3>{lang_config['guides']['salad']['title']}</h3>
          <p>{lang_config['guides']['salad']['desc']}</p>
          <div class="guide-meta">
            <span class="guide-difficulty">{lang_config[f"difficulty_{lang_config['guides']['salad']['difficulty']}"]}</span>
            <span class="guide-read-time">{lang_config['guides']['salad']['time']} {lang_config['read_time']}</span>
          </div>
        </a>
        
        <a href="/how-to-make-pizza.html" class="guide-item">
          <h3>{lang_config['guides']['pizza']['title']}</h3>
          <p>{lang_config['guides']['pizza']['desc']}</p>
          <div class="guide-meta">
            <span class="guide-difficulty">{lang_config[f"difficulty_{lang_config['guides']['pizza']['difficulty']}"]}</span>
            <span class="guide-read-time">{lang_config['guides']['pizza']['time']} {lang_config['read_time']}</span>
          </div>
        </a>
        
        <a href="/how-to-make-bread.html" class="guide-item">
          <h3>{lang_config['guides']['bread']['title']}</h3>
          <p>{lang_config['guides']['bread']['desc']}</p>
          <div class="guide-meta">
            <span class="guide-difficulty">{lang_config[f"difficulty_{lang_config['guides']['bread']['difficulty']}"]}</span>
            <span class="guide-read-time">{lang_config['guides']['bread']['time']} {lang_config['read_time']}</span>
          </div>
        </a>
        
        <a href="/how-to-make-cake.html" class="guide-item">
          <h3>{lang_config['guides']['cake']['title']}</h3>
          <p>{lang_config['guides']['cake']['desc']}</p>
          <div class="guide-meta">
            <span class="guide-difficulty">{lang_config[f"difficulty_{lang_config['guides']['cake']['difficulty']}"]}</span>
            <span class="guide-read-time">{lang_config['guides']['cake']['time']} {lang_config['read_time']}</span>
          </div>
        </a>
      </div>
    </div>
    
    <!-- 种植攻略 -->
    <div class="category-section" data-category="farming">
      <h2 class="category-title">{lang_config['farming_title']}</h2>
      <div class="guides-grid">
        <a href="/how-to-grow-corn.html" class="guide-item">
          <h3>{lang_config['guides']['corn']['title']}</h3>
          <p>{lang_config['guides']['corn']['desc']}</p>
          <div class="guide-meta">
            <span class="guide-difficulty">{lang_config[f"difficulty_{lang_config['guides']['corn']['difficulty']}"]}</span>
            <span class="guide-read-time">{lang_config['guides']['corn']['time']} {lang_config['read_time']}</span>
          </div>
        </a>
        
        <a href="/how-to-grow-oranges.html" class="guide-item">
          <h3>{lang_config['guides']['oranges']['title']}</h3>
          <p>{lang_config['guides']['oranges']['desc']}</p>
          <div class="guide-meta">
            <span class="guide-difficulty">{lang_config[f"difficulty_{lang_config['guides']['oranges']['difficulty']}"]}</span>
            <span class="guide-read-time">{lang_config['guides']['oranges']['time']} {lang_config['read_time']}</span>
          </div>
        </a>
      </div>
    </div>
    
    <!-- 收益攻略 -->
    <div class="category-section" data-category="profit">
      <h2 class="category-title">{lang_config['profit_title']}</h2>
      <div class="guides-grid">
        <a href="/how-to-make-money-fast.html" class="guide-item">
          <h3>{lang_config['guides']['money']['title']}</h3>
          <p>{lang_config['guides']['money']['desc']}</p>
          <div class="guide-meta">
            <span class="guide-difficulty">{lang_config[f"difficulty_{lang_config['guides']['money']['difficulty']}"]}</span>
            <span class="guide-read-time">{lang_config['guides']['money']['time']} {lang_config['read_time']}</span>
          </div>
        </a>
        
        <a href="/profit-strategies.html" class="guide-item">
          <h3>{lang_config['guides']['profit']['title']}</h3>
          <p>{lang_config['guides']['profit']['desc']}</p>
          <div class="guide-meta">
            <span class="guide-difficulty">{lang_config[f"difficulty_{lang_config['guides']['profit']['difficulty']}"]}</span>
            <span class="guide-read-time">{lang_config['guides']['profit']['time']} {lang_config['read_time']}</span>
          </div>
        </a>
      </div>
    </div>
  </div>'''
    
    return content

def update_guides_file(lang_code, lang_config):
    """更新攻略文件"""
    file_path = f"{lang_code}/guides.html"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找并替换内容区域
        start_marker = '<div class="guides-section">'
        end_marker = '</div>\n  <script src="/i18n/i18n.js"></script>'
        
        start_pos = content.find(start_marker)
        end_pos = content.find(end_marker)
        
        if start_pos != -1 and end_pos != -1:
            new_content = content[:start_pos] + generate_guides_content(lang_code, lang_config) + content[end_pos:]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Updated: {file_path}")
            return True
        else:
            print(f"❌ Markers not found in: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🔧 Generating complete content for all languages...")
    
    total_updated = 0
    
    for lang_code, lang_config in LANGUAGES.items():
        print(f"\n📁 Processing {lang_code}/ directory...")
        
        if update_guides_file(lang_code, lang_config):
            total_updated += 1
    
    print(f"\n🎉 Total files updated: {total_updated}")

if __name__ == "__main__":
    main() 