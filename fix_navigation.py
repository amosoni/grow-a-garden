#!/usr/bin/env python3
"""
修复所有攻略页面的导航栏，使其与首页保持一致
"""

import os
import re

# 语言配置
LANGUAGES = {
    'zh-cn': {
        'nav_live': '实时统计',
        'nav_map': '全球热力图',
        'nav_tips': '技巧',
        'nav_guides': '📚 指南',
        'nav_discord': '💬 Discord'
    },
    'es': {
        'nav_live': 'Estadísticas en Vivo',
        'nav_map': 'Mapa de Calor Global',
        'nav_tips': 'Consejos',
        'nav_guides': '📚 Guías',
        'nav_discord': '💬 Discord'
    },
    'pt-br': {
        'nav_live': 'Estatísticas ao Vivo',
        'nav_map': 'Mapa de Calor Global',
        'nav_tips': 'Dicas',
        'nav_guides': '📚 Guias',
        'nav_discord': '💬 Discord'
    },
    'fr': {
        'nav_live': 'Statistiques en Direct',
        'nav_map': 'Carte de Chaleur Mondiale',
        'nav_tips': 'Conseils',
        'nav_guides': '📚 Guides',
        'nav_discord': '💬 Discord'
    },
    'de': {
        'nav_live': 'Live-Statistiken',
        'nav_map': 'Globale Wärmekarte',
        'nav_tips': 'Tipps',
        'nav_guides': '📚 Anleitungen',
        'nav_discord': '💬 Discord'
    },
    'ru': {
        'nav_live': 'Живая Статистика',
        'nav_map': 'Глобальная Тепловая Карта',
        'nav_tips': 'Советы',
        'nav_guides': '📚 Руководства',
        'nav_discord': '💬 Discord'
    },
    'ar': {
        'nav_live': 'إحصائيات مباشرة',
        'nav_map': 'خريطة حرارية عالمية',
        'nav_tips': 'نصائح',
        'nav_guides': '📚 الأدلة',
        'nav_discord': '💬 Discord'
    },
    'hi': {
        'nav_live': 'लाइव आंकड़े',
        'nav_map': 'वैश्विक हीटमैप',
        'nav_tips': 'सुझाव',
        'nav_guides': '📚 गाइड',
        'nav_discord': '💬 Discord'
    },
    'id': {
        'nav_live': 'Statistik Langsung',
        'nav_map': 'Peta Panas Global',
        'nav_tips': 'Tips',
        'nav_guides': '📚 Panduan',
        'nav_discord': '💬 Discord'
    },
    'vi': {
        'nav_live': 'Thống Kê Trực Tiếp',
        'nav_map': 'Bản Đồ Nhiệt Toàn Cầu',
        'nav_tips': 'Mẹo',
        'nav_guides': '📚 Hướng Dẫn',
        'nav_discord': '💬 Discord'
    },
    'ja': {
        'nav_live': 'ライブ統計',
        'nav_map': 'グローバルヒートマップ',
        'nav_tips': 'ヒント',
        'nav_guides': '📚 ガイド',
        'nav_discord': '💬 Discord'
    }
}

def generate_navigation_html(lang_code, lang_config):
    """为指定语言生成完整的导航栏HTML"""
    
    # 确定语言方向和CSS类
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
    
    navigation_html = f'''  <header>
    <nav>
      <a href="/index.html" class="logo" data-i18n="nav.logo">🌱 Grow a Garden</a>
      <a href="/index.html#stats" data-i18n="nav.live">{lang_config['nav_live']}</a>
      <a href="/index.html#map" data-i18n="nav.map">{lang_config['nav_map']}</a>
      <a href="/index.html#tips" data-i18n="nav.tips">{lang_config['nav_tips']}</a>
      <a href="/guides.html" data-i18n="nav.guides">{lang_config['nav_guides']}</a>
      <a href="/index.html#community" class="discord-btn" data-i18n="nav.discord">{lang_config['nav_discord']}</a>
                  <select id="lang-switcher" aria-label="Language">
                {lang_options_html}
            </select>
    </nav>
  </header>'''
    
    return navigation_html

def fix_navigation_in_file(file_path, lang_code, lang_config):
    """修复单个文件中的导航栏"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 生成新的导航栏HTML
        new_navigation = generate_navigation_html(lang_code, lang_config)
        
        # 查找并替换现有的导航栏
        # 匹配从<header>开始到</header>结束的部分
        pattern = r'<header>.*?</header>'
        
        if re.search(pattern, content, re.DOTALL):
            # 替换现有的导航栏
            new_content = re.sub(pattern, new_navigation, content, flags=re.DOTALL)
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ 已修复 {file_path}")
            return True
        else:
            print(f"⚠️  在 {file_path} 中未找到导航栏")
            return False
            
    except Exception as e:
        print(f"❌ 修复 {file_path} 时出错: {e}")
        return False

def fix_all_guide_pages():
    """修复所有攻略页面的导航栏"""
    
    fixed_files = []
    error_files = []
    
    # 需要修复的页面类型
    guide_pages = [
        'guides.html',
        'how-to-make-spaghetti.html',
        'how-to-make-pizza.html',
        'how-to-make-bread.html',
        'how-to-make-cake.html',
        'how-to-make-cookies.html',
        'how-to-make-pie.html',
        'how-to-make-smoothie.html',
        'how-to-make-sandwich.html',
        'how-to-make-salad.html',
        'how-to-make-donut.html',
        'how-to-make-money-fast.html',
        'how-to-grow-apples.html',
        'how-to-grow-carrots.html',
        'how-to-grow-corn.html',
        'how-to-grow-oranges.html',
        'how-to-grow-berries.html',
        'how-to-grow-wheat.html',
        'how-to-build-farm.html',
        'how-to-play-with-friends.html',
        'storage-and-logistics.html',
        'ice-cream-recipe.html'
    ]
    
    for lang_code, lang_config in LANGUAGES.items():
        lang_dir = f"{lang_code}"
        
        if not os.path.exists(lang_dir):
            print(f"跳过 {lang_code}: 目录不存在")
            continue
        
        for page in guide_pages:
            file_path = f"{lang_dir}/{page}"
            
            if os.path.exists(file_path):
                if fix_navigation_in_file(file_path, lang_code, lang_config):
                    fixed_files.append(file_path)
                else:
                    error_files.append(file_path)
            else:
                print(f"跳过 {file_path}: 文件不存在")
    
    print(f"\n📊 修复完成:")
    print(f"✅ 成功修复: {len(fixed_files)} 个文件")
    if error_files:
        print(f"❌ 修复失败: {len(error_files)} 个文件")
        for file in error_files:
            print(f"   - {file}")
    
    return fixed_files, error_files

if __name__ == "__main__":
    print("🔧 开始修复攻略页面的导航栏...")
    fixed, errors = fix_all_guide_pages()
    
    if not errors:
        print("\n🎉 所有导航栏修复成功！")
    else:
        print(f"\n⚠️  有 {len(errors)} 个文件修复失败，请检查错误信息。") 