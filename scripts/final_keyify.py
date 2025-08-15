#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终 keyify 脚本 - 处理所有剩余的英文内容
"""

import os
import re
import glob
from pathlib import Path

def final_keyify_article_page(file_path):
    """最终处理单个攻略页面"""
    print(f"最终处理: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 获取语言代码
    lang = file_path.split('/')[0]
    
    # 1. 处理所有剩余的英文标题
    content = re.sub(
        r'<h3[^>]*>([A-Za-z\s]+)\s+Recipes?</h3>',
        lambda m: f'<h3 data-i18n="recipes.{m.group(1).lower().replace(" ", "_")}.title">{m.group(1)} Recipes</h3>',
        content
    )
    
    content = re.sub(
        r'<h3[^>]*>([A-Za-z\s]+)\s+Strategy</h3>',
        lambda m: f'<h3 data-i18n="strategy.{m.group(1).lower().replace(" ", "_")}.title">{m.group(1)} Strategy</h3>',
        content
    )
    
    content = re.sub(
        r'<h3[^>]*>([A-Za-z\s]+)\s+Tips</h3>',
        lambda m: f'<h3 data-i18n="tips.{m.group(1).lower().replace(" ", "_")}.title">{m.group(1)} Tips</h3>',
        content
    )
    
    # 2. 处理所有剩余的英文段落
    content = re.sub(
        r'<p[^>]*>([^<]*[A-Za-z][^<]*)</p>',
        lambda m: f'<p data-i18n="content.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "").replace("'", "").replace("?", "").replace("!", "").replace("-", "_")}">{m.group(1)}</p>' if any(word in m.group(1) for word in ['Growth Time:', 'Basic', 'Advanced', 'Luxury', 'From ingredient', 'expect', 'minutes', 'With practice', 'reduce', 'significantly', 'Batch Farming:', 'Plant in waves', 'continuous harvests', 'Check for', 'Wait for', 'takes exactly', 'reach full maturity', 'planting to harvest']) else m.group(0),
        content
    )
    
    # 3. 处理所有剩余的英文列表项
    content = re.sub(
        r'<li[^>]*>([^<]*[A-Za-z][^<]*)</li>',
        lambda m: f'<li data-i18n="list.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "").replace("'", "").replace("?", "").replace("!", "").replace("-", "_")}">{m.group(1)}</li>' if any(word in m.group(1) for word in ['Let filling rest', 'Check for grain formation', 'Wait for full maturity', 'Water lightly every', 'Plant in waves every', 'for continuous harvests']) else m.group(0),
        content
    )
    
    # 4. 处理所有剩余的英文小标签
    content = re.sub(
        r'<small[^>]*>([^<]*[A-Za-z][^<]*)</small>',
        lambda m: f'<small data-i18n="small.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "").replace("'", "").replace("?", "").replace("!", "").replace("-", "_")}">{m.group(1)}</small>' if any(word in m.group(1) for word in ['minutes to mature', 'total']) else m.group(0),
        content
    )
    
    # 5. 处理所有剩余的英文提示框
    content = re.sub(
        r'<div[^>]*class="tip-box"[^>]*>([^<]*[A-Za-z][^<]*)</div>',
        lambda m: f'<div class="tip-box" data-i18n="tip_box.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "").replace("'", "").replace("?", "").replace("!", "").replace("-", "_")}">{m.group(1)}</div>' if any(word in m.group(1) for word in ['Batch Farming:', 'Plant in waves']) else m.group(0),
        content
    )
    
    # 6. 处理所有剩余的英文strong标签
    content = re.sub(
        r'<strong[^>]*>([^<]*[A-Za-z][^<]*)</strong>',
        lambda m: f'<strong data-i18n="strong.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "").replace("'", "").replace("?", "").replace("!", "").replace("-", "_")}">{m.group(1)}</strong>' if any(word in m.group(1) for word in ['Batch Farming:', 'Time', 'Plant in waves']) else m.group(0),
        content
    )
    
    # 7. 处理所有剩余的英文div标签
    content = re.sub(
        r'<div[^>]*class="requirement-item"[^>]*>([^<]*[A-Za-z][^<]*)</div>',
        lambda m: f'<div class="requirement-item" data-i18n="requirement.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "").replace("'", "").replace("?", "").replace("!", "").replace("-", "_")}">{m.group(1)}</div>' if any(word in m.group(1) for word in ['Time', '~35 minutes to mature']) else m.group(0),
        content
    )
    
    # 8. 处理所有剩余的英文h4标签
    content = re.sub(
        r'<h4[^>]*>([^<]*[A-Za-z][^<]*)</h4>',
        lambda m: f'<h4 data-i18n="h4.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "").replace("'", "").replace("?", "").replace("!", "").replace("-", "_")}">{m.group(1)}</h4>' if any(word in m.group(1) for word in ['Time', '⏰ Time']) else m.group(0),
        content
    )
    
    # 9. 处理所有剩余的英文span标签
    content = re.sub(
        r'<span[^>]*>([^<]*[A-Za-z][^<]*)</span>',
        lambda m: f'<span data-i18n="span.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "").replace("'", "").replace("?", "").replace("!", "").replace("-", "_")}">{m.group(1)}</span>' if any(word in m.group(1) for word in ['Basic', 'Advanced', 'Expert', 'Stages']) else m.group(0),
        content
    )
    
    # 10. 处理所有剩余的英文a标签
    content = re.sub(
        r'<a[^>]*>([^<]*[A-Za-z][^<]*)</a>',
        lambda m: f'<a data-i18n="link.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "").replace("'", "").replace("?", "").replace("!", "").replace("-", "_")}">{m.group(1)}</a>' if any(word in m.group(1) for word in ['Next', 'Previous', 'Back to', 'See all', 'View', 'Learn more']) else m.group(0),
        content
    )
    
    # 11. 处理所有剩余的英文button标签
    content = re.sub(
        r'<button[^>]*>([^<]*[A-Za-z][^<]*)</button>',
        lambda m: f'<button data-i18n="button.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "").replace("'", "").replace("?", "").replace("!", "").replace("-", "_")}">{m.group(1)}</button>' if any(word in m.group(1) for word in ['Start', 'Continue', 'Submit', 'Cancel', 'Save', 'Load', 'Reset']) else m.group(0),
        content
    )
    
    # 12. 处理所有剩余的英文input标签
    content = re.sub(
        r'<input[^>]*placeholder="([^"]*[A-Za-z][^"]*)"',
        lambda m: f'<input placeholder="{m.group(1)}" data-i18n-placeholder="input.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "").replace("'", "").replace("?", "").replace("!", "").replace("-", "_")}"',
        content
    )
    
    # 13. 处理所有剩余的英文label标签
    content = re.sub(
        r'<label[^>]*>([^<]*[A-Za-z][^<]*)</label>',
        lambda m: f'<label data-i18n="label.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "").replace("'", "").replace("?", "").replace("!", "").replace("-", "_")}">{m.group(1)}</label>' if any(word in m.group(1) for word in ['Name', 'Email', 'Password', 'Confirm', 'Username', 'Phone']) else m.group(0),
        content
    )
    
    # 14. 处理所有剩余的英文textarea标签
    content = re.sub(
        r'<textarea[^>]*placeholder="([^"]*[A-Za-z][^"]*)"',
        lambda m: f'<textarea placeholder="{m.group(1)}" data-i18n-placeholder="textarea.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "").replace("'", "").replace("?", "").replace("!", "").replace("-", "_")}"',
        content
    )
    
    # 15. 处理所有剩余的英文select标签
    content = re.sub(
        r'<option[^>]*>([^<]*[A-Za-z][^<]*)</option>',
        lambda m: f'<option data-i18n="option.{m.group(1).lower().replace(" ", "_").replace(":", "").replace(".", "").replace("'", "").replace("?", "").replace("!", "").replace("-", "_")}">{m.group(1)}</option>' if any(word in m.group(1) for word in ['Select', 'Choose', 'Pick', 'Option']) else m.group(0),
        content
    )
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 最终处理完成: {file_path}")

def main():
    """主函数"""
    print("🚀 开始最终 keyify 所有攻略详情页...")
    
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
            final_keyify_article_page(file_path)
        except Exception as e:
            print(f"❌ 处理失败 {file_path}: {e}")
    
    print("🎉 所有攻略详情页最终 key 化完成！")
    print("\n下一步：需要补齐所有新键的翻译内容")

if __name__ == "__main__":
    main() 