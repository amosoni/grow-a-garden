#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有HTML页面的SEO问题
- 修复canonical URL（添加https://协议）
- 确保hreflang标签正确
- 添加必要的meta标签
"""

import os
import re
import glob

def fix_seo_issues():
    """修复所有HTML页面的SEO问题"""
    
    # 支持的语言代码
    languages = ['en', 'zh-cn', 'es', 'pt-br', 'fr', 'de', 'ru', 'ar', 'hi', 'id', 'vi', 'ja']
    
    # 获取所有HTML文件
    html_files = glob.glob('*.html') + glob.glob('*/**/*.html', recursive=True)
    
    fixed_count = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            modified = False
            
            # 检测当前页面的语言
            current_lang = 'en'  # 默认语言
            if '/zh-cn/' in file_path:
                current_lang = 'zh-cn'
            elif '/es/' in file_path:
                current_lang = 'en'
            elif '/pt-br/' in file_path:
                current_lang = 'pt-br'
            elif '/fr/' in file_path:
                current_lang = 'fr'
            elif '/de/' in file_path:
                current_lang = 'de'
            elif '/ru/' in file_path:
                current_lang = 'ru'
            elif '/ar/' in file_path:
                current_lang = 'ar'
            elif '/hi/' in file_path:
                current_lang = 'hi'
            elif '/id/' in file_path:
                current_lang = 'id'
            elif '/vi/' in file_path:
                current_lang = 'vi'
            elif '/ja/' in file_path:
                current_lang = 'ja'
            
            # 获取页面名称（去掉语言前缀和.html后缀）
            page_name = os.path.basename(file_path).replace('.html', '')
            if '/' in file_path:
                page_name = file_path.split('/')[-1].replace('.html', '')
            
            # 修复canonical URL
            canonical_pattern = r'<link rel="canonical" href="([^"]*)"'
            canonical_match = re.search(canonical_pattern, content)
            
            if canonical_match:
                old_canonical = canonical_match.group(1)
                if not old_canonical.startswith('https://'):
                    new_canonical = f'https://{old_canonical}' if not old_canonical.startswith('//') else f'https:{old_canonical}'
                    content = content.replace(f'href="{old_canonical}"', f'href="{new_canonical}"')
                    modified = True
                    print(f"✅ 修复 {file_path} 的canonical URL: {old_canonical} -> {new_canonical}")
            
            # 修复hreflang标签
            hreflang_pattern = r'<link rel="alternate" hreflang="([^"]*)" href="([^"]*)"'
            hreflang_matches = re.findall(hreflang_pattern, content)
            
            for hreflang, href in hreflang_matches:
                if not href.startswith('https://'):
                    new_href = f'https://{href}' if not href.startswith('//') else f'https:{href}'
                    content = content.replace(f'href="{href}"', f'href="{new_href}"')
                    modified = True
                    print(f"✅ 修复 {file_path} 的hreflang URL: {href} -> {new_href}")
            
            # 添加或修复meta description（如果没有的话）
            if '<meta name="description"' not in content:
                # 根据页面类型生成描述
                descriptions = {
                    'index': 'Play Grow a Garden game online. Experience the ultimate farming adventure with plant seeds, mutations, and multiplayer features!',
                    'online': 'Play Grow a Garden game online. Experience the ultimate farming adventure with plant seeds, mutations, and multiplayer features!',
                    'guides': 'Complete guides for Grow a Garden game. Learn farming strategies, plant care, and money-making tips.',
                    'farming-basics': 'Learn the basics of farming in Grow a Garden. Essential tips for beginners to start their farming journey.',
                    'watering-strategies': 'Master watering strategies in Grow a Garden. Learn when and how to water your plants for optimal growth.',
                    'profit-strategies': 'Discover profit strategies in Grow a Garden. Learn how to maximize your earnings and build a profitable farm.',
                    'mutation-guide': 'Complete mutation guide for Grow a Garden. Learn how to discover and cultivate rare plant mutations.',
                    'investment-guide': 'Investment guide for Grow a Garden. Learn how to invest wisely in your farm and maximize returns.',
                    'storage-and-logistics': 'Storage and logistics guide for Grow a Garden. Learn how to efficiently manage your farm resources.',
                    'how-to-grow-apples': 'Learn how to grow apples in Grow a Garden. Complete guide for apple farming and care.',
                    'how-to-grow-carrots': 'Learn how to grow carrots in Grow a Garden. Complete guide for carrot farming and care.',
                    'how-to-grow-wheat': 'Learn how to grow wheat in Grow a Garden. Complete guide for wheat farming and care.',
                    'how-to-grow-corn': 'Learn how to grow corn in Grow a Garden. Complete guide for corn farming and care.',
                    'how-to-grow-oranges': 'Learn how to grow oranges in Grow a Garden. Complete guide for orange farming and care.',
                    'how-to-grow-berries': 'Learn how to grow berries in Grow a Garden. Complete guide for berry farming and care.',
                    'how-to-build-farm': 'Learn how to build a farm in Grow a Garden. Complete guide for farm construction and layout.',
                    'how-to-make-bread': 'Learn how to make bread in Grow a Garden. Complete recipe and cooking guide.',
                    'how-to-make-cake': 'Learn how to make cake in Grow a Garden. Complete recipe and cooking guide.',
                    'how-to-make-cookies': 'Learn how to make cookies in Grow a Garden. Complete recipe and cooking guide.',
                    'how-to-make-donut': 'Learn how to make donuts in Grow a Garden. Complete recipe and cooking guide.',
                    'how-to-make-pie': 'Learn how to make pie in Grow a Garden. Complete recipe and cooking guide.',
                    'how-to-make-pizza': 'Learn how to make pizza in Grow a Garden. Complete recipe and cooking guide.',
                    'how-to-make-salad': 'Learn how to make salad in Grow a Garden. Complete recipe and cooking guide.',
                    'how-to-make-sandwich': 'Learn how to make sandwich in Grow a Garden. Complete recipe and cooking guide.',
                    'how-to-make-smoothie': 'Learn how to make smoothie in Grow a Garden. Complete recipe and cooking guide.',
                    'how-to-make-spaghetti': 'Learn how to make spaghetti in Grow a Garden. Complete recipe and cooking guide.',
                    'how-to-make-money-fast': 'Learn how to make money fast in Grow a Garden. Complete guide for earning money quickly.',
                    'how-to-play-with-friends': 'Learn how to play with friends in Grow a Garden. Complete multiplayer guide.'
                }
                
                description = descriptions.get(page_name, f'Complete guide for {page_name} in Grow a Garden game.')
                
                # 在title标签后添加meta description
                title_pattern = r'(<title>[^<]*</title>)'
                title_match = re.search(title_pattern, content)
                if title_match:
                    meta_description = f'\n  <meta name="description" content="{description}">'
                    content = content.replace(title_match.group(1), title_match.group(1) + meta_description)
                    modified = True
                    print(f"✅ 为 {file_path} 添加了meta description")
            
            # 添加结构化数据（JSON-LD）
            if '<script type="application/ld+json">' not in content:
                # 在</head>标签前添加结构化数据
                structured_data = '''
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "Grow a Garden - ''' + page_name.replace('-', ' ').title() + '''",
    "description": "Complete guide for ''' + page_name.replace('-', ' ').title() + ''' in Grow a Garden game",
    "url": "https://growagarden.cv/''' + file_path.replace('\\', '/') + '''",
    "inLanguage": "''' + current_lang + '''",
    "isPartOf": {
      "@type": "WebSite",
      "name": "Grow a Garden",
      "url": "https://growagarden.cv"
    }
  }
  </script>'''
                
                content = content.replace('</head>', structured_data + '\n</head>')
                modified = True
                print(f"✅ 为 {file_path} 添加了结构化数据")
            
            # 如果内容有修改，保存文件
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                
        except Exception as e:
            print(f"❌ 处理 {file_path} 时出错: {str(e)}")
    
    print(f"\n🎉 SEO修复完成！共修复了 {fixed_count} 个文件")
    print("📝 修复内容包括:")
    print("   - 修复了canonical URL（添加https://协议）")
    print("   - 修复了hreflang标签的URL")
    print("   - 添加了meta description标签")
    print("   - 添加了结构化数据（JSON-LD）")

if __name__ == "__main__":
    fix_seo_issues() 