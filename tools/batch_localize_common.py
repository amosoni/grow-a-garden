#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, time, shutil
import json

ROOT = os.path.abspath(os.path.dirname(__file__)).rsplit(os.sep, 1)[0]
LANG_DIRS = ["zh-cn","es","pt-br","fr","de","ru","ar","hi","id","vi","ja"]
BACKUP_DIR = os.path.join(ROOT, 'backups', f'batch_localize_{time.strftime("%Y%m%d_%H%M%S")}')

SCRIPT_RE = re.compile(r'<script[\s\S]*?</script>', re.IGNORECASE)
STYLE_RE = re.compile(r'<style[\s\S]*?</style>', re.IGNORECASE)

# Mappings derived from runtime i18n logic
HEADINGS = {
  'ja': {
    'Basic Salad Recipes':'基本サラダレシピ','Luxury Salad Recipes':'高級サラダレシピ','Basic Pizza Recipes':'基本ピザレシピ','Advanced Pizza Recipes':'上級ピザレシピ','Premium Recipes':'プレミアムレシピ','Pizza Varieties & Types':'ピザの種類','Making Tips & Tricks':'作りのコツとテクニック','Growing Tips':'栽培のコツ','Making Tips':'作り方のコツ','Profit Optimization':'利益最適化','Production Optimization':'生産最適化','Advanced Strategies':'高度な戦略','Next Steps':'次のステップ','Basic Bread Making':'基本的なパン作り','Basic Bread Recipes':'基本パンレシピ','Advanced Bread Recipes':'上級パンレシピ','Premium Bread Recipes':'プレミアムパンレシピ','Bread Varieties & Types':'パンの種類'
  },
  'zh-cn': {
    'Basic Salad Recipes':'基础沙拉配方','Luxury Salad Recipes':'高阶沙拉配方','Basic Pizza Recipes':'基础披萨配方','Advanced Pizza Recipes':'进阶披萨配方','Premium Recipes':'高级配方','Pizza Varieties & Types':'披萨种类','Making Tips & Tricks':'制作技巧','Growing Tips':'种植技巧','Making Tips':'制作要点','Profit Optimization':'收益优化','Production Optimization':'生产优化','Advanced Strategies':'高级策略','Next Steps':'下一步','Basic Bread Making':'基础面包制作','Basic Bread Recipes':'基础面包配方','Advanced Bread Recipes':'进阶面包配方','Premium Bread Recipes':'高级面包配方','Bread Varieties & Types':'面包种类'
  },
  'es': {
    'Basic Salad Recipes':'Recetas básicas de ensalada','Luxury Salad Recipes':'Recetas de ensalada premium','Basic Pizza Recipes':'Recetas básicas de pizza','Advanced Pizza Recipes':'Recetas avanzadas de pizza','Premium Recipes':'Recetas premium','Pizza Varieties & Types':'Variedades de pizza','Making Tips & Tricks':'Consejos y trucos','Growing Tips':'Consejos de cultivo','Making Tips':'Consejos de preparación','Profit Optimization':'Optimización de ganancias','Production Optimization':'Optimización de producción','Advanced Strategies':'Estrategias avanzadas','Next Steps':'Siguientes pasos','Basic Bread Making':'Elaboración básica de pan','Basic Bread Recipes':'Recetas básicas de pan','Advanced Bread Recipes':'Recetas avanzadas de pan','Premium Bread Recipes':'Recetas de pan premium','Bread Varieties & Types':'Tipos de pan'
  },
  'pt-br': {
    'Basic Salad Recipes':'Receitas básicas de salada','Luxury Salad Recipes':'Receitas de salada premium','Basic Pizza Recipes':'Receitas básicas de pizza','Advanced Pizza Recipes':'Receitas avançadas de pizza','Premium Recipes':'Receitas premium','Pizza Varieties & Types':'Tipos de pizza','Making Tips & Tricks':'Dicas e truques','Growing Tips':'Dicas de cultivo','Making Tips':'Dicas de preparo','Profit Optimization':'Otimização de lucro','Production Optimization':'Otimização de produção','Advanced Strategies':'Estratégias avançadas','Next Steps':'Próximos passos','Basic Bread Making':'Preparo básico de pão','Basic Bread Recipes':'Receitas básicas de pão','Advanced Bread Recipes':'Receitas avançadas de pão','Premium Bread Recipes':'Receitas de pão premium','Bread Varieties & Types':'Tipos de pão'
  },
  'fr': {
    'Basic Salad Recipes':'Recettes de salade de base','Luxury Salad Recipes':'Recettes de salade haut de gamme','Basic Pizza Recipes':'Recettes de pizza de base','Advanced Pizza Recipes':'Recettes de pizza avancées','Premium Recipes':'Recettes premium','Pizza Varieties & Types':'Variétés de pizza','Making Tips & Tricks':'Astuces et conseils','Growing Tips':'Conseils de culture','Making Tips':'Conseils de préparation','Profit Optimization':'Optimisation du profit','Production Optimization':'Optimisation de la production','Advanced Strategies':'Stratégies avancées','Next Steps':'Étapes suivantes','Basic Bread Making':'Fabrication de pain de base','Basic Bread Recipes':'Recettes de pain de base','Advanced Bread Recipes':'Recettes de pain avancées','Premium Bread Recipes':'Recettes de pain premium','Bread Varieties & Types':'Variétés de pain'
  },
  'de': {
    'Basic Salad Recipes':'Grundlegende Salatrezepte','Luxury Salad Recipes':'Luxus-Salatrezepte','Basic Pizza Recipes':'Einfache Pizzarezepte','Advanced Pizza Recipes':'Fortgeschrittene Pizzarezepte','Premium Recipes':'Premium-Rezepte','Pizza Varieties & Types':'Pizza-Varianten','Making Tips & Tricks':'Tipps und Tricks','Growing Tips':'Anbautipps','Making Tips':'Zubereitungstipps','Profit Optimization':'Gewinnoptimierung','Production Optimization':'Produktionsoptimierung','Advanced Strategies':'Fortgeschrittene Strategien','Next Steps':'Nächste Schritte','Basic Bread Making':'Grundlegendes Brotbacken','Basic Bread Recipes':'Grundrezepte für Brot','Advanced Bread Recipes':'Fortgeschrittene Brotrezepte','Premium Bread Recipes':'Premium-Brotrezepte','Bread Varieties & Types':'Brotarten'
  },
  'ru': {
    'Basic Salad Recipes':'Базовые рецепты салатов','Luxury Salad Recipes':'Премиальные рецепты салатов','Basic Pizza Recipes':'Базовые рецепты пиццы','Advanced Pizza Recipes':'Продвинутые рецепты пиццы','Premium Recipes':'Премиальные рецепты','Pizza Varieties & Types':'Виды пиццы','Making Tips & Tricks':'Советы и хитрости','Growing Tips':'Советы по выращиванию','Making Tips':'Советы по приготовлению','Profit Optimization':'Оптимизация прибыли','Production Optimization':'Оптимизация производства','Advanced Strategies':'Продвинутые стратегии','Next Steps':'Следующие шаги','Basic Bread Making':'Основы выпечки хлеба','Basic Bread Recipes':'Базовые рецепты хлеба','Advanced Bread Recipes':'Продвинутые рецепты хлеба','Premium Bread Recipes':'Премиальные рецепты хлеба','Bread Varieties & Types':'Виды хлеба'
  },
  'ar': {
    'Basic Salad Recipes':'وصفات سلطة أساسية','Luxury Salad Recipes':'وصفات سلطة فاخرة','Basic Pizza Recipes':'وصفات بيتزا أساسية','Advanced Pizza Recipes':'وصفات بيتزا متقدمة','Premium Recipes':'وصفات مميزة','Pizza Varieties & Types':'أنواع البيتزا','Making Tips & Tricks':'نصائح وحيل','Growing Tips':'نصائح الزراعة','Making Tips':'نصائح التحضير','Profit Optimization':'تحسين الأرباح','Production Optimization':'تحسين الإنتاج','Advanced Strategies':'استراتيجيات متقدمة','Next Steps':'الخطوات التالية','Basic Bread Making':'خبز أساسي','Basic Bread Recipes':'وصفات خبز أساسية','Advanced Bread Recipes':'وصفات خبز متقدمة','Premium Bread Recipes':'وصفات خبز مميزة','Bread Varieties & Types':'أنواع الخبز'
  },
  'hi': {
    'Basic Salad Recipes':'बेसिक सलाद रेसिपी','Luxury Salad Recipes':'लक्ज़री सलाद रेसिपी','Basic Pizza Recipes':'बेसिक पिज़्ज़ा रेसिपी','Advanced Pizza Recipes':'एडवांस्ड पिज़्ज़ा रेसिपी','Premium Recipes':'प्रीमियम रेसिपी','Pizza Varieties & Types':'पिज़्ज़ा के प्रकार','Making Tips & Tricks':'टिप्स और ट्रिक्स','Growing Tips':'खेती के सुझाव','Making Tips':'बनाने के सुझाव','Profit Optimization':'लाभ अनुकूलन','Production Optimization':'उत्पादन अनुकूलन','Advanced Strategies':'उन्नत रणनीतियाँ','Next Steps':'अगले कदम','Basic Bread Making':'बेसिक ब्रेड बनाना','Basic Bread Recipes':'बेसिक ब्रेड रेसिपी','Advanced Bread Recipes':'एडवांस्ड ब्रेड रेसिपी','Premium Bread Recipes':'प्रीमियम ब्रेड रेसिपी','Bread Varieties & Types':'ब्रेड के प्रकार'
  },
  'id': {
    'Basic Salad Recipes':'Resep salad dasar','Luxury Salad Recipes':'Resep salad premium','Basic Pizza Recipes':'Resep pizza dasar','Advanced Pizza Recipes':'Resep pizza lanjutan','Premium Recipes':'Resep premium','Pizza Varieties & Types':'Jenis pizza','Making Tips & Tricks':'Tips & trik','Growing Tips':'Tips budidaya','Making Tips':'Tips pembuatan','Profit Optimization':'Optimasi profit','Production Optimization':'Optimasi produksi','Advanced Strategies':'Strategi lanjutan','Next Steps':'Langkah berikutnya','Basic Bread Making':'Pembuatan roti dasar','Basic Bread Recipes':'Resep roti dasar','Advanced Bread Recipes':'Resep roti lanjutan','Premium Bread Recipes':'Resep roti premium','Bread Varieties & Types':'Jenis roti'
  },
  'vi': {
    'Basic Salad Recipes':'Công thức salad cơ bản','Luxury Salad Recipes':'Công thức salad cao cấp','Basic Pizza Recipes':'Công thức pizza cơ bản','Advanced Pizza Recipes':'Công thức pizza nâng cao','Premium Recipes':'Công thức cao cấp','Pizza Varieties & Types':'Các loại pizza','Making Tips & Tricks':'Mẹo và thủ thuật','Growing Tips':'Mẹo trồng trọt','Making Tips':'Mẹo chế biến','Profit Optimization':'Tối ưu lợi nhuận','Production Optimization':'Tối ưu sản xuất','Advanced Strategies':'Chiến lược nâng cao','Next Steps':'Bước tiếp theo','Basic Bread Making':'Làm bánh mì cơ bản','Basic Bread Recipes':'Công thức bánh mì cơ bản','Advanced Bread Recipes':'Công thức bánh mì nâng cao','Premium Bread Recipes':'Công thức bánh mì cao cấp','Bread Varieties & Types':'Các loại bánh mì'
  }
}

