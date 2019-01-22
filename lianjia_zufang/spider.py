import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient


base_url = 'https://{}.lianjia.com'
city_code_url = 'https://www.lianjia.com/city/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

zufang = '/zufang/rs'
city_code_compile = re.compile('.*?https://(.*?).lianjia.*?>(.*?)</a.*?')
city_code_dict = {}

region_url_compile = re.compile('.*?href="(.*?)".*?\>(.*?)\<\/a\>')
region_url_dict = {}

page_string = 'pg{}/#contentList'
region_per_page_url_dict = {}

browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])

house_area_compile = re.compile('.*?(\d+)㎡.*?')
house_direction_compile = re.compile('.*?([东南西北]+).*?')
house_price_compile = re.compile('.*?(\d+).*?')

# 连接MongoDB
client = MongoClient()
db = client['lianjia_zufang']


def main():
    city = '广州'
    get_city_code()
    get_region_url(city)
    get_per_page_url()
    for region, per_page_url_list in region_per_page_url_dict.items():
        for per_page_url in per_page_url_list:
            parse_per_page_url(region, per_page_url)
    browser.close()


def parse_per_page_url(region, url):
    collection = db[region]
    browser.get(url)
    print(url)
    for item in browser.find_elements_by_css_selector('#content > div.content__article > div.content__list > div'):
        info_item = {}
        # 标题
        title = item.find_element_by_xpath('./div/p[1]/a').get_attribute('innerText')
        infos = item.find_element_by_xpath('./div/p[2]').get_attribute('innerText')
        infos_list = infos.split('/')
        info_item['title'] = title

        # 面积
        try:
            area = re.search(house_area_compile, infos).group(1)
        except AttributeError:
            area = None
        info_item['area'] = area

        # 格局
        pattern = infos_list[-1].strip() or None
        info_item['pattern'] = pattern

        # 朝向
        try:
            house_direction = re.search(house_direction_compile, infos).group(1)
        except AttributeError:
            house_direction = None
        info_item['house_direction'] = house_direction

        # 位置
        if house_direction and len(infos_list) == 3:
            position = None
        elif len(infos_list) == 4 and '-' in infos_list[0]:
            position = infos_list[0].split('-')[1]
        else:
            position = None
        info_item['position'] = position

        # 来源
        house_source = item.find_element_by_xpath('./div/p[3]').get_attribute('innerText').strip()
        if '发布' in house_source:
            house_source = '未知'
        info_item['house_source'] = house_source

        # 价格
        house_price = item.find_element_by_xpath('./div/span').get_attribute('innerText')
        house_price = re.search(house_price_compile, house_price).group(1)
        info_item['house_price'] = house_price

        if collection.insert(info_item):
            print('ok')


def get_per_page_url():
    for region, url in region_url_dict.items():
        region_per_page_url_dict[region] = []
        browser.get(url)
        temp_list = []
        for page in browser.find_elements_by_xpath('//*[@id="content"]/div[1]/div[2]/a'):
            temp_list.append(page.text)
        pages = int(temp_list[-2])
        for page in range(pages):
            page_url = url + page_string.format(page+1)
            region_per_page_url_dict[region].append(page_url)


def get_region_url(city):
    code = city_code_dict.get(city, None)
    if not code:
        print('暂无此城市的租房信息')
        return code

    city_url = base_url.format(code) + zufang
    response = requests.get(city_url, headers=headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html5lib')
        for region in soup.select('ul[data-target="area"] > li'):
            region_url, region_name = re.findall(region_url_compile, str(region))[0]
            if region_name == '不限':
                continue
            region_url_dict[region_name] = base_url.format(code) + region_url

    return None


def get_city_code():
    response = requests.get(city_code_url, headers=headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html5lib')
        city_uls = soup.select('body > div.city_selection_section > div.city_recommend > div > div > ul > li')
        for province in city_uls:
            for city_li in province.select('div[class="city_list"] > div > ul > li'):
                code, city = re.findall(city_code_compile, str(city_li))[0]
                if '.' in code:
                    continue
                city_code_dict[city] = code


if __name__ == '__main__':
    main()






