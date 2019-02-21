import os
import re
import json
import requests
from bs4 import BeautifulSoup


def get_city_code():
    url = 'https://www.fang.com/SoufunFamily.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    }
    url_compile = re.compile('http://(.*?)\.fang.*?')

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        city_url_dict = {}
        save_path = os.path.join(os.getcwd(), 'city_code.json')

        soup = BeautifulSoup(response.text, 'html5lib')
        city_infos = soup.select('#senfe > tbody > tr')

        last_province = ''
        for line in city_infos:
            try:
                province = line.select('td:nth-of-type(2) > strong')[0].text
                if province == ' ':
                    province = last_province
            except:
                province = last_province
            last_province = province

            if province == '其它':
                continue

            for info in line.select('td:nth-of-type(3) > a'):
                city_name = info.text
                city_url = info.get('href')
                city_code = re.search(url_compile, city_url).group(1)
                city_url_dict[city_name] = city_code

        with open(save_path, 'w') as f:
            f.write(json.dumps(city_url_dict))

    return None


if __name__ == '__main__':
    get_city_code()
