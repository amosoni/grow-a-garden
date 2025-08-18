import os
import glob

# 语言映射
lang_map = {
    'es': {'Basic Salad Recipes': 'Recetas de Ensalada Básicas', 'Learn basic salad recipes': 'Aprende recetas básicas de ensalada'},
    'fr': {'Basic Salad Recipes': 'Recettes de Salade de Base', 'Learn basic salad recipes': 'Apprenez les recettes de salade de base'},
    'de': {'Basic Salad Recipes': 'Grundlegende Salat-Rezepte', 'Learn basic salad recipes': 'Lerne grundlegende Salat-Rezepte'},
    'ru': {'Basic Salad Recipes': 'Базовые рецепты салатов', 'Learn basic salad recipes': 'Изучите базовые рецепты салатов'},
    'pt-br': {'Basic Salad Recipes': 'Receitas de Salada Básicas', 'Learn basic salad recipes': 'Aprenda receitas básicas de salada'},
    'hi': {'Basic Salad Recipes': 'बुनियादी सलाद व्यंजन', 'Learn basic salad recipes': 'बुनियादी सलाद व्यंजन सीखें'},
    'id': {'Basic Salad Recipes': 'Resep Salad Dasar', 'Learn basic salad recipes': 'Pelajari resep salad dasar'},
    'vi': {'Basic Salad Recipes': 'Công thức Salad Cơ bản', 'Learn basic salad recipes': 'Học công thức salad cơ bản'},
    'ar': {'Basic Salad Recipes': 'وصفات السلطة الأساسية', 'Learn basic salad recipes': 'تعلم وصفات السلطة الأساسية'}
}

# 处理每个语言
for lang, translations in lang_map.items():
    file_path = f'{lang}/how-to-make-salad.html'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换内容
        for eng, trans in translations.items():
            content = content.replace(eng, trans)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'✅ {lang} 替换完成')

print('🎉 所有语言替换完成！') 