STRONG = {
  'ja': {'Optimal Watering':'最適な水やり','Golden Hours':'ゴールデンアワー','Harvest Timing':'収穫タイミング','Soil Quality':'土壌品質','Dough Quality':'生地の品質','Topping Balance':'トッピングのバランス','Recipe Efficiency':'レシピ効率','Storage Management':'在庫管理','Market Timing':'市場のタイミング','Quality vs Quantity':'品質と量のバランス','Recipe Mastery':'レシピの習熟','Supply Chain':'サプライチェーン','Automated Systems':'自動化システム','Batch Processing':'バッチ処理','Ingredient Rotation':'作物ローテーション','Quality Control':'品質管理','Market Analysis':'市場分析','Recipe Optimization':'レシピ最適化','Resource Management':'リソース管理','Skill Development':'スキル向上','Community Tip:':'コミュニティのヒント:'},
  'zh-cn': {'Optimal Watering':'最佳浇水','Golden Hours':'黄金时段','Harvest Timing':'收获时机','Soil Quality':'土壤质量','Dough Quality':'面团质量','Topping Balance':'配料平衡','Recipe Efficiency':'配方效率','Storage Management':'库存管理','Market Timing':'市场时机','Quality vs Quantity':'质量 vs 数量','Recipe Mastery':'配方熟练度','Supply Chain':'供应链','Automated Systems':'自动化系统','Batch Processing':'批量处理','Ingredient Rotation':'轮作','Quality Control':'质量控制','Market Analysis':'市场分析','Recipe Optimization':'配方优化','Resource Management':'资源管理','Skill Development':'技能提升','Community Tip:':'社区提示：'},
  'es': {'Optimal Watering':'Riego óptimo','Golden Hours':'Horas doradas','Harvest Timing':'Momento de cosecha','Soil Quality':'Calidad del suelo','Dough Quality':'Calidad de la masa','Topping Balance':'Equilibrio de ingredientes','Recipe Efficiency':'Eficiencia de recetas','Storage Management':'Gestión de inventario','Market Timing':'Momento del mercado','Quality vs Quantity':'Calidad vs Cantidad','Recipe Mastery':'Maestría de recetas','Supply Chain':'Cadena de suministro','Automated Systems':'Sistemas automatizados','Batch Processing':'Procesamiento por lotes','Ingredient Rotation':'Rotación de cultivos','Quality Control':'Control de calidad','Market Analysis':'Análisis de mercado','Recipe Optimization':'Optimización de recetas','Resource Management':'Gestión de recursos','Skill Development':'Desarrollo de habilidades','Community Tip:':'Consejo de la comunidad:'},
  'pt-br': {'Optimal Watering':'Rega ideal','Golden Hours':'Horas de ouro','Harvest Timing':'Momento da colheita','Soil Quality':'Qualidade do solo','Dough Quality':'Qualidade da massa','Topping Balance':'Equilíbrio de coberturas','Recipe Efficiency':'Eficiência da receita','Storage Management':'Gestão de estoque','Market Timing':'Momento de mercado','Quality vs Quantity':'Qualidade vs Quantidade','Recipe Mastery':'Domínio da receita','Supply Chain':'Cadeia de suprimentos','Automated Systems':'Sistemas automatizados','Batch Processing':'Processamento em lote','Ingredient Rotation':'Rotação de culturas','Quality Control':'Controle de qualidade','Market Analysis':'Análise de mercado','Recipe Optimization':'Otimização de receita','Resource Management':'Gestão de recursos','Skill Development':'Desenvolvimento de habilidades','Community Tip:':'Dica da comunidade:'},
  'fr': {'Optimal Watering':'Arrosage optimal','Golden Hours':'Heures dorées','Harvest Timing':'Moment de récolte','Soil Quality':'Qualité du sol','Dough Quality':'Qualité de la pâte','Topping Balance':'Équilibre des garnitures','Recipe Efficiency':'Efficacité des recettes','Storage Management':'Gestion du stock','Market Timing':'Timing du marché','Quality vs Quantity':'Qualité vs Quantité','Recipe Mastery':'Maîtrise des recettes','Supply Chain':'Chaîne d\'approvisionnement','Automated Systems':'Systèmes automatisés','Batch Processing':'Traitement par lot','Ingredient Rotation':'Rotation des cultures','Quality Control':'Contrôle qualité','Market Analysis':'Analyse du marché','Recipe Optimization':'Optimisation des recettes','Resource Management':'Gestion des ressources','Skill Development':'Développement des compétences','Community Tip:':'Astuce de la communauté :'},
  'de': {'Optimal Watering':'Optimale Bewässerung','Golden Hours':'Goldene Stunden','Harvest Timing':'Erntezeitpunkt','Soil Quality':'Bodenqualität','Dough Quality':'Teigqualität','Topping Balance':'Belag-Balance','Recipe Efficiency':'Rezept-Effizienz','Storage Management':'Lagerverwaltung','Market Timing':'Markt-Timing','Quality vs Quantity':'Qualität vs Quantität','Recipe Mastery':'Rezeptbeherrschung','Supply Chain':'Lieferkette','Automated Systems':'Automatisierte Systeme','Batch Processing':'Batch-Verarbeitung','Ingredient Rotation':'Fruchtfolge','Quality Control':'Qualitätskontrolle','Market Analysis':'Marktanalyse','Recipe Optimization':'Rezeptoptimierung','Resource Management':'Ressourcenmanagement','Skill Development':'Fähigkeitenentwicklung','Community Tip:':'Community-Tipp:'},
  'ru': {'Optimal Watering':'Оптимальный полив','Golden Hours':'Золотые часы','Harvest Timing':'Время сбора','Soil Quality':'Качество почвы','Dough Quality':'Качество теста','Topping Balance':'Баланс начинок','Recipe Efficiency':'Эффективность рецептов','Storage Management':'Управление запасами','Market Timing':'Тайминг рынка','Quality vs Quantity':'Качество vs Количество','Recipe Mastery':'Мастерство рецептов','Supply Chain':'Цепочка поставок','Automated Systems':'Автоматизированные системы','Batch Processing':'Пакетная обработка','Ingredient Rotation':'Севооборот','Quality Control':'Контроль качества','Market Analysis':'Анализ рынка','Recipe Optimization':'Оптимизация рецептов','Resource Management':'Управление ресурсами','Skill Development':'Развитие навыков','Community Tip:':'Совет сообщества:'},
  'ar': {'Optimal Watering':'الري الأمثل','Golden Hours':'الساعات الذهبية','Harvest Timing':'توقيت الحصاد','Soil Quality':'جودة التربة','Dough Quality':'جودة العجين','Topping Balance':'توازن الإضافات','Recipe Efficiency':'كفاءة الوصفة','Storage Management':'إدارة المخزون','Market Timing':'توقيت السوق','Quality vs Quantity':'الجودة مقابل الكمية','Recipe Mastery':'إتقان الوصفات','Supply Chain':'سلسلة الإمداد','Automated Systems':'أنظمة مؤتمتة','Batch Processing':'المعالجة الدفعية','Ingredient Rotation':'دورة المحاصيل','Quality Control':'مراقبة الجودة','Market Analysis':'تحليل السوق','Recipe Optimization':'تحسين الوصفات','Resource Management':'إدارة الموارد','Skill Development':'تطوير المهارات','Community Tip:':'نصيحة المجتمع:'},
  'hi': {'Optimal Watering':'सर्वोत्तम सिंचाई','Golden Hours':'स्वर्णिम समय','Harvest Timing':'कटाई समय','Soil Quality':'मिट्टी की गुणवत्ता','Dough Quality':'आटे की गुणवत्ता','Topping Balance':'टॉपिंग संतुलन','Recipe Efficiency':'रेसिपी दक्षता','Storage Management':'भंडारण प्रबंधन','Market Timing':'बाज़ार समय','Quality vs Quantity':'गुणवत्ता बनाम मात्रा','Recipe Mastery':'रेसिपी महारत','Supply Chain':'आपूर्ति श्रृंखला','Automated Systems':'स्वचालित प्रणालियाँ','Batch Processing':'बैच प्रसंस्करण','Ingredient Rotation':'फसल चक्र','Quality Control':'गुणवत्ता नियंत्रण','Market Analysis':'बाज़ार विश्लेषण','Recipe Optimization':'रेसिपी अनुकूलन','Resource Management':'संसाधन प्रबंधन','Skill Development':'कौशल विकास','Community Tip:':'समुदाय सुझाव:'},
  'id': {'Optimal Watering':'Penyiraman optimal','Golden Hours':'Jam emas','Harvest Timing':'Waktu panen','Soil Quality':'Kualitas tanah','Dough Quality':'Kualitas adonan','Topping Balance':'Keseimbangan topping','Recipe Efficiency':'Efisiensi resep','Storage Management':'Manajemen persediaan','Market Timing':'Timing pasar','Quality vs Quantity':'Kualitas vs Kuantitas','Recipe Mastery':'Penguasaan resep','Supply Chain':'Rantai pasok','Automated Systems':'Sistem otomatis','Batch Processing':'Pemrosesan batch','Ingredient Rotation':'Rotasi tanaman','Quality Control':'Kontrol kualitas','Market Analysis':'Analisis pasar','Recipe Optimization':'Optimasi resep','Resource Management':'Manajemen sumber daya','Skill Development':'Pengembangan keterampilan','Community Tip:':'Tips komunitas:'},
  'vi': {'Optimal Watering':'Tưới nước tối ưu','Golden Hours':'Giờ vàng','Harvest Timing':'Thời điểm thu hoạch','Soil Quality':'Chất lượng đất','Dough Quality':'Chất lượng bột','Topping Balance':'Cân bằng topping','Recipe Efficiency':'Hiệu quả công thức','Storage Management':'Quản lý kho','Market Timing':'Thời điểm thị trường','Quality vs Quantity':'Chất lượng vs Số lượng','Recipe Mastery':'Thành thạo công thức','Supply Chain':'Chuỗi cung ứng','Automated Systems':'Hệ thống tự động','Batch Processing':'Xử lý theo lô','Ingredient Rotation':'Luân canh','Quality Control':'Kiểm soát chất lượng','Market Analysis':'Phân tích thị trường','Recipe Optimization':'Tối ưu công thức','Resource Management':'Quản lý tài nguyên','Skill Development':'Phát triển kỹ năng','Community Tip:':'Mẹo cộng đồng:'}
}

