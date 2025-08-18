import json

with open('plant_img_map_final.json', encoding='utf-8') as f:
    img_map = json.load(f)

plants_js = []
for k in img_map.keys():
    plants_js.append(f'  {{ key: "{k}", name: "{k.capitalize()}", category: "Auto", value: 0 }}')

with open('plants_auto.js', 'w', encoding='utf-8') as f:
    f.write('const plants = [\n' + ',\n'.join(plants_js) + '\n];\n')

print("已生成 plants_auto.js，包含所有图片映射的植物key。")

