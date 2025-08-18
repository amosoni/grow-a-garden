#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面修复所有语言匹配问题

这个脚本将修复：
1. HTML标签损坏问题 (<./tag>)
2. 混合的i18n标签问题
3. 语言内容不一致问题
4. 国旗显示问题
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

def fix_html_tags_and_language(content, page_name):
    """修复HTML标签和语言问题"""
    
    original_content = content
    changes_made = []
    
    # 1. 修复损坏的HTML标签 (<./tag> -> </tag>)
    if '<./' in content:
        content = re.sub(r'<\./', '</', content)
        changes_made.append('修复损坏的HTML标签')
    
    # 2. 修复损坏的URL路径 (././ -> //)
    if '././' in content:
        content = content.replace('././', '//')
        changes_made.append('修复损坏的URL路径')
    
    # 3. 根据页面类型清理i18n标签
    if page_name in ['guides.html', 'index.html', 'online.html']:
        # 这些是英文页面，应该显示英文内容
        content = clean_english_page(content)
        changes_made.append('清理英文页面内容')
    else:
        # 其他页面也需要清理
        content = clean_mixed_content(content)
        changes_made.append('清理混合内容')
    
    # 4. 修复国旗显示问题
    content = fix_flag_issues(content)
    changes_made.append('修复国旗显示问题')
    
    # 5. 确保页面语言声明正确
    if page_name in ['guides.html', 'index.html', 'online.html']:
        content = ensure_english_lang(content)
        changes_made.append('确保英文语言声明')
    
    return content, changes_made

def clean_english_page(content):
    """清理英文页面，移除i18n标签，显示英文内容"""
    
    # 定义英文页面应该显示的内容
    english_content = {
        'nav.logo': '🌱 Grow a Garden',
        'nav.live': 'Live Stats',
        'nav.map': 'Global Heatmap',
        'nav.tips': 'Tips',
        'nav.guides': '📚 Guides',
        'nav.online': '🎮 Online',
        'nav.discord': '💬 Discord',
        'nav.back': '← Back',
        'hero.guides.title': '📚 Grow a Garden Guides',
        'hero.guides.subtitle': 'Complete Collection of Strategies, Recipes, and Gameplay Tips',
        'breadcrumb.home': '🏠 Home',
        'breadcrumb.guides': '📚 Guides',
        'guides.searchFilter': '🔍 Search & Filter Guides',
        'guides.searchPlaceholder': 'Search guides...',
        'guides.filter.all': 'All',
        'guides.filter.recipe': 'Recipes',
        'guides.filter.farming': 'Farming',
        'guides.filter.profit': 'Profit',
        'guides.filter.advanced': 'Advanced',
        'guides.trendingTitle': '🔥 Trending Guides',
        'guides.badge.mostPopular': '⭐ Most Popular',
        'guides.badge.trending': '📈 Trending',
        'guides.badge.new': '🆕 New',
        'guides.guideItems.salad.title': '🥗 Salad Making Guide',
        'guides.guideItems.salad.description': 'Master the art of salad making with our comprehensive guide. Learn ingredient collection, advanced recipes, and efficiency improvement methods.',
        'guides.guideItems.salad.difficulty': 'Beginner',
        'guides.guideItems.salad.readTime': '15 min read',
        'guides.guideItems.salad.views': '🔥 2.5k views',
        'guides.guideItems.pizza.title': '🍕 Pizza Making Guide',
        'guides.guideItems.pizza.description': 'Discover the best techniques for dough preparation, topping combinations, and baking to perfection.',
        'guides.guideItems.pizza.difficulty': 'Intermediate',
        'guides.guideItems.pizza.readTime': '25 min read',
        'guides.guideItems.bread.title': '🍞 Bread Making Guide',
        'guides.guideItems.bread.description': 'Master bread making techniques in Grow a Garden. Learn flour types, yeast management, and baking optimization.',
        'guides.guideItems.bread.difficulty': 'Beginner',
        'guides.guideItems.bread.readTime': '20 min read',
        'guides.guideItems.bread.views': '🔥 1.2k views',
        'hero.title': 'Play Grow a Garden Online',
        'hero.subtitle': 'Experience the ultimate farming adventure on Roblox! Plant seeds, grow crops, discover mutations, and build your dream garden with millions of players worldwide.',
        'game.playMiniPlay': 'Play on MiniPlay',
        'game.playPlayHop': 'Play on PlayHop',
        'features.title': '🎯 Game Features',
        'features.plant.title': 'Plant & Grow',
        'features.plant.desc': 'Plant various seeds and watch them grow into beautiful crops with realistic growth cycles',
        'features.mutations.title': 'Mutations',
        'features.mutations.desc': 'Discover rare mutations for higher value and unique plants with special abilities',
        'features.profit.title': 'Profit System',
        'features.profit.desc': 'Learn advanced strategies to maximize your garden\'s profitability and market timing',
        'features.multiplayer.title': 'Multiplayer',
        'features.multiplayer.desc': 'Play with friends, join guilds, and compete in seasonal events and tournaments',
        'features.world.title': 'Open World',
        'features.world.desc': 'Explore vast farming areas, discover new locations, and unlock secret areas',
        'features.achievements.title': 'Achievements',
        'features.achievements.desc': 'Unlock achievements, climb leaderboards, and earn exclusive rewards',
        'footer.copyright': '© 2025 Grow a Garden - Real-Time Player Tracker',
        'footer.disclaimer': 'Not official. Data for reference only.'
    }
    
    # 替换所有i18n标签为对应的英文内容
    for key, value in english_content.items():
        pattern = rf'<span data-i18n="{re.escape(key)}">[^<]*</span>'
        content = re.sub(pattern, value, content)
        
        # 也替换没有span包装的i18n属性
        pattern2 = rf'data-i18n="{re.escape(key)}"[^>]*>([^<]*)<'
        content = re.sub(pattern2, f'>{value}<', content)
    
    # 移除剩余的data-i18n属性
    content = re.sub(r' data-i18n="[^"]*"', '', content)
    
    return content