DIFF = {
  'ja': {'Easy':'初級','Medium':'中級','Hard':'上級','Expert':'エキスパート','Master':'マスター','Legendary':'レジェンダリー'},
  'zh-cn': {'Easy':'简单','Medium':'中等','Hard':'困难','Expert':'专家','Master':'大师','Legendary':'传说'},
  'es': {'Easy':'Fácil','Medium':'Medio','Hard':'Difícil','Expert':'Experto','Master':'Maestro','Legendary':'Legendario'},
  'pt-br': {'Easy':'Fácil','Medium':'Médio','Hard':'Difícil','Expert':'Especialista','Master':'Mestre','Legendary':'Lendário'},
  'fr': {'Easy':'Facile','Medium':'Moyen','Hard':'Difficile','Expert':'Expert','Master':'Maître','Legendary':'Légendaire'},
  'de': {'Easy':'Leicht','Medium':'Mittel','Hard':'Schwer','Expert':'Experte','Master':'Meister','Legendary':'Legendär'},
  'ru': {'Easy':'Легко','Medium':'Средне','Hard':'Сложно','Expert':'Эксперт','Master':'Мастер','Legendary':'Легендарно'},
  'ar': {'Easy':'سهل','Medium':'متوسط','Hard':'صعب','Expert':'خبير','Master':'ماستر','Legendary':'أسطوري'},
  'hi': {'Easy':'आसान','Medium':'मध्यम','Hard':'कठिन','Expert':'विशेषज्ञ','Master':'मास्टर','Legendary':'लेजेंडरी'},
  'id': {'Easy':'Mudah','Medium':'Sedang','Hard':'Sulit','Expert':'Ahli','Master':'Master','Legendary':'Legendaris'},
  'vi': {'Easy':'Dễ','Medium':'Trung bình','Hard':'Khó','Expert':'Chuyên gia','Master':'Bậc thầy','Legendary':'Huyền thoại'}
}

