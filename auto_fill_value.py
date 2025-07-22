import requests
import json
import re
from bs4 import BeautifulSoup

# 1. 爬取 Wiki 作物价值
url = 'https://growagarden.fandom.com/wiki/Crops'
headers = {'User-Agent': 'Mozilla/5.0'}
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, 'html.parser')

value_map = {}
for tr in soup.find_all('tr'):
    tds = tr.find_all('td')
    if len(tds) < 2:
        continue
    name = tds[0].get_text(strip=True).lower().replace(' ', '').replace('-', '').replace('_', '')
    value_text = tds[1].get_text(strip=True)
    m = re.search(r'\$?([0-9,]+)', value_text)
    if m:
        value = int(m.group(1).replace(',', ''))
        value_map[name] = value

# 2. 读取 plants_auto.js 并补全 value 字段
with open('plants_auto.js', encoding='utf-8') as f:
    js = f.read()

# 提取数组内容
js_array = re.search(r'const plants = \[(.*)\];', js, re.DOTALL).group(1)
# 拆分为对象
obj_strs = re.findall(r'\{[^}]+\}', js_array)
plants = []
for obj in obj_strs:
    # 替换属性名加双引号
    obj_json = re.sub(r'(\w+):', r'"\1":', obj)
    # 替换单引号为双引号
    obj_json = obj_json.replace("'", '"')
    plants.append(json.loads(obj_json))

for p in plants:
    p['value'] = value_map.get(p['key'], 1)  # 没有的用1

with open('plants_auto.js', 'w', encoding='utf-8') as f:
    f.write('const plants = [\n' + ',\n'.join([json.dumps(p, ensure_ascii=False) for p in plants]) + '\n];\n')

print('已自动爬取Wiki并补全plants_auto.js的value字段。') 