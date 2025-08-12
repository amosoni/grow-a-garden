#!/usr/bin/env python3
"""
修复所有语言目录中损坏的storage-and-logistics.html文件
"""

import os
import json

# 语言配置
LANGUAGES = {
    'zh-cn': {
        'title': 'Grow a Garden 中的存储和物流 - 优化指南',
        'description': '优化存储和物流：中心设计、标签、批处理、路线和市场交付策略，减少步行并增加利润。',
        'h1': '📦 Grow a Garden 中的存储和物流',
        'subtitle': '优化指南：存储中心、标签、路线和交付',
        'goals_title': '🎯 目标',
        'goals': ['减少步行距离和空闲时间', '保持库存清晰易找', '高效批量交付商品'],
        'storage_title': '🏗️ 存储中心设计',
        'delivery_title': '🚚 交付和市场策略',
        'back_btn': '← 返回指南'
    },
    'es': {
        'title': 'Almacenamiento y Logística en Grow a Garden - Guía de Optimización',
        'description': 'Optimiza el almacenamiento y logística en Grow a Garden: diseño de centro, etiquetado, lotes, rutas y estrategias de entrega al mercado para reducir caminar y aumentar ganancias.',
        'h1': '📦 Almacenamiento y Logística en Grow a Garden',
        'subtitle': 'Guía de Optimización: Centros de Almacenamiento, Etiquetado, Rutas y Entrega',
        'goals_title': '🎯 Objetivos',
        'goals': ['Reducir distancia de caminata y tiempo de inactividad', 'Mantener inventario claro y fácil de encontrar', 'Entregar bienes en lotes eficientes'],
        'storage_title': '🏗️ Diseño del Centro de Almacenamiento',
        'delivery_title': '🚚 Estrategia de Entrega y Mercado',
        'back_btn': '← Volver a Guías'
    },
    'pt-br': {
        'title': 'Armazenamento e Logística em Grow a Garden - Guia de Otimização',
        'description': 'Otimize armazenamento e logística em Grow a Garden: design de centro, rotulagem, lotes, rotas e estratégias de entrega ao mercado para reduzir caminhadas e aumentar lucros.',
        'h1': '📦 Armazenamento e Logística em Grow a Garden',
        'subtitle': 'Guia de Otimização: Centros de Armazenamento, Rotulagem, Rotas e Entrega',
        'goals_title': '🎯 Objetivos',
        'goals': ['Reduzir distância de caminhada e tempo ocioso', 'Manter inventário claro e fácil de encontrar', 'Entregar bens em lotes eficientes'],
        'storage_title': '🏗️ Design do Centro de Armazenamento',
        'delivery_title': '🚚 Estratégia de Entrega e Mercado',
        'back_btn': '← Voltar aos Guias'
    },
    'fr': {
        'title': 'Stockage et Logistique dans Grow a Garden - Guide d\'Optimisation',
        'description': 'Optimisez le stockage et la logistique dans Grow a Garden : conception de centre, étiquetage, lots, routage et stratégies de livraison au marché pour réduire la marche et augmenter les profits.',
        'h1': '📦 Stockage et Logistique dans Grow a Garden',
        'subtitle': 'Guide d\'Optimisation : Centres de Stockage, Étiquetage, Routage et Livraison',
        'goals_title': '🎯 Objectifs',
        'goals': ['Réduire la distance de marche et le temps d\'inactivité', 'Maintenir un inventaire clair et facile à trouver', 'Livrer les biens en lots efficaces'],
        'storage_title': '🏗️ Conception du Centre de Stockage',
        'delivery_title': '🚚 Stratégie de Livraison et Marché',
        'back_btn': '← Retour aux Guides'
    },
    'de': {
        'title': 'Lagerung und Logistik in Grow a Garden - Optimierungsleitfaden',
        'description': 'Optimieren Sie Lagerung und Logistik in Grow a Garden: Zentrumsdesign, Kennzeichnung, Batching, Routing und Marktlieferstrategien, um das Gehen zu reduzieren und Gewinne zu steigern.',
        'h1': '📦 Lagerung und Logistik in Grow a Garden',
        'subtitle': 'Optimierungsleitfaden: Lagerzentren, Kennzeichnung, Routing und Lieferung',
        'goals_title': '🎯 Ziele',
        'goals': ['Gehstrecke und Leerlaufzeit reduzieren', 'Inventar klar und leicht auffindbar halten', 'Waren in effizienten Chargen liefern'],
        'storage_title': '🏗️ Lagerzentrums-Design',
        'delivery_title': '🚚 Liefer- und Marktstrategie',
        'back_btn': '← Zurück zu Anleitungen'
    },
    'ru': {
        'title': 'Хранение и Логистика в Grow a Garden - Руководство по Оптимизации',
        'description': 'Оптимизируйте хранение и логистику в Grow a Garden: дизайн центра, маркировка, партии, маршруты и стратегии доставки на рынок для сокращения ходьбы и увеличения прибыли.',
        'h1': '📦 Хранение и Логистика в Grow a Garden',
        'subtitle': 'Руководство по Оптимизации: Центры Хранения, Маркировка, Маршруты и Доставка',
        'goals_title': '🎯 Цели',
        'goals': ['Сократить расстояние ходьбы и время простоя', 'Поддерживать четкий и легко находимый инвентарь', 'Доставлять товары эффективными партиями'],
        'storage_title': '🏗️ Дизайн Центра Хранения',
        'delivery_title': '🚚 Стратегия Доставки и Рынка',
        'back_btn': '← Назад к Руководствам'
    },
    'ar': {
        'title': 'التخزين واللوجستيات في Grow a Garden - دليل التحسين',
        'description': 'حسن التخزين واللوجستيات في Grow a Garden: تصميم المركز، التوسيم، الدفعات، المسارات واستراتيجيات التسليم للسوق لتقليل المشي وزيادة الأرباح.',
        'h1': '📦 التخزين واللوجستيات في Grow a Garden',
        'subtitle': 'دليل التحسين: مراكز التخزين، التوسيم، المسارات والتسليم',
        'goals_title': '🎯 الأهداف',
        'goals': ['تقليل مسافة المشي والوقت الخامل', 'الحفاظ على مخز واضح وسهل العثور عليه', 'تسليم البضائع في دفعات فعالة'],
        'storage_title': '🏗️ تصميم مركز التخزين',
        'delivery_title': '🚚 استراتيجية التسليم والسوق',
        'back_btn': '← العودة إلى الأدلة'
    },
    'hi': {
        'title': 'Grow a Garden में भंडारण और रसद - अनुकूलन गाइड',
        'description': 'Grow a Garden में भंडारण और रसद को अनुकूलित करें: केंद्र डिज़ाइन, लेबलिंग, बैचिंग, रूटिंग और बाजार वितरण रणनीतियां चलने को कम करने और लाभ बढ़ाने के लिए।',
        'h1': '📦 Grow a Garden में भंडारण और रसद',
        'subtitle': 'अनुकूलन गाइड: भंडारण केंद्र, लेबलिंग, रूटिंग और वितरण',
        'goals_title': '🎯 लक्ष्य',
        'goals': ['चलने की दूरी और निष्क्रिय समय कम करें', 'सूची को स्पष्ट और आसानी से खोजने योग्य रखें', 'माल को कुशल बैचों में वितरित करें'],
        'storage_title': '🏗️ भंडारण केंद्र डिज़ाइन',
        'delivery_title': '🚚 वितरण और बाजार रणनीति',
        'back_btn': '← गाइड पर वापस जाएं'
    },
    'id': {
        'title': 'Penyimpanan dan Logistik di Grow a Garden - Panduan Optimasi',
        'description': 'Optimalkan penyimpanan dan logistik di Grow a Garden: desain pusat, pelabelan, batching, routing dan strategi pengiriman pasar untuk mengurangi berjalan dan meningkatkan keuntungan.',
        'h1': '📦 Penyimpanan dan Logistik di Grow a Garden',
        'subtitle': 'Panduan Optimasi: Pusat Penyimpanan, Pelabelan, Routing dan Pengiriman',
        'goals_title': '🎯 Tujuan',
        'goals': ['Kurangi jarak berjalan dan waktu menganggur', 'Jaga inventaris tetap jelas dan mudah ditemukan', 'Kirim barang dalam batch yang efisien'],
        'storage_title': '🏗️ Desain Pusat Penyimpanan',
        'delivery_title': '🚚 Strategi Pengiriman dan Pasar',
        'back_btn': '← Kembali ke Panduan'
    },
    'vi': {
        'title': 'Lưu Trữ và Hậu Cần trong Grow a Garden - Hướng Dẫn Tối Ưu Hóa',
        'description': 'Tối ưu hóa lưu trữ và hậu cần trong Grow a Garden: thiết kế trung tâm, gắn nhãn, batching, định tuyến và chiến lược giao hàng thị trường để giảm đi bộ và tăng lợi nhuận.',
        'h1': '📦 Lưu Trữ và Hậu Cần trong Grow a Garden',
        'subtitle': 'Hướng Dẫn Tối Ưu Hóa: Trung Tâm Lưu Trữ, Gắn Nhãn, Định Tuyến và Giao Hàng',
        'goals_title': '🎯 Mục Tiêu',
        'goals': ['Giảm khoảng cách đi bộ và thời gian nhàn rỗi', 'Duy trì khoảng không rõ ràng và dễ tìm', 'Giao hàng hóa trong các lô hiệu quả'],
        'storage_title': '🏗️ Thiết Kế Trung Tâm Lưu Trữ',
        'delivery_title': '🚚 Chiến Lược Giao Hàng và Thị Trường',
        'back_btn': '← Quay Lại Hướng Dẫn'
    },
    'ja': {
        'title': 'Grow a Garden でのストレージとロジスティクス - 最適化ガイド',
        'description': 'Grow a Garden でのストレージとロジスティクスを最適化：ハブデザイン、ラベリング、バッチング、ルーティング、市場配達戦略で歩行を減らし利益を増やします。',
        'h1': '📦 Grow a Garden でのストレージとロジスティクス',
        'subtitle': '最適化ガイド：ストレージハブ、ラベリング、ルーティング、配達',
        'goals_title': '🎯 目標',
        'goals': ['歩行距離とアイドル時間を減らす', '在庫を明確で見つけやすく保つ', '効率的なバッチで商品を配達する'],
        'storage_title': '🏗️ ストレージハブデザイン',
        'delivery_title': '🚚 配達と市場戦略',
        'back_btn': '← ガイドに戻る'
    }
}