USE_LABEL = {
  'en':'Use:','zh-cn':'用途：','ja':'用途：','es':'Uso:','pt-br':'Uso:','fr':'Utilisation :','de':'Verwendung:','ru':'Использование:','ar':'الاستخدام:','hi':'उपयोग:','id':'Kegunaan:','vi':'Cách dùng:'
}

# minute/coins replacements per language
MINUTES_FMT = {
  'ja': lambda m: f"{m.group(1)}分",
  'zh-cn': lambda m: f"{m.group(1)} 分钟",
  'es': lambda m: f"{m.group(1)} minutos",
  'pt-br': lambda m: f"{m.group(1)} min",
  'fr': lambda m: f"{m.group(1)} min",
  'de': lambda m: f"{m.group(1)} Min",
  'ru': lambda m: f"{m.group(1)} мин",
  'ar': lambda m: f"{m.group(1)} دقيقة",
  'hi': lambda m: f"{m.group(1)} मिनट",
  'id': lambda m: f"{m.group(1)} mnt",
  'vi': lambda m: f"{m.group(1)} phút",
}
COINS_FMT = {
  'ja': lambda m: f"{m.group(1)} コイン",
  'zh-cn': lambda m: f"{m.group(1)} 金币",
  'es': lambda m: f"{m.group(1)} monedas",
  'pt-br': lambda m: f"{m.group(1)} moedas",
  'fr': lambda m: f"{m.group(1)} pièces",
  'de': lambda m: f"{m.group(1)} Münzen",
  'ru': lambda m: f"{m.group(1)} монет",
  'ar': lambda m: f"{m.group(1)} عملات",
  'hi': lambda m: f"{m.group(1)} सिक्के",
  'id': lambda m: f"{m.group(1)} koin",
  'vi': lambda m: f"{m.group(1)} xu",
}

