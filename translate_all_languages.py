#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有语言目录的攻略页面创建完整翻译
"""

import re
from pathlib import Path

def get_translations():
    """获取所有语言的翻译"""
    return {
        "zh-cn": {
            "nav": {"logo": "🌱 种植花园", "live": "实时统计", "map": "全球热力图", "tips": "技巧", "guides": "📚 攻略", "discord": "💬 Discord"},
            "breadcrumb": {"home": "🏠 首页", "guides": "📚 攻略"},
            "content": {"toc": "📋 目录"}
        },
        "ja": {
            "nav": {"logo": "🌱 ガーデン栽培", "live": "ライブ統計", "map": "グローバルヒートマップ", "tips": "ヒント", "guides": "📚 ガイド", "discord": "💬 Discord"},
            "breadcrumb": {"home": "🏠 ホーム", "guides": "📚 ガイド"},
            "content": {"toc": "📋 目次"}
        },
        "es": {
            "nav": {"logo": "🌱 Cultiva un Jardín", "live": "Estadísticas en Vivo", "map": "Mapa de Calor Global", "tips": "Consejos", "guides": "📚 Guías", "discord": "💬 Discord"},
            "breadcrumb": {"home": "🏠 Inicio", "guides": "📚 Guías"},
            "content": {"toc": "📋 Tabla de Contenidos"}
        },
        "pt-br": {
            "nav": {"logo": "🌱 Cultive um Jardim", "live": "Estatísticas ao Vivo", "map": "Mapa de Calor Global", "tips": "Dicas", "guides": "📚 Guias", "discord": "💬 Discord"},
            "breadcrumb": {"home": "🏠 Início", "guides": "📚 Guias"},
            "content": {"toc": "📋 Índice"}
        },
        "fr": {
            "nav": {"logo": "🌱 Cultivez un Jardin", "live": "Statistiques en Direct", "map": "Carte de Chaleur Globale", "tips": "Conseils", "guides": "📚 Guides", "discord": "💬 Discord"},
            "breadcrumb": {"home": "🏠 Accueil", "guides": "📚 Guides"},
            "content": {"toc": "📋 Table des Matières"}
        },
        "de": {
            "nav": {"logo": "🌱 Züchte einen Garten", "live": "Live-Statistiken", "map": "Globale Wärmekarte", "tips": "Tipps", "guides": "📚 Anleitungen", "discord": "💬 Discord"},
            "breadcrumb": {"home": "🏠 Startseite", "guides": "📚 Anleitungen"},
            "content": {"toc": "📋 Inhaltsverzeichnis"}
        },
        "ru": {
            "nav": {"logo": "🌱 Вырасти Сад", "live": "Живая Статистика", "map": "Глобальная Тепловая Карта", "tips": "Советы", "guides": "📚 Руководства", "discord": "💬 Discord"},
            "breadcrumb": {"home": "🏠 Главная", "guides": "📚 Руководства"},
            "content": {"toc": "📋 Содержание"}
        },
        "ar": {
            "nav": {"logo": "🌱 ازرع حديقة", "live": "إحصائيات مباشرة", "map": "خريطة حرارية عالمية", "tips": "نصائح", "guides": "📚 أدلة", "discord": "💬 Discord"},
            "breadcrumb": {"home": "🏠 الرئيسية", "guides": "📚 أدلة"},
            "content": {"toc": "📋 جدول المحتويات"}
        },
        "hi": {
            "nav": {"logo": "🌱 बगीचा उगाएं", "live": "लाइव आंकड़े", "map": "वैश्विक हीटमैप", "tips": "सुझाव", "guides": "📚 गाइड", "discord": "💬 Discord"},
            "breadcrumb": {"home": "🏠 होम", "guides": "📚 गाइड"},
            "content": {"toc": "📋 सामग्री"}
        },
        "id": {
            "nav": {"logo": "🌱 Tumbuh Kebun", "live": "Statistik Langsung", "map": "Peta Panas Global", "tips": "Tips", "guides": "📚 Panduan", "discord": "💬 Discord"},
            "breadcrumb": {"home": "🏠 Beranda", "guides": "📚 Panduan"},
            "content": {"toc": "📋 Daftar Isi"}
        },
        "vi": {
            "nav": {"logo": "🌱 Trồng Vườn", "live": "Thống Kê Trực Tiếp", "map": "Bản Đồ Nhiệt Toàn Cầu", "tips": "Mẹo", "guides": "📚 Hướng Dẫn", "discord": "💬 Discord"},
            "breadcrumb": {"home": "🏠 Trang Chủ", "guides": "📚 Hướng Dẫn"},
            "content": {"toc": "📋 Mục Lục"}
        }
    }

def apply_translation(file_path, lang_code):
    """应用翻译"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        translations = get_translations()
        
        if lang_code not in translations:
            return False
        
        translation = translations[lang_code]
        
        # 翻译导航栏
        for key, value in translation["nav"].items():
            pattern = rf'data-i18n="nav\.{key}"[^>]*>([^<]+)</a>'
            replacement = f'data-i18n="nav.{key}">{value}</a>'
            content = re.sub(pattern, replacement, content)
        
        # 翻译面包屑
        for key, value in translation["breadcrumb"].items():
            if key == "home":
                pattern = r'(<a href="[^"]*">)🏠 Home(</a>)'
                replacement = rf'\1{value}\2'
                content = re.sub(pattern, replacement, content)
            elif key == "guides":
                pattern = r'(<a href="[^"]*">)📚 Guides(</a>)'
                replacement = rf'\1{value}\2'
                content = re.sub(pattern, replacement, content)
        
        # 翻译内容
        for key, value in translation["content"].items():
            if key == "toc":
                pattern = r'(<h2[^>]*>)[^<]*Table of Contents[^<]*(</h2>)'
                replacement = rf'\1{value}\2'
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已应用 {lang_code} 翻译: {file_path.name}")
            return True
        else:
            print(f"⏭️  无需修改: {file_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ 失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始为所有语言创建翻译...")
    
    language_dirs = ["zh-cn", "ja", "es", "pt-br", "fr", "de", "ru", "ar", "hi", "id", "vi"]
    total_translated = 0
    
    for lang_dir in language_dirs:
        lang_path = Path(lang_dir)
        if not lang_path.exists():
            continue
            
        print(f"\n🔧 处理语言目录: {lang_dir}")
        
        guide_files = []
        for pattern in ['how-to-*.html', '*-guide.html', '*-strategies.html', '*-basics.html', '*-tips.html']:
            guide_files.extend(lang_path.glob(pattern))
        
        if not guide_files:
            continue
        
        print(f"   📁 找到 {len(guide_files)} 个攻略页面")
        
        for file_path in guide_files:
            if apply_translation(file_path, lang_dir):
                total_translated += 1
    
    print(f"\n🎉 所有语言翻译完成！")
    print(f"📊 成功翻译: {total_translated} 个文件")

if __name__ == "__main__":
    main() 