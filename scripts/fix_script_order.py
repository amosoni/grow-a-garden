#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有语言版本中脚本加载顺序的问题
将 PLANT_IMG_MAP_URL 的设置移到其他脚本之前
"""

import os

def fix_script_order(file_path):
    """修复单个文件的脚本加载顺序"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经修复过
        if '// 修复植物图片映射文件路径 - 必须在其他脚本之前设置' in content:
            print(f"✅ {file_path} 已经修复过了")
            return False
        
        # 查找脚本标签的开始位置
        script_start = content.find('<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>')
        if script_start == -1:
            print(f"⚠️  {file_path} 没有找到leaflet脚本标签")
            return False
        
        # 查找脚本标签的结束位置
        script_end = content.find('</script>', script_start)
        if script_end == -1:
            print(f"⚠️  {file_path} 没有找到脚本标签的结束")
            return False
        
        # 查找footer标签
        footer_start = content.find('<footer>')
        if footer_start == -1:
            print(f"⚠️  {file_path} 没有找到footer标签")
            return False
        
        # 在footer之前插入PLANT_IMG_MAP_URL设置
        new_script = '''    <script>
      // 修复植物图片映射文件路径 - 必须在其他脚本之前设置
      window.PLANT_IMG_MAP_URL = '../plant_img_map_final.json';
    </script>'''
        
        # 在footer之前插入
        new_content = content[:footer_start] + new_script + '\n' + content[footer_start:]
        
        # 移除原来的PLANT_IMG_MAP_URL设置（如果存在）
        old_script_pattern = '    <script>\n      // 修复植物图片映射文件路径\n      window.PLANT_IMG_MAP_URL = \'../plant_img_map_final.json\';\n    </script>'
        new_content = new_content.replace(old_script_pattern, '')
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ 修复了 {file_path}")
            return True
        else:
            print(f"⚠️  {file_path} 没有找到需要修复的模式")
            return False
            
    except Exception as e:
        print(f"❌ 修复 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("🔧 开始修复脚本加载顺序...")
    
    # 需要修复的语言目录
    lang_dirs = ['zh-cn', 'es', 'pt-br', 'fr', 'de', 'ru', 'ar', 'hi', 'id', 'ja']
    
    fixed_count = 0
    total_count = len(lang_dirs)
    
    for lang_dir in lang_dirs:
        index_file = os.path.join(lang_dir, 'index.html')
        if os.path.exists(index_file):
            if fix_script_order(index_file):
                fixed_count += 1
        else:
            print(f"⚠️  {index_file} 不存在")
    
    print(f"\n📊 修复完成！")
    print(f"   总计: {total_count} 个文件")
    print(f"   修复: {fixed_count} 个文件")
    print(f"   跳过: {total_count - fixed_count} 个文件")

if __name__ == "__main__":
    main() 