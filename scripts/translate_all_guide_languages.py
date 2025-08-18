#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有语言目录的攻略页面创建完整翻译
确保每个攻略页面都使用对应语言
"""

import re
from pathlib import Path

def get_all_language_translations():
    """获取所有语言的翻译"""
    return {
        "zh-cn": {
            "nav": {
                "logo": "🌱 种植花园",
                "live": "实时统计",
                "map": "全球热力图",
                "tips": "技巧",
                "guides": "📚 攻略",
                "discord": "💬 Discord"
            },
            "breadcrumb": {
                "home": "🏠 首页",
                "guides": "📚 攻略"
            },
            "content": {
                "toc": "📋 目录",
                "basics": "基础制作",
                "ingredients": "关键食材",
                "recipes": "高级食谱",
                "tips": "制作技巧",
                "efficiency": "效率提升",
                "faq": "常见问题"
            }
        },
        "ja": {
            "nav": {
                "logo": "🌱 ガーデン栽培",
                "live": "ライブ統計",
                "map": "グローバルヒートマップ",
                "tips": "ヒント",
                "guides": "📚 ガイド",
                "discord": "💬 Discord"
            },
            "breadcrumb": {
                "home": "🏠 ホーム",
                "guides": "📚 ガイド"
            },
            "content": {
                "toc": "📋 目次",
                "basics": "基本制作",
                "ingredients": "主要材料",
                "recipes": "上級レシピ",
                "tips": "制作のコツ",
                "efficiency": "効率向上",
                "faq": "よくある質問"
            }
        },
        "es": {
            "nav": {
                "logo": "🌱 Cultiva un Jardín",
                "live": "Estadísticas en Vivo",
                "map": "Mapa de Calor Global",
                "tips": "Consejos",
                "guides": "📚 Guías",
                "discord": "💬 Discord"
            },
            "breadcrumb": {
                "home": "🏠 Inicio",
                "guides": "📚 Guías"
            },
            "content": {
                "toc": "📋 Tabla de Contenidos",
                "basics": "Básicos",
                "ingredients": "Ingredientes",
                "recipes": "Recetas",
                "tips": "Consejos",
                "efficiency": "Eficiencia",
                "faq": "Preguntas Frecuentes"
            }
        },
        "pt-br": {
            "nav": {
                "logo": "🌱 Cultive um Jardim",
                "live": "Estatísticas ao Vivo",
                "map": "Mapa de Calor Global",
                "tips": "Dicas",
                "guides": "📚 Guias",
                "discord": "💬 Discord"
            },
            "breadcrumb": {
                "home": "🏠 Início",
                "guides": "📚 Guias"
            },
            "content": {
                "toc": "📋 Índice",
                "basics": "Básicos",
                "ingredients": "Ingredientes",
                "recipes": "Receitas",
                "tips": "Dicas",
                "efficiency": "Eficiência",
                "faq": "Perguntas Frequentes"
            }
        },
        "fr": {
            "nav": {
                "logo": "🌱 Cultivez un Jardin",
                "live": "Statistiques en Direct",
                "map": "Carte de Chaleur Globale",
                "tips": "Conseils",
                "guides": "📚 Guides",
                "discord": "💬 Discord"
            },
            "breadcrumb": {
                "home": "🏠 Accueil",
                "guides": "📚 Guides"
            },
            "content": {
                "toc": "📋 Table des Matières",
                "basics": "Bases",
                "ingredients": "Ingrédients",
                "recipes": "Recettes",
                "tips": "Conseils",
                "efficiency": "Efficacité",
                "faq": "Questions Fréquentes"
            }
        },
        "de": {
            "nav": {
                "logo": "🌱 Züchte einen Garten",
                "live": "Live-Statistiken",
                "map": "Globale Wärmekarte",
                "tips": "Tipps",
                "guides": "📚 Anleitungen",
                "discord": "💬 Discord"
            },
            "breadcrumb": {
                "home": "🏠 Startseite",
                "guides": "📚 Anleitungen"
            },
            "content": {
                "toc": "📋 Inhaltsverzeichnis",
                "basics": "Grundlagen",
                "ingredients": "Zutaten",
                "recipes": "Rezepte",
                "tips": "Tipps",
                "efficiency": "Effizienz",
                "faq": "Häufige Fragen"
            }
        },
        "ru": {
            "nav": {
                "logo": "🌱 Вырасти Сад",
                "live": "Живая Статистика",
                "map": "Глобальная Тепловая Карта",
                "tips": "Советы",
                "guides": "📚 Руководства",
                "discord": "💬 Discord"
            },
            "breadcrumb": {
                "home": "🏠 Главная",
                "guides": "📚 Руководства"
            },
            "content": {
                "toc": "📋 Содержание",
                "basics": "Основы",
                "ingredients": "Ингредиенты",
                "recipes": "Рецепты",
                "tips": "Советы",
                "efficiency": "Эффективность",
                "faq": "Частые Вопросы"
            }
        },
        "ar": {
            "nav": {
                "logo": "🌱 ازرع حديقة",
                "live": "إحصائيات مباشرة",
                "map": "خريطة حرارية عالمية",
                "tips": "نصائح",
                "guides": "📚 أدلة",
                "discord": "💬 Discord"
            },
            "breadcrumb": {
                "home": "🏠 الرئيسية",
                "guides": "📚 أدلة"
            },
            "content": {
                "toc": "📋 جدول المحتويات",
                "basics": "أساسيات",
                "ingredients": "مكونات",
                "recipes": "وصفات",
                "tips": "نصائح",
                "efficiency": "كفاءة",
                "faq": "أسئلة شائعة"
            }
        },
        "hi": {
            "nav": {
                "logo": "🌱 बगीचा उगाएं",
                "live": "लाइव आंकड़े",
                "map": "वैश्विक हीटमैप",
                "tips": "सुझाव",
                "guides": "📚 गाइड",
                "discord": "💬 Discord"
            },
            "breadcrumb": {
                "home": "🏠 होम",
                "guides": "📚 गाइड"
            },
            "content": {
                "toc": "📋 सामग्री",
                "basics": "मूल बातें",
                "ingredients": "सामग्री",
                "recipes": "व्यंजन",
                "tips": "सुझाव",
                "efficiency": "दक्षता",
                "faq": "सामान्य प्रश्न"
            }
        },
        "id": {
            "nav": {
                "logo": "🌱 Tumbuh Kebun",
                "live": "Statistik Langsung",
                "map": "Peta Panas Global",
                "tips": "Tips",
                "guides": "📚 Panduan",
                "discord": "💬 Discord"
            },
            "breadcrumb": {
                "home": "🏠 Beranda",
                "guides": "📚 Panduan"
            },
            "content": {
                "toc": "📋 Daftar Isi",
                "basics": "Dasar",
                "ingredients": "Bahan",
                "recipes": "Resep",
                "tips": "Tips",
                "efficiency": "Efisiensi",
                "faq": "Pertanyaan Umum"
            }
        },
        "vi": {
            "nav": {
                "logo": "🌱 Trồng Vườn",
                "live": "Thống Kê Trực Tiếp",
                "map": "Bản Đồ Nhiệt Toàn Cầu",
                "tips": "Mẹo",
                "guides": "📚 Hướng Dẫn",
                "discord": "💬 Discord"
            },
            "breadcrumb": {
                "home": "🏠 Trang Chủ",
                "guides": "📚 Hướng Dẫn"
            },
            "content": {
                "toc": "📋 Mục Lục",
                "basics": "Cơ Bản",
                "ingredients": "Nguyên Liệu",
                "recipes": "Công Thức",
                "tips": "Mẹo",
                "efficiency": "Hiệu Quả",
                "faq": "Câu Hỏi Thường Gặp"
            }
        }
    }

def apply_language_translation(file_path, language_code):
    """应用语言翻译到攻略页面"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        translations = get_all_language_translations()
        
        if language_code not in translations:
            return False
        
        translation = translations[language_code]
        
        # 1. 翻译导航栏
        for key, value in translation["nav"].items():
            pattern = rf'data-i18n="nav\.{key}"[^>]*>([^<]+)</a>'
            replacement = f'data-i18n="nav.{key}">{value}</a>'
            content = re.sub(pattern, replacement, content)
        
        # 2. 翻译面包屑导航
        for key, value in translation["breadcrumb"].items():
            if key == "home":
                pattern = r'(<a href="[^"]*">)🏠 Home(</a>)'
                replacement = rf'\1{value}\2'
                content = re.sub(pattern, replacement, content)
            elif key == "guides":
                pattern = r'(<a href="[^"]*">)📚 Guides(</a>)'
                replacement = rf'\1{value}\2'
                content = re.sub(pattern, replacement, content)
        
        # 3. 翻译页面内容
        for key, value in translation["content"].items():
            if key == "toc":
                pattern = r'(<h2[^>]*>)[^<]*Table of Contents[^<]*(</h2>)'
                replacement = rf'\1{value}\2'
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已应用 {language_code} 翻译: {file_path.name}")
            return True
        else:
            print(f"⏭️  无需修改: {file_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ 应用翻译失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始为所有语言目录的攻略页面创建翻译...")
    
    # 所有语言目录
    language_dirs = [
        "zh-cn", "ja", "es", "pt-br", "fr", "de", 
        "ru", "ar", "hi", "id", "vi"
    ]
    
    total_translated = 0
    
    for lang_dir in language_dirs:
        lang_path = Path(lang_dir)
        if not lang_path.exists():
            print(f"⚠️  语言目录不存在: {lang_dir}")
            continue
            
        print(f"\n🔧 正在处理语言目录: {lang_dir}")
        
        # 查找该语言目录下的所有攻略页面
        guide_files = []
        for pattern in ['how-to-*.html', '*-guide.html', '*-strategies.html', '*-basics.html', '*-tips.html']:
            guide_files.extend(lang_path.glob(pattern))
        
        if not guide_files:
            print(f"   ⏭️  该语言目录下没有攻略页面")
            continue
        
        print(f"   📁 找到 {len(guide_files)} 个攻略页面")
        
        # 应用翻译到每个文件
        for file_path in guide_files:
            if apply_language_translation(file_path, lang_dir):
                total_translated += 1
    
    print(f"\n🎉 所有语言攻略页面翻译完成！")
    print(f"📊 成功翻译: {total_translated} 个文件")
    print("✨ 现在所有攻略页面都使用对应语言了！")

if __name__ == "__main__":
    main() 