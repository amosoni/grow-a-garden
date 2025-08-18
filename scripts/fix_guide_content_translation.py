#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门修改攻略页面的主要内容翻译
包括导航栏、面包屑导航、尾部栏和页面内容
"""

import re
from pathlib import Path

def get_content_translations():
    """获取攻略页面内容的翻译"""
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
        }
    }

def apply_content_translation(file_path, language_code):
    """应用内容翻译到攻略页面"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        translations = get_content_translations()
        
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
            print(f"✅ 已应用 {language_code} 内容翻译: {file_path.name}")
            return True
        else:
            print(f"⏭️  无需修改: {file_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ 应用翻译失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始修改攻略页面的内容翻译...")
    
    language_mapping = {"zh-cn": "zh-cn", "ja": "ja"}
    total_translated = 0
    
    for lang_dir, lang_code in language_mapping.items():
        lang_path = Path(lang_dir)
        if not lang_path.exists():
            continue
            
        print(f"\n🔧 正在处理语言目录: {lang_dir}")
        
        guide_files = []
        for pattern in ['how-to-*.html', '*-guide.html', '*-strategies.html', '*-basics.html', '*-tips.html']:
            guide_files.extend(lang_path.glob(pattern))
        
        if not guide_files:
            continue
        
        print(f"   📁 找到 {len(guide_files)} 个攻略页面")
        
        for file_path in guide_files:
            if apply_content_translation(file_path, lang_code):
                total_translated += 1
    
    print(f"\n🎉 攻略页面内容翻译完成！")
    print(f"📊 成功翻译: {total_translated} 个文件")

if __name__ == "__main__":
    main() 