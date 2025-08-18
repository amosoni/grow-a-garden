#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, re, time, shutil

ROOT = os.path.abspath(os.path.dirname(__file__)).rsplit(os.sep, 1)[0]
I18N_DIR = os.path.join(ROOT, 'i18n')
BACKUP_DIR = os.path.join(ROOT, 'backups', f'fix_nav_keys_{time.strftime("%Y%m%d_%H%M%S")}')
NAV_KEYS = ['nav.logo','nav.live','nav.map','nav.tips','nav.guides','nav.discord']
PLACEHOLDER = re.compile(r'^\s*\[.+\]\s*$')

# 基础英文
EN = {
  'nav.logo': '🌱 Grow a Garden',
  'nav.live': 'Live Stats',
  'nav.map': 'Global Heatmap',
  'nav.tips': 'Tips',
  'nav.guides': '📚 Guides',
  'nav.discord': '💬 Discord',
}

# 其它语言翻译（如缺失则回退 EN）
TRANSLATIONS = {
  'zh-cn': {
    'nav.logo': '🌱 种植花园','nav.live': '实时数据','nav.map': '全球热力图','nav.tips': '小技巧','nav.guides': '📚 攻略','nav.discord': '💬 交流'
  },
  'ja': {
    'nav.logo': '🌱 Grow a Garden','nav.live': 'ライブ統計','nav.map': 'グローバルヒートマップ','nav.tips': 'ヒント','nav.guides': '📚 ガイド','nav.discord': '💬 Discord'
  },
  'fr': {
    'nav.logo': '🌱 Grow a Garden','nav.live': 'Statistiques en Direct','nav.map': 'Carte de Chaleur Globale','nav.tips': 'Conseils','nav.guides': '📚 Guides','nav.discord': '💬 Discord'
  },
  'de': {
    'nav.logo': '🌱 Grow a Garden','nav.live': 'Live-Statistiken','nav.map': 'Globale Wärmekarte','nav.tips': 'Tipps','nav.guides': '📚 Anleitungen','nav.discord': '💬 Discord'
  },
  'es': {
    'nav.logo': '🌱 Grow a Garden','nav.live': 'Estadísticas en Vivo','nav.map': 'Mapa de Calor Global','nav.tips': 'Consejos','nav.guides': '📚 Guías','nav.discord': '💬 Discord'
  },
  'pt-br': {
    'nav.logo': '🌱 Grow a Garden','nav.live': 'Estatísticas ao Vivo','nav.map': 'Mapa de Calor Global','nav.tips': 'Dicas','nav.guides': '📚 Guias','nav.discord': '💬 Discord'
  },
  'ru': {
    'nav.logo': '🌱 Grow a Garden','nav.live': 'Живая статистика','nav.map': 'Глобальная тепловая карта','nav.tips': 'Советы','nav.guides': '📚 Руководства','nav.discord': '💬 Discord'
  },
  'ar': {
    'nav.logo': '🌱 Grow a Garden','nav.live': 'إحصائيات مباشرة','nav.map': 'خريطة حرارية عالمية','nav.tips': 'نصائح','nav.guides': '📚 أدلة','nav.discord': '💬 Discord'
  },
  'hi': {
    'nav.logo': '🌱 Grow a Garden','nav.live': 'लाइव आंकड़े','nav.map': 'वैश्विक हीटमैप','nav.tips': 'सुझाव','nav.guides': '📚 गाइड्स','nav.discord': '💬 Discord'
  },
  'id': {
    'nav.logo': '🌱 Grow a Garden','nav.live': 'Statistik Langsung','nav.map': 'Peta Panas Global','nav.tips': 'Tips','nav.guides': '📚 Panduan','nav.discord': '💬 Discord'
  },
  'vi': {
    'nav.logo': '🌱 Grow a Garden','nav.live': 'Thống Kê Trực Tiếp','nav.map': 'Bản Đồ Nhiệt Toàn Cầu','nav.tips': 'Mẹo','nav.guides': '📚 Hướng Dẫn','nav.discord': '💬 Discord'
  },
  'en': EN,
}


def ensure_dir(p): os.makedirs(p, exist_ok=True)

def backup(path):
    dst = os.path.join(BACKUP_DIR, os.path.relpath(path, ROOT))
    ensure_dir(os.path.dirname(dst))
    shutil.copy2(path, dst)


def fix_all():
    ensure_dir(BACKUP_DIR)
    fixed_files = 0
    for fn in os.listdir(I18N_DIR):
        if not fn.endswith('.json'): continue
        lang = os.path.splitext(fn)[0].lower()
        path = os.path.join(I18N_DIR, fn)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print('Skip', fn, e)
            continue
        changed = False
        trans = TRANSLATIONS.get(lang, EN)
        for k in NAV_KEYS:
            val = data.get(k)
            if val is None or PLACEHOLDER.match(str(val)):
                data[k] = trans.get(k, EN[k])
                changed = True
        if changed:
            backup(path)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            fixed_files += 1
    print('nav keys fixed in', fixed_files, 'files. Backups at', BACKUP_DIR)

if __name__ == '__main__':
    fix_all() 