MINUTES_RE = re.compile(r'(\d+)\s+minutes', re.IGNORECASE)
COINS_RE = re.compile(r'(\d+)\s+coins', re.IGNORECASE)
Q_RE = re.compile(r'(^|\s)Q:\s*', re.IGNORECASE)
A_RE = re.compile(r'(^|\s)A:\s*', re.IGNORECASE)
PHRASES_PATH = os.path.join(ROOT, 'tools', 'phrases_map.json')
try:
  with open(PHRASES_PATH, 'r', encoding='utf-8') as _pf:
    PHRASES = json.load(_pf)
except Exception:
  PHRASES = {}

# Additional common phrase mappings across guides
COMMON_LABELS = {
  'Requirements': {
    'zh-cn':'要求','ja':'必要条件','es':'Requisitos','pt-br':'Requisitos','fr':'Prérequis','de':'Anforderungen','ru':'Требования','ar':'المتطلبات','hi':'आवश्यकताएँ','id':'Persyaratan','vi':'Yêu cầu'
  },
  'Pro Tips': {
    'zh-cn':'专业提示','ja':'プロのコツ','es':'Consejos pro','pt-br':'Dicas pro','fr':'Astuces pro','de':'Profi-Tipps','ru':'Полезные советы','ar':'نصائح احترافية','hi':'प्रो टिप्स','id':'Tips pro','vi':'Mẹo pro'
  },
  'Popular Cookie Varieties': {
    'zh-cn':'流行的曲奇种类','ja':'人気のクッキーの種類','es':'Variedades populares de galletas','pt-br':'Variedades populares de biscoitos','fr':'Variétés populaires de cookies','de':'Beliebte Keksarten','ru':'Популярные виды печенья','ar':'أنواع البسكويت الشائعة','hi':'लोकप्रिय कुकी प्रकार','id':'Varian kue kering populer','vi':'Các loại bánh quy phổ biến'
  },
  'Decoration Methods': {
    'zh-cn':'装饰方法','ja':'デコレーション方法','es':'Métodos de decoración','pt-br':'Métodos de decoração','fr':'Méthodes de décoration','de':'Dekorationsmethoden','ru':'Методы украшения','ar':'طرق التزيين','hi':'सजावट के तरीके','id':'Metode dekorasi','vi':'Phương pháp trang trí'
  },
  'Frosting Techniques': {
    'zh-cn':'糖霜技巧','ja':'フロスティングの技法','es':'Técnicas de glaseado','pt-br':'Técnicas de cobertura','fr':'Techniques de glaçage','de':'Zuckerguss-Techniken','ru':'Техники глазури','ar':'تقنيات التزيين بالكريمة','hi':'फ्रॉस्टिंग तकनीक','id':'Teknik frosting','vi':'Kỹ thuật phủ kem'
  }
}

