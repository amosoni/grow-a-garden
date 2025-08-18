#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一修复中文版页面的语言切换器格式

这个脚本将：
1. 检查中文版页面的语言切换器格式
2. 统一使用标准的select格式
3. 确保所有12种语言选项都正确显示
"""

import os
import glob
import re

def get_supported_languages():
    """获取网站支持的语言列表"""
    return ['en', 'zh-cn', 'es', 'pt-br', 'fr', 'de', 'ru', 'ar', 'hi', 'id', 'vi', 'ja']

def get_chinese_guide_pages():
    """获取所有中文版攻略页面"""
    zh_cn_dir = 'zh-cn'
    if not os.path.exists(zh_cn_dir):
        print(f"❌ 中文目录 {zh_cn_dir} 不存在")
        return []
    
    html_files = glob.glob(f'{zh_cn_dir}/*.html')
    return html_files

def fix_language_switcher_format():
    """修复语言切换器格式"""
    
    supported_languages = get_supported_languages()
    chinese_pages = get_chinese_guide_pages()
    
    print("🔍 开始统一修复中文版页面的语言切换器格式...")
    print("=" * 60)
    
    fixed_count = 0
    total_count = len(chinese_pages)
    
    for page_path in chinese_pages:
        print(f"\n📄 处理页面: {page_path}")
        
        try:
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经有正确的语言切换器
            if '<select id="lang-switcher"' in content and '🇺🇸 English' in content:
                print(f"  ✅ 已有正确的语言切换器，跳过")
                continue
            
            # 查找导航栏位置
            nav_pattern = r'(<nav>.*?)(</nav>)'
            nav_match = re.search(nav_pattern, content, re.DOTALL)
            
            if not nav_match:
                print(f"  ❌ 未找到导航栏，跳过")
                continue
            
            # 构建标准的语言切换器HTML
            language_switcher_html = '''
            <select id="lang-switcher" aria-label="Language">
<option value="en">🇺🇸 English</option>
<option value="zh-cn" selected>🇨🇳 简体中文</option>
<option value="es">🇪🇸 Español</option>
<option value="pt-br">🇧🇷 Português</option>
<option value="fr">🇫🇷 Français</option>
<option value="de">🇩🇪 Deutsch</option>
<option value="ru">🇷🇺 Русский</option>
<option value="ar">🇸🇦 العربية</option>
<option value="hi">🇮🇳 हिन्दी</option>
<option value="id">🇮🇩 Bahasa Indonesia</option>
<option value="vi">🇻🇳 Tiếng Việt</option>
<option value="ja">🇯🇵 日本語</option>
</select>'''
            
            # 移除旧的复杂语言切换器
            old_lang_pattern = r'<div class="language-selector">.*?</div>\s*</div>'
            content = re.sub(old_lang_pattern, '', content, flags=re.DOTALL)
            
            # 在导航栏结束前插入标准语言切换器
            old_nav = nav_match.group(1) + nav_match.group(2)
            new_nav = nav_match.group(1) + language_switcher_html + '\n        ' + nav_match.group(2)
            
            # 替换导航栏
            content = content.replace(old_nav, new_nav)
            
            # 添加语言切换器JavaScript
            js_script = '''
    <script>
        // 语言切换器功能
        document.addEventListener('DOMContentLoaded', function() {
            const langSwitcher = document.getElementById('lang-switcher');
            
            if (langSwitcher) {
                langSwitcher.addEventListener('change', function() {
                    const selectedLang = this.value;
                    const currentPath = window.location.pathname;
                    
                    if (selectedLang === 'en') {
                        // 如果选择英文，跳转到根目录
                        window.location.href = currentPath.replace(/^\/(zh-cn|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)\//, '/');
                    } else {
                        // 如果选择其他语言，跳转到对应语言目录
                        const newPath = '/' + selectedLang + currentPath.replace(/^\/(zh-cn|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)?/, '');
                        window.location.href = newPath;
                    }
                });
            }
        });
    </script>'''
            
            # 在body结束前插入JavaScript
            if '</body>' in content:
                content = content.replace('</body>', js_script + '\n</body>')
            
            # 写回文件
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ 成功修复语言切换器格式")
            fixed_count += 1
            
        except Exception as e:
            print(f"  ❌ 处理失败: {str(e)}")
    
    print(f"\n" + "=" * 60)
    print("🎯 修复完成总结")
    print("=" * 60)
    print(f"📊 处理结果:")
    print(f"   - 总页面数: {total_count}")
    print(f"   - 成功修复: {fixed_count}")
    print(f"   - 失败数量: {total_count - fixed_count}")
    
    if fixed_count > 0:
        print(f"\n✅ 成功修复了 {fixed_count} 个中文版页面的语言切换器格式！")
        print(f"🌍 现在所有中文版页面都使用统一的语言切换器格式")
        print(f"🚀 多语言用户体验得到显著提升")
    else:
        print(f"\n⚠️  没有页面需要修复或修复失败")
    
    return fixed_count

def verify_language_switcher():
    """验证语言切换器是否正常工作"""
    
    print(f"\n🔍 验证语言切换器功能...")
    print("=" * 60)
    
    chinese_pages = get_chinese_guide_pages()
    verified_count = 0
    
    for page_path in chinese_pages:
        try:
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查语言切换器
            if '<select id="lang-switcher"' in content:
                # 检查是否包含所有语言选项
                lang_options = re.findall(r'<option value="([^"]+)">', content)
                supported_languages = get_supported_languages()
                
                if len(lang_options) >= len(supported_languages):
                    print(f"  ✅ {page_path}: 语言切换器完整")
                    verified_count += 1
                else:
                    print(f"  ⚠️  {page_path}: 语言选项不完整 ({len(lang_options)}/{len(supported_languages)})")
            else:
                print(f"  ❌ {page_path}: 缺少语言切换器")
                
        except Exception as e:
            print(f"  ❌ {page_path}: 验证失败 - {str(e)}")
    
    print(f"\n📊 验证结果:")
    print(f"   - 总页面数: {len(chinese_pages)}")
    print(f"   - 验证通过: {verified_count}")
    print(f"   - 验证失败: {len(chinese_pages) - verified_count}")
    
    return verified_count

def main():
    """主函数"""
    
    print("🔧 开始统一修复中文版页面的语言切换器格式...")
    print("=" * 60)
    
    # 1. 修复语言切换器格式
    fixed_count = fix_language_switcher_format()
    
    # 2. 验证修复结果
    if fixed_count > 0:
        verified_count = verify_language_switcher()
        
        print(f"\n" + "=" * 60)
        print("🎉 修复完成！")
        print("=" * 60)
        
        if verified_count == len(get_chinese_guide_pages()):
            print("✅ 所有中文版页面都已成功修复语言切换器格式！")
            print("🌍 现在用户可以在所有攻略页面之间自由切换语言")
            print("🚀 多语言用户体验得到显著提升")
        else:
            print("⚠️  部分页面修复成功，建议检查失败的页面")
    else:
        print(f"\n⚠️  没有页面需要修复")

if __name__ == "__main__":
    main() 