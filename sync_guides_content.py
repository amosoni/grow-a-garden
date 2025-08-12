#!/usr/bin/env python3
"""
同步所有语言攻略页面的内容，使用日语页面作为模板
"""

import os
import re

def get_language_config(lang_code):
    """获取语言特定的配置"""
    configs = {
        'zh-cn': {
            'title': 'Grow a Garden 指南 - 完整合集',
            'hero_title': '📚 Grow a Garden 指南',
            'hero_subtitle': '策略、食谱和游戏技巧的完整合集',
            'search_title': '🔍 搜索和筛选',
            'search_placeholder': '搜索指南...',
            'filter_all': '全部',
            'filter_recipe': '食谱',
            'filter_farming': '农业',
            'filter_profit': '利润',
            'filter_advanced': '高级',
            'trending_title': '🔥 热门指南',
            'most_popular': '⭐ 最受欢迎',
            'trending': '📈 趋势',
            'new': '🆕 新内容',
            'views': '🔥 查看',
            'recipe_title': '🍽️ 食谱指南',
            'farming_title': '🌾 农业指南',
            'profit_title': '💰 利润优化',
            'coop_title': '👥 合作与运营',
            'advanced_title': '🎮 高级指南',
            'quick_tips_title': '💡 快速提示',
            'navigation_title': '🏠 导航',
            'back_to_calc': '← 返回主计算器',
            'beginner': '初学者',
            'intermediate': '中级',
            'expert': '专家',
            'advanced': '高级',
            'minutes_read': '分钟阅读'
        },
        'es': {
            'title': 'Grow a Garden Guías - Colección Completa',
            'hero_title': '📚 Grow a Garden Guías',
            'hero_subtitle': 'Colección completa de estrategias, recetas y consejos de juego',
            'search_title': '🔍 Búsqueda y Filtros',
            'search_placeholder': 'Buscar guías...',
            'filter_all': 'Todo',
            'filter_recipe': 'Recetas',
            'filter_farming': 'Agricultura',
            'filter_profit': 'Beneficios',
            'filter_advanced': 'Avanzado',
            'trending_title': '🔥 Guías Populares',
            'most_popular': '⭐ Más Popular',
            'trending': '📈 Tendencia',
            'new': '🆕 Nuevo',
            'views': '🔥 Vistas',
            'recipe_title': '🍽️ Guías de Recetas',
            'farming_title': '🌾 Guías de Agricultura',
            'profit_title': '💰 Optimización de Beneficios',
            'coop_title': '👥 Cooperación y Operación',
            'advanced_title': '🎮 Guías Avanzadas',
            'quick_tips_title': '💡 Consejos Rápidos',
            'navigation_title': '🏠 Navegación',
            'back_to_calc': '← Volver al Calculador Principal',
            'beginner': 'Principiante',
            'intermediate': 'Intermedio',
            'expert': 'Experto',
            'advanced': 'Avanzado',
            'minutes_read': 'minutos de lectura'
        },
        'pt-br': {
            'title': 'Grow a Garden Guias - Coleção Completa',
            'hero_title': '📚 Grow a Garden Guias',
            'hero_subtitle': 'Coleção completa de estratégias, receitas e dicas de jogo',
            'search_title': '🔍 Pesquisa e Filtros',
            'search_placeholder': 'Pesquisar guias...',
            'filter_all': 'Tudo',
            'filter_recipe': 'Receitas',
            'filter_farming': 'Agricultura',
            'filter_profit': 'Lucros',
            'filter_advanced': 'Avançado',
            'trending_title': '🔥 Guias Populares',
            'most_popular': '⭐ Mais Popular',
            'trending': '📈 Tendência',
            'new': '🆕 Novo',
            'views': '🔥 Visualizações',
            'recipe_title': '🍽️ Guias de Receitas',
            'farming_title': '🌾 Guias de Agricultura',
            'profit_title': '💰 Otimização de Lucros',
            'coop_title': '👥 Cooperação e Operação',
            'advanced_title': '🎮 Guias Avançados',
            'quick_tips_title': '💡 Dicas Rápidas',
            'navigation_title': '🏠 Navegação',
            'back_to_calc': '← Voltar ao Calculador Principal',
            'beginner': 'Iniciante',
            'intermediate': 'Intermediário',
            'expert': 'Especialista',
            'advanced': 'Avançado',
            'minutes_read': 'minutos de leitura'
        },
        'fr': {
            'title': 'Grow a Garden Guides - Collection Complète',
            'hero_title': '📚 Grow a Garden Guides',
            'hero_subtitle': 'Collection complète de stratégies, recettes et conseils de jeu',
            'search_title': '🔍 Recherche et Filtres',
            'search_placeholder': 'Rechercher des guides...',
            'filter_all': 'Tout',
            'filter_recipe': 'Recettes',
            'filter_farming': 'Agriculture',
            'filter_profit': 'Bénéfices',
            'filter_advanced': 'Avancé',
            'trending_title': '🔥 Guides Populaires',
            'most_popular': '⭐ Plus Populaire',
            'trending': '📈 Tendance',
            'new': '🆕 Nouveau',
            'views': '🔥 Vues',
            'recipe_title': '🍽️ Guides de Recettes',
            'farming_title': '🌾 Guides d\'Agriculture',
            'profit_title': '💰 Optimisation des Bénéfices',
            'coop_title': '👥 Coopération et Exploitation',
            'advanced_title': '🎮 Guides Avancés',
            'quick_tips_title': '💡 Conseils Rapides',
            'navigation_title': '🏠 Navigation',
            'back_to_calc': '← Retour au Calculateur Principal',
            'beginner': 'Débutant',
            'intermediate': 'Intermédiaire',
            'expert': 'Expert',
            'advanced': 'Avancé',
            'minutes_read': 'minutes de lecture'
        },
        'de': {
            'title': 'Grow a Garden Anleitungen - Vollständige Sammlung',
            'hero_title': '📚 Grow a Garden Anleitungen',
            'hero_subtitle': 'Vollständige Sammlung von Strategien, Rezepten und Spieltipps',
            'search_title': '🔍 Suche und Filter',
            'search_placeholder': 'Anleitungen suchen...',
            'filter_all': 'Alle',
            'filter_recipe': 'Rezepte',
            'filter_farming': 'Landwirtschaft',
            'filter_profit': 'Gewinn',
            'filter_advanced': 'Fortgeschritten',
            'trending_title': '🔥 Beliebte Anleitungen',
            'most_popular': '⭐ Am Beliebtesten',
            'trending': '📈 Trend',
            'new': '🆕 Neu',
            'views': '🔥 Aufrufe',
            'recipe_title': '🍽️ Rezept-Anleitungen',
            'farming_title': '🌾 Landwirtschafts-Anleitungen',
            'profit_title': '💰 Gewinnoptimierung',
            'coop_title': '👥 Zusammenarbeit und Betrieb',
            'advanced_title': '🎮 Fortgeschrittene Anleitungen',
            'quick_tips_title': '💡 Schnelle Tipps',
            'navigation_title': '🏠 Navigation',
            'back_to_calc': '← Zurück zum Hauptrechner',
            'beginner': 'Anfänger',
            'intermediate': 'Fortgeschritten',
            'expert': 'Experte',
            'advanced': 'Fortgeschritten',
            'minutes_read': 'Minuten Lesezeit'
        },
        'ru': {
            'title': 'Grow a Garden Руководства - Полная Коллекция',
            'hero_title': '📚 Grow a Garden Руководства',
            'hero_subtitle': 'Полная коллекция стратегий, рецептов и игровых советов',
            'search_title': '🔍 Поиск и Фильтры',
            'search_placeholder': 'Поиск руководств...',
            'filter_all': 'Все',
            'filter_recipe': 'Рецепты',
            'filter_farming': 'Сельское хозяйство',
            'filter_profit': 'Прибыль',
            'filter_advanced': 'Продвинутый',
            'trending_title': '🔥 Популярные Руководства',
            'most_popular': '⭐ Самые Популярные',
            'trending': '📈 Тренд',
            'new': '🆕 Новое',
            'views': '🔥 Просмотры',
            'recipe_title': '🍽️ Руководства по Рецептам',
            'farming_title': '🌾 Руководства по Сельскому Хозяйству',
            'profit_title': '💰 Оптимизация Прибыли',
            'coop_title': '👥 Сотрудничество и Эксплуатация',
            'advanced_title': '🎮 Продвинутые Руководства',
            'quick_tips_title': '💡 Быстрые Советы',
            'navigation_title': '🏠 Навигация',
            'back_to_calc': '← Вернуться к Главному Калькулятору',
            'beginner': 'Новичок',
            'intermediate': 'Средний',
            'expert': 'Эксперт',
            'advanced': 'Продвинутый',
            'minutes_read': 'минут чтения'
        },
        'ar': {
            'title': 'Grow a Garden أدلة - مجموعة كاملة',
            'hero_title': '📚 Grow a Garden أدلة',
            'hero_subtitle': 'مجموعة كاملة من الاستراتيجيات والوصفات ونصائح اللعب',
            'search_title': '🔍 البحث والتصفية',
            'search_placeholder': 'البحث عن الأدلة...',
            'filter_all': 'الكل',
            'filter_recipe': 'الوصفات',
            'filter_farming': 'الزراعة',
            'filter_profit': 'الربح',
            'filter_advanced': 'متقدم',
            'trending_title': '🔥 الأدلة الشائعة',
            'most_popular': '⭐ الأكثر شعبية',
            'trending': '📈 الاتجاه',
            'new': '🆕 جديد',
            'views': '🔥 المشاهدات',
            'recipe_title': '🍽️ أدلة الوصفات',
            'farming_title': '🌾 أدلة الزراعة',
            'profit_title': '💰 تحسين الربح',
            'coop_title': '👥 التعاون والتشغيل',
            'advanced_title': '🎮 الأدلة المتقدمة',
            'quick_tips_title': '💡 نصائح سريعة',
            'navigation_title': '🏠 التنقل',
            'back_to_calc': '← العودة إلى الحاسبة الرئيسية',
            'beginner': 'مبتدئ',
            'intermediate': 'متوسط',
            'expert': 'خبير',
            'advanced': 'متقدم',
            'minutes_read': 'دقائق للقراءة'
        },
        'hi': {
            'title': 'Grow a Garden गाइड - पूर्ण संग्रह',
            'hero_title': '📚 Grow a Garden गाइड',
            'hero_subtitle': 'रणनीतियों, व्यंजनों और गेम टिप्स का पूर्ण संग्रह',
            'search_title': '🔍 खोज और फ़िल्टर',
            'search_placeholder': 'गाइड खोजें...',
            'filter_all': 'सभी',
            'filter_recipe': 'व्यंजन',
            'filter_farming': 'कृषि',
            'filter_profit': 'लाभ',
            'filter_advanced': 'उन्नत',
            'trending_title': '🔥 लोकप्रिय गाइड',
            'most_popular': '⭐ सबसे लोकप्रिय',
            'trending': '📈 ट्रेंड',
            'new': '🆕 नया',
            'views': '🔥 दृश्य',
            'recipe_title': '🍽️ व्यंजन गाइड',
            'farming_title': '🌾 कृषि गाइड',
            'profit_title': '💰 लाभ अनुकूलन',
            'coop_title': '👥 सहयोग और संचालन',
            'advanced_title': '🎮 उन्नत गाइड',
            'quick_tips_title': '💡 त्वरित सुझाव',
            'navigation_title': '🏠 नेविगेशन',
            'back_to_calc': '← मुख्य कैलकुलेटर पर वापस जाएं',
            'beginner': 'शुरुआती',
            'intermediate': 'मध्यम',
            'expert': 'विशेषज्ञ',
            'advanced': 'उन्नत',
            'minutes_read': 'मिनट पढ़ने में'
        },
        'id': {
            'title': 'Grow a Garden Panduan - Koleksi Lengkap',
            'hero_title': '📚 Grow a Garden Panduan',
            'hero_subtitle': 'Koleksi lengkap strategi, resep, dan tips permainan',
            'search_title': '🔍 Pencarian dan Filter',
            'search_placeholder': 'Cari panduan...',
            'filter_all': 'Semua',
            'filter_recipe': 'Resep',
            'filter_farming': 'Pertanian',
            'filter_profit': 'Keuntungan',
            'filter_advanced': 'Lanjutan',
            'trending_title': '🔥 Panduan Populer',
            'most_popular': '⭐ Paling Populer',
            'trending': '📈 Tren',
            'new': '🆕 Baru',
            'views': '🔥 Dilihat',
            'recipe_title': '🍽️ Panduan Resep',
            'farming_title': '🌾 Panduan Pertanian',
            'profit_title': '💰 Optimasi Keuntungan',
            'coop_title': '👥 Kerjasama dan Operasi',
            'advanced_title': '🎮 Panduan Lanjutan',
            'quick_tips_title': '💡 Tips Cepat',
            'navigation_title': '🏠 Navigasi',
            'back_to_calc': '← Kembali ke Kalkulator Utama',
            'beginner': 'Pemula',
            'intermediate': 'Menengah',
            'expert': 'Ahli',
            'advanced': 'Lanjutan',
            'minutes_read': 'menit membaca'
        },
        'vi': {
            'title': 'Grow a Garden Hướng Dẫn - Bộ Sưu Tập Đầy Đủ',
            'hero_title': '📚 Grow a Garden Hướng Dẫn',
            'hero_subtitle': 'Bộ sưu tập đầy đủ chiến lược, công thức và mẹo chơi',
            'search_title': '🔍 Tìm Kiếm và Lọc',
            'search_placeholder': 'Tìm kiếm hướng dẫn...',
            'filter_all': 'Tất cả',
            'filter_recipe': 'Công thức',
            'filter_farming': 'Nông nghiệp',
            'filter_profit': 'Lợi nhuận',
            'filter_advanced': 'Nâng cao',
            'trending_title': '🔥 Hướng Dẫn Phổ Biến',
            'most_popular': '⭐ Phổ Biến Nhất',
            'trending': '📈 Xu Hướng',
            'new': '🆕 Mới',
            'views': '🔥 Lượt xem',
            'recipe_title': '🍽️ Hướng Dẫn Công Thức',
            'farming_title': '🌾 Hướng Dẫn Nông Nghiệp',
            'profit_title': '💰 Tối Ưu Hóa Lợi Nhuận',
            'coop_title': '👥 Hợp Tác và Vận Hành',
            'advanced_title': '🎮 Hướng Dẫn Nâng Cao',
            'quick_tips_title': '💡 Mẹo Nhanh',
            'navigation_title': '🏠 Điều Hướng',
            'back_to_calc': '← Quay Lại Máy Tính Chính',
            'beginner': 'Người mới',
            'intermediate': 'Trung cấp',
            'expert': 'Chuyên gia',
            'advanced': 'Nâng cao',
            'minutes_read': 'phút đọc'
        }
    }
    return configs.get(lang_code, configs['en'])