# Step header localization
STEP_RE = re.compile(r'\bStep\s+(\d+)\s*:', re.IGNORECASE)
STEP_FMT = {
  'zh-cn': lambda n: f'步骤 {n}：',
  'ja': lambda n: f'手順 {n}:',
  'es': lambda n: f'Paso {n}:',
  'pt-br': lambda n: f'Passo {n}:',
  'fr': lambda n: f'Étape {n} :',
  'de': lambda n: f'Schritt {n}:',
  'ru': lambda n: f'Шаг {n}:',
  'ar': lambda n: f'الخطوة {n}:',
  'hi': lambda n: f'चरण {n}:',
  'id': lambda n: f'Langkah {n}:',
  'vi': lambda n: f'Bước {n}:'
}

# Mixed Chinese + English action phrases within titles like "如何在种植花园中 grow apples - 完整指南"
TITLE_ACTIONS = {
  'zh-cn': {
    'grow apples':'种苹果','grow berries':'种浆果','grow carrots':'种胡萝卜','grow corn':'种玉米','grow wheat':'种小麦','grow oranges':'种橙子',
    'build farm':'建农场',
    'make bread':'做面包','make cake':'做蛋糕','make cookies':'做饼干','make donut':'做甜甜圈','make pie':'做馅饼'
  },
  'ja': {
    'grow apples':'リンゴを育てる','grow berries':'ベリーを育てる','grow carrots':'ニンジンを育てる','grow corn':'トウモロコシを育てる','grow wheat':'小麦を育てる','grow oranges':'オレンジを育てる',
    'build farm':'農場を作る',
    'make bread':'パンを作る','make cake':'ケーキを作る','make cookies':'クッキーを作る','make donut':'ドーナツを作る','make pie':'パイを作る'
  },
  'es': {
    'grow apples':'cultivar manzanas','grow berries':'cultivar bayas','grow carrots':'cultivar zanahorias','grow corn':'cultivar maíz','grow wheat':'cultivar trigo','grow oranges':'cultivar naranjas',
    'build farm':'construir granja',
    'make bread':'hacer pan','make cake':'hacer pastel','make cookies':'hacer galletas','make donut':'hacer rosquilla','make pie':'hacer tarta'
  },
  'pt-br': {
    'grow apples':'cultivar maçãs','grow berries':'cultivar frutas vermelhas','grow carrots':'cultivar cenouras','grow corn':'cultivar milho','grow wheat':'cultivar trigo','grow oranges':'cultivar laranjas',
    'build farm':'construir fazenda',
    'make bread':'fazer pão','make cake':'fazer bolo','make cookies':'fazer biscoitos','make donut':'fazer rosquinha','make pie':'fazer torta'
  },
  'fr': {
    'grow apples':'cultiver des pommes','grow berries':'cultiver des baies','grow carrots':'cultiver des carottes','grow corn':'cultiver du maïs','grow wheat':'cultiver du blé','grow oranges':'cultiver des oranges',
    'build farm':'construire une ferme',
    'make bread':'faire du pain','make cake':'faire un gâteau','make cookies':'faire des biscuits','make donut':'faire des beignets','make pie':'faire une tarte'
  },
  'de': {
    'grow apples':'Äpfel anbauen','grow berries':'Beeren anbauen','grow carrots':'Karotten anbauen','grow corn':'Mais anbauen','grow wheat':'Weizen anbauen','grow oranges':'Orangen anbauen',
    'build farm':'Bauernhof bauen',
    'make bread':'Brot backen','make cake':'Kuchen backen','make cookies':'Kekse backen','make donut':'Donuts backen','make pie':'Torte backen'
  },
  'ru': {
    'grow apples':'выращивать яблоки','grow berries':'выращивать ягоды','grow carrots':'выращивать морковь','grow corn':'выращивать кукурузу','grow wheat':'выращивать пшеницу','grow oranges':'выращивать апельсины',
    'build farm':'строить ферму',
    'make bread':'делать хлеб','make cake':'делать торт','make cookies':'делать печенье','make donut':'делать пончик','make pie':'делать пирог'
  },
  'ar': {
    'grow apples':'زراعة التفاح','grow berries':'زراعة التوت','grow carrots':'زراعة الجزر','grow corn':'زراعة الذرة','grow wheat':'زراعة القمح','grow oranges':'زراعة البرتقال',
    'build farm':'بناء مزرعة',
    'make bread':'صنع الخبز','make cake':'صنع الكعك','make cookies':'صنع البسكويت','make donut':'صنع الدونات','make pie':'صنع الفطيرة'
  },
  'hi': {
    'grow apples':'सेब उगाना','grow berries':'बेरी उगाना','grow carrots':'गाजर उगाना','grow corn':'मक्का उगाना','grow wheat':'गेहूं उगाना','grow oranges':'संतरे उगाना',
    'build farm':'खेत बनाना',
    'make bread':'ब्रेड बनाना','make cake':'केक बनाना','make cookies':'कुकीज़ बनाना','make donut':'डोनट बनाना','make pie':'पाई बनाना'
  },
  'id': {
    'grow apples':'menanam apel','grow berries':'menanam beri','grow carrots':'menanam wortel','grow corn':'menanam jagung','grow wheat':'menanam gandum','grow oranges':'menanam jeruk',
    'build farm':'membangun kebun',
    'make bread':'membuat roti','make cake':'membuat kue','make cookies':'membuat kue kering','make donut':'membuat donat','make pie':'membuat pai'
  },
  'vi': {
    'grow apples':'trồng táo','grow berries':'trồng dâu','grow carrots':'trồng cà rốt','grow corn':'trồng ngô','grow wheat':'trồng lúa mì','grow oranges':'trồng cam',
    'build farm':'xây trang trại',
    'make bread':'làm bánh mì','make cake':'làm bánh kem','make cookies':'làm bánh quy','make donut':'làm bánh donut','make pie':'làm bánh pie'
  }
}

