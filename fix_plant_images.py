#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复所有语言目录的植物图片显示问题
"""

import os

def fix_plant_images(file_path):
    """修复单个index.html文件的植物图片问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有修复脚本
        if 'window.PLANT_IMG_MAP_URL' in content:
            print(f"⏭️  无需修复: {file_path}")
            return False
        
        # 在script标签前添加修复脚本
        if '</script>' in content and 'i18n/i18n.js' in content:
            # 找到最后一个script标签的位置
            script_end = content.rfind('</script>')
            if script_end != -1:
                # 在最后一个script标签前插入修复脚本
                fix_script = '''
    <script>
      // 修复植物图片映射文件路径
      window.PLANT_IMG_MAP_URL = '../plant_img_map_final.json';
    </script>
'''
                content = content[:script_end] + fix_script + content[script_end:]
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ 已修复: {file_path}")
                return True
        
        print(f"⚠️  无法修复: {file_path}")
        return False
            
    except Exception as e:
        print(f"❌ 修复失败: {file_path} - {e}")
        return False

def main():
    """主函数"""
    # 语言目录列表
    lang_dirs = [
        'vi', 'zh-cn', 'es', 'pt-br', 'fr', 'de', 
        'ru', 'ar', 'hi', 'id', 'ja'
    ]
    
    total_fixed = 0
    
    for lang_dir in lang_dirs:
        if os.path.exists(lang_dir):
            index_file = os.path.join(lang_dir, 'index.html')
            if os.path.exists(index_file):
                print(f"\n🔧 处理语言目录: {lang_dir}")
                if fix_plant_images(index_file):
                    total_fixed += 1
            else:
                print(f"⚠️  跳过: {lang_dir}/index.html 不存在")
        else:
            print(f"⚠️  跳过: {lang_dir} 目录不存在")
    
    print(f"\n🎉 修复完成! 总共修复了 {total_fixed} 个文件")
    print("\n修复内容:")
    print("- 添加植物图片映射文件路径修复")
    print("- 确保植物图片能正常显示")

if __name__ == "__main__":
    main() 