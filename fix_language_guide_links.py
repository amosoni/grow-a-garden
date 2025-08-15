#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复语言目录下攻略页面的链接问题
确保链接指向正确的页面
"""

import os
import re
from pathlib import Path

def fix_guide_links(file_path, language_dir):
    """修复攻略页面的链接"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # 根据语言目录修复链接
        if language_dir == "zh-cn":
            # 中文目录：链接应该指向当前目录下的页面
            content = re.sub(r'href="/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/guides\.html', 'href="guides.html', content)
            content = re.sub(r'href="/zh-cn/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/zh-cn/guides\.html', 'href="guides.html', content)
            
        elif language_dir == "ja":
            # 日语目录：链接应该指向当前目录下的页面
            content = re.sub(r'href="/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/guides\.html', 'href="guides.html', content)
            content = re.sub(r'href="/ja/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/ja/guides\.html', 'href="guides.html', content)
            
        elif language_dir == "es":
            # 西班牙语目录
            content = re.sub(r'href="/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/guides\.html', 'href="guides.html', content)
            content = re.sub(r'href="/es/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/es/guides\.html', 'href="guides.html', content)
            
        elif language_dir == "pt-br":
            # 葡萄牙语目录
            content = re.sub(r'href="/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/guides\.html', 'href="guides.html', content)
            content = re.sub(r'href="/pt-br/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/pt-br/guides\.html', 'href="guides.html', content)
            
        elif language_dir == "fr":
            # 法语目录
            content = re.sub(r'href="/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/guides\.html', 'href="guides.html', content)
            content = re.sub(r'href="/fr/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/fr/guides\.html', 'href="guides.html', content)
            
        elif language_dir == "de":
            # 德语目录
            content = re.sub(r'href="/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/guides\.html', 'href="guides.html', content)
            content = re.sub(r'href="/de/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/de/guides\.html', 'href="guides.html', content)
            
        elif language_dir == "ru":
            # 俄语目录
            content = re.sub(r'href="/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/guides\.html', 'href="guides.html', content)
            content = re.sub(r'href="/ru/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/ru/guides\.html', 'href="guides.html', content)
            
        elif language_dir == "ar":
            # 阿拉伯语目录
            content = re.sub(r'href="/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/guides\.html', 'href="guides.html', content)
            content = re.sub(r'href="/ar/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/ar/guides\.html', 'href="guides.html', content)
            
        elif language_dir == "hi":
            # 印地语目录
            content = re.sub(r'href="/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/guides\.html', 'href="guides.html', content)
            content = re.sub(r'href="/hi/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/hi/guides\.html', 'href="guides.html', content)
            
        elif language_dir == "id":
            # 印尼语目录
            content = re.sub(r'href="/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/guides\.html', 'href="guides.html', content)
            content = re.sub(r'href="/id/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/id/guides\.html', 'href="guides.html', content)
            
        elif language_dir == "vi":
            # 越南语目录
            content = re.sub(r'href="/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/guides\.html', 'href="guides.html', content)
            content = re.sub(r'href="/vi/index\.html', 'href="index.html', content)
            content = re.sub(r'href="/vi/guides\.html', 'href="guides.html', content)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已修复链接: {file_path}")
            return True
        else:
            print(f"⏭️  链接已正确: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ 修复失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始修复语言目录下攻略页面的链接...")
    
    # 语言目录列表
    language_dirs = [
        "zh-cn", "ja", "es", "pt-br", "fr", "de", 
        "ru", "ar", "hi", "id", "vi"
    ]
    
    total_fixed = 0
    
    for lang_dir in language_dirs:
        lang_path = Path(lang_dir)
        if not lang_path.exists():
            print(f"⚠️  语言目录不存在: {lang_dir}")
            continue
            
        print(f"\n🔧 正在处理语言目录: {lang_dir}")
        
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
        
        # 排除非攻略页面
        exclude_files = [
            'index.html',
            'test_*.html',
            'debug_*.html',
            'force_refresh.html',
            'preview.html'
        ]
        
        guide_files = [f for f in guide_files if not any(ex in f.name for ex in exclude_files)]
        
        if not guide_files:
            print(f"   ⏭️  该语言目录下没有攻略页面")
            continue
            
        print(f"   📁 找到 {len(guide_files)} 个攻略页面:")
        for f in guide_files:
            print(f"      - {f.name}")
        
        # 修复每个文件的链接
        fixed_count = 0
        for file_path in guide_files:
            if fix_guide_links(file_path, lang_dir):
                fixed_count += 1
        
        total_fixed += fixed_count
        print(f"   ✅ 该语言目录修复了 {fixed_count} 个文件")
    
    print(f"\n🎉 链接修复完成！总共修复了 {total_fixed} 个文件")
    print("✨ 现在所有语言目录下的攻略页面链接都应该正确了！")
    print("💡 请测试一下链接是否正常工作！")

if __name__ == "__main__":
    main() 