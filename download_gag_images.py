import requests
from bs4 import BeautifulSoup
import json

url = "https://growagarden.fandom.com/wiki/Crops"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")

mapping = {}
for img in soup.find_all("img"):
    src = img.get("data-src") or img.get("src")
    alt = img.get("alt", "").strip()
    if not src or not alt:
        continue
    # 只取主图片链接
    if "/revision/" in src:
        src_main = src.split("/revision/")[0]
    else:
        src_main = src
    # 只保留常见图片格式
    if not src_main.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        continue
    # 规范key（全部小写、去空格、去特殊符号）
    key = alt.lower().replace(" ", "").replace("-", "").replace("_", "")
    mapping[key] = src_main

with open("plant_img_map.json", "w", encoding="utf-8") as f:
    json.dump(mapping, f, indent=2, ensure_ascii=False)

print("已生成 plant_img_map.json，映射数量：", len(mapping))
