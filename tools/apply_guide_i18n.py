#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, time, shutil

ROOT = os.path.abspath(os.path.dirname(__file__)).rsplit(os.sep, 1)[0]
BACKUP_DIR = os.path.join(ROOT, 'backups', f'apply_guide_i18n_{time.strftime("%Y%m%d_%H%M%S")}')
LANG_DIRS = [d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d)) and not d.startswith('.') and d not in ('backups','i18n','node_modules','.git','tools')]

FILE_NAME = 'how-to-make-salad.html'

# patterns
HERO_H1 = re.compile(r'(\<section[^>]*class=["\'][^"\']*salad-hero[^>]*\>.*?<h1)([^>]*)(>)', re.IGNORECASE|re.DOTALL)
HERO_P  = re.compile(r'(\<section[^>]*class=["\'][^"\']*salad-hero[^>]*\>.*?<p)([^>]*)(>)', re.IGNORECASE|re.DOTALL)
BREADCRUMB_CUR = re.compile(r'(<nav[^>]*class=["\']breadcrumb["\'][^>]*>.*?<li[^>]*aria-current=["\']page["\'][^>]*)(>)', re.IGNORECASE|re.DOTALL)

# section id -> key
SECTION_KEYS = {
    'basics'     : 'salad.basics.title',
    'ingredients': 'salad.ingredients.title',
    'recipes'    : 'salad.recipes.title',
    'tips'       : 'salad.tips.title',
    'efficiency' : 'salad.efficiency.title',
    'faq'        : 'salad.faq.title',
    'summary'    : 'salad.summary.title',
}

GUIDE_CARD_H2 = re.compile(r'(\<div[^>]*class=["\']guide-card["\'][^>]*id=["\']([a-z0-9_-]+)["\'][^>]*\>.*?<h2)([^>]*)(>)', re.IGNORECASE|re.DOTALL)


def ensure_dir(p): os.makedirs(p, exist_ok=True)

def backup(path):
    dst = os.path.join(BACKUP_DIR, os.path.relpath(path, ROOT))
    ensure_dir(os.path.dirname(dst))
    shutil.copy2(path, dst)


def inject_i18n(html: str) -> str:
    changed = False
    # hero h1
    def _h1(m):
        nonlocal changed
        attrs = m.group(2)
        if 'data-i18n=' not in attrs:
            changed = True
            return m.group(1) + attrs + ' data-i18n="salad.hero.title"' + m.group(3)
        return m.group(0)
    html2 = HERO_H1.sub(_h1, html, count=1)

    # hero p
    def _p(m):
        nonlocal changed
        attrs = m.group(2)
        if 'data-i18n=' not in attrs:
            changed = True
            return m.group(1) + attrs + ' data-i18n="salad.hero.subtitle"' + m.group(3)
        return m.group(0)
    html2 = HERO_P.sub(_p, html2, count=1)

    # breadcrumb current
    def _bc(m):
        nonlocal changed
        prefix = m.group(1)
        if 'data-i18n=' not in prefix:
            changed = True
            return prefix + ' data-i18n="salad.breadcrumb.current"' + m.group(2)
        return m.group(0)
    html2 = BREADCRUMB_CUR.sub(_bc, html2, count=1)

    # guide-card h2 per section id
    def _h2(m):
        nonlocal changed
        attrs = m.group(3)
        sec_id = m.group(2)
        key = SECTION_KEYS.get(sec_id)
        if key and 'data-i18n=' not in attrs:
            changed = True
            return m.group(1) + attrs + f' data-i18n="{key}"' + m.group(4)
        return m.group(0)
    html2 = GUIDE_CARD_H2.sub(_h2, html2)

    return html2, changed


def main():
    ensure_dir(BACKUP_DIR)
    fixed = 0
    for lang in LANG_DIRS:
        fp = os.path.join(ROOT, lang, FILE_NAME)
        if not os.path.isfile(fp):
            continue
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                s = f.read()
            new_s, changed = inject_i18n(s)
            if changed:
                backup(fp)
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_s)
                fixed += 1
        except Exception as e:
            print('ERR', fp, e)
    print('Applied guide i18n to', fixed, 'files. Backups at', BACKUP_DIR)

if __name__ == '__main__':
    main() 