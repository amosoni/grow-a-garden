#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度 keyify 脚本 - 处理所有剩余的英文内容
"""

import os
import re
import glob
from pathlib import Path

def deep_keyify_article_page(file_path):
    """深度处理单个攻略页面"""
    print(f"深度处理: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 获取语言代码
    lang = file_path.split('/')[0]
    
    # 1. 处理稀有食材名称
    content = re.sub(
        r'<h4[^>]*>([A-Za-z\s]+)</h4>',
        lambda m: f'<h4 data-i18n="ingredient.{m.group(1).lower().replace(" ", "_")}.name">{m.group(1)}</h4>',
        content
    )
    
    # 2. 处理食材的 Use 描述
    content = re.sub(
        r'<p>用途：([^<]+)</p>',
        lambda m: f'<p data-i18n="ingredient.use.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "")}">用途：{m.group(1)}</p>',
        content
    )
    
    # 3. 处理表格标题
    content = re.sub(
        r'<h3[^>]*>([A-Za-z\s]+)\s+Recipes?</h3>',
        lambda m: f'<h3 data-i18n="recipes.{m.group(1).lower().replace(" ", "_")}.title">{m.group(1)} Recipes</h3>',
        content
    )
    
    # 4. 处理表格内容 - 沙拉名称
    content = re.sub(
        r'<td[^>]*>([A-Za-z\s]+)\s+Salad</td>',
        lambda m: f'<td data-i18n="salad.{m.group(1).lower().replace(" ", "_")}.name">{m.group(1)} Salad</td>',
        content
    )
    
    # 5. 处理表格内容 - 食材列表
    content = re.sub(
        r'<td[^>]*>([A-Za-z\s]+)\s+x(\d+)</td>',
        lambda m: f'<td data-i18n="ingredient.{m.group(1).lower().replace(" ", "_")}.quantity">{m.group(1)} x{m.group(2)}</td>',
        content
    )
    
    # 6. 处理时间单位
    content = re.sub(
        r'<td[^>]*>(\d+)\s+minutes?</td>',
        lambda m: f'<td data-i18n="time.minutes" data-time="{m.group(1)}">{m.group(1)} minutes</td>',
        content
    )
    
    # 7. 处理货币单位
    content = re.sub(
        r'<td[^>]*>(\d+)\s+Coins?</td>',
        lambda m: f'<td data-i18n="currency.coins" data-amount="{m.group(1)}">{m.group(1)} Coins</td>',
        content
    )
    
    # 8. 处理效果描述
    content = re.sub(
        r'<td[^>]*>([A-Za-z\s]+)</td>',
        lambda m: f'<td data-i18n="effect.{m.group(1).lower().replace(" ", "_")}">{m.group(1)}</td>' if any(effect in m.group(1) for effect in ['Basic Nutrition', 'Vitamin Rich', 'High Moisture', 'Healthy Body', 'Antioxidant', 'Fiber Rich', 'Immunity Boost', 'Metabolism Boost', 'Vitamin C Rich']) else m.group(0),
        content
    )
    
    # 9. 处理提示框标题
    content = re.sub(
        r'<h4[^>]*>([A-Za-z\s]+)</h4>',
        lambda m: f'<h4 data-i18n="tip.{m.group(1).lower().replace(" ", "_")}.title">{m.group(1)}</h4>' if any(tip in m.group(1) for tip in ['Time Management Tips', 'Planting Strategy', 'Resource Management']) else m.group(0),
        content
    )
    
    # 10. 处理提示框内容
    content = re.sub(
        r'<li[^>]*>([A-Za-z\s]+):</li>',
        lambda m: f'<li data-i18n="tip.{m.group(1).lower().replace(" ", "_")}.label">{m.group(1)}:</li>' if any(tip in m.group(1) for tip in ['Staggered Planting', 'Batch Making', 'Golden Hours', 'Daily Login', 'Priority Planting', 'Upgrade Tools', 'Friend Cooperation', 'Event Participation']) else m.group(0),
        content
    )
    
    # 11. 处理 FAQ 问题
    content = re.sub(
        r'<strong>Q:\s*([^<]+)</strong>',
        lambda m: f'<strong data-i18n="faq.{m.group(1).lower().replace(" ", "_").replace("?", "").replace("'", "").replace(":", "")}.question">Q: {m.group(1)}</strong>',
        content
    )
    
    # 12. 处理 FAQ 答案
    content = re.sub(
        r'<strong>A:\s*([^<]+)</strong>',
        lambda m: f'<strong data-i18n="faq.{m.group(1).lower().replace(" ", "_").replace("?", "").replace("'", "").replace(":", "")}.answer">A: {m.group(1)}</strong>',
        content
    )
    
    # 13. 处理总结段落
    content = re.sub(
        r'<p[^>]*>([^<]+)</p>',
        lambda m: f'<p data-i18n="summary.{m.group(1).lower().replace(" ", "_").replace("?", "").replace("'", "").replace(":", "").replace(".", "")}">{m.group(1)}</p>' if any(word in m.group(1) for word in ['Start planting', 'Learn basic', 'Join player', 'Participate in']) else m.group(0),
        content
    )
    
    # 14. 处理总结要点
    content = re.sub(
        r'<li[^>]*>([^<]+)</li>',
        lambda m: f'<li data-i18n="summary.bullet.{m.group(1).lower().replace(" ", "_").replace("?", "").replace("'", "").replace(":", "").replace(".", "")}">{m.group(1)}</li>' if any(word in m.group(1) for word in ['Start planting', 'Learn basic', 'Join player', 'Participate in']) else m.group(0),
        content
    )
    
    # 15. 处理页脚
    content = re.sub(
        r'<p[^>]*>©\s+(\d{4})\s+([^<]+)</p>',
        lambda m: f'<p data-i18n="footer.copyright" data-year="{m.group(1)}">© {m.group(1)} {m.group(2)}</p>',
        content
    )
    
    content = re.sub(
        r'<p[^>]*>([^<]+)</p>',
        lambda m: f'<p data-i18n="footer.disclaimer">{m.group(1)}</p>' if any(word in m.group(1) for word in ['Not Official', 'Data for reference only']) else m.group(0),
        content
    )
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 深度处理完成: {file_path}")

def main():
    """主函数"""
    print("🚀 开始深度 keyify 所有攻略详情页...")
    
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
            deep_keyify_article_page(file_path)
        except Exception as e:
            print(f"❌ 处理失败 {file_path}: {e}")
    
    print("🎉 所有攻略详情页深度 key 化完成！")
    print("\n下一步：需要补齐所有新键的翻译内容")

if __name__ == "__main__":
    main() 