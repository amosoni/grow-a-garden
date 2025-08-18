#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建i18n系统并开始替换硬编码文本

这个脚本将：
1. 创建i18n目录结构
2. 生成基础翻译文件
3. 开始替换硬编码文本
"""

import os
import glob
import re
import json

def get_guide_pages():
    """获取所有攻略页面列表"""
    root_guides = glob.glob('*.html')
    guide_pages = []
    
    for page in root_guides:
        if page.startswith('how-to-') or page.startswith('ice-cream-') or page in ['guides.html', 'index.html', 'online.html']:
            guide_pages.append(page)
    
    return guide_pages

def create_i18n_directory():
    """创建i18n目录结构"""
    
    print("📁 创建i18n目录结构...")
    
    # 创建i18n目录
    if not os.path.exists('i18n'):
        os.makedirs('i18n')
        print("  ✅ 创建 i18n 目录")
    
    # 创建语言子目录
    languages = ['en', 'zh-cn', 'es', 'pt-br', 'fr', 'de', 'ru', 'ar', 'hi', 'id', 'vi', 'ja']
    
    for lang in languages:
        lang_dir = f'i18n/{lang}'
        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)
            print(f"  ✅ 创建 {lang_dir} 目录")
    
    return languages

def generate_base_translations():
    """生成基础翻译文件"""
    
    print("\n📝 生成基础翻译文件...")
    
    # 基础翻译内容
    base_translations = {
        'en': {
            'nav': {
                'logo': '🌱 Grow a Garden',
                'live': 'Live Stats',
                'map': 'Global Heatmap',
                'tips': 'Tips',
                'guides': '📚 Guides',
                'online': '🎮 Online',
                'discord': '💬 Discord'
            },
            'common': {
                'home': '🏠 Home',
                'back': '← Back',
                'loading': 'Loading...',
                'error': 'Error occurred',
                'success': 'Success!'
            }
        },
        'zh-cn': {
            'nav': {
                'logo': '🌱 种植花园',
                'live': '实时统计',
                'map': '全球热图',
                'tips': '技巧',
                'guides': '📚 攻略',
                'online': '🎮 在线',
                'discord': '💬 讨论'
            },
            'common': {
                'home': '🏠 首页',
                'back': '← 返回',
                'loading': '加载中...',
                'error': '发生错误',
                'success': '成功！'
            }
        }
    }
    
    # 为每个语言生成翻译文件
    languages = ['en', 'zh-cn', 'es', 'pt-br', 'fr', 'de', 'ru', 'ar', 'hi', 'id', 'vi', 'ja']
    
    for lang in languages:
        if lang in base_translations:
            translations = base_translations[lang]
        else:
            # 为其他语言创建基础结构
            translations = {
                'nav': {
                    'logo': '🌱 Grow a Garden',
                    'live': 'Live Stats',
                    'map': 'Global Heatmap',
                    'tips': 'Tips',
                    'guides': '📚 Guides',
                    'online': '🎮 Online',
                    'discord': '💬 Discord'
                },
                'common': {
                    'home': '🏠 Home',
                    'back': '← Back',
                    'loading': 'Loading...',
                    'error': 'Error occurred',
                    'success': 'Success!'
                }
            }
        
        # 写入翻译文件
        lang_file = f'i18n/{lang}/translations.json'
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
        
        print(f"  ✅ 生成 {lang_file}")
    
    return languages

def create_i18n_loader():
    """创建i18n加载器JavaScript文件"""
    
    print("\n🔧 创建i18n加载器...")
    
    i18n_loader_content = '''// i18n 系统加载器
class I18nLoader {
    constructor() {
        this.currentLang = 'en';
        this.translations = {};
        this.init();
    }
    
    async init() {
        // 检测当前语言
        this.detectLanguage();
        
        // 加载翻译文件
        await this.loadTranslations();
        
        // 应用翻译
        this.applyTranslations();
        
        // 设置语言切换器
        this.setupLanguageSwitcher();
    }
    
    detectLanguage() {
        // 从URL路径检测语言
        const path = window.location.pathname;
        const langMatch = path.match(/\/(zh-cn|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)\//);
        if (langMatch) {
            this.currentLang = langMatch[1];
        } else {
            this.currentLang = 'en';
        }
    }
    
    async loadTranslations() {
        try {
            const response = await fetch(`i18n/${this.currentLang}/translations.json`);
            this.translations = await response.json();
        } catch (error) {
            console.warn('Failed to load translations:', error);
            // 使用默认英文
            this.currentLang = 'en';
        }
    }
    
    applyTranslations() {
        // 查找所有带有 data-i18n 属性的元素
        const elements = document.querySelectorAll('[data-i18n]');
        
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.getTranslation(key);
            
            if (translation) {
                if (element.tagName === 'INPUT' && element.type === 'placeholder') {
                    element.placeholder = translation;
                } else {
                    element.textContent = translation;
                }
            }
        });
    }
    
    getTranslation(key) {
        // 支持嵌套键，如 'nav.logo'
        const keys = key.split('.');
        let value = this.translations;
        
        for (const k of keys) {
            if (value && typeof value === 'object' && k in value) {
                value = value[k];
            } else {
                return null;
            }
        }
        
        return value;
    }
    
    setupLanguageSwitcher() {
        const langSwitcher = document.getElementById('lang-switcher');
        if (langSwitcher) {
            langSwitcher.value = this.currentLang;
            langSwitcher.addEventListener('change', (e) => {
                this.switchLanguage(e.target.value);
            });
        }
    }
    
    switchLanguage(lang) {
        const currentPath = window.location.pathname;
        let newPath;
        
        if (lang === 'en') {
            // 跳转到根目录
            newPath = currentPath.replace(/^\/(zh-cn|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)\//, '/');
        } else {
            // 跳转到对应语言目录
            if (currentPath.includes('/zh-cn/') || currentPath.includes('/es/') || 
                currentPath.includes('/pt-br/') || currentPath.includes('/fr/') || 
                currentPath.includes('/de/') || currentPath.includes('/ru/') || 
                currentPath.includes('/ar/') || currentPath.includes('/hi/') || 
                currentPath.includes('/id/') || currentPath.includes('/vi/') || 
                currentPath.includes('/ja/')) {
                newPath = currentPath.replace(/\/(zh-cn|es|pt-br|fr|de|ru|ar|hi|id|vi|ja)\//, '/' + lang + '/');
            } else {
                newPath = '/' + lang + currentPath;
            }
        }
        
        window.location.href = newPath;
    }
}

// 页面加载完成后初始化i18n
document.addEventListener('DOMContentLoaded', () => {
    new I18nLoader();
});
'''
    
    # 写入i18n加载器文件
    with open('i18n/i18n.js', 'w', encoding='utf-8') as f:
        f.write(i18n_loader_content)
    
    print("  ✅ 创建 i18n/i18n.js")
    
    return True

def start_text_replacement():
    """开始替换硬编码文本"""
    
    print("\n🔧 开始替换硬编码文本...")
    
    guide_pages = get_guide_pages()
    
    # 示例：替换一个页面的部分硬编码文本
    sample_page = 'how-to-make-salad.html'
    
    if os.path.exists(sample_page):
        print(f"📄 示例：替换 {sample_page} 中的硬编码文本...")
        
        try:
            with open(sample_page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换导航栏文本
            replacements = [
                ('🌱 Grow a Garden', '🌱 <span data-i18n="nav.logo">Grow a Garden</span>'),
                ('Live Stats', '<span data-i18n="nav.live">Live Stats</span>'),
                ('Global Heatmap', '<span data-i18n="nav.map">Global Heatmap</span>'),
                ('Tips', '<span data-i18n="nav.tips">Tips</span>'),
                ('📚 Guides', '<span data-i18n="nav.guides">📚 Guides</span>'),
                ('🎮 Online', '<span data-i18n="nav.online">🎮 Online</span>'),
                ('💬 Discord', '<span data-i18n="nav.discord">💬 Discord</span>'),
            ]
            
            for old_text, new_text in replacements:
                if old_text in content:
                    content = content.replace(old_text, new_text)
                    print(f"  ✅ 替换: {old_text[:30]}...")
            
            # 写回文件
            with open(sample_page, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ 成功替换 {sample_page} 中的部分硬编码文本")
            
        except Exception as e:
            print(f"  ❌ 替换失败: {str(e)}")
    
    return True

def main():
    """主函数"""
    
    print("🚀 开始创建i18n系统并修复硬编码问题...")
    print("=" * 60)
    
    # 1. 创建i18n目录结构
    languages = create_i18n_directory()
    
    # 2. 生成基础翻译文件
    generate_base_translations()
    
    # 3. 创建i18n加载器
    create_i18n_loader()
    
    # 4. 开始替换硬编码文本
    start_text_replacement()
    
    print(f"\n" + "=" * 60)
    print("🎉 i18n系统创建完成！")
    print("=" * 60)
    print(f"✅ 已创建 {len(languages)} 种语言的翻译系统")
    print(f"✅ 已生成基础翻译文件")
    print(f"✅ 已创建i18n加载器")
    print(f"✅ 已开始替换硬编码文本")
    print(f"\n🌍 下一步：")
    print(f"1. 继续替换所有页面的硬编码文本")
    print(f"2. 完善翻译文件内容")
    print(f"3. 测试多语言功能")

if __name__ == "__main__":
    main() 