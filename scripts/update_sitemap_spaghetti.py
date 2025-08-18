#!/usr/bin/env python3
"""
更新sitemap.xml，添加新的spaghetti页面
"""

import re

def update_sitemap():
    """更新sitemap.xml，添加新的spaghetti页面"""
    
    # 读取现有的sitemap.xml
    with open('sitemap.xml', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到</urlset>标签的位置
    urlset_end = content.find('</urlset>')
    if urlset_end == -1:
        print("❌ 无法找到</urlset>标签")
        return
    
    # 准备新的spaghetti页面条目
    new_entries = []
    
    # 为每个语言添加spaghetti页面
    languages = [
        ('zh-cn', 'zh-CN'),
        ('es', 'es'),
        ('pt-br', 'pt-BR'),
        ('fr', 'fr'),
        ('de', 'de'),
        ('ru', 'ru'),
        ('ar', 'ar'),
        ('hi', 'hi'),
        ('id', 'id'),
        ('vi', 'vi'),
        ('ja', 'ja')
    ]
    
    for lang_code, hreflang in languages:
        # 创建主要URL条目
        main_entry = f'''  <url>
    <loc>https://growagarden.cv/{lang_code}/how-to-make-spaghetti.html</loc>'''
        
        # 添加hreflang链接
        hreflang_links = []
        for code, hreflang_code in languages:
            if code == lang_code:
                hreflang_links.append(f'    <xhtml:link rel="alternate" hreflang="{hreflang_code}" href="https://growagarden.cv/{code}/how-to-make-spaghetti.html"/>')
            else:
                hreflang_links.append(f'    <xhtml:link rel="alternate" hreflang="{hreflang_code}" href="https://growagarden.cv/{code}/how-to-make-spaghetti.html"/>')
        
        # 添加英文版本链接
        hreflang_links.append('    <xhtml:link rel="alternate" hreflang="en" href="https://growagarden.cv/how-to-make-spaghetti.html"/>')
        hreflang_links.append('    <xhtml:link rel="alternate" hreflang="x-default" href="https://growagarden.cv/how-to-make-spaghetti.html"/>')
        
        # 组合完整的条目
        full_entry = f'''{main_entry}
{chr(10).join(hreflang_links)}
    <lastmod>2024-12-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>'''
        
        new_entries.append(full_entry)
    
    # 在</urlset>之前插入新条目
    new_content = content[:urlset_end] + '\n' + '\n'.join(new_entries) + '\n' + content[urlset_end:]
    
    # 写入更新后的文件
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 已成功添加 {len(new_entries)} 个spaghetti页面到sitemap.xml")
    print("📝 添加的页面:")
    for lang_code, _ in languages:
        print(f"   - {lang_code}/how-to-make-spaghetti.html")

if __name__ == "__main__":
    print("🔄 开始更新sitemap.xml...")
    update_sitemap()
    print("�� sitemap.xml更新完成！") 