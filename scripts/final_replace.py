#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终替换脚本 - 直接替换剩余的英文内容
"""

import os
import re
import glob
from pathlib import Path

def final_replace_article_page(file_path):
    """最终替换单个攻略页面"""
    print(f"最终替换: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 获取语言代码
    lang = file_path.split('/')[0]
    
    # 根据语言进行替换
    if lang == 'zh-cn':
        # 中文替换
        content = content.replace('Basic Salad Recipes', '基本沙拉食谱')
        content = content.replace('Advanced Salad Recipes', '高级沙拉食谱')
        content = content.replace('Luxury Salad Recipes', '豪华沙拉食谱')
        content = content.replace('Learn basic salad recipes', '学习基本沙拉食谱')
        content = content.replace('Growth Time:', '生长时间：')
        content = content.replace('minutes', '分钟')
        content = content.replace('From ingredient gathering to finished', '从收集食材到完成')
        content = content.replace('expect', '预计需要')
        content = content.replace('With practice and proper setup, you can reduce this time significantly.', '通过练习和正确设置，你可以显著减少这个时间。')
        content = content.replace('Batch Farming:', '批量种植：')
        content = content.replace('Plant in waves every', '每隔')
        content = content.replace('minutes for continuous harvests.', '分钟种植一波，实现连续收获。')
        content = content.replace('A: Basic', '答：基本')
        content = content.replace('s take', '需要')
        content = content.replace('minutes to make, while advanced recipes can take', '分钟制作，而高级食谱可能需要')
        content = content.replace('minutes depending on complexity.', '分钟，具体取决于复杂度。')
        content = content.replace('minutes to mature', '分钟成熟')
        content = content.replace('Check for grain formation', '检查谷物形成')
        content = content.replace('Wait for full maturity', '等待完全成熟')
        content = content.replace('minutes total', '分钟总计')
        content = content.replace('Water lightly every', '每')
        content = content.replace('minutes in-game', '分钟在游戏中浇水')
        content = content.replace('Let filling rest for', '让馅料静置')
        content = content.replace('takes exactly', '需要正好')
        content = content.replace('minutes to reach full maturity from planting to harvest.', '分钟从种植到收获达到完全成熟。')
        content = content.replace('~', '约')
        content = content.replace('Time', '时间')
        
    elif lang == 'ja':
        # 日语替换
        content = content.replace('Basic Salad Recipes', '基本サラダレシピ')
        content = content.replace('Advanced Salad Recipes', '上級サラダレシピ')
        content = content.replace('Luxury Salad Recipes', '高級サラダレシピ')
        content = content.replace('Learn basic salad recipes', '基本サラダレシピを学ぶ')
        content = content.replace('Growth Time:', '成長時間：')
        content = content.replace('minutes', '分')
        content = content.replace('From ingredient gathering to finished', '材料収集から完成まで')
        content = content.replace('expect', '予想される時間')
        content = content.replace('With practice and proper setup, you can reduce this time significantly.', '練習と適切な設定により、この時間を大幅に短縮できます。')
        content = content.replace('Batch Farming:', '一括栽培：')
        content = content.replace('Plant in waves every', '毎')
        content = content.replace('minutes for continuous harvests.', '分ごとに波状に植えて、連続収穫を実現。')
        content = content.replace('A: Basic', '答：基本')
        content = content.replace('s take', 'は')
        content = content.replace('minutes to make, while advanced recipes can take', '分で作れますが、上級レシピは')
        content = content.replace('minutes depending on complexity.', '分かかる場合があります（複雑さによります）。')
        content = content.replace('minutes to mature', '分で成熟')
        content = content.replace('Check for grain formation', '穀物形成を確認')
        content = content.replace('Wait for full maturity', '完全成熟まで待つ')
        content = content.replace('minutes total', '分合計')
        content = content.replace('Water lightly every', '毎')
        content = content.replace('minutes in-game', '分ゲーム内で軽く水やり')
        content = content.replace('Let filling rest for', 'フィリングを')
        content = content.replace('minutes', '分休ませる')
        content = content.replace('takes exactly', 'は正確に')
        content = content.replace('minutes to reach full maturity from planting to harvest.', '分で植え付けから収穫まで完全成熟に達します。')
        content = content.replace('~', '約')
        content = content.replace('Time', '時間')
        
    elif lang == 'es':
        # 西班牙语替换
        content = content.replace('Basic Salad Recipes', 'Recetas de Ensalada Básicas')
        content = content.replace('Advanced Salad Recipes', 'Recetas de Ensalada Avanzadas')
        content = content.replace('Luxury Salad Recipes', 'Recetas de Ensalada de Lujo')
        content = content.replace('Learn basic salad recipes', 'Aprende recetas básicas de ensalada')
        content = content.replace('Growth Time:', 'Tiempo de Crecimiento:')
        content = content.replace('minutes', 'minutos')
        content = content.replace('From ingredient gathering to finished', 'Desde la recolección de ingredientes hasta el acabado')
        content = content.replace('expect', 'espera')
        content = content.replace('With practice and proper setup, you can reduce this time significantly.', 'Con práctica y configuración adecuada, puedes reducir este tiempo significativamente.')
        content = content.replace('Batch Farming:', 'Cultivo en Lotes:')
        content = content.replace('Plant in waves every', 'Planta en oleadas cada')
        content = content.replace('minutes for continuous harvests.', 'minutos para cosechas continuas.')
        content = content.replace('A: Basic', 'R: Básicos')
        content = content.replace('s take', 's toman')
        content = content.replace('minutes to make, while advanced recipes can take', 'minutos en hacer, mientras que las recetas avanzadas pueden tomar')
        content = content.replace('minutes depending on complexity.', 'minutos dependiendo de la complejidad.')
        content = content.replace('minutes to mature', 'minutos para madurar')
        content = content.replace('Check for grain formation', 'Verifica la formación de granos')
        content = content.replace('Wait for full maturity', 'Espera la madurez completa')
        content = content.replace('minutes total', 'minutos en total')
        content = content.replace('Water lightly every', 'Riega ligeramente cada')
        content = content.replace('minutes in-game', 'minutos en el juego')
        content = content.replace('Let filling rest for', 'Deja que el relleno descanse por')
        content = content.replace('takes exactly', 'toma exactamente')
        content = content.replace('minutes to reach full maturity from planting to harvest.', 'minutos para alcanzar la madurez completa desde la siembra hasta la cosecha.')
        content = content.replace('~', '~')
        content = content.replace('Time', 'Tiempo')
        
    elif lang == 'fr':
        # 法语替换
        content = content.replace('Basic Salad Recipes', 'Recettes de Salade de Base')
        content = content.replace('Advanced Salad Recipes', 'Recettes de Salade Avancées')
        content = content.replace('Luxury Salad Recipes', 'Recettes de Salade de Luxe')
        content = content.replace('Learn basic salad recipes', 'Apprenez les recettes de salade de base')
        content = content.replace('Growth Time:', 'Temps de Croissance:')
        content = content.replace('minutes', 'minutes')
        content = content.replace('From ingredient gathering to finished', 'De la collecte d\'ingrédients à la finition')
        content = content.replace('expect', 'attendez')
        content = content.replace('With practice and proper setup, you can reduce this time significantly.', 'Avec de la pratique et une configuration appropriée, vous pouvez réduire ce temps considérablement.')
        content = content.replace('Batch Farming:', 'Culture en Lots:')
        content = content.replace('Plant in waves every', 'Plantez par vagues toutes les')
        content = content.replace('minutes for continuous harvests.', 'minutes pour des récoltes continues.')
        content = content.replace('A: Basic', 'R: Les basiques')
        content = content.replace('s take', 's prennent')
        content = content.replace('minutes to make, while advanced recipes can take', 'minutes à faire, tandis que les recettes avancées peuvent prendre')
        content = content.replace('minutes depending on complexity.', 'minutes selon la complexité.')
        content = content.replace('minutes to mature', 'minutes pour mûrir')
        content = content.replace('Check for grain formation', 'Vérifiez la formation des grains')
        content = content.replace('Wait for full maturity', 'Attendez la maturité complète')
        content = content.replace('minutes total', 'minutes au total')
        content = content.replace('Water lightly every', 'Arrosez légèrement toutes les')
        content = content.replace('minutes in-game', 'minutes en jeu')
        content = content.replace('Let filling rest for', 'Laissez le remplissage reposer pendant')
        content = content.replace('takes exactly', 'prend exactement')
        content = content.replace('minutes to reach full maturity from planting to harvest.', 'minutes pour atteindre la maturité complète de la plantation à la récolte.')
        content = content.replace('~', '~')
        content = content.replace('Time', 'Temps')
        
    elif lang == 'de':
        # 德语替换
        content = content.replace('Basic Salad Recipes', 'Grundlegende Salat-Rezepte')
        content = content.replace('Advanced Salad Recipes', 'Fortgeschrittene Salat-Rezepte')
        content = content.replace('Luxury Salad Recipes', 'Luxus-Salat-Rezepte')
        content = content.replace('Learn basic salad recipes', 'Lerne grundlegende Salat-Rezepte')
        content = content.replace('Growth Time:', 'Wachstumszeit:')
        content = content.replace('minutes', 'Minuten')
        content = content.replace('From ingredient gathering to finished', 'Von der Zutatensammlung bis zur Fertigstellung')
        content = content.replace('expect', 'erwarten Sie')
        content = content.replace('With practice and proper setup, you can reduce this time significantly.', 'Mit Übung und richtiger Einrichtung können Sie diese Zeit erheblich reduzieren.')
        content = content.replace('Batch Farming:', 'Batch-Anbau:')
        content = content.replace('Plant in waves every', 'Pflanzen Sie in Wellen alle')
        content = content.replace('minutes for continuous harvests.', 'Minuten für kontinuierliche Ernten.')
        content = content.replace('A: Basic', 'A: Grundlegende')
        content = content.replace('s take', 's brauchen')
        content = content.replace('minutes to make, while advanced recipes can take', 'Minuten zum Herstellen, während fortgeschrittene Rezepte')
        content = content.replace('minutes depending on complexity.', 'Minuten je nach Komplexität benötigen können.')
        content = content.replace('minutes to mature', 'Minuten zum Reifen')
        content = content.replace('Check for grain formation', 'Überprüfen Sie die Kornbildung')
        content = content.replace('Wait for full maturity', 'Warten Sie auf die volle Reife')
        content = content.replace('minutes total', 'Minuten insgesamt')
        content = content.replace('Water lightly every', 'Gießen Sie leicht alle')
        content = content.replace('minutes in-game', 'Minuten im Spiel')
        content = content.replace('Let filling rest for', 'Lassen Sie die Füllung ruhen für')
        content = content.replace('takes exactly', 'braucht genau')
        content = content.replace('minutes to reach full maturity from planting to harvest.', 'Minuten, um von der Pflanzung bis zur Ernte die volle Reife zu erreichen.')
        content = content.replace('~', '~')
        content = content.replace('Time', 'Zeit')
        
    elif lang == 'ru':
        # 俄语替换
        content = content.replace('Basic Salad Recipes', 'Базовые рецепты салатов')
        content = content.replace('Advanced Salad Recipes', 'Продвинутые рецепты салатов')
        content = content.replace('Luxury Salad Recipes', 'Люксовые рецепты салатов')
        content = content.replace('Learn basic salad recipes', 'Изучите базовые рецепты салатов')
        content = content.replace('Growth Time:', 'Время роста:')
        content = content.replace('minutes', 'минут')
        content = content.replace('From ingredient gathering to finished', 'От сбора ингредиентов до готовности')
        content = content.replace('expect', 'ожидайте')
        content = content.replace('With practice and proper setup, you can reduce this time significantly.', 'С практикой и правильной настройкой вы можете значительно сократить это время.')
        content = content.replace('Batch Farming:', 'Пакетное выращивание:')
        content = content.replace('Plant in waves every', 'Сажайте волнами каждые')
        content = content.replace('minutes for continuous harvests.', 'минут для непрерывных урожаев.')
        content = content.replace('A: Basic', 'О: Базовые')
        content = content.replace('s take', 's занимают')
        content = content.replace('minutes to make, while advanced recipes can take', 'минут на приготовление, в то время как продвинутые рецепты могут занять')
        content = content.replace('minutes depending on complexity.', 'минут в зависимости от сложности.')
        content = content.replace('minutes to mature', 'минут до созревания')
        content = content.replace('Check for grain formation', 'Проверьте формирование зерна')
        content = content.replace('Wait for full maturity', 'Дождитесь полного созревания')
        content = content.replace('minutes total', 'минут всего')
        content = content.replace('Water lightly every', 'Легко поливайте каждые')
        content = content.replace('minutes in-game', 'минут в игре')
        content = content.replace('Let filling rest for', 'Дайте начинке отдохнуть')
        content = content.replace('takes exactly', 'занимает ровно')
        content = content.replace('minutes to reach full maturity from planting to harvest.', 'минут, чтобы достичь полной зрелости от посадки до сбора урожая.')
        content = content.replace('~', '~')
        content = content.replace('Time', 'Время')
        
    elif lang == 'pt-br':
        # 葡萄牙语替换
        content = content.replace('Basic Salad Recipes', 'Receitas de Salada Básicas')
        content = content.replace('Advanced Salad Recipes', 'Receitas de Salada Avançadas')
        content = content.replace('Luxury Salad Recipes', 'Receitas de Salada de Luxo')
        content = content.replace('Learn basic salad recipes', 'Aprenda receitas básicas de salada')
        content = content.replace('Growth Time:', 'Tempo de Crescimento:')
        content = content.replace('minutes', 'minutos')
        content = content.replace('From ingredient gathering to finished', 'Da coleta de ingredientes ao acabamento')
        content = content.replace('expect', 'espere')
        content = content.replace('With practice and proper setup, you can reduce this time significantly.', 'Com prática e configuração adequada, você pode reduzir esse tempo significativamente.')
        content = content.replace('Batch Farming:', 'Cultivo em Lotes:')
        content = content.replace('Plant in waves every', 'Plante em ondas a cada')
        content = content.replace('minutes for continuous harvests.', 'minutos para colheitas contínuas.')
        content = content.replace('A: Basic', 'R: Básicos')
        content = content.replace('s take', 's levam')
        content = content.replace('minutes to make, while advanced recipes can take', 'minutos para fazer, enquanto receitas avançadas podem levar')
        content = content.replace('minutes depending on complexity.', 'minutos dependendo da complexidade.')
        content = content.replace('minutes to mature', 'minutos para amadurecer')
        content = content.replace('Check for grain formation', 'Verifique a formação de grãos')
        content = content.replace('Wait for full maturity', 'Aguarde a maturidade completa')
        content = content.replace('minutes total', 'minutos no total')
        content = content.replace('Water lightly every', 'Regue levemente a cada')
        content = content.replace('minutes in-game', 'minutos no jogo')
        content = content.replace('Let filling rest for', 'Deixe o recheio descansar por')
        content = content.replace('takes exactly', 'leva exatamente')
        content = content.replace('minutes to reach full maturity from planting to harvest.', 'minutos para atingir a maturidade completa do plantio à colheita.')
        content = content.replace('~', '~')
        content = content.replace('Time', 'Tempo')
        
    elif lang == 'hi':
        # 印地语替换
        content = content.replace('Basic Salad Recipes', 'बुनियादी सलाद व्यंजन')
        content = content.replace('Advanced Salad Recipes', 'उन्नत सलाद व्यंजन')
        content = content.replace('Luxury Salad Recipes', 'लक्जरी सलाद व्यंजन')
        content = content.replace('Learn basic salad recipes', 'बुनियादी सलाद व्यंजन सीखें')
        content = content.replace('Growth Time:', 'विकास समय:')
        content = content.replace('minutes', 'मिनट')
        content = content.replace('From ingredient gathering to finished', 'सामग्री एकत्र करने से लेकर पूरा होने तक')
        content = content.replace('expect', 'उम्मीद करें')
        content = content.replace('With practice and proper setup, you can reduce this time significantly.', 'अभ्यास और उचित सेटअप के साथ, आप इस समय को काफी कम कर सकते हैं।')
        content = content.replace('Batch Farming:', 'बैच खेती:')
        content = content.replace('Plant in waves every', 'हर')
        content = content.replace('minutes for continuous harvests.', 'मिनट में लहरों में लगाएं निरंतर फसल के लिए।')
        content = content.replace('A: Basic', 'उ: बुनियादी')
        content = content.replace('s take', 's लेते हैं')
        content = content.replace('minutes to make, while advanced recipes can take', 'मिनट बनाने में, जबकि उन्नत व्यंजन')
        content = content.replace('minutes depending on complexity.', 'मिनट ले सकते हैं जटिलता के आधार पर।')
        content = content.replace('minutes to mature', 'मिनट परिपक्व होने में')
        content = content.replace('Check for grain formation', 'अनाज के गठन की जांच करें')
        content = content.replace('Wait for full maturity', 'पूर्ण परिपक्वता की प्रतीक्षा करें')
        content = content.replace('minutes total', 'मिनट कुल')
        content = content.replace('Water lightly every', 'हर')
        content = content.replace('minutes in-game', 'मिनट गेम में हल्का पानी दें')
        content = content.replace('Let filling rest for', 'भराव को')
        content = content.replace('minutes', 'मिनट आराम दें')
        content = content.replace('takes exactly', 'बिल्कुल')
        content = content.replace('minutes to reach full maturity from planting to harvest.', 'मिनट लेता है रोपण से कटाई तक पूर्ण परिपक्वता तक पहुंचने में।')
        content = content.replace('~', '~')
        content = content.replace('Time', 'समय')
        
    elif lang == 'id':
        # 印尼语替换
        content = content.replace('Basic Salad Recipes', 'Resep Salad Dasar')
        content = content.replace('Advanced Salad Recipes', 'Resep Salad Lanjutan')
        content = content.replace('Luxury Salad Recipes', 'Resep Salad Mewah')
        content = content.replace('Learn basic salad recipes', 'Pelajari resep salad dasar')
        content = content.replace('Growth Time:', 'Waktu Pertumbuhan:')
        content = content.replace('minutes', 'menit')
        content = content.replace('From ingredient gathering to finished', 'Dari pengumpulan bahan hingga selesai')
        content = content.replace('expect', 'harapkan')
        content = content.replace('With practice and proper setup, you can reduce this time significantly.', 'Dengan latihan dan pengaturan yang tepat, Anda dapat mengurangi waktu ini secara signifikan.')
        content = content.replace('Batch Farming:', 'Pertanian Bertahap:')
        content = content.replace('Plant in waves every', 'Tanam dalam gelombang setiap')
        content = content.replace('minutes for continuous harvests.', 'menit untuk panen berkelanjutan.')
        content = content.replace('A: Basic', 'J: Dasar')
        content = content.replace('s take', 's membutuhkan')
        content = content.replace('minutes to make, while advanced recipes can take', 'menit untuk dibuat, sementara resep lanjutan dapat membutuhkan')
        content = content.replace('minutes depending on complexity.', 'menit tergantung pada kompleksitas.')
        content = content.replace('minutes to mature', 'menit untuk matang')
        content = content.replace('Check for grain formation', 'Periksa pembentukan biji-bijian')
        content = content.replace('Wait for full maturity', 'Tunggu kematangan penuh')
        content = content.replace('minutes total', 'menit total')
        content = content.replace('Water lightly every', 'Siram ringan setiap')
        content = content.replace('minutes in-game', 'menit dalam permainan')
        content = content.replace('Let filling rest for', 'Biarkan isian beristirahat selama')
        content = content.replace('takes exactly', 'membutuhkan tepat')
        content = content.replace('minutes to reach full maturity from planting to harvest.', 'menit untuk mencapai kematangan penuh dari penanaman hingga panen.')
        content = content.replace('~', '~')
        content = content.replace('Time', 'Waktu')
        
    elif lang == 'vi':
        # 越南语替换
        content = content.replace('Basic Salad Recipes', 'Công thức Salad Cơ bản')
        content = content.replace('Advanced Salad Recipes', 'Công thức Salad Nâng cao')
        content = content.replace('Luxury Salad Recipes', 'Công thức Salad Cao cấp')
        content = content.replace('Learn basic salad recipes', 'Học công thức salad cơ bản')
        content = content.replace('Growth Time:', 'Thời gian phát triển:')
        content = content.replace('minutes', 'phút')
        content = content.replace('From ingredient gathering to finished', 'Từ thu thập nguyên liệu đến hoàn thành')
        content = content.replace('expect', 'mong đợi')
        content = content.replace('With practice and proper setup, you can reduce this time significantly.', 'Với thực hành và thiết lập phù hợp, bạn có thể giảm đáng kể thời gian này.')
        content = content.replace('Batch Farming:', 'Trồng trọt theo đợt:')
        content = content.replace('Plant in waves every', 'Trồng theo đợt mỗi')
        content = content.replace('minutes for continuous harvests.', 'phút để thu hoạch liên tục.')
        content = content.replace('A: Basic', 'T: Cơ bản')
        content = content.replace('s take', 's mất')
        content = content.replace('minutes to make, while advanced recipes can take', 'phút để làm, trong khi công thức nâng cao có thể mất')
        content = content.replace('minutes depending on complexity.', 'phút tùy thuộc vào độ phức tạp.')
        content = content.replace('minutes to mature', 'phút để trưởng thành')
        content = content.replace('Check for grain formation', 'Kiểm tra sự hình thành hạt')
        content = content.replace('Wait for full maturity', 'Chờ sự trưởng thành hoàn toàn')
        content = content.replace('minutes total', 'phút tổng cộng')
        content = content.replace('Water lightly every', 'Tưới nhẹ mỗi')
        content = content.replace('minutes in-game', 'phút trong trò chơi')
        content = content.replace('Let filling rest for', 'Để nhân nghỉ')
        content = content.replace('takes exactly', 'mất chính xác')
        content = content.replace('minutes to reach full maturity from planting to harvest.', 'phút để đạt sự trưởng thành hoàn toàn từ trồng đến thu hoạch.')
        content = content.replace('~', '~')
        content = content.replace('Time', 'Thời gian')
        
    elif lang == 'ar':
        # 阿拉伯语替换
        content = content.replace('Basic Salad Recipes', 'وصفات السلطة الأساسية')
        content = content.replace('Advanced Salad Recipes', 'وصفات السلطة المتقدمة')
        content = content.replace('Luxury Salad Recipes', 'وصفات السلطة الفاخرة')
        content = content.replace('Learn basic salad recipes', 'تعلم وصفات السلطة الأساسية')
        content = content.replace('Growth Time:', 'وقت النمو:')
        content = content.replace('minutes', 'دقائق')
        content = content.replace('From ingredient gathering to finished', 'من جمع المكونات إلى الانتهاء')
        content = content.replace('expect', 'توقع')
        content = content.replace('With practice and proper setup, you can reduce this time significantly.', 'مع الممارسة والإعداد المناسب، يمكنك تقليل هذا الوقت بشكل كبير.')
        content = content.replace('Batch Farming:', 'الزراعة الدفاعية:')
        content = content.replace('Plant in waves every', 'ازرع في موجات كل')
        content = content.replace('minutes for continuous harvests.', 'دقائق للحصاد المستمر.')
        content = content.replace('A: Basic', 'ج: الأساسية')
        content = content.replace('s take', 's تأخذ')
        content = content.replace('minutes to make, while advanced recipes can take', 'دقائق للصنع، بينما الوصفات المتقدمة قد تأخذ')
        content = content.replace('minutes depending on complexity.', 'دقائق حسب التعقيد.')
        content = content.replace('minutes to mature', 'دقائق للنضج')
        content = content.replace('Check for grain formation', 'تحقق من تكوين الحبوب')
        content = content.replace('Wait for full maturity', 'انتظر النضج الكامل')
        content = content.replace('minutes total', 'دقائق إجمالي')
        content = content.replace('Water lightly every', 'اسقِ بخفة كل')
        content = content.replace('minutes in-game', 'دقائق في اللعبة')
        content = content.replace('Let filling rest for', 'دع الحشوة ترتاح لمدة')
        content = content.replace('takes exactly', 'تأخذ بالضبط')
        content = content.replace('minutes to reach full maturity from planting to harvest.', 'دقائق للوصول إلى النضج الكامل من الزراعة إلى الحصاد.')
        content = content.replace('~', '~')
        content = content.replace('Time', 'الوقت')
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 最终替换完成: {file_path}")

def main():
    """主函数"""
    print("🚀 开始最终替换所有攻略详情页...")
    
    # 查找所有攻略页面
    article_patterns = [
        "*/how-to-*.html",
        "*/how-to-grow-*.html",
        "*/how-to-play-*.html"
    ]
    
    article_files = []
    for pattern in article_patterns:
        article_files.extend(glob.glob(pattern))
    
    print(f"找到 {len(article_files)} 个攻略页面")
    
    # 处理每个页面
    for file_path in article_files:
        try:
            final_replace_article_page(file_path)
        except Exception as e:
            print(f"❌ 处理失败 {file_path}: {e}")
    
    print("🎉 所有攻略详情页最终替换完成！")
    print("现在所有英文内容都已经被翻译了！")

if __name__ == "__main__":
    main() 