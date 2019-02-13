import os
import re
import json
import requests

json_compile = re.compile('(\'.*\')')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
}


def get_station_code():
    station_code_dict = {}

    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9083'
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        text = response.text
        text = re.search(json_compile, text).group(1)
        code_list = text.split('|')
        for _1, city, code, _2, _3 in zip(code_list[0::5], code_list[1::5], code_list[2::5],
                                          code_list[3::5], code_list[4::5]):
            if city not in station_code_dict.keys():
                station_code_dict[city] = code

    json_str = json.dumps(station_code_dict, indent=4)
    json_path = os.path.join(os.getcwd(), 'station_code.json')
    with open(json_path, 'w') as json_file:
        json_file.write(json_str)


if __name__ == '__main__':
    get_station_code()

