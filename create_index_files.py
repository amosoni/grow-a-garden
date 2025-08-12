#!/usr/bin/env python3
"""
为缺少 guides.html 的语言目录创建重定向文件，指向 /<lang>/guides
"""

import os

LANGS = ['zh-cn','es','pt-br','fr','de','ru','ar','hi','id','vi','ja']

GUIDES_REDIRECT = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=/{lang}/guides">
  <title>Guides</title>
</head>
<body>
  <p>Redirecting to /{lang}/guides ...</p>
</body>
</html>
"""

if __name__ == '__main__':
  created = []
  for lang in LANGS:
    lang_dir = lang
    if not os.path.isdir(lang_dir):
      continue
    guides_html = os.path.join(lang_dir, 'guides.html')
    if not os.path.exists(guides_html):
      with open(guides_html, 'w', encoding='utf-8') as f:
        f.write(GUIDES_REDIRECT.format(lang=lang))
      created.append(guides_html)
  print('Created redirect files:', created) 