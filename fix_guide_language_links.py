#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复攻略页面中语言不匹配的链接问题

问题描述：
- 中文版攻略页面中的链接使用了 zh-cn/how-to-make-*.html 格式
- 英文版攻略页面中的链接使用了 en/how-to-make-*.html 格式
- 这些链接应该指向对应语言目录下的页面，而不是在URL中包含语言前缀

修复方案：
- 将 zh-cn/guides.html 中的链接改为 ../how-to-make-*.html
- 将 en/guides.html 中的链接改为 ../how-to-make-*.html
- 其他语言版本类似处理
"""

import os
import re
import glob

def fix_guide_language_links():
    """修复攻略页面中的语言链接问题"""
    
    # 支持的语言代码
    languages = ['en', 'zh-cn', 'es', 'pt-br', 'fr', 'de', 'ru', 'ar', 'hi', 'id', 'vi', 'ja']
    
    fixed_count = 0
    
    for lang in languages:
        guides_file = f'{lang}/guides.html'
        
        if not os.path.exists(guides_file):
            continue
            
        try:
            with open(guides_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            modified = False
            
            # 修复链接格式
            # 将 lang/how-to-make-*.html 改为 ../how-to-make-*.html
            # 将 lang/how-to-grow-*.html 改为 ../how-to-grow-*.html
            # 将 lang/how-to-build-*.html 改为 ../how-to-build-*.html
            # 将 lang/ice-cream-recipe.html 改为 ../ice-cream-recipe.html
            
            patterns_to_fix = [
                (rf'{lang}/how-to-make-([^"]*)\.html', r'../how-to-make-\1.html'),
                (rf'{lang}/how-to-grow-([^"]*)\.html', r'../how-to-grow-\1.html'),
                (rf'{lang}/how-to-build-([^"]*)\.html', r'../how-to-build-\1.html'),
                (rf'{lang}/ice-cream-recipe\.html', r'../ice-cream-recipe.html'),
                (rf'{lang}/farming-basics\.html', r'../farming-basics.html'),
                (rf'{lang}/watering-strategies\.html', r'../watering-strategies.html'),
                (rf'{lang}/profit-strategies\.html', r'../profit-strategies.html'),
                (rf'{lang}/mutation-guide\.html', r'../mutation-guide.html'),
                (rf'{lang}/investment-guide\.html', r'../investment-guide.html'),
                (rf'{lang}/storage-and-logistics\.html', r'../storage-and-logistics.html'),
                (rf'{lang}/game-mechanics\.html', r'../game-mechanics.html'),
                (rf'{lang}/special-events\.html', r'../special-events.html'),
                (rf'{lang}/speed-running\.html', r'../speed-running.html'),
                (rf'{lang}/resource-management\.html', r'../resource-management.html'),
                (rf'{lang}/crop-rotation\.html', r'../crop-rotation.html'),
                (rf'{lang}/seed-selection\.html', r'../seed-selection.html'),
                (rf'{lang}/market-analysis\.html', r'../market-analysis.html'),
            ]
            
            for pattern, replacement in patterns_to_fix:
                if re.search(pattern, content):
                    old_content = content
                    content = re.sub(pattern, replacement, content)
                    if old_content != content:
                        modified = True
                        print(f"✅ 修复 {guides_file}: {pattern} -> {replacement}")
            
            # 如果内容有修改，保存文件
            if modified:
                with open(guides_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                
        except Exception as e:
            print(f"❌ 处理 {guides_file} 时出错: {str(e)}")
    
    # 修复根目录的guides.html
    root_guides = 'guides.html'
    if os.path.exists(root_guides):
        try:
            with open(root_guides, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            modified = False
            
            # 修复根目录攻略页面的链接，确保指向正确的页面
            # 这里不需要添加语言前缀，因为根目录的页面本身就是英文版
            
            if modified:
                with open(root_guides, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print(f"✅ 修复根目录攻略页面: {root_guides}")
                
        except Exception as e:
            print(f"❌ 处理根目录攻略页面时出错: {str(e)}")
    
    print(f"\n🎉 攻略页面语言链接修复完成！共修复了 {fixed_count} 个文件")
    return fixed_count

def verify_fixes():
    """验证修复结果"""
    
    print("\n🔍 验证修复结果...")
    
    # 检查是否还有错误的链接格式
    languages = ['en', 'zh-cn', 'es', 'pt-br', 'fr', 'de', 'ru', 'ar', 'hi', 'id', 'vi', 'ja']
    
    for lang in languages:
        guides_file = f'{lang}/guides.html'
        
        if not os.path.exists(guides_file):
            continue
            
        try:
            with open(guides_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否还有错误的链接格式
            wrong_patterns = [
                rf'{lang}/how-to-make-',
                rf'{lang}/how-to-grow-',
                rf'{lang}/how-to-build-',
                rf'{lang}/ice-cream-recipe',
            ]
            
            for pattern in wrong_patterns:
                if re.search(pattern, content):
                    print(f"⚠️  {guides_file} 仍存在错误链接: {pattern}")
                else:
                    print(f"✅ {guides_file} 链接格式正确")
                    
        except Exception as e:
            print(f"❌ 验证 {guides_file} 时出错: {str(e)}")

def main():
    """主函数"""
    
    print("🔧 开始修复攻略页面中的语言链接问题...")
    print("=" * 60)
    
    # 1. 修复语言链接
    print("\n🔧 步骤1: 修复语言链接")
    fixed_count = fix_guide_language_links()
    
    # 2. 验证修复结果
    print("\n🔍 步骤2: 验证修复结果")
    verify_fixes()
    
    # 总结
    print("\n" + "=" * 60)
    print("🎉 攻略页面语言链接修复完成！")
    print(f"📊 修复统计:")
    print(f"   - 修复文件数: {fixed_count}")
    print(f"   - 修复类型: 语言链接格式")
    
    print("\n📋 修复说明:")
    print("1. 将语言前缀从链接中移除")
    print("2. 使用相对路径 ../ 指向上级目录")
    print("3. 确保每个语言版本的攻略页面链接正确")
    
    print("\n💡 下一步建议:")
    print("1. 测试所有攻略页面的链接是否正常工作")
    print("2. 验证多语言导航功能")
    print("3. 检查SEO和用户体验")

if __name__ == "__main__":
    main() 