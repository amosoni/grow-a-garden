#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有攻略详情页注入 data-i18n 键值
"""

import os
import re
import glob
from pathlib import Path

def keyify_article_page(file_path):
    """为单个攻略页面注入 data-i18n 键"""
    print(f"处理: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 获取语言代码
    lang = file_path.split('/')[0]
    
    # 注入标题和副标题的键
    content = re.sub(
        r'<h1[^>]*>([^<]+)</h1>',
        r'<h1 data-i18n="\1.hero.title">\1</h1>',
        content
    )
    
    content = re.sub(
        r'<p[^>]*>([^<]+)</p>',
        lambda m: f'<p data-i18n="{m.group(1).lower().replace(" ", "_")}.hero.subtitle">{m.group(1)}</p>' if 'Grow a Garden' in m.group(1) else m.group(0),
        content
    )
    
    # 注入面包屑当前项的键
    content = re.sub(
        r'<li[^>]*aria-current="page"[^>]*>([^<]+)</li>',
        lambda m: f'<li aria-current="page" data-i18n="{m.group(1).lower().replace(" ", "_").replace("🥗", "").replace("🍕", "").replace("🍰", "").replace("🥖", "").replace("🍪", "").replace("🍩", "").replace("🥪", "").replace("🥤", "").replace("🍝", "").replace("🥕", "").replace("🌽", "").replace("🍊", "").replace("🫐", "").replace("🌾", "").replace("💰", "").replace("👥", "").strip()}.breadcrumb.current">{m.group(1)}</li>',
        content
    )
    
    # 注入目录标题的键
    content = re.sub(
        r'<h2[^>]*>📋\s*([^<]+)</h2>',
        lambda m: f'<h2 data-i18n="{m.group(1).lower().replace(" ", "_")}.toc.title">📋 {m.group(1)}</h2>',
        content
    )
    
    # 注入目录链接的键
    content = re.sub(
        r'<a[^>]*href="#([^"]+)"[^>]*>([^<]+)</a>',
        lambda m: f'<a href="#{m.group(1)}" data-i18n="{m.group(1).lower().replace("-", "_")}.toc.{m.group(1)}">{m.group(2)}</a>' if m.group(1) in ['basics', 'ingredients', 'recipes', 'tips', 'efficiency', 'faq'] else m.group(0),
        content
    )
    
    # 注入区块标题的键
    content = re.sub(
        r'<h2[^>]*>([^<]+)</h2>',
        lambda m: f'<h2 data-i18n="{m.group(1).lower().replace(" ", "_").replace("🌱", "").replace("🥬", "").replace("🍅", "").replace("🥕", "").replace("🌽", "").replace("🍊", "").replace("🫐", "").replace("🌾", "").replace("💰", "").replace("👥", "").strip()}.{m.group(1).lower().replace(" ", "_").replace("🌱", "").replace("🥬", "").replace("🍅", "").replace("🥕", "").replace("🌽", "").replace("🍊", "").replace("🫐", "").replace("🌾", "").replace("💰", "").replace("👥", "").strip()}.title">{m.group(1)}</h2>' if any(emoji in m.group(1) for emoji in ['🌱', '🥬', '🍅', '🥕', '🌽', '🍊', '🫐', '🌾', '💰', '👥']) else m.group(0),
        content
    )
    
    # 注入子标题的键
    content = re.sub(
        r'<h3[^>]*>([^<]+)</h3>',
        lambda m: f'<h3 data-i18n="{m.group(1).lower().replace(" ", "_").replace("（", "").replace("）", "").replace("(", "").replace(")", "")}.{m.group(1).lower().replace(" ", "_").replace("（", "").replace("）", "").replace("(", "").replace(")", "")}.title">{m.group(1)}</h3>' if any(word in m.group(1) for word in ['基本', '上級', '高級', 'Basic', 'Advanced', 'Luxury', 'Básico', 'Avanzado', 'Lujo', 'Basique', 'Avancé', 'Luxe', 'Grundlegend', 'Fortgeschritten', 'Luxus', 'Базовый', 'Продвинутый', 'Люкс', 'बुनियादी', 'उन्नत', 'लक्जरी', 'Dasar', 'Lanjutan', 'Mewah', 'Cơ bản', 'Nâng cao', 'Xa xỉ']) else m.group(0),
        content
    )
    
    # 注入表格标题的键
    content = re.sub(
        r'<th[^>]*>([^<]+)</th>',
        lambda m: f'<th data-i18n="{m.group(1).lower().replace(" ", "_").replace("サラダ名", "salad_name").replace("必要な材料", "ingredients").replace("調理時間", "time").replace("報酬価値", "rewards").replace("特別効果", "effect")}.table.{m.group(1).lower().replace(" ", "_").replace("サラダ名", "salad_name").replace("必要な材料", "ingredients").replace("調理時間", "time").replace("報酬価値", "rewards").replace("特別効果", "effect")}">{m.group(1)}</th>' if any(word in m.group(1) for word in ['Name', 'Ingredients', 'Time', 'Rewards', 'Effects', 'サラダ名', '必要な材料', '調理時間', '報酬価値', '特別効果', 'Nombre', 'Ingredientes', 'Tiempo', 'Recompensas', 'Efectos', 'Nom', 'Ingrédients', 'Temps', 'Récompenses', 'Effets', 'Name', 'Zutaten', 'Zeit', 'Belohnungen', 'Effekte', 'Имя', 'Ингредиенты', 'Время', 'Награды', 'Эффекты', 'नाम', 'सामग्री', 'समय', 'पुरस्कार', 'प्रभाव', 'Nama', 'Bahan', 'Waktu', 'Hadiah', 'Efek', 'Tên', 'Nguyên liệu', 'Thời gian', 'Phần thưởng', 'Hiệu ứng']) else m.group(0),
        content
    )
    
    # 注入步骤描述的键
    content = re.sub(
        r'<p[^>]*>(\d+\.\s*[^<]+)</p>',
        lambda m: f'<p data-i18n="step.{m.group(1).split(".")[0]}.description">{m.group(1)}</p>',
        content
    )
    
    # 注入提示框的键
    content = re.sub(
        r'<div[^>]*class="tip"[^>]*>([^<]+)</div>',
        lambda m: f'<div class="tip" data-i18n="tip.{m.group(1).lower().replace(" ", "_").replace("：", "").replace(":", "")}">{m.group(1)}</div>',
        content
    )
    
    # 注入食材属性的键
    content = re.sub(
        r'<p>成長時間：(\d+分|\d+\s*minutes?)</p>',
        lambda m: f'<p data-i18n="ingredient.growth_time">{m.group(1)}</p>',
        content
    )
    
    content = re.sub(
        r'<p>価値：([^<]+)</p>',
        lambda m: f'<p data-i18n="ingredient.value">{m.group(1)}</p>',
        content
    )
    
    content = re.sub(
        r'<p>用途：([^<]+)</p>',
        lambda m: f'<p data-i18n="ingredient.use">{m.group(1)}</p>',
        content
    )
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 完成: {file_path}")

def main():
    """主函数"""
    print("🚀 开始为攻略详情页注入 data-i18n 键...")
    
    # 查找所有攻略页面
    article_patterns = [
        "*/how-to-*.html",
        "*/how-to-grow-*.html",
        "*/how-to-play-*.html"
    ]
    
    article_files = []
    for pattern in article_patterns:
        article_files.extend(glob.glob(pattern))
    
    print(f"找到 {len(article_files)} 个攻略页面")
    
    # 处理每个页面
    for file_path in article_files:
        try:
            keyify_article_page(file_path)
        except Exception as e:
            print(f"❌ 处理失败 {file_path}: {e}")
    
    print("🎉 所有攻略详情页 key 化完成！")
    print("\n下一步：需要补齐各语言的翻译内容")

if __name__ == "__main__":
    main() 