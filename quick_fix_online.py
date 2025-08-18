#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速修复online.html文件
"""

def fix_online_html():
    """修复online.html文件"""
    
    print("🔧 开始快速修复online.html...")
    
    try:
        with open('online.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # 修复所有损坏的链接和属性
        fixes = [
            ('https://./..../..', 'https://unpkg.com/simple.css@2.1.0/simple.min.css'),
            ('data:image./svg+xml,<svg xmlns=\'http://.././\' \'   \' \'.\' -\'\'🌱//', 'data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>🌱</text></svg>'),
            ('center center./cover', 'center center/cover'),
            ('"@context": "https://."', '"@context": "https://schema.org"'),
            ('"url": "https://./."', '"url": "https://growagarden.cv/online.html"'),
            ('"url": "https:// JS comment', '"url": "https://growagarden.cv"'),
            ('https://.././--', 'https://www.miniplay.com/embed/grow-a-garden'),
            ('https://./-./&&', 'https://playhop.com/dist-app/437622?header=no&utm_source=distrib&utm_medium=gameflare'),
            ('./\./(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)\//', '/(zh-cn|en|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)/'),
            ('./\' +  + \'./\'', './' + 'lang' + './'),
            ('// （）', '// 使用i18n系统'),
            ('//  - ', '// 初始化当前语言 - 根据URL路径设置正确的语言'),
            ('// ，DOM', '// 延迟再次初始化，确保DOM完全加载')
        ]
        
        for old_text, new_text in fixes:
            if old_text in content:
                content = content.replace(old_text, new_text)
                changes_made.append(f'修复: {old_text[:30]}...')
        
        if content != original_content:
            # 写回修复后的内容
            with open('online.html', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 成功修复 {len(changes_made)} 个问题:")
            for change in changes_made:
                print(f"  - {change}")
        else:
            print("✅ 无需修复")
            
    except Exception as e:
        print(f"❌ 修复失败: {str(e)}")

if __name__ == "__main__":
    fix_online_html() 