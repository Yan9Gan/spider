import requests
from bs4 import BeautifulSoup
import random
import string
import math
from urllib.parse import urlencode
import json
import re
from pandas import DataFrame

# 爬取http://www.weather.com.cn/weather40d/101280101.shtml
base_url = 'http://d1.weather.com.cn/calendar_new/2018/101280101_201812.templates?'
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'UM_distinctid=167cabb1a3344-01e75fe4d3d34c-b781636-1fa400-167cabb1a3893; vjuids=-9b3c1e207.167cabb1dd2.0.ab9a7f96f35f7; vjlast=1545294520.1545294520.30; Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b=1545294520; f_city=%E5%8C%97%E4%BA%AC%7C101010100%7C; Wa_lvt_1=1545294532; Wa_lpvt_1=1545298480; Hm_lpvt_080dabacb001ad3dc8b9b9049b36d43b=1545298600',
    'Host': 'd1.weather.com.cn',
    'Pragma': 'no-cache',
    'Referer': 'http://www.weather.com.cn/weather40d/101280101.shtml',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
regex = re.compile(r'\\(?![/u"])')
data = []


def get_json():
    _ = get_random_digits(13)
    params = {_: _}
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError as e:
        print('Error:', e.args)


def parse_json(text):
    if text:
        text = re.search('(\[.*?\])', text).group(1)
        text_json = json.loads(text)
        for item in text_json:
            print(item)
            yes = item.get('alins')
            no = item.get('als')
            date = item.get('date')
            date = date[:4] + '-' + date[4:6] + '-' + date[6:] + ' ' + '星期' + item.get('wk')
            rain_chance = item.get('hgl')
            min_temperature = item.get('hmin')
            max_temperature = item.get('hmax')
            nongli = item.get('nlyf') + item.get('nl')
            status = item.get('w1', '') + ' ' + item.get('wd1', '')
            festival = item.get('yl', '')
            data.append([date, nongli, yes, no, min_temperature, max_temperature,
                         status, rain_chance, festival])
        data_frame = DataFrame(data, columns=['日期', '农历', '宜', '忌', '最低温', '最高温',
                                              '天气', '降水概率', '节日'])
        data_frame.to_csv('weather.csv', encoding='utf-8')


def get_random_digits(n):
    random_str = ''.join(random.sample(string.digits, int(n/2))) + \
                 ''.join(random.sample(string.digits, math.ceil(n/2)))
    return random_str


def main():
    json = get_json()
    parse_json(json)


if __name__ == '__main__':
    main()


