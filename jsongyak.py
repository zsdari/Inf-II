import json

with open("json_file.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# print(type(data))
# print(data)

for item in data['studs']:
    item['class'] = '12.C'
    item['phone'] = '06 30 123 4567'
    # print(item['name'], end=' ')
    # print(item['e-mail'], end=' ')
    # print(item['class'], end=' ')
    # print(item['dorm'])

with open("json_file2.json", "w", encoding="utf-8") as f2:
    json.dump(data, f2, indent=2)

with open("json_file2.json", "r", encoding="utf-8") as f3:
    data2 = json.load(f3)

for item in data2 ['studs']:
    print(item)