def generate_html_content(lang_code, lang_config):
    """为指定语言生成HTML内容"""
    
    # 确定语言方向和CSS类
    if lang_code == 'ar':
        lang_attr = 'lang="ar" dir="rtl"'
        css_class = 'rtl'
    else:
        lang_attr = f'lang="{lang_code}"'
        css_class = ''
    
    # 生成目标语言列表
    lang_options = []
    for code, name in [
        ('en', 'English'),
        ('zh-cn', '简体中文'),
        ('es', 'Español'),
        ('pt-br', 'Português'),
        ('fr', 'Français'),
        ('de', 'Deutsch'),
        ('ru', 'Русский'),
        ('ar', 'العربية'),
        ('hi', 'हिन्दी'),
        ('id', 'Bahasa Indonesia'),
        ('vi', 'Tiếng Việt'),
        ('ja', '日本語')
    ]:
        selected = 'selected=""' if code == lang_code else ''
        lang_options.append(f'<option value="{code}" {selected}>{name}</option>')
    
    lang_options_html = '\n                '.join(lang_options)
    
    html_content = f'''<!DOCTYPE html>
<html {lang_attr}>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{lang_config['title']}</title>
  <meta name="description" content="{lang_config['description']}">
  <meta name="keywords" content="grow a garden storage, logistics, routing, chest labeling, batching, delivery, optimization">
  <link rel="canonical" href="https://growagarden.cv/{lang_code}/storage-and-logistics.html">
  <link rel="alternate" hreflang="en" href="https://growagarden.cv/storage-and-logistics.html">
  <link rel="alternate" hreflang="{lang_code}" href="https://growagarden.cv/{lang_code}/storage-and-logistics.html">
  <link rel="alternate" hreflang="x-default" href="https://growagarden.cv/storage-and-logistics.html">
  <link rel="stylesheet" href="https://unpkg.com/simple.css@2.1.0/simple.min.css">
  <link rel="stylesheet" href="/styles.css">
</head>
<body class="{css_class}">
  <header>
    <nav>
      <a href="/index.html" class="logo" data-i18n="nav.logo">🌱 Grow a Garden</a>
      <a href="/guides.html" data-i18n="nav.guides">📚 {'Guides' if lang_code == 'en' else 'الأدلة' if lang_code == 'ar' else 'Anleitungen' if lang_code == 'de' else 'Guías' if lang_code == 'es' else 'Guides' if lang_code == 'fr' else 'Guides' if lang_code == 'pt-br' else 'Руководства' if lang_code == 'ru' else 'गाइड' if lang_code == 'hi' else 'Panduan' if lang_code == 'id' else 'Hướng Dẫn' if lang_code == 'vi' else 'ガイド'} </a>
                  <select id="lang-switcher" aria-label="Language">
                {lang_options_html}
            </select>
    </nav>
  </header>
  <main>
    <h1>{lang_config['h1']}</h1>
    <p>{lang_config['subtitle']}</p>
    
    <div class="guide-section">
      <div class="guide-card">
        <h2>{lang_config['goals_title']}</h2>
        <ul>
          <li>{lang_config['goals'][0]}</li>
          <li>{lang_config['goals'][1]}</li>
          <li>{lang_config['goals'][2]}</li>
        </ul>
      </div>

      <div class="guide-card">
        <h2>{lang_config['storage_title']}</h2>
        <p>Design efficient storage hubs with proper labeling and routing systems.</p>
      </div>

      <div class="guide-card">
        <h2>{lang_config['delivery_title']}</h2>
        <p>Optimize delivery routes and market strategies for maximum efficiency.</p>
      </div>

      <div class="guide-card" style="text-align:center;">
        <a href="/guides.html" class="back-btn">{lang_config['back_btn']}</a>
      </div>
    </div>
  </main>
  <script src="/i18n/i18n.js"></script>
</body>
</html>'''
    
    return html_content

