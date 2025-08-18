#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, time, shutil

ROOT = os.path.abspath(os.path.dirname(__file__)).rsplit(os.sep, 1)[0]
BACKUP_DIR = os.path.join(ROOT, 'backups', f'apply_guides_i18n_{time.strftime("%Y%m%d_%H%M%S")}')

SKIP_DIRS = {'backups','i18n','node_modules','.git','tools'}

# Matches: <section class="{topic}-hero ..."> ... </section>
HERO_SECTION_RE = re.compile(r'(<section[^>]*class=["\"][^"\']*([a-z0-9-]+)-hero[^"\']*["\'][^>]*>)([\s\S]*?)(</section>)', re.IGNORECASE)
H1_INNER_RE = re.compile(r'(<h1)([^>]*)(>)', re.IGNORECASE)
P_INNER_RE  = re.compile(r'(<p)([^>]*)(>)', re.IGNORECASE)

# Breadcrumb current item
BREADCRUMB_CUR_RE = re.compile(r'(<nav[^>]*class=["\']breadcrumb["\'][^>]*>[\s\S]*?<li[^>]*aria-current=["\']page["\'][^>]*)(>)', re.IGNORECASE)

# Guide-card title inside sections with id
GUIDE_CARD_H2_RE = re.compile(r'(\<div[^>]*class=["\'][^"\']*guide-card[^"\']*["\'][^>]*\s+id=["\']([a-z0-9_-]+)["\'][^>]*\>[\s\S]*?<h2)([^>]*)(>)', re.IGNORECASE)


def ensure_dir(p):
	os.makedirs(p, exist_ok=True)


def backup(path):
	dst = os.path.join(BACKUP_DIR, os.path.relpath(path, ROOT))
	ensure_dir(os.path.dirname(dst))
	shutil.copy2(path, dst)


def add_attr_if_missing(tag_prefix: str, attrs: str, tag_suffix: str, key: str) -> str:
	# if data-i18n already present, keep as-is
	if 'data-i18n=' in attrs:
		return tag_prefix + attrs + tag_suffix
	return f'{tag_prefix}{attrs} data-i18n="{key}"{tag_suffix}'


def inject_for_file(content: str, topic_hint: str = None) -> tuple[str, bool]:
	changed = False

	# 1) Hero section processing (h1 + p)
	def _hero(m):
		nonlocal changed
		open_tag, inner_topic, inner_html, close_tag = m.group(1), m.group(2), m.group(3), m.group(4)
		topic = (topic_hint or inner_topic or '').strip().lower()

		def _h1(mh):
			nonlocal changed
			return add_attr_if_missing(mh.group(1), mh.group(2), mh.group(3), f"{topic}.hero.title") if topic else mh.group(0)

		def _p(mp):
			nonlocal changed
			return add_attr_if_missing(mp.group(1), mp.group(2), mp.group(3), f"{topic}.hero.subtitle") if topic else mp.group(0)

		new_inner = inner_html
		new_inner2 = H1_INNER_RE.sub(_h1, new_inner, count=1)
		new_inner3 = P_INNER_RE.sub(_p, new_inner2, count=1)
		if new_inner3 != inner_html:
			changed = True
		return open_tag + new_inner3 + close_tag

	content2 = HERO_SECTION_RE.sub(_hero, content, count=1)

	# Extract topic again (in case hero not matched, try from class somewhere else)
	topic = None
	m_topic = re.search(r'class=["\'][^"\']*([a-z0-9-]+)-hero', content2, flags=re.IGNORECASE)
	if m_topic:
		topic = m_topic.group(1).lower()
	if topic_hint and not topic:
		topic = topic_hint.lower()

	# 2) Breadcrumb current item
	def _bc(m):
		nonlocal changed
		if 'data-i18n=' in m.group(1) or not topic:
			return m.group(0)
		changed = True
		return m.group(1) + f' data-i18n="{topic}.breadcrumb.current"' + m.group(2)

	content3 = BREADCRUMB_CUR_RE.sub(_bc, content2, count=1)

	# 3) Guide-card h2 based on id -> {topic}.{id}.title
	def _h2(m):
		nonlocal changed
		attrs = m.group(3)
		sec_id = m.group(2)
		if 'data-i18n=' in attrs or not sec_id or not topic:
			return m.group(0)
		changed = True
		return m.group(1) + attrs + f' data-i18n="{topic}.{sec_id}.title"' + m.group(4)

	content4 = GUIDE_CARD_H2_RE.sub(_h2, content3)

	return content4, changed


def main():
	ensure_dir(BACKUP_DIR)
	processed = 0
	changed_files = 0
	for lang in [d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d)) and d not in SKIP_DIRS and not d.startswith('.')]:
		lang_dir = os.path.join(ROOT, lang)
		for fn in os.listdir(lang_dir):
			if not fn.lower().endswith('.html'):
				continue
			if not (fn.startswith('how-to-')):
				continue
			fp = os.path.join(lang_dir, fn)
			try:
				with open(fp, 'r', encoding='utf-8') as f:
					content = f.read()
				new_content, changed = inject_for_file(content)
				processed += 1
				if changed:
					backup(fp)
					with open(fp, 'w', encoding='utf-8') as f:
						f.write(new_content)
					changed_files += 1
			except Exception as e:
				print('ERR', fp, e)
	print(f'Guides processed: {processed}, modified: {changed_files}. Backups at {BACKUP_DIR}')

if __name__ == '__main__':
	main() 