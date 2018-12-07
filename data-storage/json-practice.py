import json


string = '[{"name": "Bob", "gender": "male", "birthday": "1992-10-18"},' \
         ' {"name": "Selina", "gender": "female", "birthday": "1995-10-18"}]'

# print(type(string))
data = json.loads(string)
# print(images)
# print(type(images))
# print(images[0]['name'])
# print(images[0].get('name'))


"""写入json"""
# with open('../images/images.json', 'w') as f:
#     f.write(json.dumps(images))


"""读出json"""
# with open('../images/images.json', 'r') as f:
#     string2 = f.read()
#     data2 = json.loads(string2)
#     print(data2)


"""带缩进写入json"""
# with open('../images/data2.json', 'w') as f:
#     f.write(json.dumps(images, indent=2))


data3 = [{
    'name': '王伟',
    'gender': '男',
    'birthday': '1992-10-18'
}]
with open('../images/data3.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data3, indent=2, ensure_ascii=False))



