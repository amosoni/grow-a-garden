#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细检查每个攻略页面的语言匹配问题

这个脚本将深入检查：
1. 页面标题和描述的语言一致性
2. 内容文本的语言匹配
3. 元标签的语言一致性
4. 链接和导航的语言匹配
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

def detect_language(text):
    """检测文本语言"""
    # 简单的语言检测规则
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    japanese_chars = re.findall(r'[\u3040-\u309f\u30a0-\u30ff]', text)
    korean_chars = re.findall(r'[\uac00-\ud7af]', text)
    arabic_chars = re.findall(r'[\u0600-\u06ff]', text)
    hindi_chars = re.findall(r'[\u0900-\u097f]', text)
    thai_chars = re.findall(r'[\u0e00-\u0e7f]', text)
    
    if chinese_chars:
        return 'zh-cn'
    elif japanese_chars:
        return 'ja'
    elif korean_chars:
        return 'ko'
    elif arabic_chars:
        return 'ar'
    elif hindi_chars:
        return 'hi'
    elif thai_chars:
        return 'th'
    else:
        # 检查是否包含非英文字符
        non_english = re.findall(r'[^\x00-\x7f]', text)
        if non_english:
            # 尝试识别其他语言
            if any(char in 'áéíóúñü' for char in non_english):
                return 'es'
            elif any(char in 'àâäéèêëïîôöùûüÿç' for char in non_english):
                return 'fr'
            elif any(char in 'äöüß' for char in non_english):
                return 'de'
            elif any(char in 'àáâãçéêíóôõú' for char in non_english):
                return 'pt-br'
            elif any(char in 'а-яё' for char in non_english):
                return 'ru'
            elif any(char in 'àáạảãăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ' for char in non_english):
                return 'vi'
            elif any(char in 'àáạảãăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ' for char in non_english):
                return 'id'
            else:
                return 'unknown'
        else:
            return 'en'

