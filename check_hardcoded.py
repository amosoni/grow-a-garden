#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查攻略页面中的硬编码问题
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

def check_hardcoded_text():
    """检查硬编码的文本内容"""
    
    guide_pages = get_guide_pages()
    
    print("🔍 检查攻略页面中的硬编码文本内容...")
    print("=" * 60)
    
    hardcoded_text_report = {}
    
    for guide_page in guide_pages:
        print(f"\n📄 检查攻略页面: {guide_page}")
        hardcoded_text_report[guide_page] = []
        
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查硬编码的英文文本
            hardcoded_patterns = [
                r'<h1[^>]*>([^<]+)</h1>',  # 标题
                r'<h2[^>]*>([^<]+)</h2>',  # 副标题
                r'<h3[^>]*>([^<]+)</h3>',  # 小标题
                r'<p[^>]*>([^<]+)</p>',    # 段落
                r'<li[^>]*>([^<]+)</li>',  # 列表项
            ]
            
            for pattern in hardcoded_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    # 检查是否包含英文文本
                    if re.search(r'[a-zA-Z]{3,}', match) and not re.search(r'[<>"\']', match):
                        # 检查是否应该使用i18n
                        if not re.search(r'data-i18n', match):
                            hardcoded_text_report[guide_page].append({
                                'type': 'hardcoded_text',
                                'content': match.strip()[:50],
                                'pattern': pattern
                            })
            
            if hardcoded_text_report[guide_page]:
                print(f"  ❌ 发现 {len(hardcoded_text_report[guide_page])} 个硬编码文本")
                for item in hardcoded_text_report[guide_page][:3]:
                    print(f"    - {item['type']}: {item['content']}...")
            else:
                print(f"  ✅ 未发现硬编码文本")
                
        except Exception as e:
            print(f"  ❌ 读取失败: {str(e)}")
    
    return hardcoded_text_report

def check_hardcoded_urls():
    """检查硬编码的URL路径"""
    
    guide_pages = get_guide_pages()
    
    print("\n🔍 检查攻略页面中的硬编码URL路径...")
    print("=" * 60)
    
    hardcoded_url_report = {}
    
    for guide_page in guide_pages:
        print(f"\n📄 检查攻略页面: {guide_page}")
        hardcoded_url_report[guide_page] = []
        
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查硬编码的URL
            url_patterns = [
                r'href="([^"]+)"',
                r'src="([^"]+)"',
            ]
            
            for pattern in url_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    # 检查是否是硬编码的绝对路径
                    if match.startswith('/') and not match.startswith('//'):
                        hardcoded_url_report[guide_page].append({
                            'type': 'hardcoded_url',
                            'url': match,
                            'pattern': pattern
                        })
            
            if hardcoded_url_report[guide_page]:
                print(f"  ❌ 发现 {len(hardcoded_url_report[guide_page])} 个硬编码URL")
                for item in hardcoded_url_report[guide_page][:3]:
                    print(f"    - {item['type']}: {item['url']}")
            else:
                print(f"  ✅ 未发现硬编码URL")
                
        except Exception as e:
            print(f"  ❌ 读取失败: {str(e)}")
    
    return hardcoded_url_report

def check_hardcoded_styles():
    """检查硬编码的样式和配置"""
    
    guide_pages = get_guide_pages()
    
    print("\n🔍 检查攻略页面中的硬编码样式和配置...")
    print("=" * 60)
    
    hardcoded_style_report = {}
    
    for guide_page in guide_pages:
        print(f"\n📄 检查攻略页面: {guide_page}")
        hardcoded_style_report[guide_page] = []
        
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查内联样式
            inline_style_pattern = r'style="([^"]+)"'
            inline_styles = re.findall(inline_style_pattern, content)
            
            if inline_styles:
                hardcoded_style_report[guide_page].append({
                    'type': 'inline_styles',
                    'count': len(inline_styles)
                })
                print(f"  ❌ 发现 {len(inline_styles)} 个内联样式")
            else:
                print(f"  ✅ 未发现内联样式")
            
            # 检查硬编码的颜色值
            color_patterns = [
                r'#[0-9a-fA-F]{3,6}',  # 十六进制颜色
                r'rgb\([^)]+\)',         # RGB颜色
            ]
            
            for pattern in color_patterns:
                colors = re.findall(pattern, content)
                if colors:
                    hardcoded_style_report[guide_page].append({
                        'type': 'hardcoded_colors',
                        'count': len(colors)
                    })
                    print(f"  ❌ 发现 {len(colors)} 个硬编码颜色值")
                
        except Exception as e:
            print(f"  ❌ 读取失败: {str(e)}")
    
    return hardcoded_style_report

