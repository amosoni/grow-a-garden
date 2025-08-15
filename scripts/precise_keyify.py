#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确 keyify 脚本 - 处理剩余的特定英文内容
"""

import os
import re
import glob
from pathlib import Path

def precise_keyify_article_page(file_path):
    """精确处理单个攻略页面"""
    print(f"精确处理: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 处理特定的英文标题
    content = re.sub(
        r'<h3[^>]*data-i18n="recipes\.basic_salad\.title"[^>]*>Basic Salad Recipes</h3>',
        r'<h3 data-i18n="recipes.basic_salad.title">Basic Salad Recipes</h3>',
        content
    )
    
    content = re.sub(
        r'<h3[^>]*data-i18n="recipes\.advanced_salad\.title"[^>]*>Advanced Salad Recipes</h3>',
        r'<h3 data-i18n="recipes.advanced_salad.title">Advanced Salad Recipes</h3>',
        content
    )
    
    content = re.sub(
        r'<h3[^>]*data-i18n="recipes\.luxury_salad\.title"[^>]*>Luxury Salad Recipes</h3>',
        r'<h3 data-i18n="recipes.luxury_salad.title">Luxury Salad Recipes</h3>',
        content
    )
    
    # 2. 处理特定的英文列表项
    content = re.sub(
        r'<li[^>]*data-i18n="summary\.bullet\.learn_basic_salad_recipes"[^>]*>Learn basic salad recipes</li>',
        r'<li data-i18n="summary.bullet.learn_basic_salad_recipes">Learn basic salad recipes</li>',
        content
    )
    
    # 3. 处理所有剩余的英文内容（更精确的模式）
    # 处理 Growth Time 相关
    content = re.sub(
        r'<p[^>]*>Growth Time: (\d+) minutes</p>',
        lambda m: f'<p data-i18n="growth_time.minutes" data-time="{m.group(1)}">Growth Time: {m.group(1)} minutes</p>',
        content
    )
    
    # 处理 From ingredient 相关
    content = re.sub(
        r'<p[^>]*>From ingredient gathering to finished ([^,]+), expect (\d+)-(\d+) minutes\. With practice and proper setup, you can reduce this time significantly\.</p>',
        lambda m: f'<p data-i18n="time_estimate.{m.group(1).lower().replace(" ", "_")}" data-min="{m.group(2)}" data-max="{m.group(3)}">From ingredient gathering to finished {m.group(1)}, expect {m.group(2)}-{m.group(3)} minutes. With practice and proper setup, you can reduce this time significantly.</p>',
        content
    )
    
    # 处理 Batch Farming 相关
    content = re.sub(
        r'<div[^>]*class="tip-box"[^>]*><strong>Batch Farming:</strong> Plant in waves every (\d+) minutes for continuous harvests\.</div>',
        lambda m: f'<div class="tip-box" data-i18n="tip.batch_farming" data-interval="{m.group(1)}"><strong data-i18n="tip.batch_farming.label">Batch Farming:</strong> Plant in waves every {m.group(1)} minutes for continuous harvests.</div>',
        content
    )
    
    # 处理 FAQ 相关
    content = re.sub(
        r'<p[^>]*>A: Basic ([^s]+)s take (\d+)-(\d+) minutes to make, while advanced recipes can take (\d+)-(\d+) minutes depending on complexity\.</p>',
        lambda m: f'<p data-i18n="faq.cooking_time.{m.group(1).lower()}" data-basic-min="{m.group(2)}" data-basic-max="{m.group(3)}" data-advanced-min="{m.group(4)}" data-advanced-max="{m.group(5)}">A: Basic {m.group(1)}s take {m.group(2)}-{m.group(3)} minutes to make, while advanced recipes can take {m.group(4)}-{m.group(5)} minutes depending on complexity.</p>',
        content
    )
    
    # 处理时间相关
    content = re.sub(
        r'<small[^>]*>(\d+) minutes to mature</small>',
        lambda m: f'<small data-i18n="maturity_time.minutes" data-time="{m.group(1)}">{m.group(1)} minutes to mature</small>',
        content
    )
    
    content = re.sub(
        r'<li[^>]*>Check for grain formation \((\d+)-(\d+) minutes\)</li>',
        lambda m: f'<li data-i18n="growth_check.grain_formation" data-min="{m.group(1)}" data-max="{m.group(2)}">Check for grain formation ({m.group(1)}-{m.group(2)} minutes)</li>',
        content
    )
    
    content = re.sub(
        r'<li[^>]*>Wait for full maturity \((\d+) minutes total\)</li>',
        lambda m: f'<li data-i18n="growth_wait.full_maturity" data-time="{m.group(1)}">Wait for full maturity ({m.group(1)} minutes total)</li>',
        content
    )
    
    content = re.sub(
        r'<li[^>]*>Water lightly every (\d+)-(\d+) minutes in-game</li>',
        lambda m: f'<li data-i18n="watering.frequency" data-min="{m.group(1)}" data-max="{m.group(2)}">Water lightly every {m.group(1)}-{m.group(2)} minutes in-game</li>',
        content
    )
    
    content = re.sub(
        r'<li[^>]*>Plant in waves every (\d+) minutes for continuous harvests</li>',
        lambda m: f'<li data-i18n="planting.waves" data-interval="{m.group(1)}">Plant in waves every {m.group(1)} minutes for continuous harvests</li>',
        content
    )
    
    content = re.sub(
        r'<li[^>]*>Let filling rest for (\d+) minutes</li>',
        lambda m: f'<li data-i18n="filling.rest_time" data-time="{m.group(1)}">Let filling rest for {m.group(1)} minutes</li>',
        content
    )
    
    # 处理具体的时间描述
    content = re.sub(
        r'<p[^>]*>A: ([^t]+) takes exactly (\d+) minutes to reach full maturity from planting to harvest\.</p>',
        lambda m: f'<p data-i18n="faq.maturity_time.{m.group(1).lower().replace(" ", "_")}" data-time="{m.group(2)}">A: {m.group(1)} takes exactly {m.group(2)} minutes to reach full maturity from planting to harvest.</p>',
        content
    )
    
    # 处理要求项目
    content = re.sub(
        r'<div[^>]*class="requirement-item"[^>]*><h4[^>]*>⏰ Time</h4><p>~(\d+) minutes to mature</p></div>',
        lambda m: f'<div class="requirement-item" data-i18n="requirement.maturity_time" data-time="{m.group(1)}"><h4 data-i18n="requirement.time.label">⏰ Time</h4><p data-i18n="requirement.time.value">~{m.group(1)} minutes to mature</p></div>',
        content
    )
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 精确处理完成: {file_path}")

def main():
    """主函数"""
    print("🚀 开始精确 keyify 所有攻略详情页...")
    
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
            precise_keyify_article_page(file_path)
        except Exception as e:
            print(f"❌ 处理失败 {file_path}: {e}")
    
    print("🎉 所有攻略详情页精确 key 化完成！")
    print("\n下一步：需要补齐所有新键的翻译内容")

if __name__ == "__main__":
    main() 