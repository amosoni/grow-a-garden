#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, time, shutil

ROOT = os.path.abspath(os.path.dirname(__file__)).rsplit(os.sep, 1)[0]
BACKUP_DIR = os.path.join(ROOT, 'backups', f'guides_lang_audit_{time.strftime("%Y%m%d_%H%M%S")}')
LANG_DIRS = ["en","zh-cn","es","pt-br","fr","de","ru","ar","hi","id","vi","ja"]

HTML_RE = re.compile(r'<html[^>]*>', re.IGNORECASE)
LANG_ATTR_RE = re.compile(r'lang="([^"]*)"', re.IGNORECASE)

NEED_I18N = re.compile(r'i18n\/i18n\.js', re.IGNORECASE)
NEED_FLAG = re.compile(r'flag-switcher\.js', re.IGNORECASE)
CSS_REL_RE = re.compile(r'<link\s+rel=["\']stylesheet["\']\s+href=["\'](styles\.css)["\']', re.IGNORECASE)


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)


def read(p):
    with open(p, 'r', encoding='utf-8') as f:
        return f.read()


def write(p, s):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)


def backup(fp):
    dst = os.path.join(BACKUP_DIR, os.path.relpath(fp, ROOT))
    ensure_dir(os.path.dirname(dst))
    shutil.copy2(fp, dst)


def audit_and_fix():
    ensure_dir(BACKUP_DIR)
    report = { 'checked':0, 'fixed_lang':0, 'fixed_i18n':0, 'fixed_flag':0, 'fixed_css':0 }
    details = []
    for lang in LANG_DIRS:
        lang_dir = os.path.join(ROOT, lang)
        if not os.path.isdir(lang_dir):
            continue
        for fn in os.listdir(lang_dir):
            if not fn.endswith('.html'): continue
            fp = os.path.join(lang_dir, fn)
            if not (fn.startswith('how-to-') or fn == 'guides.html' or fn == 'index.html'):
                # 仅检查攻略/首页类页面
                continue
            try:
                s = read(fp)
                report['checked'] += 1
                fixed = False
                # 1) html lang
                m = HTML_RE.search(s)
                if m:
                    tag = m.group(0)
                    cur = LANG_ATTR_RE.search(tag)
                    expected = lang
                    if cur:
                        val = cur.group(1).lower()
                        if val != expected:
                            new_tag = LANG_ATTR_RE.sub(lambda mm: mm.group(0).replace(mm.group(1), expected), tag)
                            s = s.replace(tag, new_tag)
                            report['fixed_lang'] += 1
                            fixed = True
                    else:
                        new_tag = tag[:-1] + f' lang="{expected}">'
                        s = s.replace(tag, new_tag)
                        report['fixed_lang'] += 1
                        fixed = True
                # 2) i18n script (subdir pages需要 ../i18n/i18n.js)
                need_rel = '../i18n/i18n.js'
                if not NEED_I18N.search(s):
                    # 插入到 </body> 前
                    if '</body>' in s.lower():
                        idx = s.lower().rfind('</body>')
                        s = s[:idx] + f"\n    <script src=\"{need_rel}\"></script>" + s[idx:]
                        report['fixed_i18n'] += 1
                        fixed = True
                else:
                    # 规范为 ../i18n/i18n.js
                    s = re.sub(r'<script\s+src=["\'](?:\.\./)?i18n/i18n\.js["\']\s*></script>',
                               f'<script src="{need_rel}"></script>', s, flags=re.IGNORECASE)
                # 3) flag-switcher.js 路径规范 ../flag-switcher.js
                if not NEED_FLAG.search(s):
                    if '</body>' in s.lower():
                        idx = s.lower().rfind('</body>')
                        s = s[:idx] + "\n    <script src=\"../flag-switcher.js\"></script>" + s[idx:]
                        report['fixed_flag'] += 1
                        fixed = True
                else:
                    s = re.sub(r'<script\s+src=["\'](?:\.\./)?flag-switcher\.js["\']\s*></script>',
                               '<script src="../flag-switcher.js"></script>', s, flags=re.IGNORECASE)
                # 4) CSS 相对路径规范
                if CSS_REL_RE.search(s):
                    s = CSS_REL_RE.sub('<link rel="stylesheet" href="../styles.css">', s)
                    report['fixed_css'] += 1
                    fixed = True
                if fixed:
                    backup(fp)
                    write(fp, s)
            except Exception as e:
                details.append(f'ERROR {fp}: {e}')
    return report, details

if __name__ == '__main__':
    rep, det = audit_and_fix()
    print('Audit complete:', rep)
    if det:
        print('\n'.join(det)) 