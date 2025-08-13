#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补齐所有语言的翻译内容
"""

import os
import json
import re
import glob
from pathlib import Path

def extract_keys_from_html(file_path):
    """从HTML文件中提取所有data-i18n键"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有data-i18n键
    keys = re.findall(r'data-i18n="([^"]+)"', content)
    return list(set(keys))  # 去重

def get_all_keys_from_articles():
    """从所有攻略页面中提取所有键"""
    all_keys = set()
    
    # 查找所有攻略页面
    article_patterns = [
        "*/how-to-*.html",
        "*/how-to-grow-*.html", 
        "*/how-to-play-*.html"
    ]
    
    for pattern in article_patterns:
        for file_path in glob.glob(pattern):
            keys = extract_keys_from_html(file_path)
            all_keys.update(keys)
    
    return sorted(list(all_keys))

def create_translation_template(keys):
    """创建翻译模板"""
    template = {}
    
    for key in keys:
        # 根据键的结构生成默认翻译
        if key.endswith('.hero.title'):
            template[key] = f"[{key}]"
        elif key.endswith('.hero.subtitle'):
            template[key] = f"[{key}]"
        elif key.endswith('.breadcrumb.current'):
            template[key] = f"[{key}]"
        elif key.endswith('.toc.title'):
            template[key] = f"[{key}]"
        elif key.endswith('.toc.basics'):
            template[key] = f"[{key}]"
        elif key.endswith('.toc.ingredients'):
            template[key] = f"[{key}]"
        elif key.endswith('.toc.recipes'):
            template[key] = f"[{key}]"
        elif key.endswith('.toc.tips'):
            template[key] = f"[{key}]"
        elif key.endswith('.toc.efficiency'):
            template[key] = f"[{key}]"
        elif key.endswith('.toc.faq'):
            template[key] = f"[{key}]"
        elif key.endswith('.basics.title'):
            template[key] = f"[{key}]"
        elif key.endswith('.ingredients.title'):
            template[key] = f"[{key}]"
        elif key.endswith('.recipes.title'):
            template[key] = f"[{key}]"
        elif key.endswith('.tips.title'):
            template[key] = f"[{key}]"
        elif key.endswith('.efficiency.title'):
            template[key] = f"[{key}]"
        elif key.endswith('.faq.title'):
            template[key] = f"[{key}]"
        elif key.endswith('.table.name'):
            template[key] = f"[{key}]"
        elif key.endswith('.table.ingredients'):
            template[key] = f"[{key}]"
        elif key.endswith('.table.time'):
            template[key] = f"[{key}]"
        elif key.endswith('.table.rewards'):
            template[key] = f"[{key}]"
        elif key.endswith('.table.effect'):
            template[key] = f"[{key}]"
        elif key.startswith('step.'):
            template[key] = f"[{key}]"
        elif key.startswith('tip.'):
            template[key] = f"[{key}]"
        elif key.startswith('ingredient.'):
            template[key] = f"[{key}]"
        else:
            template[key] = f"[{key}]"
    
    return template

def update_language_file(lang_file_path, new_keys):
    """更新语言文件，添加缺失的键"""
    try:
        with open(lang_file_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}
    
    # 添加缺失的键
    updated = False
    for key in new_keys:
        if key not in existing_data:
            existing_data[key] = f"[{key}]"
            updated = True
    
    if updated:
        # 按键排序
        sorted_data = dict(sorted(existing_data.items()))
        
        # 写入文件
        with open(lang_file_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 更新: {lang_file_path}")
        return True
    
    return False

def main():
    """主函数"""
    print("🚀 开始补齐所有语言的翻译内容...")
    
    # 获取所有键
    print("📋 提取所有攻略页面的键...")
    all_keys = get_all_keys_from_articles()
    print(f"找到 {len(all_keys)} 个唯一键")
    
    # 获取所有语言文件
    i18n_dir = Path("i18n")
    lang_files = list(i18n_dir.glob("*.json"))
    lang_files = [f for f in lang_files if not f.name.startswith(('en', 'fr_base', 'fr_clean', 'fr_temp', 'de_backup'))]
    
    print(f"找到 {len(lang_files)} 个语言文件")
    
    # 为每个语言文件添加缺失的键
    updated_count = 0
    for lang_file in lang_files:
        if update_language_file(lang_file, all_keys):
            updated_count += 1
    
    print(f"\n🎉 完成！更新了 {updated_count} 个语言文件")
    print(f"总共添加了 {len(all_keys)} 个翻译键")
    print("\n下一步：需要手动填写各语言的具体翻译内容")

if __name__ == "__main__":
    main() 