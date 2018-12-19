from urllib.parse import urlencode
import requests
import random
import string
import urllib.request
import os
from multiprocessing.pool import Pool
import json
import math
import re
from pymongo import MongoClient
import uuid


client = MongoClient()
db = client['kobe']
collection = db['kobe']

base_url = 'https://image.baidu.com/search/acjson?'
headers = {
    'Host': 'image.baidu.com',
    'Pragma': 'no-cache',
    'Referer': 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E7%A7%91%E6%AF%94&oq=kebi&rsp=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
regex = re.compile(r'\\(?![/u"])')


def get_page(pn):
    gsm = get_gsm(2)
    random_digits = get_random_digits(13)
    params = {
        'tn': 'resultjson_com',
        'ipn': 'rj',
        'cv': 201326592,
        'is': '',
        'fp': 'result',
        'queryWord': '科比',
        'cl': 2,
        'lm': -1,
        'ie': 'utf-8',
        'oe': 'utf-8',
        'adpicid': '',
        'st': -1,
        'z': '',
        'ic': 0,
        'hd': '',
        'latest': '',
        'copyright': '',
        'word': '科比',
        's': '',
        'se': '',
        'tab': '',
        'width': '',
        'height': '',
        'face': 0,
        'istype': 2,
        'qc': '',
        'nc': 1,
        'fr': '',
        'expermode': '',
        'cg': 'star',
        'pn': pn,
        'rn': 30,
        'gsm': gsm,
        random_digits: '',
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            response_content = regex.sub(r'\\\\', response.content.decode())
            return json.loads(response_content, strict=False)
    except requests.ConnectionError as e:
        print('Error:', e.args)


def parse_page(json, pn):
    if json:
        base_path = os.path.abspath('.')
        if not os.path.exists(os.path.join(base_path, 'kobe-images')):
            os.mkdir(os.path.join(base_path, 'kobe-images'))
        items = json.get('data')
        for i, item in enumerate(items):
            kobe = {}
            image_url = item.get('thumbURL')
            kobe['_id'] = uuid.uuid1()
            kobe['title'] = item.get('fromPageTitleEnc')
            if image_url:
                req = urllib.request.urlopen(image_url)
                buf = req.read()
                file_path = os.path.join(base_path, 'kobe-images', str(pn + i + 1) + '.jpg')
                kobe['path'] = file_path
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        f.write(buf)
                save_to_mongo(kobe)


def save_to_mongo(result):
    if collection.insert(result):
        print('Saved to Mongo')


def get_gsm(n):
    random_str = ''.join(random.sample(string.ascii_letters[:26] + string.digits, n))
    return random_str


def get_random_digits(n):
    random_str = ''.join(random.sample(string.digits, int(n/2))) + \
                 ''.join(random.sample(string.digits, math.ceil(n/2)))
    return random_str


def main(pn):
    json = get_page(pn)
    parse_page(json, pn)


GROUP_START = 0
GROUP_END = 20


if __name__ == '__main__':
    import datetime

    print(datetime.datetime.now())
    for i in range(GROUP_START, GROUP_END):
        main(i*30)
    print(datetime.datetime.now())

    # print(datetime.datetime.now())
    # pool = Pool()
    # group = [x * 30 for x in range(GROUP_START, GROUP_END)]
    # pool.map(main, group)
    # pool.close()
    # pool.join()
    # print(datetime.datetime.now())







