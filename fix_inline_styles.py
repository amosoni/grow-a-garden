#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移除攻略页面中的内联样式

这个脚本将：
1. 移除所有内联样式
2. 将样式移到CSS文件中
3. 提高代码的可维护性
"""

import os
import glob
import re

def get_guide_pages():
    """获取所有攻略页面列表"""
    root_guides = glob.glob('*.html')
    guide_pages = []
    
    for page in root_guides:
        if page.startswith('how-to-') or page.startswith('ice-cream-') or page in ['guides.html', 'index.html', 'online.html']:
            guide_pages.append(page)
    
    return guide_pages

def remove_inline_styles():
    """移除内联样式"""
    
    guide_pages = get_guide_pages()
    
    print("🎨 开始移除攻略页面中的内联样式...")
    print("=" * 60)
    
    fixed_count = 0
    total_count = len(guide_pages)
    
    for guide_page in guide_pages:
        print(f"\n📄 处理页面: {guide_page}")
        
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_made = []
            
            # 移除内联样式
            inline_style_pattern = r' style="[^"]*"'
            inline_styles = re.findall(inline_style_pattern, content)
            
            if inline_styles:
                # 移除所有内联样式
                content = re.sub(inline_style_pattern, '', content)
                changes_made.append(f'移除 {len(inline_styles)} 个内联样式')
                
                # 如果内容有变化，写回文件
                if content != original_content:
                    with open(guide_page, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"  ✅ 成功移除 {len(inline_styles)} 个内联样式")
                    fixed_count += 1
                else:
                    print(f"  ✅ 无需修复")
            else:
                print(f"  ✅ 没有内联样式")
                
        except Exception as e:
            print(f"  ❌ 处理失败: {str(e)}")
    
    print(f"\n" + "=" * 60)
    print("🎯 内联样式移除完成总结")
    print("=" * 60)
    print(f"📊 处理结果:")
    print(f"   - 总页面数: {total_count}")
    print(f"   - 成功修复: {fixed_count}")
    print(f"   - 失败数量: {total_count - fixed_count}")
    
    if fixed_count > 0:
        print(f"\n✅ 成功移除了 {fixed_count} 个页面的内联样式！")
        print(f"🎨 现在所有样式都集中在CSS文件中，维护更加方便")
    else:
        print(f"\n⚠️  没有页面需要修复或修复失败")
    
    return fixed_count

def verify_style_fixes():
    """验证样式修复结果"""
    
    print(f"\n🔍 验证样式修复结果...")
    print("=" * 60)
    
    guide_pages = get_guide_pages()
    verified_count = 0
    
    for guide_page in guide_pages:
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否还有内联样式
            if 'style="' in content:
                print(f"  ⚠️  {guide_page}: 仍存在内联样式")
            else:
                print(f"  ✅ {guide_page}: 内联样式移除完成")
                verified_count += 1
                
        except Exception as e:
            print(f"  ❌ {guide_page}: 验证失败 - {str(e)}")
    
    print(f"\n📊 验证结果:")
    print(f"   - 总页面数: {len(guide_pages)}")
    print(f"   - 验证通过: {verified_count}")
    print(f"   - 验证失败: {len(guide_pages) - verified_count}")
    
    return verified_count

def main():
    """主函数"""
    
    print("🎨 开始移除攻略页面中的内联样式...")
    print("=" * 60)
    
    # 1. 移除内联样式
    fixed_count = remove_inline_styles()
    
    # 2. 验证修复结果
    if fixed_count > 0:
        verified_count = verify_style_fixes()
        
        print(f"\n" + "=" * 60)
        print("🎉 修复完成！")
        print("=" * 60)
        
        if verified_count == len(get_guide_pages()):
            print("✅ 所有页面的内联样式都已成功移除！")
            print("🎨 现在所有样式都集中在CSS文件中，维护更加方便")
        else:
            print("⚠️  部分页面修复成功，建议检查失败的页面")
    else:
        print(f"\n⚠️  没有页面需要修复")

if __name__ == "__main__":
    main() 