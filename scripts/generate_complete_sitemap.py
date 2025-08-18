#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成完整的sitemap.xml，包含所有多语言版本的页面
"""

import os
import glob
from datetime import datetime

def generate_complete_sitemap():
    """生成包含所有多语言版本的完整sitemap.xml"""
    
    # 支持的语言代码
    languages = ['en', 'zh-cn', 'es', 'pt-br', 'fr', 'de', 'ru', 'ar', 'hi', 'id', 'vi', 'ja']
    
    # 基础页面（不需要语言前缀的页面）
    base_pages = [
        'index.html',
        'online.html',
        'guides.html',
        'farming-basics.html',
        'watering-strategies.html',
        'profit-strategies.html',
        'mutation-guide.html',
        'investment-guide.html',
        'storage-and-logistics.html',
        'how-to-grow-apples.html',
        'how-to-grow-carrots.html',
        'how-to-grow-wheat.html',
        'how-to-grow-corn.html',
        'how-to-grow-oranges.html',
        'how-to-grow-berries.html',
        'how-to-build-farm.html',
        'how-to-make-bread.html',
        'how-to-make-cake.html',
        'how-to-make-cookies.html',
        'how-to-make-donut.html',
        'how-to-make-pie.html',
        'how-to-make-pizza.html',
        'how-to-make-salad.html',
        'how-to-make-sandwich.html',
        'how-to-make-smoothie.html',
        'how-to-make-spaghetti.html',
        'how-to-make-money-fast.html',
        'how-to-play-with-friends.html'
    ]
    
    # 生成sitemap内容
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
    sitemap_content += '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n\n'
    
    # 添加基础页面
    for page in base_pages:
        if os.path.exists(page):
            sitemap_content += f'  <url>\n'
            sitemap_content += f'    <loc>https://growagarden.cv/{page}</loc>\n'
            
            # 添加多语言链接
            for lang in languages:
                lang_dir = lang if lang != 'en' else ''
                lang_path = f'{lang_dir}/{page}' if lang_dir else page
                if os.path.exists(lang_path):
                    hreflang = 'en' if lang == 'en' else lang
                    sitemap_content += f'    <xhtml:link rel="alternate" hreflang="{hreflang}" href="https://growagarden.cv/{lang_path}"/>\n'
            
            sitemap_content += f'    <xhtml:link rel="alternate" hreflang="x-default" href="https://growagarden.cv/{page}"/>\n'
            sitemap_content += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
            sitemap_content += f'    <changefreq>monthly</changefreq>\n'
            sitemap_content += f'    <priority>0.8</priority>\n'
            sitemap_content += f'  </url>\n\n'
    
    # 添加多语言页面
    for lang in languages:
        if lang == 'en':
            continue  # 英文页面已经在上面处理过了
            
        lang_dir = lang
        if os.path.exists(lang_dir):
            for page in base_pages:
                lang_page_path = f'{lang_dir}/{page}'
                if os.path.exists(lang_page_path):
                    sitemap_content += f'  <url>\n'
                    sitemap_content += f'    <loc>https://growagarden.cv/{lang_page_path}</loc>\n'
                    
                    # 添加多语言链接
                    for other_lang in languages:
                        other_lang_dir = other_lang if other_lang != 'en' else ''
                        other_lang_path = f'{other_lang_dir}/{page}' if other_lang_dir else page
                        if os.path.exists(other_lang_path):
                            hreflang = 'en' if other_lang == 'en' else other_lang
                            sitemap_content += f'    <xhtml:link rel="alternate" hreflang="{hreflang}" href="https://growagarden.cv/{other_lang_path}"/>\n'
                    
                    sitemap_content += f'    <xhtml:link rel="alternate" hreflang="x-default" href="https://growagarden.cv/{page}"/>\n'
                    sitemap_content += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
                    sitemap_content += f'    <changefreq>monthly</changefreq>\n'
                    sitemap_content += f'    <priority>0.7</priority>\n'
                    sitemap_content += f'  </url>\n\n'
    
    sitemap_content += '</urlset>'
    
    # 写入文件
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"✅ 已生成完整的sitemap.xml，包含所有多语言版本页面")
    print(f"📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    generate_complete_sitemap() 