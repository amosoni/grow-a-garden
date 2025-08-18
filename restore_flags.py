#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复原来的图片国旗系统
"""

import os
import glob
import re

def get_html_files():
    """获取所有HTML文件"""
    return glob.glob('**/*.html', recursive=True)

def restore_image_flags(content):
    """恢复图片国旗系统"""
    
    changes_made = []
    
    # 替换emoji国旗为图片国旗
    if 'flag-emoji' in content:
        # 替换span标签为img标签
        content = content.replace('<span class="flag-emoji">🇺🇸</span>', '<img src="flags/en.png" alt="US Flag" class="flag-img">')
        content = content.replace('<span class="flag-emoji">🇨🇳</span>', '<img src="flags/zh-cn.png" alt="CN Flag" class="flag-img">')
        content = content.replace('<span class="flag-emoji">🇪🇸</span>', '<img src="flags/es.png" alt="ES Flag" class="flag-img">')
        content = content.replace('<span class="flag-emoji">🇧🇷</span>', '<img src="flags/pt-br.png" alt="BR Flag" class="flag-img">')
        content = content.replace('<span class="flag-emoji">🇫🇷</span>', '<img src="flags/fr.png" alt="FR Flag" class="flag-img">')
        content = content.replace('<span class="flag-emoji">🇩🇪</span>', '<img src="flags/de.png" alt="DE Flag" class="flag-img">')
        content = content.replace('<span class="flag-emoji">🇷🇺</span>', '<img src="flags/ru.png" alt="RU Flag" class="flag-img">')
        content = content.replace('<span class="flag-emoji">🇸🇦</span>', '<img src="flags/ar.png" alt="SA Flag" class="flag-img">')
        content = content.replace('<span class="flag-emoji">🇮🇳</span>', '<img src="flags/hi.png" alt="IN Flag" class="flag-img">')
        content = content.replace('<span class="flag-emoji">🇮🇩</span>', '<img src="flags/en.png" alt="ID Flag" class="flag-img">')
        content = content.replace('<span class="flag-emoji">🇻🇳</span>', '<img src="flags/vi.png" alt="VN Flag" class="flag-img">')
        content = content.replace('<span class="flag-emoji">🇯🇵</span>', '<img src="flags/ja.png" alt="JP Flag" class="flag-img">')
        changes_made.append('恢复图片国旗HTML结构')
        
        # 替换CSS样式
        if 'flag-emoji' in content:
            content = content.replace('.flag-emoji', '.flag-img')
            changes_made.append('恢复图片国旗CSS样式')
    
    # 修复CSS样式 - 确保flag-img有正确的图片样式
    if '.flag-img' in content and 'font-size:' in content:
        # 替换CSS样式
        old_css = r'\.flag-img\s*\{[^}]*font-size:\s*[^;]*;[^}]*line-height:\s*[^;]*;[^}]*display:\s*[^;]*;[^}]*\}'
        new_css = '''        .flag-img {
            width: 24px;
            height: 16px;
            object-fit: cover;
            border-radius: 2px;
            vertical-align: middle;
        }'''
        
        if re.search(old_css, content, re.DOTALL):
            content = re.sub(old_css, new_css, content, flags=re.DOTALL)
            changes_made.append('修复flag-img CSS样式')
    
    # 修复JavaScript中的错误代码 - 恢复src设置
    if "flag-img').textContent =" in content:
        content = content.replace("flag-img').textContent =", "flag-img').src =")
        changes_made.append('恢复JavaScript中的src设置')
    
    return content, changes_made

def restore_all_files():
    """恢复所有HTML文件的图片国旗系统"""
    
    html_files = get_html_files()
    
    print("🔧 开始恢复原来的图片国旗系统...")
    print("=" * 80)
    
    total_files = len(html_files)
    restored_files = 0
    total_changes = 0
    
    for html_file in html_files:
        print(f"\n📄 处理文件: {html_file}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_changes = []
            
            # 恢复图片国旗系统
            content, changes = restore_image_flags(content)
            file_changes.extend(changes)
            
            if content != original_content:
                # 写回恢复后的内容
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ 成功恢复 {len(file_changes)} 个组件:")
                for change in file_changes:
                    print(f"    - {change}")
                
                restored_files += 1
                total_changes += len(file_changes)
            else:
                print(f"  ✅ 无需修改")
                
        except Exception as e:
            print(f"  ❌ 处理失败: {str(e)}")
    
    print(f"\n" + "=" * 80)
    print("🎯 恢复完成总结")
    print("=" * 80)
    print(f"📊 恢复结果:")
    print(f"   - 总文件数: {total_files}")
    print(f"   - 成功恢复: {restored_files}")
    print(f"   - 失败数量: {total_files - restored_files}")
    print(f"   - 总恢复项: {total_changes}")
    
    if restored_files > 0:
        print(f"\n✅ 成功恢复了 {restored_files} 个文件的图片国旗系统！")
        print(f"🔧 总共恢复了 {total_changes} 个组件")
        print(f"🌍 现在所有页面都使用原来的图片国旗了")
    else:
        print(f"\n⚠️  没有文件需要恢复")
    
    return restored_files, total_changes

def main():
    """主函数"""
    
    print("🔧 开始恢复原来的图片国旗系统...")
    print("=" * 80)
    
    # 恢复所有文件
    restored_files, total_changes = restore_all_files()
    
    print(f"\n" + "=" * 80)
    print("🎉 恢复完成！")
    print("=" * 80)
    
    if restored_files > 0:
        print("✅ 所有页面的图片国旗系统都已恢复！")
        print("🌍 现在所有页面都使用原来的图片国旗了")
    else:
        print("⚠️  没有页面需要恢复")

if __name__ == "__main__":
    main() 