def generate_report(text_report, url_report, style_report):
    """生成硬编码问题综合报告"""
    
    print("\n" + "=" * 60)
    print("📊 硬编码问题综合报告")
    print("=" * 60)
    
    guide_pages = get_guide_pages()
    
    total_issues = 0
    pages_with_issues = 0
    
    for guide_page in guide_pages:
        page_issues = 0
        
        if guide_page in text_report:
            page_issues += len(text_report[guide_page])
        if guide_page in url_report:
            page_issues += len(url_report[guide_page])
        if guide_page in style_report:
            page_issues += len(style_report[guide_page])
        
        if page_issues > 0:
            pages_with_issues += 1
            total_issues += page_issues
    
    print(f"\n📈 问题统计:")
    print(f"   - 攻略页面总数: {len(guide_pages)}")
    print(f"   - 存在问题页面: {pages_with_issues}")
    print(f"   - 问题总数: {total_issues}")
    
    # 详细报告
    print(f"\n📋 详细问题报告:")
    
    for guide_page in guide_pages:
        page_issues = []
        
        if guide_page in text_report and text_report[guide_page]:
            page_issues.append(f"硬编码文本: {len(text_report[guide_page])}个")
        if guide_page in url_report and url_report[guide_page]:
            page_issues.append(f"硬编码URL: {len(url_report[guide_page])}个")
        if guide_page in style_report and style_report[guide_page]:
            page_issues.append(f"硬编码样式: {len(style_report[guide_page])}个")
        
        if page_issues:
            print(f"\n📄 {guide_page}:")
            for issue in page_issues:
                print(f"  ❌ {issue}")
        else:
            print(f"\n📄 {guide_page}: ✅ 无硬编码问题")
    
    # 建议
    print(f"\n💡 改进建议:")
    
    if total_issues > 0:
        print(f"1. 🔧 移除硬编码文本，使用i18n系统")
        print(f"2. 🌐 使用相对路径替代硬编码URL")
        print(f"3. 🎨 将内联样式移到CSS文件")
        print(f"4. 📱 使用CSS变量管理颜色和尺寸")
    else:
        print(f"🎉 恭喜！没有发现硬编码问题")
    
    return {
        'total_pages': len(guide_pages),
        'pages_with_issues': pages_with_issues,
        'total_issues': total_issues
    }

def main():
    """主函数"""
    
    print("🔍 开始检查攻略页面中的硬编码问题...")
    print("=" * 60)
    
    # 1. 检查硬编码文本
    text_report = check_hardcoded_text()
    
    # 2. 检查硬编码URL
    url_report = check_hardcoded_urls()
    
    # 3. 检查硬编码样式
    style_report = check_hardcoded_styles()
    
    # 4. 生成综合报告
    comprehensive_report = generate_report(text_report, url_report, style_report)
    
    # 总结
    print(f"\n" + "=" * 60)
    print("🎯 检查完成总结")
    print("=" * 60)
    
    if comprehensive_report['total_issues'] == 0:
        print("🎉 优秀！没有发现硬编码问题")
    elif comprehensive_report['total_issues'] <= 10:
        print("✅ 良好！硬编码问题较少")
    else:
        print("⚠️  存在硬编码问题，需要改进")
    
    print(f"\n📊 当前状态:")
    print(f"   - 问题总数: {comprehensive_report['total_issues']}")
    print(f"   - 存在问题页面: {comprehensive_report['pages_with_issues']}")

if __name__ == "__main__":
    main() 