def clean_mixed_content(content):
    """清理混合内容，确保语言一致性"""
    
    # 移除所有i18n相关的标签和属性
    content = re.sub(r'<span data-i18n="[^"]*">[^<]*</span>', '', content)
    content = re.sub(r' data-i18n="[^"]*"', '', content)
    
    # 确保内容只包含英文（对于根目录的英文页面）
    # 这里可以根据需要调整
    
    return content

def fix_flag_issues(content):
    """修复国旗显示问题"""
    
    # 修复国旗显示
    flag_fixes = {
        '🇺🇸 简体中文': '🇨🇳 简体中文',
        '🇺🇸 Español': '🇪🇸 Español',
        '🇺🇸 Português': '🇧🇷 Português',
        '🇺🇸 Français': '🇫🇷 Français',
        '🇺🇸 Deutsch': '🇩🇪 Deutsch',
        '🇺🇸 Русский': '🇷🇺 Русский',
        '🇺🇸 العربية': '🇸🇦 العربية',
        '🇺🇸 हिन्दी': '🇮🇳 हिन्दी',
        '🇺🇸 Bahasa Indonesia': '🇮🇩 Bahasa Indonesia',
        '🇺🇸 Tiếng Việt': '🇻🇳 Tiếng Việt',
        '🇺🇸 日本語': '🇯🇵 日本語'
    }
    
    for old_flag, new_flag in flag_fixes.items():
        if old_flag in content:
            content = content.replace(old_flag, new_flag)
    
    return content

def ensure_english_lang(content):
    """确保英文页面的语言声明正确"""
    
    # 确保html lang属性是en
    content = re.sub(r'<html lang="[^"]*"', '<html lang="en"', content)
    
    # 确保meta language是English
    content = re.sub(r'<meta name="language" content="[^"]*"', '<meta name="language" content="English"', content)
    
    return content

