#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复所有攻略页面的导航栏和尾部栏
统一导航栏结构，添加语言切换器，添加尾部栏
"""

import os
import re
from pathlib import Path

# 统一的导航栏模板
NAVIGATION_TEMPLATE = '''    <header>
        <nav>
            <a href="index.html" class="logo" data-i18n="nav.logo">🌱 Grow a Garden</a>
            <a href="index.html#stats" data-i18n="nav.live">Live Stats</a>
            <a href="index.html#map" data-i18n="nav.map">Global Heatmap</a>
            <a href="index.html#tips" data-i18n="nav.tips">Tips</a>
            <a href="guides.html" data-i18n="nav.guides">📚 Guides</a>
            <a href="index.html#community" class="discord-btn" data-i18n="nav.discord">💬 Discord</a>
            <select id="lang-switcher" aria-label="Language">
                <option value="en">English</option>
                <option value="zh-cn">简体中文</option>
                <option value="es">Español</option>
                <option value="pt-br">Português</option>
                <option value="fr">Français</option>
                <option value="de">Deutsch</option>
                <option value="ru">Русский</option>
                <option value="ar">العربية</option>
                <option value="hi">हिन्दी</option>
                <option value="id">Bahasa Indonesia</option>
                <option value="vi">Tiếng Việt</option>
                <option value="ja">日本語</option>
            </select>
        </nav>
    </header>'''

# 统一的尾部栏模板
FOOTER_TEMPLATE = '''    <footer>
        <div class="footer-content">
            <p data-i18n="footer.copyright">© 2025 Grow a Garden - Real-Time Player Tracker</p>
            <p data-i18n="footer.disclaimer">Not official. Data for reference only.</p>
        </div>
    </footer>'''

def fix_navigation_and_footer(file_path):
    """修复单个文件的导航栏和尾部栏"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # 修复导航栏
        # 查找现有的导航栏并替换
        nav_patterns = [
            # 模式1: 简单的导航栏
            r'<header>\s*<nav>.*?</nav>\s*</header>',
            # 模式2: 带有javascript:void(0)的导航栏
            r'<header>\s*<nav>.*?javascript:void\(0\).*?</nav>\s*</header>',
            # 模式3: 不完整的导航栏
            r'<header>\s*<nav>.*?guides\.html.*?</nav>\s*</header>'
        ]
        
        for pattern in nav_patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, NAVIGATION_TEMPLATE, content, flags=re.DOTALL)
                modified = True
                break
        
        # 如果没有找到导航栏，在body标签后添加
        if not modified and '<header>' not in content:
            body_match = re.search(r'(<body[^>]*>)', content)
            if body_match:
                insert_pos = body_match.end()
                content = content[:insert_pos] + '\n    <div class="bg-blur"></div>\n\n' + NAVIGATION_TEMPLATE + '\n\n    <div class="content-wrapper">\n' + content[insert_pos:]
                # 在</body>前添加</div>
                content = content.replace('</body>', '    </div>\n\n' + FOOTER_TEMPLATE + '\n\n    <script src="script.js"></script>\n</body>')
                modified = True
        
        # 添加尾部栏（如果没有的话）
        if '<footer>' not in content:
            # 在</body>前添加尾部栏
            content = content.replace('</body>', '\n\n' + FOOTER_TEMPLATE + '\n\n</body>')
            modified = True
        
        # 如果内容有变化，写回文件
        if modified and content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已修复: {file_path}")
            return True
        else:
            print(f"⏭️  无需修复: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ 修复失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始批量修复攻略页面导航栏和尾部栏...")
    
    # 查找所有攻略页面
    guide_files = []
    
    # 根目录下的攻略页面
    root_dir = Path('.')
    guide_patterns = [
        'how-to-*.html',
        '*-guide.html',
        '*-strategies.html',
        '*-basics.html',
        '*-tips.html'
    ]
    
    for pattern in guide_patterns:
        guide_files.extend(root_dir.glob(pattern))
    
    # 排除已经修复过的文件
    already_fixed = [
        'guides.html',
        'how-to-make-salad.html',
        'how-to-make-bread.html',
        'how-to-make-donut.html',
        'how-to-make-pizza.html',
        'how-to-make-cake.html',
        'how-to-make-pie.html',
        'how-to-make-spaghetti.html',
        'how-to-grow-wheat.html',
        'how-to-grow-apples.html',
        'how-to-grow-carrots.html'
    ]
    
    guide_files = [f for f in guide_files if f.name not in already_fixed]
    
    print(f"📁 找到 {len(guide_files)} 个攻略页面需要修复:")
    for f in guide_files:
        print(f"   - {f.name}")
    
    # 修复每个文件
    fixed_count = 0
    for file_path in guide_files:
        if fix_navigation_and_footer(file_path):
            fixed_count += 1
    
    print(f"\n🎉 修复完成！共修复了 {fixed_count} 个文件")
    print(f"📊 总计: {len(guide_files)} 个文件")

if __name__ == "__main__":
    main() 