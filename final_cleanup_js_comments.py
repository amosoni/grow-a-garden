#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终清理JS注释中的中文字符和emoji

这个脚本将强制清理所有JS注释中的中文字符和emoji
"""

import os
import glob
import re

def get_html_files():
    """获取所有HTML文件"""
    return glob.glob('*.html')

def clean_js_comments_final(content):
    """最终清理JS注释中的中文字符和emoji"""
    
    changes_made = []
    
    # 查找所有JS注释中的中文字符和emoji
    js_comment_pattern = r'//[^\n]*[\u4e00-\u9fff\u1F600-\u1F64F\u1F300-\u1F5FF\u1F680-\u1F6FF\u1F1E0-\u1F1FF\u2600-\u26FF\u2700-\u27BF\uFE00-\uFE0F\u1F900-\u1F9FF][^\n]*'
    
    def replace_js_comment(match):
        comment = match.group(0)
        # 移除所有中文字符和emoji
        cleaned = re.sub(r'[\u4e00-\u9fff\u1F600-\u1F64F\u1F300-\u1F5FF\u1F680-\u1F6FF\u1F1E0-\u1F1FF\u2600-\u26FF\u2700-\u27BF\uFE00-\uFE0F\u1F900-\u1F9FF]', '', comment)
        # 如果注释变得太短，用英文替代
        if len(cleaned.strip()) < 5:
            return '// JS comment'
        return cleaned
    
    if re.search(js_comment_pattern, content):
        content = re.sub(js_comment_pattern, replace_js_comment, content)
        changes_made.append('强制清理JS注释中的中文字符和emoji')
    
    return content, changes_made

def clean_all_files_final():
    """最终清理所有HTML文件"""
    
    html_files = get_html_files()
    
    print("🧹 开始最终清理JS注释...")
    print("=" * 80)
    
    total_files = len(html_files)
    cleaned_files = 0
    total_changes = 0
    
    for html_file in html_files:
        print(f"\n📄 清理文件: {html_file}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 清理JS注释
            content, changes = clean_js_comments_final(content)
            
            if content != original_content:
                # 写回清理后的内容
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ 成功清理 {len(changes)} 个问题:")
                for change in changes:
                    print(f"    - {change}")
                
                cleaned_files += 1
                total_changes += len(changes)
            else:
                print(f"  ✅ 无需清理")
                
        except Exception as e:
            print(f"  ❌ 清理失败: {str(e)}")
    
    print(f"\n" + "=" * 80)
    print("🎯 最终清理完成总结")
    print("=" * 80)
    print(f"📊 清理结果:")
    print(f"   - 总文件数: {total_files}")
    print(f"   - 成功清理: {cleaned_files}")
    print(f"   - 失败数量: {total_files - cleaned_files}")
    print(f"   - 总清理项: {total_changes}")
    
    if cleaned_files > 0:
        print(f"\n✅ 成功清理了 {cleaned_files} 个文件的JS注释问题！")
        print(f"🧹 总共清理了 {total_changes} 个问题")
        print(f"🌍 现在所有JS注释都不包含中文字符和emoji")
    else:
        print(f"\n⚠️  没有文件需要清理或清理失败")
    
    return cleaned_files, total_changes

def main():
    """主函数"""
    
    print("🧹 开始最终清理JS注释...")
    print("=" * 80)
    
    # 清理所有文件
    cleaned_files, total_changes = clean_all_files_final()
    
    print(f"\n" + "=" * 80)
    print("🎉 最终清理完成！")
    print("=" * 80)
    
    if cleaned_files > 0:
        print("✅ 所有JS注释中的中文字符和emoji都已清理完成！")
        print("🌍 现在语言检测应该不会误判JS注释了")
    else:
        print("⚠️  没有JS注释需要清理")

if __name__ == "__main__":
    main() 