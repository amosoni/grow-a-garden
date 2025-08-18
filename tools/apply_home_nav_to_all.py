#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, shutil, time

ROOT = os.path.abspath(os.path.dirname(__file__)).rsplit(os.sep, 1)[0]
BACKUP_DIR = os.path.join(ROOT, 'backups', f'nav_apply_{time.strftime("%Y%m%d_%H%M%S")}')

INDEX_HTML = os.path.join(ROOT, 'index.html')

HEADER_RE = re.compile(r'<header[\s\S]*?</header>', re.IGNORECASE)
BODY_OPEN_RE = re.compile(r'<body[^>]*>', re.IGNORECASE)


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)


def read_file(p):
    with open(p, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(p, content):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)


def extract_home_header():
    html = read_file(INDEX_HTML)
    m = HEADER_RE.search(html)
    if not m:
        raise RuntimeError('No <header> found in root index.html')
    return m.group(0)


def apply_nav(header_html):
    changed = 0
    ensure_dir(BACKUP_DIR)
    for dirpath, _, filenames in os.walk(ROOT):
        if any(skip in dirpath for skip in (os.sep+'backups', os.sep+'.git', os.sep+'node_modules')):
            continue
        for fn in filenames:
            if not fn.lower().endswith('.html'): continue
            fp = os.path.join(dirpath, fn)
            if os.path.abspath(fp) == os.path.abspath(INDEX_HTML):
                continue
            try:
                content = read_file(fp)
                new_content = content
                if HEADER_RE.search(content):
                    new_content = HEADER_RE.sub(header_html, content, count=1)
                else:
                    m = BODY_OPEN_RE.search(content)
                    if m:
                        insert_at = m.end()
                        new_content = content[:insert_at] + '\n' + header_html + '\n' + content[insert_at:]
                    else:
                        # fallback: prepend
                        new_content = header_html + '\n' + content
                if new_content != content:
                    # backup original
                    dst_dir = os.path.join(BACKUP_DIR, os.path.relpath(dirpath, ROOT))
                    ensure_dir(dst_dir)
                    shutil.copy2(fp, os.path.join(dst_dir, fn))
                    write_file(fp, new_content)
                    changed += 1
            except Exception as e:
                print('Failed', fp, e)
    print(f'Unified nav applied to {changed} files. Backups at {BACKUP_DIR}')


def main():
    header = extract_home_header()
    apply_nav(header)

if __name__ == '__main__':
    main() 