def create_guides_content(lang_code, lang_config):
    """创建指定语言的攻略页面内容"""
    
    # 读取日语模板
    with open('ja/guides.html', 'r', encoding='utf-8') as f:
        ja_content = f.read()
    
    # 替换语言相关的内容
    content = ja_content
    
    # 替换标题和描述
    content = content.replace('lang="ja"', f'lang="{lang_code}"')
    content = content.replace('dir="ltr"', 'dir="ltr"' if lang_code != 'ar' else 'dir="rtl"')
    content = content.replace('Grow a Garden ガイド - 総合コレクション', lang_config['title'])
    content = content.replace('📚 Grow a Garden ガイド', lang_config['hero_title'])
    content = content.replace('戦略、レシピ、ゲームプレイのヒントの完全コレクション', lang_config['hero_subtitle'])
    
    # 替换搜索和筛选部分
    content = content.replace('🔍 検索とフィルター', lang_config['search_title'])
    content = content.replace('ガイドを検索...', lang_config['search_placeholder'])
    content = content.replace('すべて', lang_config['filter_all'])
    content = content.replace('レシピ', lang_config['filter_recipe'])
    content = content.replace('農業', lang_config['filter_farming'])
    content = content.replace('利益', lang_config['filter_profit'])
    content = content.replace('上級', lang_config['filter_advanced'])
    
    # 替换热门指南部分
    content = content.replace('🔥 人気のガイド', lang_config['trending_title'])
    content = content.replace('⭐ 最も人気', lang_config['most_popular'])
    content = content.replace('📈 トレンド', lang_config['trending'])
    content = content.replace('🆕 新着', lang_config['new'])
    content = content.replace('🔥 2.5k 閲覧', f"🔥 2.5k {lang_config['views']}")
    content = content.replace('🔥 1.8k 閲覧', f"🔥 1.8k {lang_config['views']}")
    content = content.replace('🔥 1.2k 閲覧', f"🔥 1.2k {lang_config['views']}")
    
    # 替换分类标题
    content = content.replace('🍽️ レシピガイド', lang_config['recipe_title'])
    content = content.replace('🌾 農業ガイド', lang_config['farming_title'])
    content = content.replace('💰 利益最適化', lang_config['profit_title'])
    content = content.replace('👥 協力と運用', lang_config['coop_title'])
    content = content.replace('🎮 上級ガイド', lang_config['advanced_title'])
    
    # 替换快速提示部分
    content = content.replace('💡 クイックヒント', lang_config['quick_tips_title'])
    
    # 替换导航部分
    content = content.replace('🏠 ナビゲーション', lang_config['navigation_title'])
    content = content.replace('← メイン計算機に戻る', lang_config['back_to_calc'])
    
    # 替换难度和阅读时间
    content = content.replace('初心者', lang_config['beginner'])
    content = content.replace('中級', lang_config['intermediate'])
    content = content.replace('エキスパート', lang_config['expert'])
    content = content.replace('上級', lang_config['advanced'])
    content = content.replace('分読了', f" {lang_config['minutes_read']}")
    
    # 替换语言选择器的选中状态
    content = re.sub(r'<option value="[^"]*" selected="">[^<]*</option>', 
                     f'<option value="{lang_code}" selected="">', content)
    
    # 替换所有链接前缀
    content = content.replace('/ja/', f'/{lang_code}/')
    
    return content

def main():
    """主函数"""
    print("🔄 开始同步所有语言攻略页面的内容...")
    
    # 需要同步的语言列表
    languages = ['zh-cn', 'es', 'pt-br', 'fr', 'de', 'ru', 'ar', 'hi', 'id', 'vi']
    
    for lang_code in languages:
        print(f"📝 正在处理 {lang_code} 语言...")
        
        # 获取语言配置
        lang_config = get_language_config(lang_code)
        
        # 创建攻略页面内容
        content = create_guides_content(lang_code, lang_config)
        
        # 写入文件
        guides_file = f"{lang_code}/guides.html"
        with open(guides_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新: {guides_file}")
    
    print("\n🎉 所有语言攻略页面内容同步完成！")
    print("📋 已同步的语言:")
    for lang in languages:
        print(f"   - {lang}")

if __name__ == "__main__":
    main() 