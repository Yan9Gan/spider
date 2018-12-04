import requests
import re


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
# }
# r = requests.get('https://www.zhihu.com/explore', headers=headers)
# pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
# titles = re.findall(pattern, r.text)
# print(titles)


# r = requests.get('https://github.com/favicon.ico')
# # print(r.text)  # 乱码
# # print(r.content)  # bytes类型
# with open('../data/github-favicon.ico', 'wb') as f:
#     f.write(r.content)


# r = requests.get('https://www.zhihu.com/explore')
# print(r.text)


# r = requests.get('https://www.baidu.com')
# print(r.cookies)
# for key, value in r.cookies.items():
#     print(key + '=' + value)


response = requests.get('https://www.12306.cn', verify=False)
print(response.status_code)





