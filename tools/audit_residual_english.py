#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, json, time

ROOT = os.path.abspath(os.path.dirname(__file__)).rsplit(os.sep, 1)[0]
LANG_DIRS = ["zh-cn","es","pt-br","fr","de","ru","ar","hi","id","vi","ja"]
OUT_PATH = os.path.join(ROOT, 'residuals.report.json')

TAG_RE = re.compile(r'<[^>]+>')
SCRIPT_RE = re.compile(r'<script[\s\S]*?</script>', re.IGNORECASE)
STYLE_RE = re.compile(r'<style[\s\S]*?</style>', re.IGNORECASE)
COMMENT_RE = re.compile(r'<!--([\s\S]*?)-->', re.DOTALL)
HEADER_RE = re.compile(r'<header[\s\S]*?</header>', re.IGNORECASE)
NAV_RE = re.compile(r'<nav[\s\S]*?</nav>', re.IGNORECASE)
FOOTER_RE = re.compile(r'<footer[\s\S]*?</footer>', re.IGNORECASE)
MAIN_RE = re.compile(r'<main[\s\S]*?</main>', re.IGNORECASE)
WS_RE = re.compile(r'\s+')
ASCII_RE = re.compile(r'[A-Za-z]')
NUMERIC_ONLY = re.compile(r'^[\d\s:.,%()\-+/*]+$')

# Heuristic whitelist words that may legitimately appear
WHITELIST = set([
    'US','CN','ES','BR','FR','DE','RU','SA','IN','ID','VN','JP',
    'Discord','Roblox','Grow','Garden','Grow a Garden','FAQ','min','Min','k','M',
])

MIN_LEN = 4  # minimal token len to consider


def extract_text(html: str) -> str:
    s = SCRIPT_RE.sub(' ', html)
    s = STYLE_RE.sub(' ', s)
    s = COMMENT_RE.sub(' ', s)
    # Prefer main content if present
    m = MAIN_RE.search(s)
    if m:
        s = m.group(0)
    # Remove header/nav/footer blocks to avoid counting chrome
    s = HEADER_RE.sub(' ', s)
    s = NAV_RE.sub(' ', s)
    s = FOOTER_RE.sub(' ', s)
    s = TAG_RE.sub(' ', s)
    s = WS_RE.sub(' ', s)
    return s.strip()


def is_suspicious_segment(seg: str) -> bool:
    if not seg: return False
    if not ASCII_RE.search(seg): return False
    if len(seg) < MIN_LEN: return False
    if seg in WHITELIST: return False
    if NUMERIC_ONLY.match(seg): return False
    # ignore mailto/http urls
    if 'http://' in seg or 'https://' in seg: return False
    return True


def audit():
    report = { 'generatedAt': time.strftime('%Y-%m-%d %H:%M:%S'), 'files': [] }
    total_candidates = 0
    for lang in LANG_DIRS:
        lang_dir = os.path.join(ROOT, lang)
        if not os.path.isdir(lang_dir):
            continue
        for fn in os.listdir(lang_dir):
            if not fn.lower().endswith('.html'): continue
            fp = os.path.join(lang_dir, fn)
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    html = f.read()
                text = extract_text(html)
                parts = re.split(r'[\.!?\n\r;]+', text)
                hits = []
                for p in parts:
                    t = p.strip()
                    if not t: continue
                    if len(t) > 140:
                        t = t[:140] + '…'
                    if is_suspicious_segment(t):
                        ascii_count = sum(1 for c in t if ord(c) < 128)
                        non_ascii = sum(1 for c in t if ord(c) >= 128)
                        if non_ascii > ascii_count:
                            continue
                        hits.append(t)
                        if len(hits) >= 20:
                            break
                if hits:
                    total_candidates += len(hits)
                    report['files'].append({ 'file': os.path.relpath(fp, ROOT), 'samples': hits })
            except Exception as e:
                report['files'].append({ 'file': os.path.relpath(fp, ROOT), 'error': str(e) })
    report['total'] = total_candidates
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Residual English audit complete. Candidates: {total_candidates}. Report: {OUT_PATH}")

if __name__ == '__main__':
    audit() 