def fix_storage_logistics_files():
    """修复所有语言目录中的storage-and-logistics.html文件"""
    
    fixed_files = []
    error_files = []
    
    for lang_code, lang_config in LANGUAGES.items():
        file_path = f"{lang_code}/storage-and-logistics.html"
        
        if not os.path.exists(f"{lang_code}"):
            print(f"跳过 {lang_code}: 目录不存在")
            continue
            
        try:
            # 生成新的HTML内容
            new_content = generate_html_content(lang_code, lang_config)
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ 已修复 {file_path}")
            fixed_files.append(file_path)
            
        except Exception as e:
            print(f"❌ 修复 {file_path} 时出错: {e}")
            error_files.append(file_path)
    
    print(f"\n📊 修复完成:")
    print(f"✅ 成功修复: {len(fixed_files)} 个文件")
    if error_files:
        print(f"❌ 修复失败: {len(error_files)} 个文件")
        for file in error_files:
            print(f"   - {file}")
    
    return fixed_files, error_files

if __name__ == "__main__":
    print("🔧 开始修复storage-and-logistics.html文件...")
    fixed, errors = fix_storage_logistics_files()
    
    if not errors:
        print("\n🎉 所有文件修复成功！")
    else:
        print(f"\n⚠️  有 {len(errors)} 个文件修复失败，请检查错误信息。") 