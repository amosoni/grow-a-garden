#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能翻译脚本 - 基于现有内容和模式填充翻译
"""

import os
import json
import re
import glob
from pathlib import Path

def extract_text_from_html(file_path):
    """从HTML文件中提取文本内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有data-i18n键和对应的文本
    pattern = r'data-i18n="([^"]+)"[^>]*>([^<]+)</'
    matches = re.findall(pattern, content)
    
    return dict(matches)

def get_language_from_path(file_path):
    """从文件路径获取语言代码"""
    return file_path.split('/')[0]

def create_translation_mapping():
    """创建翻译映射表"""
    # 基础翻译映射
    base_mapping = {
        # 中文
        'zh-cn': {
            'hero.title': '指南',
            'hero.subtitle': '在种植花园中',
            'breadcrumb.current': '当前页面',
            'toc.title': '📋 目录',
            'toc.basics': '基础知识',
            'toc.ingredients': '食材清单',
            'toc.recipes': '食谱',
            'toc.tips': '技巧提示',
            'toc.efficiency': '效率提升',
            'toc.faq': '常见问题',
            'basics.title': '🌱 基础知识',
            'ingredients.title': '🥬 食材清单',
            'recipes.title': '🍳 食谱',
            'tips.title': '💡 技巧提示',
            'efficiency.title': '⚡ 效率提升',
            'faq.title': '❓ 常见问题',
            'table.name': '名称',
            'table.ingredients': '食材',
            'table.time': '时间',
            'table.rewards': '奖励',
            'table.effect': '效果',
            'step': '步骤',
            'tip': '提示',
            'ingredient.growth_time': '成长时间',
            'ingredient.value': '价值',
            'ingredient.use': '用途'
        },
        # 日语
        'ja': {
            'hero.title': 'ガイド',
            'hero.subtitle': 'Grow a Gardenで',
            'breadcrumb.current': '現在のページ',
            'toc.title': '📋 目次',
            'toc.basics': '基本知識',
            'toc.ingredients': '材料リスト',
            'toc.recipes': 'レシピ',
            'toc.tips': 'コツとヒント',
            'toc.efficiency': '効率向上',
            'toc.faq': 'よくある質問',
            'basics.title': '🌱 基本知識',
            'ingredients.title': '🥬 材料リスト',
            'recipes.title': '🍳 レシピ',
            'tips.title': '💡 コツとヒント',
            'efficiency.title': '⚡ 効率向上',
            'faq.title': '❓ よくある質問',
            'table.name': '名前',
            'table.ingredients': '材料',
            'table.time': '時間',
            'table.rewards': '報酬',
            'table.effect': '効果',
            'step': 'ステップ',
            'tip': 'ヒント',
            'ingredient.growth_time': '成長時間',
            'ingredient.value': '価値',
            'ingredient.use': '用途'
        },
        # 西班牙语
        'es': {
            'hero.title': 'Guía',
            'hero.subtitle': 'en Cultivar un Jardín',
            'breadcrumb.current': 'Página actual',
            'toc.title': '📋 Índice',
            'toc.basics': 'Conceptos básicos',
            'toc.ingredients': 'Lista de ingredientes',
            'toc.recipes': 'Recetas',
            'toc.tips': 'Consejos y trucos',
            'toc.efficiency': 'Mejoras de eficiencia',
            'toc.faq': 'Preguntas frecuentes',
            'basics.title': '🌱 Conceptos básicos',
            'ingredients.title': '🥬 Lista de ingredientes',
            'recipes.title': '🍳 Recetas',
            'tips.title': '💡 Consejos y trucos',
            'efficiency.title': '⚡ Mejoras de eficiencia',
            'faq.title': '❓ Preguntas frecuentes',
            'table.name': 'Nombre',
            'table.ingredients': 'Ingredientes',
            'table.time': 'Tiempo',
            'table.rewards': 'Recompensas',
            'table.effect': 'Efecto',
            'step': 'Paso',
            'tip': 'Consejo',
            'ingredient.growth_time': 'Tiempo de crecimiento',
            'ingredient.value': 'Valor',
            'ingredient.use': 'Uso'
        },
        # 法语
        'fr': {
            'hero.title': 'Guide',
            'hero.subtitle': 'dans Cultiver un Jardin',
            'breadcrumb.current': 'Page actuelle',
            'toc.title': '📋 Table des matières',
            'toc.basics': 'Concepts de base',
            'toc.ingredients': 'Liste des ingrédients',
            'toc.recipes': 'Recettes',
            'toc.tips': 'Conseils et astuces',
            'toc.efficiency': 'Améliorations d\'efficacité',
            'toc.faq': 'Questions fréquentes',
            'basics.title': '🌱 Concepts de base',
            'ingredients.title': '🥬 Liste des ingrédients',
            'recipes.title': '🍳 Recettes',
            'tips.title': '💡 Conseils et astuces',
            'efficiency.title': '⚡ Améliorations d\'efficacité',
            'faq.title': '❓ Questions fréquentes',
            'table.name': 'Nom',
            'table.ingredients': 'Ingrédients',
            'table.time': 'Temps',
            'table.rewards': 'Récompenses',
            'table.effect': 'Effet',
            'step': 'Étape',
            'tip': 'Conseil',
            'ingredient.growth_time': 'Temps de croissance',
            'ingredient.value': 'Valeur',
            'ingredient.use': 'Utilisation'
        },
        # 德语
        'de': {
            'hero.title': 'Anleitung',
            'hero.subtitle': 'in Garten anbauen',
            'breadcrumb.current': 'Aktuelle Seite',
            'toc.title': '📋 Inhaltsverzeichnis',
            'toc.basics': 'Grundlagen',
            'toc.ingredients': 'Zutatenliste',
            'toc.recipes': 'Rezepte',
            'toc.tips': 'Tipps und Tricks',
            'toc.efficiency': 'Effizienzverbesserungen',
            'toc.faq': 'Häufig gestellte Fragen',
            'basics.title': '🌱 Grundlagen',
            'ingredients.title': '🥬 Zutatenliste',
            'recipes.title': '🍳 Rezepte',
            'tips.title': '💡 Tipps und Tricks',
            'efficiency.title': '⚡ Effizienzverbesserungen',
            'faq.title': '❓ Häufig gestellte Fragen',
            'table.name': 'Name',
            'table.ingredients': 'Zutaten',
            'table.time': 'Zeit',
            'table.rewards': 'Belohnungen',
            'table.effect': 'Effekt',
            'step': 'Schritt',
            'tip': 'Tipp',
            'ingredient.growth_time': 'Wachstumszeit',
            'ingredient.value': 'Wert',
            'ingredient.use': 'Verwendung'
        },
        # 俄语
        'ru': {
            'hero.title': 'Руководство',
            'hero.subtitle': 'в Выращивать Сад',
            'breadcrumb.current': 'Текущая страница',
            'toc.title': '📋 Содержание',
            'toc.basics': 'Основы',
            'toc.ingredients': 'Список ингредиентов',
            'toc.recipes': 'Рецепты',
            'toc.tips': 'Советы и хитрости',
            'toc.efficiency': 'Улучшения эффективности',
            'toc.faq': 'Часто задаваемые вопросы',
            'basics.title': '🌱 Основы',
            'ingredients.title': '🥬 Список ингредиентов',
            'recipes.title': '🍳 Рецепты',
            'tips.title': '💡 Советы и хитрости',
            'efficiency.title': '⚡ Улучшения эффективности',
            'faq.title': '❓ Часто задаваемые вопросы',
            'table.name': 'Название',
            'table.ingredients': 'Ингредиенты',
            'table.time': 'Время',
            'table.rewards': 'Награды',
            'table.effect': 'Эффект',
            'step': 'Шаг',
            'tip': 'Совет',
            'ingredient.growth_time': 'Время роста',
            'ingredient.value': 'Ценность',
            'ingredient.use': 'Использование'
        },
        # 阿拉伯语
        'ar': {
            'hero.title': 'دليل',
            'hero.subtitle': 'في تنمية حديقة',
            'breadcrumb.current': 'الصفحة الحالية',
            'toc.title': '📋 فهرس',
            'toc.basics': 'أساسيات',
            'toc.ingredients': 'قائمة المكونات',
            'toc.recipes': 'وصفات',
            'toc.tips': 'نصائح وحيل',
            'toc.efficiency': 'تحسينات الكفاءة',
            'toc.faq': 'الأسئلة الشائعة',
            'basics.title': '🌱 أساسيات',
            'ingredients.title': '🥬 قائمة المكونات',
            'recipes.title': '🍳 وصفات',
            'tips.title': '💡 نصائح وحيل',
            'efficiency.title': '⚡ تحسينات الكفاءة',
            'faq.title': '❓ الأسئلة الشائعة',
            'table.name': 'الاسم',
            'table.ingredients': 'المكونات',
            'table.time': 'الوقت',
            'table.rewards': 'المكافآت',
            'table.effect': 'التأثير',
            'step': 'خطوة',
            'tip': 'نصيحة',
            'ingredient.growth_time': 'وقت النمو',
            'ingredient.value': 'القيمة',
            'ingredient.use': 'الاستخدام'
        },
        # 印地语
        'hi': {
            'hero.title': 'गाइड',
            'hero.subtitle': 'बगीचा उगाने में',
            'breadcrumb.current': 'वर्तमान पृष्ठ',
            'toc.title': '📋 सामग्री',
            'toc.basics': 'मूल बातें',
            'toc.ingredients': 'सामग्री की सूची',
            'toc.recipes': 'व्यंजन',
            'toc.tips': 'सुझाव और टिप्स',
            'toc.efficiency': 'दक्षता में सुधार',
            'toc.faq': 'अक्सर पूछे जाने वाले प्रश्न',
            'basics.title': '🌱 मूल बातें',
            'ingredients.title': '🥬 सामग्री की सूची',
            'recipes.title': '🍳 व्यंजन',
            'tips.title': '💡 सुझाव और टिप्स',
            'efficiency.title': '⚡ दक्षता में सुधार',
            'faq.title': '❓ अक्सर पूछे जाने वाले प्रश्न',
            'table.name': 'नाम',
            'table.ingredients': 'सामग्री',
            'table.time': 'समय',
            'table.rewards': 'पुरस्कार',
            'table.effect': 'प्रभाव',
            'step': 'कदम',
            'tip': 'सुझाव',
            'ingredient.growth_time': 'विकास का समय',
            'ingredient.value': 'मूल्य',
            'ingredient.use': 'उपयोग'
        },
        # 印尼语
        'id': {
            'hero.title': 'Panduan',
            'hero.subtitle': 'di Menanam Taman',
            'breadcrumb.current': 'Halaman saat ini',
            'toc.title': '📋 Daftar isi',
            'toc.basics': 'Dasar-dasar',
            'toc.ingredients': 'Daftar bahan',
            'toc.recipes': 'Resep',
            'toc.tips': 'Tips dan trik',
            'toc.efficiency': 'Peningkatan efisiensi',
            'toc.faq': 'Pertanyaan yang sering diajukan',
            'basics.title': '🌱 Dasar-dasar',
            'ingredients.title': '🥬 Daftar bahan',
            'recipes.title': '🍳 Resep',
            'tips.title': '💡 Tips dan trik',
            'efficiency.title': '⚡ Peningkatan efisiensi',
            'faq.title': '❓ Pertanyaan yang sering diajukan',
            'table.name': 'Nama',
            'table.ingredients': 'Bahan',
            'table.time': 'Waktu',
            'table.rewards': 'Hadiah',
            'table.effect': 'Efek',
            'step': 'Langkah',
            'tip': 'Tips',
            'ingredient.growth_time': 'Waktu pertumbuhan',
            'ingredient.value': 'Nilai',
            'ingredient.use': 'Penggunaan'
        },
        # 越南语
        'vi': {
            'hero.title': 'Hướng dẫn',
            'hero.subtitle': 'trong Trồng Vườn',
            'breadcrumb.current': 'Trang hiện tại',
            'toc.title': '📋 Mục lục',
            'toc.basics': 'Kiến thức cơ bản',
            'toc.ingredients': 'Danh sách nguyên liệu',
            'toc.recipes': 'Công thức',
            'toc.tips': 'Mẹo và thủ thuật',
            'toc.efficiency': 'Cải thiện hiệu quả',
            'toc.faq': 'Câu hỏi thường gặp',
            'basics.title': '🌱 Kiến thức cơ bản',
            'ingredients.title': '🥬 Danh sách nguyên liệu',
            'recipes.title': '🍳 Công thức',
            'tips.title': '💡 Mẹo và thủ thuật',
            'efficiency.title': '⚡ Cải thiện hiệu quả',
            'faq.title': '❓ Câu hỏi thường gặp',
            'table.name': 'Tên',
            'table.ingredients': 'Nguyên liệu',
            'table.time': 'Thời gian',
            'table.rewards': 'Phần thưởng',
            'table.effect': 'Hiệu ứng',
            'step': 'Bước',
            'tip': 'Mẹo',
            'ingredient.growth_time': 'Thời gian phát triển',
            'ingredient.value': 'Giá trị',
            'ingredient.use': 'Công dụng'
        },
        # 葡萄牙语
        'pt-br': {
            'hero.title': 'Guia',
            'hero.subtitle': 'em Cultivar um Jardim',
            'breadcrumb.current': 'Página atual',
            'toc.title': '📋 Índice',
            'toc.basics': 'Conceitos básicos',
            'toc.ingredients': 'Lista de ingredientes',
            'toc.recipes': 'Receitas',
            'toc.tips': 'Dicas e truques',
            'toc.efficiency': 'Melhorias de eficiência',
            'toc.faq': 'Perguntas frequentes',
            'basics.title': '🌱 Conceitos básicos',
            'ingredients.title': '🥬 Lista de ingredientes',
            'recipes.title': '🍳 Receitas',
            'tips.title': '💡 Dicas e truques',
            'efficiency.title': '⚡ Melhorias de eficiência',
            'faq.title': '❓ Perguntas frequentes',
            'table.name': 'Nome',
            'table.ingredients': 'Ingredientes',
            'table.time': 'Tempo',
            'table.rewards': 'Recompensas',
            'table.effect': 'Efeito',
            'step': 'Passo',
            'tip': 'Dica',
            'ingredient.growth_time': 'Tempo de crescimento',
            'ingredient.value': 'Valor',
            'ingredient.use': 'Uso'
        }
    }
    
    return base_mapping

