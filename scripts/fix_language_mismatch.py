#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面检查和修复攻略页面的语言匹配问题
确保每个攻略页面的语言与目录语言一致
"""

import os
import re
from pathlib import Path

def check_language_consistency(file_path, expected_language):
    """检查文件的语言一致性"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # 检查HTML lang属性
        lang_match = re.search(r'<html[^>]*lang=["\']([^"\']+)["\']', content)
        if lang_match:
            actual_lang = lang_match.group(1)
            if actual_lang != expected_language:
                issues.append(f"HTML lang属性不匹配: 期望 {expected_language}, 实际 {actual_lang}")
        else:
            issues.append("缺少HTML lang属性")
        
        # 检查页面标题语言
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
        if title_match:
            title = title_match.group(1)
            # 简单的语言检测（可以根据需要改进）
            if expected_language == "zh-cn" and not re.search(r'[\u4e00-\u9fff]', title):
                issues.append(f"标题应该包含中文: {title}")
            elif expected_language == "ja" and not re.search(r'[\u3040-\u309f\u30a0-\u30ff]', title):
                issues.append(f"标题应该包含日文: {title}")
        
        # 检查导航栏语言
        nav_links = re.findall(r'<a[^>]*data-i18n="([^"]+)"[^>]*>([^<]+)</a>', content)
        if not nav_links:
            issues.append("导航栏缺少data-i18n属性")
        
        # 检查语言切换器
        if 'id="lang-switcher"' not in content:
            issues.append("缺少语言切换器")
        
        # 检查内容语言
        if expected_language == "zh-cn":
            # 检查是否包含中文内容
            chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
            if len(chinese_chars) < 100:  # 至少应该有100个中文字符
                issues.append("中文内容太少，可能还是英文")
        elif expected_language == "ja":
            # 检查是否包含日文内容
            japanese_chars = re.findall(r'[\u3040-\u309f\u30a0-\u30ff]', content)
            if len(japanese_chars) < 100:
                issues.append("日文内容太少，可能还是英文")
        
        return issues
        
    except Exception as e:
        return [f"检查失败: {e}"]

def fix_language_consistency(file_path, expected_language):
    """修复文件的语言一致性问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # 修复HTML lang属性
        if re.search(r'<html[^>]*lang=["\']([^"\']+)["\']', content):
            content = re.sub(r'(<html[^>]*lang=["\'])[^"\']+(["\'])', r'\1' + expected_language + r'\2', content)
            modified = True
        else:
            # 添加lang属性
            content = re.sub(r'(<html[^>]*>)', r'\1 lang="' + expected_language + '"', content)
            modified = True
        
        # 确保语言切换器正确设置当前语言
        if expected_language == "zh-cn":
            content = re.sub(r'(<option value="zh-cn"[^>]*>)[^<]*(</option>)', r'\1简体中文\2', content)
            content = re.sub(r'(<option value="zh-cn"[^>]*>)[^<]*(</option>)', r'\1 selected\2', content)
        elif expected_language == "ja":
            content = re.sub(r'(<option value="ja"[^>]*>)[^<]*(</option>)', r'\1日本語\2', content)
            content = re.sub(r'(<option value="ja"[^>]*>)[^<]*(</option>)', r'\1 selected\2', content)
        
        # 如果内容有变化，写回文件
        if modified and content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ 修复失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始全面检查和修复攻略页面的语言匹配问题...")
    
    # 语言目录映射
    language_mapping = {
        "zh-cn": "zh-CN",
        "ja": "ja",
        "es": "es",
        "pt-br": "pt-BR",
        "fr": "fr",
        "de": "de",
        "ru": "ru",
        "ar": "ar",
        "hi": "hi",
        "id": "id",
        "vi": "vi"
    }
    
    total_issues = 0
    total_fixed = 0
    
    # 检查语言目录
    for lang_dir, lang_code in language_mapping.items():
        lang_path = Path(lang_dir)
        if not lang_path.exists():
            continue
            
        print(f"\n🔍 检查语言目录: {lang_dir} ({lang_code})")
        
        # 查找该语言目录下的所有攻略页面
        guide_files = []
        guide_patterns = [
            'how-to-*.html',
            '*-guide.html',
            '*-strategies.html',
            '*-basics.html',
            '*-tips.html'
        ]
        
        for pattern in guide_patterns:
            guide_files.extend(lang_path.glob(pattern))
        
        if not guide_files:
            print(f"   ⏭️  该语言目录下没有攻略页面")
            continue
        
        print(f"   📁 找到 {len(guide_files)} 个攻略页面")
        
        # 检查每个文件
        for file_path in guide_files:
            print(f"      🔍 检查: {file_path.name}")
            issues = check_language_consistency(file_path, lang_code)
            
            if issues:
                print(f"         ❌ 发现问题:")
                for issue in issues:
                    print(f"            - {issue}")
                total_issues += len(issues)
                
                # 尝试修复
                if fix_language_consistency(file_path, lang_code):
                    print(f"         ✅ 已修复")
                    total_fixed += 1
                else:
                    print(f"         ⚠️  修复失败")
            else:
                print(f"         ✅ 语言一致")
    
    print(f"\n🎉 语言一致性检查完成！")
    print(f"📊 发现问题: {total_issues} 个")
    print(f"📊 成功修复: {total_fixed} 个")
    
    if total_issues > 0:
        print(f"\n⚠️  还有 {total_issues - total_fixed} 个问题需要手动修复")
        print("💡 建议:")
        print("   1. 检查每个语言版本的翻译完整性")
        print("   2. 确保语言切换器正确工作")
        print("   3. 验证页面内容的语言一致性")
    else:
        print("✨ 所有攻略页面的语言都匹配了！")

if __name__ == "__main__":
    main() 