def fix_all_pages():
    """修复所有页面的语言问题"""
    
    guide_pages = get_guide_pages()
    
    print("🔧 开始全面修复所有页面的语言匹配问题...")
    print("=" * 80)
    
    total_pages = len(guide_pages)
    fixed_pages = 0
    total_changes = 0
    
    for guide_page in guide_pages:
        print(f"\n📄 修复页面: {guide_page}")
        
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 修复页面
            fixed_content, changes_made = fix_html_tags_and_language(content, guide_page)
            
            if fixed_content != original_content:
                # 写回修复后的内容
                with open(guide_page, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f"  ✅ 成功修复 {len(changes_made)} 个问题:")
                for change in changes_made:
                    print(f"    - {change}")
                
                fixed_pages += 1
                total_changes += len(changes_made)
            else:
                print(f"  ✅ 无需修复")
                
        except Exception as e:
            print(f"  ❌ 修复失败: {str(e)}")
    
    print(f"\n" + "=" * 80)
    print("🎯 全面修复完成总结")
    print("=" * 80)
    print(f"📊 修复结果:")
    print(f"   - 总页面数: {total_pages}")
    print(f"   - 成功修复: {fixed_pages}")
    print(f"   - 失败数量: {total_pages - fixed_pages}")
    print(f"   - 总修复项: {total_changes}")
    
    if fixed_pages > 0:
        print(f"\n✅ 成功修复了 {fixed_pages} 个页面的语言匹配问题！")
        print(f"🔧 总共修复了 {total_changes} 个问题")
        print(f"🌍 现在所有页面都应该有正确的语言内容和HTML结构")
    else:
        print(f"\n⚠️  没有页面需要修复或修复失败")
    
    return fixed_pages, total_changes

def verify_fixes():
    """验证修复结果"""
    
    print(f"\n🔍 验证修复结果...")
    print("=" * 80)
    
    guide_pages = get_guide_pages()
    verified_count = 0
    
    for guide_page in guide_pages:
        try:
            with open(guide_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否还有问题
            has_broken_tags = '<./' in content
            has_mixed_i18n = 'data-i18n=' in content
            has_wrong_flags = '🇺🇸 简体中文' in content or '🇺🇸 Español' in content
            
            if not has_broken_tags and not has_mixed_i18n and not has_wrong_flags:
                print(f"  ✅ {guide_page}: 修复完成")
                verified_count += 1
            else:
                remaining_issues = []
                if has_broken_tags: remaining_issues.append('损坏标签')
                if has_mixed_i18n: remaining_issues.append('i18n标签')
                if has_wrong_flags: remaining_issues.append('错误国旗')
                print(f"  ⚠️  {guide_page}: 仍有问题: {', '.join(remaining_issues)}")
                
        except Exception as e:
            print(f"  ❌ {guide_page}: 验证失败 - {str(e)}")
    
    print(f"\n📊 验证结果:")
    print(f"   - 总页面数: {len(guide_pages)}")
    print(f"   - 验证通过: {verified_count}")
    print(f"   - 验证失败: {len(guide_pages) - verified_count}")
    
    return verified_count

def main():
    """主函数"""
    
    print("🔧 开始全面修复所有页面的语言匹配问题...")
    print("=" * 80)
    
    # 1. 修复所有页面
    fixed_pages, total_changes = fix_all_pages()
    
    # 2. 验证修复结果
    if fixed_pages > 0:
        verified_count = verify_fixes()
        
        print(f"\n" + "=" * 80)
        print("🎉 修复完成！")
        print("=" * 80)
        
        if verified_count == len(get_guide_pages()):
            print("✅ 所有页面的语言匹配问题都已成功修复！")
            print("🌍 现在所有页面都有正确的语言内容和HTML结构")
        else:
            print("⚠️  部分页面修复成功，建议检查失败的页面")
    else:
        print(f"\n⚠️  没有页面需要修复")

if __name__ == "__main__":
    main() 