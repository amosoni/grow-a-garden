#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, shutil, time

ROOT = os.path.abspath(os.path.dirname(__file__)).rsplit(os.sep, 1)[0]
BACKUP_DIR = os.path.join(ROOT, 'backups', f'flag_switcher_{time.strftime("%Y%m%d_%H%M%S")}')

FLAG_JS = os.path.join(ROOT, 'flag-switcher.js')
STYLES_CSS = os.path.join(ROOT, 'styles.css')

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def backup_files():
    ensure_dir(BACKUP_DIR)
    for f in [FLAG_JS, STYLES_CSS]:
        if os.path.exists(f):
            shutil.copy2(f, os.path.join(BACKUP_DIR, os.path.basename(f)))

SCRIPT_TAG_RE = re.compile(r'<script\s+src=["\"](\.\./)?flag-switcher\.js["\"][^>]*></script>', re.IGNORECASE)

def compute_script_path(html_path: str) -> str:
    # root level uses 'flag-switcher.js', subfolders use '../flag-switcher.js'
    rel = os.path.relpath(os.path.dirname(html_path), ROOT)
    if rel == '.' or rel == '':
        return 'flag-switcher.js'
    return '../flag-switcher.js'

def apply_to_html():
    changed = 0
    for dirpath, _, filenames in os.walk(ROOT):
        # skip backups, node_modules, .git
        if any(x in dirpath for x in (os.sep+'backups', os.sep+'node_modules', os.sep+'.git')):
            continue
        for fn in filenames:
            if not fn.lower().endswith('.html'): continue
            fp = os.path.join(dirpath, fn)
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                if SCRIPT_TAG_RE.search(content):
                    continue  # already has
                # insert before </body>
                script_path = compute_script_path(fp)
                tag = f'\n    <script src="{script_path}"></script>'
                if '</body>' in content.lower():
                    # find last occurrence case-insensitively
                    idx = content.lower().rfind('</body>')
                    new = content[:idx] + tag + content[idx:]
                else:
                    new = content + tag + '\n'
                # backup original file
                dst_dir = os.path.join(BACKUP_DIR, os.path.relpath(dirpath, ROOT))
                ensure_dir(dst_dir)
                shutil.copy2(fp, os.path.join(dst_dir, fn))
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new)
                changed += 1
            except Exception as e:
                print('Failed', fp, e)
    print(f'Applied to {changed} HTML files. Backups in {BACKUP_DIR}')

if __name__ == '__main__':
    backup_files()
    apply_to_html() 