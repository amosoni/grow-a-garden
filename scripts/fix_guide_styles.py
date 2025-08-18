#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复攻略页面的CSS样式，确保使用首页的完整样式
包括导航栏、尾部栏和所有视觉效果
"""

import os
import re
from pathlib import Path

def fix_guide_styles(file_path):
    """修复攻略页面的CSS样式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # 1. 确保CSS文件正确引用
        if 'styles.css' not in content:
            # 在head标签中添加CSS引用
            head_match = re.search(r'(</head>)', content)
            if head_match:
                css_link = '\n    <link rel="stylesheet" href="styles.css">'
                insert_pos = head_match.start()
                content = content[:insert_pos] + css_link + content[insert_pos:]
                modified = True
                print(f"  ✅ 已添加CSS引用")
        
        # 2. 确保导航栏使用正确的CSS类
        # 检查导航栏是否有正确的样式类
        if 'class="bg-blur"' in content and 'class="logo"' in content:
            # 导航栏结构正确，检查是否需要添加额外的样式类
            if 'class="nav-container"' not in content:
                # 在header标签上添加nav-container类
                content = re.sub(r'<header>', '<header class="nav-container">', content)
                modified = True
                print(f"  ✅ 已添加nav-container类")
        
        # 3. 确保页面内容有正确的样式类
        # 检查是否有content-wrapper类
        if '<div class="content-wrapper">' not in content:
            # 在header后添加content-wrapper
            header_match = re.search(r'(</header>)', content)
            if header_match:
                insert_pos = header_match.end()
                content = content[:insert_pos] + '\n\n    <div class="content-wrapper">\n' + content[insert_pos:]
                # 在</body>前添加</div>
                content = content.replace('</body>', '    </div>\n\n</body>')
                modified = True
                print(f"  ✅ 已添加content-wrapper包装")
        
        # 4. 确保页面有正确的背景和样式
        # 检查body标签是否有正确的类
        if 'class="guide-page"' not in content:
            # 在body标签上添加guide-page类
            content = re.sub(r'<body([^>]*)>', r'<body\1 class="guide-page">', content)
            modified = True
            print(f"  ✅ 已添加guide-page类")
        
        # 5. 确保导航栏有正确的z-index和定位
        # 检查header样式是否正确
        if 'position: fixed' not in content and 'z-index: 9999' not in content:
            # 这些样式应该在CSS文件中，但我们可以确保HTML结构正确
            if '<header' in content and 'class="nav-container"' in content:
                print(f"  ✅ 导航栏结构已正确")
        
        # 如果内容有变化，写回文件
        if modified and content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已修复样式: {file_path}")
            return True
        else:
            print(f"⏭️  样式已正确: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ 修复失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始修复攻略页面的CSS样式...")
    
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
    
    print(f"📁 找到 {len(guide_files)} 个攻略页面需要检查样式:")
    for f in guide_files:
        print(f"   - {f.name}")
    
    # 修复每个文件
    fixed_count = 0
    for file_path in guide_files:
        print(f"\n🔧 正在检查样式: {file_path.name}")
        if fix_guide_styles(file_path):
            fixed_count += 1
    
    print(f"\n🎉 样式检查完成！共修复了 {fixed_count} 个文件")
    print(f"📊 总计: {len(guide_files)} 个文件")
    print("\n✨ 现在所有攻略页面都应该使用首页的完整CSS样式了！")
    print("💡 如果样式还是不对，请检查浏览器缓存或刷新页面！")

if __name__ == "__main__":
    main() 