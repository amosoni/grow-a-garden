#!/usr/bin/env python3
"""
为所有语言创建how-to-make-spaghetti.html页面
"""

import os
import json

# 语言配置
LANGUAGES = {
    'zh-cn': {
        'lang_attr': 'lang="zh-CN"',
        'title': '如何在Grow a Garden中制作意大利面 - 完整指南',
        'description': '学习如何在Roblox Grow a Garden中制作美味的意大利面！从面条准备到酱料制作，包括所有意大利面制作技巧、最佳配料组合和效率提升方法。',
        'keywords': '如何在grow a garden中制作意大利面, roblox意大利面食谱, grow a garden指南, 意大利面制作指南, roblox农场游戏, 意大利面配料收集, grow a garden技巧',
        'h1': '🍝 如何在Grow a Garden中制作意大利面',
        'subtitle': '完整指南：从配料收集到美味上桌',
        'ingredients_title': '📋 所需配料',
        'steps_title': '👨‍🍳 制作步骤',
        'tips_title': '💡 制作技巧',
        'back_btn': '← 返回指南'
    },
    'es': {
        'lang_attr': 'lang="es"',
        'title': 'Cómo Hacer Espaguetis en Grow a Garden - Guía Completa',
        'description': '¡Aprende a hacer deliciosos espaguetis en Roblox Grow a Garden! Desde la preparación de la pasta hasta la salsa, incluyendo todos los consejos para hacer espaguetis, las mejores combinaciones de ingredientes y métodos para mejorar la eficiencia.',
        'keywords': 'cómo hacer espaguetis en grow a garden, receta de espaguetis roblox, guía grow a garden, guía para hacer espaguetis, juego de granja roblox, recolección de ingredientes para espaguetis, consejos grow a garden',
        'h1': '🍝 Cómo Hacer Espaguetis en Grow a Garden',
        'subtitle': 'Guía Completa: Desde la Recolección de Ingredientes hasta la Mesa',
        'ingredients_title': '📋 Ingredientes Necesarios',
        'steps_title': '👨‍🍳 Pasos de Preparación',
        'tips_title': '💡 Consejos de Preparación',
        'back_btn': '← Volver a Guías'
    },
    'pt-br': {
        'lang_attr': 'lang="pt-BR"',
        'title': 'Como Fazer Espaguete no Grow a Garden - Guia Completo',
        'description': 'Aprenda a fazer deliciosos espaguetes no Roblox Grow a Garden! Desde a preparação da massa até o molho, incluindo todas as dicas para fazer espaguete, as melhores combinações de ingredientes e métodos para melhorar a eficiência.',
        'keywords': 'como fazer espaguete no grow a garden, receita de espaguete roblox, guia grow a garden, guia para fazer espaguete, jogo de fazenda roblox, coleta de ingredientes para espaguete, dicas grow a garden',
        'h1': '🍝 Como Fazer Espaguete no Grow a Garden',
        'subtitle': 'Guia Completo: Da Coleta de Ingredientes à Mesa',
        'ingredients_title': '📋 Ingredientes Necessários',
        'steps_title': '👨‍🍳 Passos de Preparação',
        'tips_title': '💡 Dicas de Preparação',
        'back_btn': '← Voltar aos Guias'
    },
    'fr': {
        'lang_attr': 'lang="fr"',
        'title': 'Comment Faire des Spaghettis dans Grow a Garden - Guide Complet',
        'description': 'Apprenez à faire de délicieux spaghettis dans Roblox Grow a Garden ! De la préparation des pâtes à la sauce, incluant tous les conseils pour faire des spaghettis, les meilleures combinaisons d\'ingrédients et les méthodes pour améliorer l\'efficacité.',
        'keywords': 'comment faire des spaghettis dans grow a garden, recette de spaghettis roblox, guide grow a garden, guide pour faire des spaghettis, jeu de ferme roblox, collecte d\'ingrédients pour spaghettis, conseils grow a garden',
        'h1': '🍝 Comment Faire des Spaghettis dans Grow a Garden',
        'subtitle': 'Guide Complet : De la Collecte d\'Ingrédients à la Table',
        'ingredients_title': '📋 Ingrédients Nécessaires',
        'steps_title': '👨‍🍳 Étapes de Préparation',
        'tips_title': '💡 Conseils de Préparation',
        'back_btn': '← Retour aux Guides'
    },
    'de': {
        'lang_attr': 'lang="de"',
        'title': 'Wie man Spaghetti in Grow a Garden macht - Vollständige Anleitung',
        'description': 'Lerne, wie man köstliche Spaghetti in Roblox Grow a Garden macht! Von der Nudelzubereitung bis zur Soße, einschließlich aller Tipps zum Spaghetti-Machen, der besten Zutatenkombinationen und Methoden zur Effizienzsteigerung.',
        'keywords': 'wie man spaghetti in grow a garden macht, roblox spaghetti rezept, grow a garden anleitung, spaghetti zubereitung anleitung, roblox farmspiel, spaghetti zutaten sammeln, grow a garden tipps',
        'h1': '🍝 Wie man Spaghetti in Grow a Garden macht',
        'subtitle': 'Vollständige Anleitung: Von der Zutatensammlung bis zum Tisch',
        'ingredients_title': '📋 Benötigte Zutaten',
        'steps_title': '👨‍🍳 Zubereitungsschritte',
        'tips_title': '💡 Zubereitungstipps',
        'back_btn': '← Zurück zu Anleitungen'
    },
    'ru': {
        'lang_attr': 'lang="ru"',
        'title': 'Как Сделать Спагетти в Grow a Garden - Полное Руководство',
        'description': 'Узнайте, как приготовить вкусные спагетти в Roblox Grow a Garden! От приготовления пасты до соуса, включая все советы по приготовлению спагетти, лучшие комбинации ингредиентов и методы повышения эффективности.',
        'keywords': 'как сделать спагетти в grow a garden, рецепт спагетти roblox, руководство grow a garden, руководство по приготовлению спагетти, игра ферма roblox, сбор ингредиентов для спагетти, советы grow a garden',
        'h1': '🍝 Как Сделать Спагетти в Grow a Garden',
        'subtitle': 'Полное Руководство: От Сбора Ингредиентов до Стола',
        'ingredients_title': '📋 Необходимые Ингредиенты',
        'steps_title': '👨‍🍳 Шаги Приготовления',
        'tips_title': '💡 Советы по Приготовлению',
        'back_btn': '← Назад к Руководствам'
    },
    'ar': {
        'lang_attr': 'lang="ar" dir="rtl"',
        'title': 'كيفية صنع السباغيتي في Grow a Garden - دليل شامل',
        'description': 'تعلم كيفية صنع السباغيتي اللذيذ في Roblox Grow a Garden! من تحضير المعكرونة إلى صنع الصلصة، بما في ذلك جميع نصائح صنع السباغيتي وأفضل تركيبات المكونات وطرق تحسين الكفاءة.',
        'keywords': 'كيفية صنع السباغيتي في grow a garden, وصفة السباغيتي roblox, دليل grow a garden, دليل صنع السباغيتي, لعبة المزرعة roblox, جمع مكونات السباغيتي, نصائح grow a garden',
        'h1': '🍝 كيفية صنع السباغيتي في Grow a Garden',
        'subtitle': 'دليل شامل: من جمع المكونات إلى المائدة',
        'ingredients_title': '📋 المكونات المطلوبة',
        'steps_title': '👨‍🍳 خطوات التحضير',
        'tips_title': '💡 نصائح التحضير',
        'back_btn': '← العودة إلى الأدلة'
    },
    'hi': {
        'lang_attr': 'lang="hi"',
        'title': 'Grow a Garden में स्पेगेटी कैसे बनाएं - पूर्ण गाइड',
        'description': 'Roblox Grow a Garden में स्वादिष्ट स्पेगेटी बनाना सीखें! पास्ता तैयारी से लेकर सॉस बनाने तक, स्पेगेटी बनाने के सभी टिप्स, सर्वोत्तम सामग्री संयोजन और दक्षता सुधार के तरीके शामिल हैं।',
        'keywords': 'grow a garden में स्पेगेटी कैसे बनाएं, roblox स्पेगेटी रेसिपी, grow a garden गाइड, स्पेगेटी बनाने का गाइड, roblox फार्मिंग गेम, स्पेगेटी सामग्री संग्रह, grow a garden टिप्स',
        'h1': '🍝 Grow a Garden में स्पेगेटी कैसे बनाएं',
        'subtitle': 'पूर्ण गाइड: सामग्री संग्रह से मेज तक',
        'ingredients_title': '📋 आवश्यक सामग्री',
        'steps_title': '👨‍🍳 तैयारी के चरण',
        'tips_title': '💡 तैयारी के टिप्स',
        'back_btn': '← गाइड पर वापस जाएं'
    },
    'id': {
        'lang_attr': 'lang="id"',
        'title': 'Cara Membuat Spaghetti di Grow a Garden - Panduan Lengkap',
        'description': 'Pelajari cara membuat spaghetti lezat di Roblox Grow a Garden! Dari persiapan pasta hingga pembuatan saus, termasuk semua tips membuat spaghetti, kombinasi bahan terbaik, dan metode untuk meningkatkan efisiensi.',
        'keywords': 'cara membuat spaghetti di grow a garden, resep spaghetti roblox, panduan grow a garden, panduan membuat spaghetti, permainan pertanian roblox, pengumpulan bahan spaghetti, tips grow a garden',
        'h1': '🍝 Cara Membuat Spaghetti di Grow a Garden',
        'subtitle': 'Panduan Lengkap: Dari Pengumpulan Bahan hingga Meja',
        'ingredients_title': '📋 Bahan yang Diperlukan',
        'steps_title': '👨‍🍳 Langkah-langkah Persiapan',
        'tips_title': '💡 Tips Persiapan',
        'back_btn': '← Kembali ke Panduan'
    },
    'vi': {
        'lang_attr': 'lang="vi"',
        'title': 'Cách Làm Mì Ý trong Grow a Garden - Hướng Dẫn Đầy Đủ',
        'description': 'Học cách làm mì Ý ngon trong Roblox Grow a Garden! Từ chuẩn bị mì đến làm nước sốt, bao gồm tất cả mẹo làm mì Ý, kết hợp nguyên liệu tốt nhất và phương pháp cải thiện hiệu quả.',
        'keywords': 'cách làm mì Ý trong grow a garden, công thức mì Ý roblox, hướng dẫn grow a garden, hướng dẫn làm mì Ý, trò chơi nông trại roblox, thu thập nguyên liệu mì Ý, mẹo grow a garden',
        'h1': '🍝 Cách Làm Mì Ý trong Grow a Garden',
        'subtitle': 'Hướng Dẫn Đầy Đủ: Từ Thu Thập Nguyên Liệu đến Bàn',
        'ingredients_title': '📋 Nguyên Liệu Cần Thiết',
        'steps_title': '👨‍🍳 Các Bước Chuẩn Bị',
        'tips_title': '💡 Mẹo Chuẩn Bị',
        'back_btn': '← Quay Lại Hướng Dẫn'
    },
    'ja': {
        'lang_attr': 'lang="ja"',
        'title': 'Grow a Gardenでスパゲッティの作り方 - 完全ガイド',
        'description': 'Roblox Grow a Gardenで美味しいスパゲッティの作り方を学びましょう！パスタの準備からソース作りまで、スパゲッティ作りのすべてのコツ、最高の材料の組み合わせ、効率を向上させる方法を含みます。',
        'keywords': 'grow a gardenでスパゲッティの作り方, robloxスパゲッティレシピ, grow a gardenガイド, スパゲッティ作りガイド, roblox農場ゲーム, スパゲッティ材料収集, grow a gardenコツ',
        'h1': '🍝 Grow a Gardenでスパゲッティの作り方',
        'subtitle': '完全ガイド：材料収集から食卓まで',
        'ingredients_title': '📋 必要な材料',
        'steps_title': '👨‍🍳 調理手順',
        'tips_title': '💡 調理のコツ',
        'back_btn': '← ガイドに戻る'
    }
}