ZH_MIXED_TITLE_RE = re.compile(r'(如何在种植花园中)\s+([A-Za-z ]+)(\s*-\s*完整指南)', re.IGNORECASE)

# Small word replacements frequently mixed into CJK text
SMALL_WORDS = {
  'zh-cn': {
    'Types':'类型','Tricks':'技巧'
  },
  'ja': {
    'Types':'種類','Tricks':'コツ'
  }
}

def apply_common_labels(text: str, lang: str) -> str:
  for en, lang_map in COMMON_LABELS.items():
    tr = lang_map.get(lang)
    if tr:
      text = text.replace(en, tr)
  # Step headers
  def _step_sub(m):
    n = m.group(1)
    fmt = STEP_FMT.get(lang)
    return fmt(n) if fmt else m.group(0)
  text = STEP_RE.sub(_step_sub, text)
  # Small words
  for en, tr in SMALL_WORDS.get(lang, {}).items():
    text = re.sub(rf'\b{re.escape(en)}\b', tr, text)
  return text


def apply_mixed_title(text: str, lang: str) -> str:
  if lang in ('zh-cn','ja'):
    def _sub(m):
      prefix, phrase, suffix = m.group(1), m.group(2).strip().lower(), m.group(3)
      mapping = TITLE_ACTIONS.get(lang, {})
      repl = mapping.get(phrase)
      if repl:
        return f"{prefix} {repl}{suffix}"
      return m.group(0)
    text = ZH_MIXED_TITLE_RE.sub(_sub, text)
  # Also replace bare action phrases if they appear elsewhere
  for en_phrase, tr_phrase in TITLE_ACTIONS.get(lang, {}).items():
    text = re.sub(rf'\b{re.escape(en_phrase)}\b', tr_phrase, text, flags=re.IGNORECASE)
  return text


