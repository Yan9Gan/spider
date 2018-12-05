import json


string = '[{"name": "Bob", "gender": "male", "birthday": "1992-10-18"},' \
         ' {"name": "Selina", "gender": "female", "birthday": "1995-10-18"}]'

# print(type(string))
data = json.loads(string)
# print(data)
# print(type(data))
# print(data[0]['name'])
# print(data[0].get('name'))


"""写入json"""
# with open('../data/data.json', 'w') as f:
#     f.write(json.dumps(data))


"""读出json"""
# with open('../data/data.json', 'r') as f:
#     string2 = f.read()
#     data2 = json.loads(string2)
#     print(data2)


"""带缩进写入json"""
# with open('../data/data2.json', 'w') as f:
#     f.write(json.dumps(data, indent=2))


data3 = [{
    'name': '王伟',
    'gender': '男',
    'birthday': '1992-10-18'
}]
with open('../data/data3.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data3, indent=2, ensure_ascii=False))