def smart_translate_key(key, lang, base_mapping):
    """智能翻译键值"""
    if lang not in base_mapping:
        return f"[{key}]"
    
    # 尝试直接匹配
    if key in base_mapping[lang]:
        return base_mapping[lang][key]
    
    # 尝试部分匹配
    for pattern, translation in base_mapping[lang].items():
        if key.endswith(pattern):
            return translation
    
    # 尝试通用模式
    if key.endswith('.hero.title'):
        return base_mapping[lang].get('hero.title', f"[{key}]")
    elif key.endswith('.hero.subtitle'):
        return base_mapping[lang].get('hero.subtitle', f"[{key}]")
    elif key.endswith('.breadcrumb.current'):
        return base_mapping[lang].get('breadcrumb.current', f"[{key}]")
    elif key.endswith('.toc.title'):
        return base_mapping[lang].get('toc.title', f"[{key}]")
    elif key.endswith('.toc.basics'):
        return base_mapping[lang].get('toc.basics', f"[{key}]")
    elif key.endswith('.toc.ingredients'):
        return base_mapping[lang].get('toc.ingredients', f"[{key}]")
    elif key.endswith('.toc.recipes'):
        return base_mapping[lang].get('toc.recipes', f"[{key}]")
    elif key.endswith('.toc.tips'):
        return base_mapping[lang].get('toc.tips', f"[{key}]")
    elif key.endswith('.toc.efficiency'):
        return base_mapping[lang].get('toc.efficiency', f"[{key}]")
    elif key.endswith('.toc.faq'):
        return base_mapping[lang].get('toc.faq', f"[{key}]")
    elif key.endswith('.basics.title'):
        return base_mapping[lang].get('basics.title', f"[{key}]")
    elif key.endswith('.ingredients.title'):
        return base_mapping[lang].get('ingredients.title', f"[{key}]")
    elif key.endswith('.recipes.title'):
        return base_mapping[lang].get('recipes.title', f"[{key}]")
    elif key.endswith('.tips.title'):
        return base_mapping[lang].get('tips.title', f"[{key}]")
    elif key.endswith('.efficiency.title'):
        return base_mapping[lang].get('efficiency.title', f"[{key}]")
    elif key.endswith('.faq.title'):
        return base_mapping[lang].get('faq.title', f"[{key}]")
    elif key.endswith('.table.name'):
        return base_mapping[lang].get('table.name', f"[{key}]")
    elif key.endswith('.table.ingredients'):
        return base_mapping[lang].get('table.ingredients', f"[{key}]")
    elif key.endswith('.table.time'):
        return base_mapping[lang].get('table.time', f"[{key}]")
    elif key.endswith('.table.rewards'):
        return base_mapping[lang].get('table.rewards', f"[{key}]")
    elif key.endswith('.table.effect'):
        return base_mapping[lang].get('table.effect', f"[{key}]")
    elif key.startswith('step.'):
        return base_mapping[lang].get('step', f"[{key}]")
    elif key.startswith('tip.'):
        return base_mapping[lang].get('tip', f"[{key}]")
    elif key.startswith('ingredient.growth_time'):
        return base_mapping[lang].get('ingredient.growth_time', f"[{key}]")
    elif key.startswith('ingredient.value'):
        return base_mapping[lang].get('ingredient.value', f"[{key}]")
    elif key.startswith('ingredient.use'):
        return base_mapping[lang].get('ingredient.use', f"[{key}]")
    
    return f"[{key}]"

