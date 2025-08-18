#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复项目中的严重问题
1. 修复URL格式错误 (https:///)
2. 替换占位符域名 (your-domain.com)
3. 清理测试文件
4. 重新生成sitemap
"""

import os
import glob
import re
from datetime import datetime

def fix_url_format_issues():
    """修复所有URL格式问题"""
    
    # 获取所有HTML文件
    html_files = glob.glob('*.html') + glob.glob('*/**/*.html', recursive=True)
    
    fixed_count = 0
    url_fixes = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            modified = False
            
            # 修复 https:/// 格式的URL
            patterns_to_fix = [
                (r'href="https:///([^"]*)"', r'href="https://growagarden.cv/\1"'),
                (r'content="https:///([^"]*)"', r'content="https://growagarden.cv/\1"'),
                (r'src="https:///([^"]*)"', r'src="https://growagarden.cv/\1"'),
                (r'url": "https:///([^"]*)"', r'url": "https://growagarden.cv/\1"'),
            ]
            
            for pattern, replacement in patterns_to_fix:
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    modified = True
                    url_fixes += 1
            
            # 替换占位符域名
            placeholder_fixes = [
                (r'your-domain\.com', 'growagarden.cv'),
                (r'https://your-domain\.com', 'https://growagarden.cv'),
            ]
            
            for old, new in placeholder_fixes:
                if re.search(old, content):
                    content = re.sub(old, new, content)
                    modified = True
                    url_fixes += 1
            
            # 如果内容有修改，保存文件
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print(f"✅ 修复 {file_path}: {url_fixes} 个URL问题")
                
        except Exception as e:
            print(f"❌ 处理 {file_path} 时出错: {str(e)}")
    
    print(f"\n🎉 URL格式修复完成！共修复了 {fixed_count} 个文件，{url_fixes} 个URL问题")
    return fixed_count

def clean_test_files():
    """清理所有测试文件"""
    
    # 要删除的测试文件模式
    test_patterns = [
        'test_*.html',
        'test_*.js',
        'preview.html',
        'debug_*.html',
        'force_refresh.html'
    ]
    
    deleted_files = []
    
    for pattern in test_patterns:
        files = glob.glob(pattern)
        for file_path in files:
            try:
                os.remove(file_path)
                deleted_files.append(file_path)
                print(f"🗑️ 删除测试文件: {file_path}")
            except Exception as e:
                print(f"❌ 删除 {file_path} 时出错: {str(e)}")
    
    print(f"\n🧹 测试文件清理完成！共删除 {len(deleted_files)} 个文件")
    return deleted_files

def clean_scripts_directory():
    """整理脚本目录"""
    
    # 创建scripts目录（如果不存在）
    if not os.path.exists('scripts'):
        os.makedirs('scripts')
        print("📁 创建scripts目录")
    
    # 移动Python脚本到scripts目录
    python_scripts = glob.glob('*.py')
    moved_scripts = []
    
    for script in python_scripts:
        if script != 'fix_critical_issues.py':  # 保留当前脚本
            try:
                new_path = os.path.join('scripts', script)
                os.rename(script, new_path)
                moved_scripts.append(script)
                print(f"📦 移动脚本: {script} -> scripts/{script}")
            except Exception as e:
                print(f"❌ 移动 {script} 时出错: {str(e)}")
    
    print(f"\n📦 脚本整理完成！共移动 {len(moved_scripts)} 个脚本到scripts目录")
    return moved_scripts

def regenerate_sitemap():
    """重新生成sitemap.xml"""
    
    try:
        # 运行sitemap生成脚本
        if os.path.exists('scripts/generate_complete_sitemap.py'):
            os.system('python scripts/generate_complete_sitemap.py')
            print("✅ 重新生成sitemap.xml")
        else:
            print("⚠️ 未找到sitemap生成脚本")
    except Exception as e:
        print(f"❌ 重新生成sitemap时出错: {str(e)}")

def create_robots_txt():
    """创建/更新robots.txt"""
    
    robots_content = """User-agent: *
Allow: /

# 允许所有搜索引擎爬取
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Slurp
Allow: /

# 站点地图位置
Sitemap: https://growagarden.cv/sitemap.xml

# 爬取延迟（可选，避免服务器过载）
Crawl-delay: 1

# 允许CSS和JS文件（有助于页面渲染）
Allow: /*.css
Allow: /*.js
Allow: /*.png
Allow: /*.jpg
Allow: /*.jpeg
Allow: /*.gif
Allow: /*.svg

# 禁止爬取管理或临时文件
Disallow: /admin/
Disallow: /temp/
Disallow: /private/
Disallow: /*.log
Disallow: /*.tmp
Disallow: /scripts/
"""
    
    with open('robots.txt', 'w', encoding='utf-8') as f:
        f.write(robots_content)
    
    print("✅ 更新robots.txt")

def main():
    """主函数"""
    
    print("🚀 开始修复项目中的严重问题...")
    print("=" * 60)
    
    # 1. 修复URL格式问题
    print("\n🔧 步骤1: 修复URL格式问题")
    fixed_files = fix_url_format_issues()
    
    # 2. 清理测试文件
    print("\n🧹 步骤2: 清理测试文件")
    deleted_files = clean_test_files()
    
    # 3. 整理脚本目录
    print("\n📦 步骤3: 整理脚本目录")
    moved_scripts = clean_scripts_directory()
    
    # 4. 重新生成sitemap
    print("\n🗺️ 步骤4: 重新生成sitemap")
    regenerate_sitemap()
    
    # 5. 更新robots.txt
    print("\n🤖 步骤5: 更新robots.txt")
    create_robots_txt()
    
    # 总结
    print("\n" + "=" * 60)
    print("🎉 严重问题修复完成！")
    print(f"📊 修复统计:")
    print(f"   - 修复文件数: {fixed_files}")
    print(f"   - 删除测试文件: {len(deleted_files)}")
    print(f"   - 整理脚本: {len(moved_scripts)}")
    print(f"   - 重新生成sitemap: ✅")
    print(f"   - 更新robots.txt: ✅")
    
    print("\n📋 下一步建议:")
    print("1. 测试网站功能是否正常")
    print("2. 验证所有URL格式正确")
    print("3. 检查sitemap.xml内容")
    print("4. 在搜索引擎控制台重新提交sitemap")
    print("5. 监控索引状态变化")
    
    print(f"\n⏰ 修复完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 