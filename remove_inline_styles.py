#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移除攻略页面的内联样式，让CSS文件完全控制样式
"""

import os
import re
from pathlib import Path

def remove_inline_styles(file_path):
    """移除攻略页面的内联样式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 移除整个style标签及其内容
        content = re.sub(r'<style>.*?</style>', '<!-- 内联样式已移除，使用styles.css中的统一样式 -->', content, flags=re.DOTALL)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已移除内联样式: {file_path}")
            return True
        else:
            print(f"⏭️  无内联样式: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ 移除失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始移除攻略页面的内联样式...")
    
    # 查找所有攻略页面
    guide_files = []
    
    # 根目录下的攻略页面
    root_dir = Path('.')
    guide_patterns = [
        'how-to-*.html',
        '*-guide.html',
        '*-strategies.html',
        '*-basics.html',
        '*-tips.html'
    ]
    
    for pattern in guide_patterns:
        guide_files.extend(root_dir.glob(pattern))
    
    # 排除非攻略页面
    exclude_files = [
        'index.html',
        'test_*.html',
        'debug_*.html',
        'force_refresh.html',
        'preview.html'
    ]
    
    guide_files = [f for f in guide_files if not any(ex in f.name for ex in exclude_files)]
    
    print(f"📁 找到 {len(guide_files)} 个攻略页面需要处理:")
    for f in guide_files:
        print(f"   - {f.name}")
    
    # 处理每个文件
    processed_count = 0
    for file_path in guide_files:
        print(f"\n🔧 正在处理: {file_path.name}")
        if remove_inline_styles(file_path):
            processed_count += 1
    
    print(f"\n🎉 内联样式移除完成！共处理了 {processed_count} 个文件")
    print(f"📊 总计: {len(guide_files)} 个文件")
    print("\n✨ 现在所有攻略页面都使用styles.css中的统一样式了！")
    print("💡 请刷新页面查看效果！")

if __name__ == "__main__":
    main() 