def check_page_language_consistency(guide_page):
    """检查单个页面的语言一致性"""
    
    print(f"\n📄 详细检查页面: {guide_page}")
    print("-" * 50)
    
    try:
        with open(guide_page, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # 1. 检查页面声明的语言
        html_lang_match = re.search(r'<html lang="([^"]+)"', content)
        declared_lang = html_lang_match.group(1) if html_lang_match else 'unknown'
        print(f"  🌐 页面声明语言: {declared_lang}")
        
        # 2. 检查标题语言
        title_match = re.search(r'<title>([^<]+)</title>', content)
        if title_match:
            title = title_match.group(1)
            title_lang = detect_language(title)
            print(f"  📝 标题语言: {title_lang} - {title[:50]}...")
            
            if title_lang != declared_lang and title_lang != 'unknown':
                issues.append(f"标题语言不匹配: 声明{declared_lang}, 实际{title_lang}")
        
        # 3. 检查描述语言
        desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
        if desc_match:
            desc = desc_match.group(1)
            desc_lang = detect_language(desc)
            print(f"  📋 描述语言: {desc_lang} - {desc[:50]}...")
            
            if desc_lang != declared_lang and desc_lang != 'unknown':
                issues.append(f"描述语言不匹配: 声明{declared_lang}, 实际{desc_lang}")
        
        # 4. 检查主要内容语言
        # 查找h1, h2, h3, p标签中的文本
        content_tags = re.findall(r'<(h[1-3]|p)[^>]*>([^<]+)</\1>', content)
        if content_tags:
            content_texts = [tag[1] for tag in content_tags]
            content_sample = ' '.join(content_texts[:5])  # 取前5个文本样本
            content_lang = detect_language(content_sample)
            print(f"  📖 内容语言: {content_lang} - 样本: {content_sample[:100]}...")
            
            if content_lang != declared_lang and content_lang != 'unknown':
                issues.append(f"内容语言不匹配: 声明{declared_lang}, 实际{content_lang}")
        
        # 5. 检查导航链接语言
        nav_links = re.findall(r'<a[^>]*>([^<]+)</a>', content)
        if nav_links:
            nav_texts = [link for link in nav_links if len(link.strip()) > 3]  # 过滤掉太短的链接
            if nav_texts:
                nav_sample = ' '.join(nav_texts[:3])  # 取前3个导航文本
                nav_lang = detect_language(nav_sample)
                print(f"  🧭 导航语言: {nav_lang} - 样本: {nav_sample[:50]}...")
                
                if nav_lang != declared_lang and nav_lang != 'unknown':
                    issues.append(f"导航语言不匹配: 声明{declared_lang}, 实际{nav_lang}")
        
        # 6. 检查混合语言问题
        mixed_language_patterns = [
            (r'[\u4e00-\u9fff].*[a-zA-Z]', '中文+英文混合'),
            (r'[a-zA-Z].*[\u4e00-\u9fff]', '英文+中文混合'),
            (r'[\u4e00-\u9fff].*[\u3040-\u309f\u30a0-\u30ff]', '中文+日文混合'),
            (r'[\u3040-\u309f\u30a0-\u30ff].*[\u4e00-\u9fff]', '日文+中文混合'),
        ]
        
        for pattern, description in mixed_language_patterns:
            if re.search(pattern, content):
                issues.append(f"发现{description}")
        
        # 7. 检查特定语言问题
        if declared_lang == 'en':
            # 英文页面不应该包含其他语言
            if re.search(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af\u0600-\u06ff\u0900-\u097f]', content):
                issues.append("英文页面包含非英文字符")
        
        elif declared_lang == 'zh-cn':
            # 中文页面不应该包含其他语言
            if re.search(r'[\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af\u0600-\u06ff\u0900-\u097f]', content):
                issues.append("中文页面包含非中文字符")
        
        # 输出检查结果
        if issues:
            print(f"  ❌ 发现 {len(issues)} 个语言匹配问题:")
            for issue in issues:
                print(f"    - {issue}")
            return False, issues
        else:
            print(f"  ✅ 语言匹配检查通过")
            return True, []
            
    except Exception as e:
        print(f"  ❌ 检查失败: {str(e)}")
        return False, [f"检查失败: {str(e)}"]

def check_all_pages_language_consistency():
    """检查所有页面的语言一致性"""
    
    guide_pages = get_guide_pages()
    
    print("🔍 开始详细检查每个攻略页面的语言匹配问题...")
    print("=" * 80)
    
    total_pages = len(guide_pages)
    consistent_pages = 0
    inconsistent_pages = 0
    all_issues = []
    
    for guide_page in guide_pages:
        is_consistent, issues = check_page_language_consistency(guide_page)
        
        if is_consistent:
            consistent_pages += 1
        else:
            inconsistent_pages += 1
            all_issues.extend(issues)
    
    # 生成详细报告
    print(f"\n" + "=" * 80)
    print("📊 语言匹配问题详细报告")
    print("=" * 80)
    
    print(f"\n📈 检查结果统计:")
    print(f"   - 总页面数: {total_pages}")
    print(f"   - 语言一致: {consistent_pages}")
    print(f"   - 语言不一致: {inconsistent_pages}")
    print(f"   - 一致率: {(consistent_pages/total_pages)*100:.1f}%")
    
    if all_issues:
        print(f"\n❌ 发现的问题类型:")
        issue_counts = {}
        for issue in all_issues:
            issue_type = issue.split(':')[0] if ':' in issue else issue
            issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        for issue_type, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {issue_type}: {count} 次")
        
        print(f"\n📋 所有问题列表:")
        for i, issue in enumerate(all_issues, 1):
            print(f"   {i}. {issue}")
    
    print(f"\n💡 改进建议:")
    if inconsistent_pages > 0:
        print(f"1. 🔧 修复语言不匹配的页面")
        print(f"2. 🌐 确保每个页面的声明语言与实际内容语言一致")
        print(f"3. 📝 检查并修正混合语言内容")
        print(f"4. 🔍 验证元标签的语言一致性")
    else:
        print(f"✅ 所有页面的语言匹配检查都通过了！")
    
    return consistent_pages, inconsistent_pages, all_issues

def main():
    """主函数"""
    
    print("🔍 开始详细检查每个攻略页面的语言匹配问题...")
    print("=" * 80)
    
    # 检查所有页面的语言一致性
    consistent_pages, inconsistent_pages, all_issues = check_all_pages_language_consistency()
    
    print(f"\n" + "=" * 80)
    print("🎉 语言匹配检查完成！")
    print("=" * 80)
    
    if inconsistent_pages == 0:
        print("🎉 恭喜！所有页面的语言匹配检查都通过了！")
        print("✅ 您的网站语言一致性非常好！")
    else:
        print(f"⚠️  发现 {inconsistent_pages} 个页面存在语言匹配问题")
        print(f"🔧 建议优先修复这些问题以提升用户体验")

if __name__ == "__main__":
    main() 