def generate_html_content(lang_code, lang_config):
    """为指定语言生成HTML内容"""
    
    # 确定CSS类
    css_class = 'rtl' if lang_code == 'ar' else ''
    
    # 生成语言选择器选项
    lang_options = []
    for code, name in [
        ('en', 'English'),
        ('zh-cn', '简体中文'),
        ('es', 'Español'),
        ('pt-br', 'Português'),
        ('fr', 'Français'),
        ('de', 'Deutsch'),
        ('ru', 'Русский'),
        ('ar', 'العربية'),
        ('hi', 'हिन्दी'),
        ('id', 'Bahasa Indonesia'),
        ('vi', 'Tiếng Việt'),
        ('ja', '日本語')
    ]:
        selected = 'selected=""' if code == lang_code else ''
        lang_options.append(f'<option value="{code}" {selected}>{name}</option>')
    
    lang_options_html = '\n                '.join(lang_options)
    
    # 根据语言确定导航文本
    nav_text = {
        'en': '📚 Guides',
        'zh-cn': '📚 指南',
        'es': '📚 Guías',
        'pt-br': '📚 Guias',
        'fr': '📚 Guides',
        'de': '📚 Anleitungen',
        'ru': '📚 Руководства',
        'ar': '📚 الأدلة',
        'hi': '📚 गाइड',
        'id': '📚 Panduan',
        'vi': '📚 Hướng Dẫn',
        'ja': '📚 ガイド'
    }
    
    html_content = f'''<!DOCTYPE html>
<html {lang_config['lang_attr']}>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{lang_config['title']}</title>
  <meta name="description" content="{lang_config['description']}">
  <meta name="keywords" content="{lang_config['keywords']}">
  <link rel="canonical" href="https://growagarden.cv/{lang_code}/how-to-make-spaghetti.html">
  <link rel="alternate" hreflang="en" href="https://growagarden.cv/how-to-make-spaghetti.html">
  <link rel="alternate" hreflang="{lang_code}" href="https://growagarden.cv/{lang_code}/how-to-make-spaghetti.html">
  <link rel="alternate" hreflang="x-default" href="https://growagarden.cv/how-to-make-spaghetti.html">
  <link rel="stylesheet" href="https://unpkg.com/simple.css@2.1.0/simple.min.css">
  <link rel="stylesheet" href="/styles.css">
</head>
<body class="{css_class}">
  <header>
    <nav>
      <a href="/index.html" class="logo" data-i18n="nav.logo">🌱 Grow a Garden</a>
      <a href="/guides.html" data-i18n="nav.guides">{nav_text.get(lang_code, '📚 Guides')}</a>
                  <select id="lang-switcher" aria-label="Language">
                {lang_options_html}
            </select>
    </nav>
  </header>
  <main>
    <h1>{lang_config['h1']}</h1>
    <p>{lang_config['subtitle']}</p>
    
    <div class="guide-section">
      <div class="guide-card">
        <h2>{lang_config['ingredients_title']}</h2>
        <ul>
          <li>🌾 Wheat Flour - 2 cups</li>
          <li>🥚 Eggs - 2 pieces</li>
          <li>🍅 Tomatoes - 3 pieces</li>
          <li>🧄 Garlic - 2 cloves</li>
          <li>🌿 Basil - 1 bunch</li>
          <li>🧂 Salt - to taste</li>
        </ul>
      </div>

      <div class="guide-card">
        <h2>{lang_config['steps_title']}</h2>
        <ol>
          <li>Mix flour and eggs to make pasta dough</li>
          <li>Roll out the dough and cut into strips</li>
          <li>Boil the pasta in salted water</li>
          <li>Prepare tomato sauce with garlic and basil</li>
          <li>Combine pasta with sauce and serve</li>
        </ol>
      </div>

      <div class="guide-card">
        <h2>{lang_config['tips_title']}</h2>
        <ul>
          <li>Use fresh ingredients for better taste</li>
          <li>Don\'t overcook the pasta</li>
          <li>Save some pasta water for sauce consistency</li>
          <li>Add cheese on top for extra flavor</li>
        </ul>
      </div>

      <div class="guide-card" style="text-align:center;">
        <a href="/guides.html" class="back-btn">{lang_config['back_btn']}</a>
      </div>
    </div>
  </main>
  <script src="/i18n/i18n.js"></script>
</body>
</html>'''
    
    return html_content