def safe_replace_text(text: str, lang: str) -> str:
  # headings
  for en, tr in HEADINGS.get(lang, {}).items():
    text = text.replace(en, tr)
  # strong labels
  for en, tr in STRONG.get(lang, {}).items():
    text = text.replace(en, tr)
  # difficulty
  for en, tr in DIFF.get(lang, {}).items():
    text = re.sub(rf'\b{re.escape(en)}\b', tr, text)
  # Use:
  text = text.replace('Use:', USE_LABEL.get(lang, 'Use:'))
  # units
  text = MINUTES_RE.sub(MINUTES_FMT.get(lang, lambda m: m.group(0)), text)
  text = COINS_RE.sub(COINS_FMT.get(lang, lambda m: m.group(0)), text)
  # FAQ labels
  q = {'zh-cn':'问：','ja':'Q：','es':'P:','pt-br':'P:','fr':'Q :','de':'F:','ru':'В:','ar':'س:','hi':'प्र:','id':'T:','vi':'H:'}.get(lang)
  a = {'zh-cn':'答：','ja':'A：','es':'R:','pt-br':'R:','fr':'R :','de':'A:','ru':'О:','ar':'ج:','hi':'उ:','id':'J:','vi':'Đ:'}.get(lang)
  if q:
    text = Q_RE.sub(lambda m: (m.group(1) + q), text)
  if a:
    text = A_RE.sub(lambda m: (m.group(1) + a), text)
  # new: common labels & mixed titles
  text = apply_common_labels(text, lang)
  text = apply_mixed_title(text, lang)
  # phrases map replacements (exact matches)
  lang_map = PHRASES.get(lang, {})
  if lang_map:
    for en, tr in lang_map.items():
      if en and tr:
        text = text.replace(en, tr)
  return text


def process_html(content: str, lang: str) -> str:
  # split out script/style blocks to avoid altering them
  blocks = []
  idx = 0
  def _push_literal(s):
    blocks.append(('txt', s))
  for regex in (SCRIPT_RE, STYLE_RE):
    pass
  # Manually walk: replace script/style with placeholders
  placeholders = []
  def _extract(regex, s):
    out = []
    pos = 0
    for m in regex.finditer(s):
      out.append(('txt', s[pos:m.start()]))
      ph = f"__PLACEHOLDER_{len(placeholders)}__"
      placeholders.append(m.group(0))
      out.append(('ph', ph))
      pos = m.end()
    out.append(('txt', s[pos:]))
    return out
  segs = _extract(SCRIPT_RE, content)
  final = []
  for kind, seg in segs:
    if kind == 'ph':
      final.append((kind, seg))
    else:
      for kind2, seg2 in _extract(STYLE_RE, seg):
        final.append((kind2, seg2))
  # process text segments
  processed = []
  for kind, seg in final:
    if kind == 'txt':
      processed.append(safe_replace_text(seg, lang))
    else:
      processed.append(seg)
  # restore placeholders
  result = ''.join(processed)
  for i, block in enumerate(placeholders):
    result = result.replace(f"__PLACEHOLDER_{i}__", block)
  return result


def ensure_backup(fp: str):
  dst = os.path.join(BACKUP_DIR, os.path.relpath(os.path.dirname(fp), ROOT))
  os.makedirs(dst, exist_ok=True)
  shutil.copy2(fp, os.path.join(dst, os.path.basename(fp)))


def main():
  os.makedirs(BACKUP_DIR, exist_ok=True)
  changed = 0
  checked = 0
  for lang in LANG_DIRS:
    d = os.path.join(ROOT, lang)
    if not os.path.isdir(d):
      continue
    for fn in os.listdir(d):
      if not fn.lower().endswith('.html'): continue
      fp = os.path.join(d, fn)
      try:
        with open(fp, 'r', encoding='utf-8') as f:
          s = f.read()
        new_s = process_html(s, lang)
        checked += 1
        if new_s != s:
          ensure_backup(fp)
          with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_s)
          changed += 1
      except Exception as e:
        print('ERR', fp, e)
  print(f'Batch localized. Checked {checked} files, modified {changed}. Backups: {BACKUP_DIR}')

if __name__ == '__main__':
  main() 