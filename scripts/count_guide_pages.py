#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计项目中实际的攻略页面总数
"""

import os
from pathlib import Path

def count_guide_pages():
    """统计攻略页面总数"""
    print("🔍 正在统计项目中的攻略页面...")
    
    total_count = 0
    language_counts = {}
    
    # 根目录
    root_dir = Path('.')
    root_guides = []
    
    # 根目录下的攻略页面
    guide_patterns = [
        'how-to-*.html',
        '*-guide.html',
        '*-strategies.html',
        '*-basics.html',
        '*-tips.html'
    ]
    
    for pattern in guide_patterns:
        root_guides.extend(root_dir.glob(pattern))
    
    # 排除非攻略页面
    exclude_files = [
        'test_*.html',
        'debug_*.html',
        'force_refresh.html',
        'preview.html'
    ]
    
    root_guides = [f for f in root_guides if not any(ex in f.name for ex in exclude_files)]
    
    print(f"📁 根目录攻略页面: {len(root_guides)} 个")
    for f in root_guides:
        print(f"   - {f.name}")
    
    total_count += len(root_guides)
    
    # 语言目录
    language_dirs = [
        "zh-cn", "ja", "es", "pt-br", "fr", "de", 
        "ru", "ar", "hi", "id", "vi"
    ]
    
    for lang_dir in language_dirs:
        lang_path = Path(lang_dir)
        if not lang_path.exists():
            continue
            
        lang_guides = []
        for pattern in guide_patterns:
            lang_guides.extend(lang_path.glob(pattern))
        
        # 排除非攻略页面
        lang_guides = [f for f in lang_guides if not any(ex in f.name for ex in exclude_files)]
        
        if lang_guides:
            print(f"\n📁 {lang_dir}/ 目录攻略页面: {len(lang_guides)} 个")
            for f in lang_guides:
                print(f"   - {f.name}")
            
            language_counts[lang_dir] = len(lang_guides)
            total_count += len(lang_guides)
    
    print(f"\n📊 统计结果:")
    print(f"   根目录: {len(root_guides)} 个")
    for lang, count in language_counts.items():
        print(f"   {lang}/: {count} 个")
    print(f"   总计: {total_count} 个攻略页面")
    
    return total_count

if __name__ == "__main__":
    count_guide_pages() 