def create_spaghetti_pages():
    """为所有语言创建how-to-make-spaghetti.html页面"""
    
    created_files = []
    error_files = []
    
    for lang_code, lang_config in LANGUAGES.items():
        file_path = f"{lang_code}/how-to-make-spaghetti.html"
        
        if not os.path.exists(f"{lang_code}"):
            print(f"跳过 {lang_code}: 目录不存在")
            continue
            
        try:
            # 生成新的HTML内容
            new_content = generate_html_content(lang_code, lang_config)
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ 已创建 {file_path}")
            created_files.append(file_path)
            
        except Exception as e:
            print(f"❌ 创建 {file_path} 时出错: {e}")
            error_files.append(file_path)
    
    print(f"\n📊 创建完成:")
    print(f"✅ 成功创建: {len(created_files)} 个文件")
    if error_files:
        print(f"❌ 创建失败: {len(error_files)} 个文件")
        for file in error_files:
            print(f"   - {file}")
    
    return created_files, error_files

if __name__ == "__main__":
    print("🍝 开始创建how-to-make-spaghetti.html页面...")
    created, errors = create_spaghetti_pages()
    
    if not errors:
        print("\n🎉 所有页面创建成功！")
    else:
        print(f"\n⚠️  有 {len(errors)} 个页面创建失败，请检查错误信息。") 