#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, shutil, time

ROOT = os.path.abspath(os.path.dirname(__file__)).rsplit(os.sep, 1)[0]
BACKUP_DIR = os.path.join(ROOT, 'backups', f'fix_css_{time.strftime("%Y%m%d_%H%M%S")}')

PATTERN = re.compile(r'(\<link\s+rel=["\']stylesheet["\']\s+href=["\'])styles\.css(["\'][^>]*\>)', re.IGNORECASE)


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)


def is_root_html(path: str) -> bool:
    return os.path.dirname(os.path.relpath(path, ROOT)) in ('.', '')


def process():
    ensure_dir(BACKUP_DIR)
    changed = 0
    for dirpath, _, filenames in os.walk(ROOT):
        if any(skip in dirpath for skip in (os.sep+'backups', os.sep+'.git', os.sep+'node_modules')):
            continue
        for fn in filenames:
            if not fn.lower().endswith('.html'): continue
            fp = os.path.join(dirpath, fn)
            if is_root_html(fp):
                continue
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                new = PATTERN.sub(r"\1../styles.css\2", content)
                if new != content:
                    dst_dir = os.path.join(BACKUP_DIR, os.path.relpath(dirpath, ROOT))
                    ensure_dir(dst_dir)
                    shutil.copy2(fp, os.path.join(dst_dir, fn))
                    with open(fp, 'w', encoding='utf-8') as f:
                        f.write(new)
                    changed += 1
            except Exception as e:
                print('Failed', fp, e)
    print(f'Updated CSS paths in {changed} files. Backups at {BACKUP_DIR}')

if __name__ == '__main__':
    process() 