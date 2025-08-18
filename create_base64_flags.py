#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建base64编码的国旗图片
"""

import base64
import os

def create_base64_flags():
    """创建base64编码的国旗图片"""
    
    # 创建flags文件夹
    flags_dir = "flags"
    if not os.path.exists(flags_dir):
        os.makedirs(flags_dir)
        print(f"✅ 创建了 {flags_dir} 文件夹")
    
    # 简单的国旗SVG内容（base64编码）
    flag_svgs = {
        'en': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 480">
            <defs><clipPath id="a"><path d="M-85.3 0h682.6v512H-85.3z"/></clipPath></defs>
            <clipPath id="b"><use href="#a"/></clipPath>
            <g clip-path="url(#b)" transform="scale(.9375)">
                <g fill-rule="evenodd" stroke-width="1pt">
                    <path d="M-256 0H768v512H-256z" fill="#bd3d44"/>
                    <path d="M-256 0H768v102.4H-256z" fill="#fff"/>
                    <path d="M-256 102.4H768v102.4H-256z" fill="#fff"/>
                    <path d="M-256 204.8H768v102.4H-256z" fill="#fff"/>
                    <path d="M-256 307.2H768v102.4H-256z" fill="#fff"/>
                    <path d="M-256 409.6H768V512H-256z" fill="#fff"/>
                </g>
                <g fill="#192f5d">
                    <path d="M-256 0v512l256-256z"/>
                </g>
            </g>
        </svg>''',
        
        'zh-cn': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
            <rect width="900" height="600" fill="#de2910"/>
            <g fill="#ffde00">
                <path d="M450 120l-45.7 140.7-119.3 0h154l-119.3 0z"/>
                <path d="M450 300l-45.7 140.7-119.3 0h154l-119.3 0z"/>
                <path d="M450 480l-45.7 140.7-119.3 0h154l-119.3 0z"/>
            </g>
        </svg>''',
        
        'es': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 500">
            <rect width="750" height="500" fill="#c60b1e"/>
            <rect width="750" height="250" y="125" fill="#ffc400"/>
        </svg>''',
        
        'pt-br': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 504">
            <rect width="720" height="504" fill="#009b3a"/>
            <path d="M360 252l-180-126v252z" fill="#fedf00"/>
            <circle cx="360" cy="252" r="60" fill="#002776"/>
        </svg>''',
        
        'fr': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
            <rect width="300" height="600" fill="#002395"/>
            <rect width="300" height="600" x="300" fill="#fff"/>
            <rect width="300" height="600" x="600" fill="#ed2939"/>
        </svg>''',
        
        'de': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
            <rect width="900" height="200" fill="#000"/>
            <rect width="900" height="200" y="200" fill="#dd0000"/>
            <rect width="900" height="200" y="400" fill="#ffce00"/>
        </svg>''',
        
        'ru': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
            <rect width="900" height="200" fill="#fff"/>
            <rect width="900" height="200" y="200" fill="#0039a6"/>
            <rect width="900" height="200" y="400" fill="#d52b1e"/>
        </svg>''',
        
        'ar': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
            <rect width="900" height="600" fill="#006c35"/>
            <rect width="900" height="400" y="100" fill="#fff"/>
            <rect width="900" height="200" y="200" fill="#ce1126"/>
        </svg>''',
        
        'hi': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
            <rect width="900" height="200" fill="#ff9933"/>
            <rect width="900" height="200" y="200" fill="#fff"/>
            <rect width="900" height="200" y="400" fill="#138808"/>
            <circle cx="450" cy="300" r="60" fill="#000080"/>
        </svg>''',
        
        'id': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
            <rect width="900" height="300" fill="#fff"/>
            <rect width="900" height="300" y="300" fill="#ce1126"/>
        </svg>''',
        
        'vi': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
            <rect width="900" height="600" fill="#da251d"/>
            <path d="M450 300l-180-126v252z" fill="#ffff00"/>
        </svg>''',
        
        'ja': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
            <rect width="900" height="600" fill="#fff"/>
            <circle cx="450" cy="300" r="180" fill="#bc002d"/>
        </svg>'''
    }
    
    print("🔧 开始创建国旗图片...")
    print("=" * 80)
    
    created_count = 0
    
    for lang, svg_content in flag_svgs.items():
        try:
            print(f"🎨 创建 {lang} 国旗...")
            
            # 将SVG转换为base64
            svg_bytes = svg_content.encode('utf-8')
            base64_content = base64.b64encode(svg_bytes).decode('utf-8')
            
            # 创建HTML文件，使用base64图片
            html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{lang} Flag</title>
</head>
<body style="margin:0;padding:0;">
    <img src="data:image/svg+xml;base64,{base64_content}" 
         alt="{lang} Flag" 
         style="width:100%;height:100%;object-fit:contain;">
</body>
</html>'''
            
            # 保存HTML文件
            file_path = os.path.join(flags_dir, f"{lang}.html")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"  ✅ 成功创建: {lang}.html")
            created_count += 1
            
        except Exception as e:
            print(f"  ❌ 创建失败: {lang} - {str(e)}")
    
    print(f"\n" + "=" * 80)
    print("🎯 创建完成总结")
    print("=" * 80)
    print(f"📊 创建结果:")
    print(f"   - 成功创建: {created_count}")
    print(f"   - 总数量: {len(flag_svgs)}")
    
    if created_count > 0:
        print(f"\n✅ 成功创建了 {created_count} 个国旗文件！")
        print(f"🌍 现在国旗应该可以正确显示了")
        print(f"📁 文件保存在: {flags_dir}/ 文件夹中")
        print(f"💡 注意：这些是HTML文件，包含base64编码的SVG国旗")
    else:
        print(f"\n⚠️  没有国旗文件创建成功")
    
    return created_count

def main():
    """主函数"""
    
    print("🔧 开始创建国旗图片...")
    print("=" * 80)
    
    # 创建国旗文件
    created_count = create_base64_flags()
    
    print(f"\n" + "=" * 80)
    print("🎉 创建完成！")
    print("=" * 80)
    
    if created_count > 0:
        print("✅ 国旗文件创建完成！")
        print("🌍 现在页面应该可以显示国旗了")
    else:
        print("⚠️  国旗文件创建失败")

if __name__ == "__main__":
    main() 