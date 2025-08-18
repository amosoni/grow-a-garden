#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载国旗图片
"""

import os
import requests
from urllib.parse import urljoin

def download_flag_images():
    """下载国旗图片"""
    
    # 创建flags文件夹
    flags_dir = "flags"
    if not os.path.exists(flags_dir):
        os.makedirs(flags_dir)
        print(f"✅ 创建了 {flags_dir} 文件夹")
    
    # 国旗图片URL映射
    flag_urls = {
        'en': 'https://flagcdn.com/w40/us.png',
        'zh-cn': 'https://flagcdn.com/w40/cn.png',
        'es': 'https://flagcdn.com/w40/es.png',
        'pt-br': 'https://flagcdn.com/w40/br.png',
        'fr': 'https://flagcdn.com/w40/fr.png',
        'de': 'https://flagcdn.com/w40/de.png',
        'ru': 'https://flagcdn.com/w40/ru.png',
        'ar': 'https://flagcdn.com/w40/sa.png',
        'hi': 'https://flagcdn.com/w40/in.png',
        'id': 'https://flagcdn.com/w40/id.png',
        'vi': 'https://flagcdn.com/w40/vn.png',
        'ja': 'https://flagcdn.com/w40/jp.png'
    }
    
    print("🔧 开始下载国旗图片...")
    print("=" * 80)
    
    downloaded_count = 0
    failed_count = 0
    
    for lang, url in flag_urls.items():
        try:
            print(f"📥 下载 {lang} 国旗...")
            
            # 下载图片
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # 保存图片
            file_path = os.path.join(flags_dir, f"{lang}.png")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"  ✅ 成功下载: {lang}.png")
            downloaded_count += 1
            
        except Exception as e:
            print(f"  ❌ 下载失败: {lang}.png - {str(e)}")
            failed_count += 1
    
    print(f"\n" + "=" * 80)
    print("🎯 下载完成总结")
    print("=" * 80)
    print(f"📊 下载结果:")
    print(f"   - 成功下载: {downloaded_count}")
    print(f"   - 失败数量: {failed_count}")
    print(f"   - 总数量: {len(flag_urls)}")
    
    if downloaded_count > 0:
        print(f"\n✅ 成功下载了 {downloaded_count} 个国旗图片！")
        print(f"🌍 现在国旗应该可以正确显示了")
        print(f"📁 图片保存在: {flags_dir}/ 文件夹中")
    else:
        print(f"\n⚠️  没有国旗图片下载成功")
    
    return downloaded_count, failed_count

def main():
    """主函数"""
    
    print("🔧 开始下载国旗图片...")
    print("=" * 80)
    
    # 下载国旗图片
    downloaded_count, failed_count = download_flag_images()
    
    print(f"\n" + "=" * 80)
    print("🎉 下载完成！")
    print("=" * 80)
    
    if downloaded_count > 0:
        print("✅ 国旗图片下载完成！")
        print("🌍 现在页面应该可以显示国旗了")
    else:
        print("⚠️  国旗图片下载失败")

if __name__ == "__main__":
    main() 