#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用首页的完整导航栏和尾部栏样式替换攻略页面
包括完整的HTML结构、CSS类和样式
"""

import os
import re
from pathlib import Path

# 首页的完整导航栏模板（包含所有样式类）
HOME_NAVIGATION = '''    <div class="bg-blur"></div>
    <header>
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

# 首页的完整尾部栏模板（包含所有样式类）
HOME_FOOTER = '''    <footer>
        <div class="footer-content">
            <p data-i18n="footer.copyright">© 2025 Grow a Garden - Real-Time Player Tracker</p>
            <p data-i18n="footer.disclaimer">Not official. Data for reference only.</p>
        </div>
    </footer>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="plants_auto.js"></script>
    <script src="script.js"></script>
    <script src="/i18n/i18n.js"></script>'''

def replace_navigation_and_footer(file_path):
    """用首页的完整样式替换攻略页面的导航栏和尾部栏"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # 1. 替换导航栏 - 查找并替换现有的header部分
        header_patterns = [
            # 模式1: 完整的header标签
            r'<header>.*?</header>',
            # 模式2: 包含bg-blur的header
            r'<div class="bg-blur"></div>\s*<header>.*?</header>',
            # 模式3: 任何header标签
            r'<header>.*?</header>'
        ]
        
        for pattern in header_patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, HOME_NAVIGATION, content, flags=re.DOTALL)
                modified = True
                print(f"  ✅ 已替换导航栏")
                break
        
        # 如果没有找到header，在body标签后添加
        if not modified and '<header>' not in content:
            body_match = re.search(r'(<body[^>]*>)', content)
            if body_match:
                insert_pos = body_match.end()
                content = content[:insert_pos] + '\n' + HOME_NAVIGATION + '\n\n    <div class="content-wrapper">\n' + content[insert_pos:]
                # 在</body>前添加</div>
                content = content.replace('</body>', '    </div>\n\n' + HOME_FOOTER + '\n\n</body>')
                modified = True
                print(f"  ✅ 已添加完整导航栏和尾部栏")
        
        # 2. 替换尾部栏 - 查找并替换现有的footer部分
        footer_patterns = [
            # 模式1: 完整的footer标签
            r'<footer>.*?</footer>',
            # 模式2: 包含script的footer
            r'<footer>.*?</script>\s*</body>',
            # 模式3: 任何footer标签
            r'<footer>.*?</footer>'
        ]
        
        for pattern in footer_patterns:
            if re.search(pattern, content, re.DOTALL):
                # 保留页面特定的script，但替换footer
                content = re.sub(r'<footer>.*?</footer>', '', content, flags=re.DOTALL)
                # 在</body>前添加首页的footer
                content = content.replace('</body>', '\n\n' + HOME_FOOTER + '\n\n</body>')
                modified = True
                print(f"  ✅ 已替换尾部栏")
                break
        
        # 如果没有找到footer，在</body>前添加
        if '<footer>' not in content:
            content = content.replace('</body>', '\n\n' + HOME_FOOTER + '\n\n</body>')
            modified = True
            print(f"  ✅ 已添加尾部栏")
        
        # 3. 确保页面有正确的CSS引用
        if 'styles.css' not in content:
            # 在head标签中添加CSS引用
            head_match = re.search(r'(</head>)', content)
            if head_match:
                css_link = '\n    <link rel="stylesheet" href="styles.css">'
                insert_pos = head_match.start()
                content = content[:insert_pos] + css_link + content[insert_pos:]
                modified = True
                print(f"  ✅ 已添加CSS引用")
        
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
    print("🚀 开始用首页样式替换攻略页面导航栏和尾部栏...")
    
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
    
    # 排除非攻略页面
    exclude_files = [
        'index.html',
        'test_*.html',
        'debug_*.html',
        'force_refresh.html',
        'preview.html'
    ]
    
    guide_files = [f for f in guide_files if not any(ex in f.name for ex in exclude_files)]
    
    print(f"📁 找到 {len(guide_files)} 个攻略页面需要修复:")
    for f in guide_files:
        print(f"   - {f.name}")
    
    # 修复每个文件
    fixed_count = 0
    for file_path in guide_files:
        print(f"\n🔧 正在修复: {file_path.name}")
        if replace_navigation_and_footer(file_path):
            fixed_count += 1
    
    print(f"\n🎉 修复完成！共修复了 {fixed_count} 个文件")
    print(f"📊 总计: {len(guide_files)} 个文件")
    print("\n✨ 现在所有攻略页面都使用首页的完整导航栏和尾部栏样式！")

if __name__ == "__main__":
    main() 