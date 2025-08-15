#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为每个语言生成完整的翻译模板
确保攻略页面的内容语言与目录语言完全匹配
"""

import os
import re
from pathlib import Path

def get_language_templates():
    """获取各语言的翻译模板"""
    templates = {
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
            "hero": {
                "salad": "🥗 沙拉制作指南",
                "pizza": "🍕 披萨制作指南",
                "cake": "🍰 蛋糕制作指南",
                "bread": "🍞 面包制作指南",
                "donut": "🍩 甜甜圈制作指南",
                "cookies": "🍪 饼干制作指南",
                "pie": "🥧 派制作指南",
                "sandwich": "🥪 三明治制作指南",
                "smoothie": "🥤 冰沙制作指南",
                "spaghetti": "🍝 意大利面制作指南"
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
            "hero": {
                "salad": "🥗 サラダ作りのガイド",
                "pizza": "🍕 ピザ作りのガイド",
                "cake": "🍰 ケーキ作りのガイド",
                "bread": "🍞 パン作りのガイド",
                "donut": "🍩 ドーナツ作りのガイド",
                "cookies": "🍪 クッキー作りのガイド",
                "pie": "🥧 パイ作りのガイド",
                "sandwich": "🥪 サンドイッチ作りのガイド",
                "smoothie": "🥤 スムージー作りのガイド",
                "spaghetti": "🍝 スパゲッティ作りのガイド"
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
            "hero": {
                "salad": "🥗 Guía para Hacer Ensaladas",
                "pizza": "🍕 Guía para Hacer Pizza",
                "cake": "🍰 Guía para Hacer Pasteles",
                "bread": "🍞 Guía para Hacer Pan",
                "donut": "🍩 Guía para Hacer Donas",
                "cookies": "🍪 Guía para Hacer Galletas",
                "pie": "🥧 Guía para Hacer Pasteles",
                "sandwich": "🥪 Guía para Hacer Sándwiches",
                "smoothie": "🥤 Guía para Hacer Batidos",
                "spaghetti": "🍝 Guía para Hacer Espaguetis"
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
        }
    }
    return templates

def apply_language_template(file_path, language_code):
    """应用语言模板到文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        templates = get_language_templates()
        
        if language_code not in templates:
            print(f"⚠️  没有 {language_code} 的翻译模板")
            return False
        
        template = templates[language_code]
        
        # 应用导航栏翻译
        for key, value in template["nav"].items():
            pattern = rf'data-i18n="nav\.{key}"[^>]*>([^<]+)</a>'
            replacement = f'data-i18n="nav.{key}">{value}</a>'
            content = re.sub(pattern, replacement, content)
        
        # 应用面包屑翻译
        for key, value in template["breadcrumb"].items():
            if key == "home":
                pattern = r'(<a href="[^"]*">)🏠 Home(</a>)'
                replacement = rf'\1{value}\2'
                content = re.sub(pattern, replacement, content)
            elif key == "guides":
                pattern = r'(<a href="[^"]*">)📚 Guides(</a>)'
                replacement = rf'\1{value}\2'
                content = re.sub(pattern, replacement, content)
        
        # 应用hero区域翻译
        for key, value in template["hero"].items():
            if key in file_path.name:
                # 根据文件名匹配对应的hero翻译
                if "salad" in file_path.name:
                    pattern = r'(<h1[^>]*>)[^<]+(</h1>)'
                    replacement = rf'\1{template["hero"]["salad"]}\2'
                    content = re.sub(pattern, replacement, content)
                elif "pizza" in file_path.name:
                    pattern = r'(<h1[^>]*>)[^<]+(</h1>)'
                    replacement = rf'\1{template["hero"]["pizza"]}\2'
                    content = re.sub(pattern, replacement, content)
                # 可以继续添加其他类型的匹配
        
        # 应用内容翻译
        for key, value in template["content"].items():
            if key == "toc":
                pattern = r'(<h2[^>]*>)[^<]*Table of Contents[^<]*(</h2>)'
                replacement = rf'\1{value}\2'
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已应用 {language_code} 翻译模板: {file_path.name}")
            return True
        else:
            print(f"⏭️  无需修改: {file_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ 应用模板失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始为攻略页面应用语言翻译模板...")
    
    # 语言目录映射
    language_mapping = {
        "zh-cn": "zh-cn",
        "ja": "ja",
        "es": "es"
    }
    
    total_applied = 0
    
    # 处理语言目录
    for lang_dir, lang_code in language_mapping.items():
        lang_path = Path(lang_dir)
        if not lang_path.exists():
            continue
            
        print(f"\n🔧 正在处理语言目录: {lang_dir} ({lang_code})")
        
        # 查找该语言目录下的所有攻略页面
        guide_files = []
        guide_patterns = [
            'how-to-*.html',
            '*-guide.html',
            '*-strategies.html',
            '*-basics.html',
            '*-tips.html'
        ]
        
        for pattern in guide_patterns:
            guide_files.extend(lang_path.glob(pattern))
        
        if not guide_files:
            print(f"   ⏭️  该语言目录下没有攻略页面")
            continue
        
        print(f"   📁 找到 {len(guide_files)} 个攻略页面")
        
        # 应用翻译模板到每个文件
        for file_path in guide_files:
            if apply_language_template(file_path, lang_code):
                total_applied += 1
    
    print(f"\n🎉 语言翻译模板应用完成！")
    print(f"📊 成功应用: {total_applied} 个文件")
    print("✨ 现在攻略页面的语言应该与目录语言匹配了！")

if __name__ == "__main__":
    main() 