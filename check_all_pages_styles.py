#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查所有页面的样式问题
"""

import os
import re

def check_page_styles(file_path):
    """检查单个页面的样式问题"""
    
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查CSS文件引用
        css_links = re.findall(r'<link[^>]*href=["\']([^"\']*\.css[^"\']*)["\'][^>]*>', content)
        for css_link in css_links:
            if css_link.startswith('http'):
                if not css_link.startswith('https://'):
                    issues.append(f"⚠️  不安全的CSS链接: {css_link}")
            elif css_link.startswith('//'):
                issues.append(f"⚠️  协议相对链接: {css_link}")
            elif css_link.startswith('./') or css_link.startswith('../'):
                # 检查相对路径是否正确
                if '..' in css_link and css_link.count('..') > 2:
                    issues.append(f"⚠️  可疑的相对路径: {css_link}")
        
        # 检查CSS文件是否存在
        for css_link in css_links:
            if not css_link.startswith('http') and not css_link.startswith('//'):
                # 构建完整路径
                if css_link.startswith('./'):
                    css_path = os.path.join(os.path.dirname(file_path), css_link[2:])
                elif css_link.startswith('../'):
                    css_path = os.path.join(os.path.dirname(file_path), css_link)
                else:
                    css_path = os.path.join(os.path.dirname(file_path), css_link)
                
                if not os.path.exists(css_path):
                    issues.append(f"❌ CSS文件不存在: {css_link} -> {css_path}")
        
        # 检查内联样式问题
        inline_styles = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
        for style in inline_styles:
            if '/*' in style and '*/' not in style:
                issues.append("❌ 未闭合的CSS注释")
            if '/*' in style and '*/' in style:
                # 检查注释语法
                if re.search(r'/\*[^*]*\*/', style):
                    pass  # 正常
                else:
                    issues.append("⚠️  可疑的CSS注释语法")
        
        # 检查SVG国旗
        svg_flags = re.findall(r'<svg[^>]*>.*?</svg>', content, re.DOTALL)
        if not svg_flags:
            issues.append("❌ 没有找到SVG国旗")
        else:
            # 检查SVG语法
            for svg in svg_flags:
                if '<svg' in svg and '</svg>' not in svg:
                    issues.append("❌ 未闭合的SVG标签")
                if 'viewBox=' not in svg:
                    issues.append("⚠️  SVG缺少viewBox属性")
        
        # 检查图片引用
        img_srcs = re.findall(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*>', content)
        for img_src in img_srcs:
            if img_src.startswith('flags/') and img_src.endswith('.png'):
                issues.append(f"❌ 仍然使用图片国旗: {img_src}")
        
        # 检查JavaScript问题
        script_tags = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
        for script in script_tags:
            if 'flags/' in script and '.png' in script:
                issues.append("❌ JavaScript中仍然引用图片国旗")
        
        # 检查HTML结构问题
        if '<html' not in content:
            issues.append("❌ 缺少<html>标签")
        if '<head' not in content:
            issues.append("❌ 缺少<head>标签")
        if '<body' not in content:
            issues.append("❌ 缺少<body>标签")
        
        # 检查语言属性
        if 'lang=' not in content:
            issues.append("⚠️  缺少lang属性")
        
        # 检查字符编码
        if 'charset=' not in content:
            issues.append("⚠️  缺少字符编码声明")
        
        # 检查viewport
        if 'viewport' not in content:
            issues.append("⚠️  缺少viewport设置")
        
        return issues
        
    except Exception as e:
        return [f"❌ 读取文件失败: {str(e)}"]

def check_all_pages():
    """检查所有页面"""
    
    print("🔍 开始检查所有页面的样式问题...")
    print("=" * 80)
    
    # 获取所有HTML文件
    html_files = []
    for root, dirs, files in os.walk('.'):
        # 跳过node_modules和其他不需要的目录
        if 'node_modules' in root or '.git' in root or '.next' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"📁 找到 {len(html_files)} 个HTML文件")
    print("=" * 80)
    
    total_issues = 0
    files_with_issues = 0
    
    for file_path in html_files:
        print(f"🔍 检查: {file_path}")
        
        issues = check_page_styles(file_path)
        
        if issues:
            files_with_issues += 1
            total_issues += len(issues)
            print(f"  ❌ 发现 {len(issues)} 个问题:")
            for issue in issues:
                print(f"    {issue}")
        else:
            print(f"  ✅ 没有发现问题")
        
        print()
    
    print("=" * 80)
    print("🎯 检查完成总结")
    print("=" * 80)
    print(f"📊 检查结果:")
    print(f"   - 检查文件: {len(html_files)}")
    print(f"   - 有问题文件: {files_with_issues}")
    print(f"   - 总问题数: {total_issues}")
    
    if total_issues > 0:
        print(f"\n⚠️  发现了 {total_issues} 个样式问题！")
        print(f"🔧 需要修复这些问题以确保页面正常显示")
    else:
        print(f"\n✅ 所有页面都没有样式问题！")
    
    return total_issues

def main():
    """主函数"""
    
    print("🔍 开始检查所有页面的样式问题...")
    print("=" * 80)
    
    # 检查所有页面
    total_issues = check_all_pages()
    
    print(f"\n" + "=" * 80)
    print("🎉 检查完成！")
    print("=" * 80)
    
    if total_issues > 0:
        print("⚠️  发现了样式问题，需要修复")
    else:
        print("✅ 所有页面样式都正常")

if __name__ == "__main__":
    main() 