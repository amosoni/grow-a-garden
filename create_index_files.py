#!/usr/bin/env python3
import os

# 语言配置
LANGUAGES = {
    'fr': {
        'title': 'Calculatrice Grow a Garden - Outil de Valeur des Fruits et Mutation Roblox',
        'h1': '🌱 Calculatrice Grow a Garden',
        'h2': 'Outil de Valeur des Fruits et Mutation Roblox',
        'p': 'Entrez les informations de la plante pour calculer instantanément la valeur de mutation. Le multiplicateur de mutation Roblox Grow a Garden le plus précis.',
        'nav_live': 'Statistiques en Direct',
        'nav_map': 'Carte de Chaleur Globale',
        'nav_tips': 'Conseils',
        'nav_guides': '📚 Guides',
        'nav_discord': '💬 Communication'
    },
    'de': {
        'title': 'Grow a Garden Rechner - Roblox Fruchtwert und Mutation Tool',
        'h1': '🌱 Grow a Garden Rechner',
        'h2': 'Roblox Fruchtwert und Mutation Tool',
        'p': 'Geben Sie Pflanzeninformationen ein, um den Mutationswert sofort zu berechnen. Der genaueste Roblox Grow a Garden Mutationsmultiplikator.',
        'nav_live': 'Live-Statistiken',
        'nav_map': 'Globale Wärmekarte',
        'nav_tips': 'Tipps',
        'nav_guides': '📚 Anleitungen',
        'nav_discord': '💬 Kommunikation'
    },
    'ru': {
        'title': 'Калькулятор Grow a Garden - Инструмент стоимости фруктов и мутаций Roblox',
        'h1': '🌱 Калькулятор Grow a Garden',
        'h2': 'Инструмент стоимости фруктов и мутаций Roblox',
        'p': 'Введите информацию о растении для мгновенного расчета стоимости мутации. Самый точный множитель мутации Roblox Grow a Garden.',
        'nav_live': 'Живая статистика',
        'nav_map': 'Глобальная тепловая карта',
        'nav_tips': 'Советы',
        'nav_guides': '📚 Руководства',
        'nav_discord': '💬 Общение'
    },
    'ja': {
        'title': 'Grow a Garden 計算機 - Roblox フルーツ価値とミューテーション ツール',
        'h1': '🌱 Grow a Garden 計算機',
        'h2': 'Roblox フルーツ価値とミューテーション ツール',
        'p': '植物情報を入力してミューテーション価値を即座に計算します。最も正確なRoblox Grow a Gardenミューテーション乗数。',
        'nav_live': 'ライブ統計',
        'nav_map': 'グローバルヒートマップ',
        'nav_tips': 'ヒント',
        'nav_guides': '📚 ガイド',
        'nav_discord': '💬 コミュニケーション'
    }
}

def create_index_file(lang_code, lang_config):
    """创建index.html文件"""
    content = f'''<!DOCTYPE html>
<html lang="{lang_code}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{lang_config['title']}</title>
  <link rel="canonical" href="https://growagarden.cv/{lang_code}/index.html">
  <link rel="alternate" hreflang="en" href="https://growagarden.cv/en/index.html">
  <link rel="alternate" hreflang="zh-CN" href="https://growagarden.cv/zh-cn/index.html">
  <link rel="alternate" hreflang="{lang_code}" href="https://growagarden.cv/{lang_code}/index.html">
  <link rel="alternate" hreflang="x-default" href="https://growagarden.cv/index.html">
  <link rel="stylesheet" href="https://unpkg.com/simple.css@2.1.0/simple.min.css">
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <header>
    <nav>
      <a href="/index.html" class="logo" data-i18n="nav.logo">🌱 Grow a Garden</a>
      <a href="javascript:void(0)" onclick="scrollToSection('stats')" data-i18n="nav.live">{lang_config['nav_live']}</a>
      <a href="javascript:void(0)" onclick="scrollToSection('map')" data-i18n="nav.map">{lang_config['nav_map']}</a>
      <a href="javascript:void(0)" onclick="scrollToSection('tips')" data-i18n="nav.tips">{lang_config['nav_tips']}</a>
      <a href="/guides.html" data-i18n="nav.guides">{lang_config['nav_guides']}</a>
      <a href="javascript:void(0)" onclick="scrollToSection('community')" class="discord-btn" data-i18n="nav.discord">{lang_config['nav_discord']}</a>
                  <select id="lang-switcher" aria-label="Language">
                <option value="en">English</option>
                <option value="zh-cn">简体中文</option>
                <option value="es">Español</option>
                <option value="pt-br">Português</option>
                <option value="fr">Français</option>
                <option value="de">Deutsch</option>
                <option value="ru">Русский</option>
                <option value="ar">العربية</option>
                <option value="hi">हिन्दी</option>
                <option value="id">Bahasa Indonesia</option>
                <option value="vi">Tiếng Việt</option>
                <option value="ja">日本語</option>
            </select>
    </nav>
  </header>
  <section class="hero">
    <div class="hero-blur-bg"></div>
    <div class="hero-content">
      <div class="hero-glass">
        <h1>{lang_config['h1']}</h1>
        <h2>{lang_config['h2']}</h2>
        <p class="hero-subtitle">{lang_config['p']}</p>
      </div>
    </div>
  </section>
  <script src="/i18n/i18n.js"></script>
  <script src="/script.js"></script>
</body>
</html>'''
    
    file_path = f"{lang_code}/index.html"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created: {file_path}")

def main():
    """主函数"""
    print("🔧 Creating missing index.html files for all languages...")
    
    for lang_code, lang_config in LANGUAGES.items():
        if not os.path.exists(f"{lang_code}/index.html"):
            create_index_file(lang_code, lang_config)
        else:
            print(f"⚠️  Already exists: {lang_code}/index.html")
    
    print("\n🎉 All index.html files created!")

if __name__ == "__main__":
    main() 