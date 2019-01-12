import requests
from urllib.parse import urlencode
import string
import random
import math
import uuid
import os
import urllib.request


base_url = 'https://image.baidu.com/search/acjson?'
params = {
    'tn': 'resultjson_com',
    'ipn': 'rj',
    'ct': '201326592',
    'is': '',
    'fp': 'result',
    'queryWord': '',
    'cl': '2',
    'lm': '-1',
    'ie': 'utf-8',
    'oe': 'utf-8',
    'adpicid': '',
    'st': '-1',
    'z': '',
    'ic': '0',
    'hd': '',
    'latest': '',
    'copyright': '',
    'word': '',
    's': '',
    'se': '',
    'tab': '',
    'width': '',
    'height': '',
    'face': '0',
    'istype': '2',
    'qc': '',
    'nc': '1',
    'fr': '',
    'expermode': '',
    'force': '',
    'pn': '',
    'rn': '30',
    'gsm': ''
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
}
# 当前文件路径
current_path = os.path.dirname(__file__)
if not os.path.exists(os.path.join(current_path, 'images')):
    os.mkdir(os.path.join(current_path, 'images'))
# 要搜索的关键字
key_word = '伦敦'


# 获取页面，需要传入要搜索图片的关键字和页数
def get_page_data(page):
    # 获取gsm和数字字符串
    gsm = get_gsm()
    long_string = get_long_string(13)
    # 填充params
    params['queryWord'] = params['word'] = key_word
    params['gsm'] = gsm
    params[long_string] = ''
    params['pn'] = str(page * 30)
    # 构造请求url
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
    except requests.ConnectionError:
        print('请求失败')
        return None
    else:
        if response.status_code == 200:
            # 修改response编码
            response.encoding = 'utf-8'
            return response.json()


# 解析数据
def parse_page_data(json_data, page):
    # 遍历key为data的数据
    for index, item in enumerate(json_data['data']):
        # 取出图片的url
        image_url = item.get('thumbURL')
        if image_url:
            print(image_url)
            # 将图片数据保存到buf
            req = urllib.request.urlopen(image_url)
            buf = req.read()
            file_path = os.path.join(current_path, 'images', str(page*30+index+1)+'.jpg').replace('\\', '/')
            with open(file_path, 'wb') as f:
                f.write(buf)


def main(page):
    json_data = get_page_data(page)
    parse_page_data(json_data, page)


# 生成随机gsm参数
def get_gsm():
    gsm = ''.join(random.sample(string.ascii_lowercase + string.digits, 2))
    return gsm


# 生成长字符串，这里我们需要生成13位的数字
def get_long_string(n):
    long_string = ''.join(random.sample(string.digits, math.ceil(n/2))) + \
                  ''.join(random.sample(string.digits, math.floor(n/2)))
    return long_string


if __name__ == '__main__':
    # for i in range(30):
    #     main(i)

    # 多进程
    from multiprocessing import Pool
    pool = Pool()
    pool.map(main, range(30))
    pool.close()
    pool.join()

