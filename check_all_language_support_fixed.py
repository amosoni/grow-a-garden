#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查所有攻略页面的语言支持情况

这个脚本将检查：
1. 每个攻略页面是否存在于所有12种语言目录中
2. 语言切换器是否包含所有语言选项
3. hreflang标签是否完整
"""

import os
import glob
import re

def get_supported_languages():
    """获取支持的12种语言列表"""
    return ['en', 'zh-cn', 'es', 'pt-br', 'fr', 'de', 'ru', 'ar', 'hi', 'id', 'vi', 'ja']

def get_guide_pages():
    """获取所有攻略页面列表"""
    root_guides = glob.glob('*.html')
    guide_pages = []
    
    for page in root_guides:
        if page.startswith('how-to-') or page.startswith('ice-cream-') or page in ['guides.html', 'index.html', 'online.html']:
            guide_pages.append(page)
    
    return guide_pages

def check_language_coverage():
    """检查语言覆盖情况"""
    
    supported_languages = get_supported_languages()
    guide_pages = get_guide_pages()
    
    print("🔍 检查攻略页面的语言覆盖情况...")
    print("=" * 60)
    
    coverage_report = {}
    
    for guide_page in guide_pages:
        print(f"\n📄 检查攻略页面: {guide_page}")
        coverage_report[guide_page] = {}
        
        for lang in supported_languages:
            lang_file_path = f'{lang}/{guide_page}'
            
            if os.path.exists(lang_file_path):
                coverage_report[guide_page][lang] = '✅ 存在'
                print(f"  ✅ {lang}: 存在")
            else:
                coverage_report[guide_page][lang] = '❌ 缺失'
                print(f"  ❌ {lang}: 缺失")
    
    return coverage_report

def check_language_switcher():
    """检查语言切换器的完整性"""
    
    supported_languages = get_supported_languages()
    guide_pages = get_guide_pages()
    
    print("\n🔍 检查语言切换器的完整性...")
    print("=" * 60)
    
    switcher_report = {}
    
    for guide_page in guide_pages:
        print(f"\n📄 检查攻略页面: {guide_page}")
        switcher_report[guide_page] = {}
        
        # 检查根目录版本
        if os.path.exists(guide_page):
            try:
                with open(guide_page, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否有语言切换器
                if '<select id="lang-switcher">' in content:
                    # 提取语言选项
                    lang_options = re.findall(r'<option value="([^"]+)">', content)
                    
                    if lang_options:
                        missing_langs = set(supported_languages) - set(lang_options)
                        if missing_langs:
                            switcher_report[guide_page]['root'] = f'❌ 缺失语言: {", ".join(missing_langs)}'
                            print(f"  ❌ 根目录: 缺失语言: {', '.join(missing_langs)}")
                        else:
                            switcher_report[guide_page]['root'] = '✅ 完整'
                            print(f"  ✅ 根目录: 语言选项完整")
                    else:
                        switcher_report[guide_page]['root'] = '❌ 未找到语言选项'
                        print(f"  ❌ 根目录: 未找到语言选项")
                else:
                    switcher_report[guide_page]['root'] = '❌ 未找到语言切换器'
                    print(f"  ❌ 根目录: 未找到语言切换器")
                    
            except Exception as e:
                switcher_report[guide_page]['root'] = f'❌ 读取错误: {str(e)}'
                print(f"  ❌ 根目录: 读取错误: {str(e)}")
        
        # 检查中文版本
        zh_cn_file_path = f'zh-cn/{guide_page}'
        if os.path.exists(zh_cn_file_path):
            try:
                with open(zh_cn_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否有语言切换器
                if '<select id="lang-switcher">' in content:
                    # 提取语言选项
                    lang_options = re.findall(r'<option value="([^"]+)">', content)
                    
                    if lang_options:
                        missing_langs = set(supported_languages) - set(lang_options)
                        if missing_langs:
                            switcher_report[guide_page]['zh-cn'] = f'❌ 缺失语言: {", ".join(missing_langs)}'
                            print(f"  ❌ 中文版: 缺失语言: {', '.join(missing_langs)}")
                        else:
                            switcher_report[guide_page]['zh-cn'] = '✅ 完整'
                            print(f"  ✅ 中文版: 语言选项完整")
                    else:
                        switcher_report[guide_page]['zh-cn'] = '❌ 未找到语言选项'
                        print(f"  ❌ 中文版: 未找到语言选项")
                else:
                    switcher_report[guide_page]['zh-cn'] = '❌ 未找到语言切换器'
                    print(f"  ❌ 中文版: 未找到语言切换器")
                    
            except Exception as e:
                switcher_report[guide_page]['zh-cn'] = f'❌ 读取错误: {str(e)}'
                print(f"  ❌ 中文版: 读取错误: {str(e)}")
    
    return switcher_report

def check_hreflang_tags():
    """检查hreflang标签的完整性"""
    
    supported_languages = get_supported_languages()
    guide_pages = get_guide_pages()
    
    print("\n🔍 检查hreflang标签的完整性...")
    print("=" * 60)
    
    hreflang_report = {}
    
    for guide_page in guide_pages:
        print(f"\n📄 检查攻略页面: {guide_page}")
        hreflang_report[guide_page] = {}
        
        # 检查根目录版本
        if os.path.exists(guide_page):
            try:
                with open(guide_page, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查hreflang标签
                hreflang_tags = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', content)
                
                if hreflang_tags:
                    found_langs = [tag[0] for tag in hreflang_tags]
                    missing_langs = set(supported_languages) - set(found_langs)
                    
                    if missing_langs:
                        hreflang_report[guide_page]['root'] = f'❌ 缺失语言: {", ".join(missing_langs)}'
                        print(f"  ❌ 根目录: 缺失hreflang: {', '.join(missing_langs)}")
                    else:
                        hreflang_report[guide_page]['root'] = '✅ 完整'
                        print(f"  ✅ 根目录: hreflang标签完整")
                else:
                    hreflang_report[guide_page]['root'] = '❌ 未找到hreflang标签'
                    print(f"  ❌ 根目录: 未找到hreflang标签")
                    
            except Exception as e:
                hreflang_report[guide_page]['root'] = f'❌ 读取错误: {str(e)}'
                print(f"  ❌ 根目录: 读取错误: {str(e)}")
    
    return hreflang_report

def generate_comprehensive_report(coverage_report, switcher_report, hreflang_report):
    """生成综合报告"""
    
    supported_languages = get_supported_languages()
    guide_pages = get_guide_pages()
    
    print("\n" + "=" * 60)
    print("📊 综合语言支持报告")
    print("=" * 60)
    
    # 语言覆盖统计
    total_pages = len(guide_pages)
    total_languages = len(supported_languages)
    total_expected = total_pages * total_languages
    
    existing_count = 0
    missing_count = 0
    
    for guide_page in guide_pages:
        for lang in supported_languages:
            if guide_page in coverage_report and lang in coverage_report[guide_page]:
                if coverage_report[guide_page][lang] == '✅ 存在':
                    existing_count += 1
                else:
                    missing_count += 1
    
    coverage_percentage = (existing_count / total_expected) * 100
    
    print(f"\n📈 语言覆盖统计:")
    print(f"   - 攻略页面总数: {total_pages}")
    print(f"   - 支持语言总数: {total_languages}")
    print(f"   - 预期页面总数: {total_expected}")
    print(f"   - 实际存在页面: {existing_count}")
    print(f"   - 缺失页面数量: {missing_count}")
    print(f"   - 覆盖率: {coverage_percentage:.1f}%")
    
    # 详细报告
    print(f"\n📋 详细报告:")
    
    for guide_page in guide_pages:
        print(f"\n📄 {guide_page}:")
        
        # 语言覆盖
        if guide_page in coverage_report:
            missing_langs = []
            for lang in supported_languages:
                if lang in coverage_report[guide_page] and coverage_report[guide_page][lang] == '❌ 缺失':
                    missing_langs.append(lang)
            
            if missing_langs:
                print(f"  ❌ 缺失语言版本: {', '.join(missing_langs)}")
            else:
                print(f"  ✅ 所有语言版本完整")
        
        # 语言切换器
        if guide_page in switcher_report:
            if 'root' in switcher_report[guide_page]:
                print(f"  🔘 根目录语言切换器: {switcher_report[guide_page]['root']}")
            if 'zh-cn' in switcher_report[guide_page]:
                print(f"  🔘 中文版语言切换器: {switcher_report[guide_page]['zh-cn']}")
        
        # hreflang标签
        if guide_page in hreflang_report:
            if 'root' in hreflang_report[guide_page]:
                print(f"  🔗 hreflang标签: {hreflang_report[guide_page]['root']}")
    
    # 建议
    print(f"\n💡 改进建议:")
    
    if coverage_percentage < 100:
        print(f"1. 🔧 创建缺失的语言版本页面")
        print(f"2. 🌐 确保每个页面都有完整的12种语言支持")
    
    if missing_count > 0:
        print(f"3. 📝 检查缺失页面的内容质量")
        print(f"4. 🔄 同步更新所有语言版本的内容")
    
    print(f"5. 🎯 完善语言切换器功能")
    print(f"6. 🔗 添加完整的hreflang标签")

def main():
    """主函数"""
    
    print("🚀 开始检查所有攻略页面的语言支持情况...")
    print("=" * 60)
    
    # 1. 检查语言覆盖
    coverage_report = check_language_coverage()
    
    # 2. 检查语言切换器
    switcher_report = check_language_switcher()
    
    # 3. 检查hreflang标签
    hreflang_report = check_hreflang_tags()
    
    # 4. 生成综合报告
    generate_comprehensive_report(coverage_report, switcher_report, hreflang_report)
    
    print(f"\n" + "=" * 60)
    print("🎉 语言支持检查完成！")
    print("=" * 60)

if __name__ == "__main__":
    main() 