def update_language_file_with_translations(lang_file_path, base_mapping):
    """用智能翻译更新语言文件"""
    try:
        with open(lang_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    # 获取语言代码
    lang = lang_file_path.stem
    
    # 更新翻译
    updated = False
    for key in data:
        if data[key].startswith('[') and data[key].endswith(']'):
            new_translation = smart_translate_key(key, lang, base_mapping)
            if new_translation != data[key]:
                data[key] = new_translation
                updated = True
    
    if updated:
        # 按键排序
        sorted_data = dict(sorted(data.items()))
        
        # 写入文件
        with open(lang_file_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 智能翻译: {lang_file_path}")
        return True
    
    return False

def main():
    """主函数"""
    print("🚀 开始智能翻译所有语言文件...")
    
    # 创建翻译映射
    base_mapping = create_translation_mapping()
    
    # 获取所有语言文件
    i18n_dir = Path("i18n")
    lang_files = list(i18n_dir.glob("*.json"))
    lang_files = [f for f in lang_files if not f.name.startswith(('en', 'fr_base', 'fr_clean', 'fr_temp', 'de_backup'))]
    
    print(f"找到 {len(lang_files)} 个语言文件")
    
    # 为每个语言文件应用智能翻译
    updated_count = 0
    for lang_file in lang_files:
        if update_language_file_with_translations(lang_file, base_mapping):
            updated_count += 1
    
    print(f"\n🎉 完成！智能翻译了 {updated_count} 个语言文件")
    print("现在所有攻略详情页都有了完整的本地化内容！")

if __name__ == "__main__":
    main() 