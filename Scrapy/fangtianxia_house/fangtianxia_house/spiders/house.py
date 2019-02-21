# -*- coding: utf-8 -*-
import os
import re
import json
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request


class HouseSpider(scrapy.Spider):
    name = 'house'
    allowed_domains = ['https://gz.fang.com/']

    def __init__(self, city_name, *args, **kwargs):
        super(HouseSpider, self).__init__(*args, **kwargs)
        self.city_name = city_name

        with open(os.path.join(os.getcwd(), 'city_code.json'), 'r') as f:
            data = f.read()
            self.city_url_dict = json.loads(data)

        self.city_code = self.city_url_dict.get(self.city_name)
        self.current_url = 'https://' + self.city_code + '.newhouse.fang.com/house/s/'

        self.detail_code_compile = re.compile('.*?(\d{10}).*?')
        self.price_compile = re.compile('.*?(\d+.*?)元.*?')
        self.park_compile = re.compile('.*?(\d+).*?')

        self.per_page_url_list = []
        self.detail_url_list = []

    def start_requests(self):
        yield Request(self.current_url, callback=self.get_per_page_url)

    def get_per_page_url(self, response):
        page_info = response.xpath('/html/body/div[9]/div/ul/li[4]/div[2]/span[2]/text()').extract_first()
        page = int(page_info[1:])
        for i in range(page):
            url = self.current_url + 'b9{}/?ctm=1.{}.xf_search.list_type.9'.format(i+1, self.city_code)
            print(url)
            self.per_page_url_list.append(url)

        if len(self.per_page_url_list) != 0:
            self.current_url = self.per_page_url_list.pop(0)
            yield Request(self.current_url, callback=self.get_detail_url, dont_filter=True)

    def get_detail_url(self, response):
        infos = response.xpath('//*[@id="newhouse_loupai_list"]/ul/li')
        for info in infos:
            base_url = info.xpath('./div/div[1]/a/@href').extract_first()
            temp_info = info.xpath('./div/div[2]/div[2]/a/@href').extract_first()

            if not temp_info or not temp_info.startswith('//'):
                continue

            detail_code = re.search(self.detail_code_compile, temp_info).group(1)
            url = 'https:' + base_url + 'house/{}/housedetail.htm'.format(detail_code)
            self.detail_url_list.append(url)

        if len(self.detail_url_list) != 0:
            self.current_url = self.detail_url_list.pop(0)
            yield Request(self.current_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')

        # 名字
        name = soup.select(
            '#daohang > div > div.lpname.fl > dl > dd > div.lpbt.tf.jq_nav > h1 > a'
        )[0].text

        # 均价
        average_price = soup.select(
            'div.main-left > div:nth-of-type(1) > div > div > em'
        )[0].text.strip()
        average_price = re.search(self.price_compile, average_price).group(1)

        # 物业类型
        property_type = soup.select(
            'div.main-left > div:nth-of-type(1) > ul > li:nth-of-type(1) > div.list-right'
        )[0].text.strip()

        # 特色
        features = soup.select(
            'div.main-left > div:nth-of-type(1) > ul > li:nth-of-type(2) > div.list-right > span'
        )
        feature = ''
        for item in features:
            feature += item.text + ','
        feature = feature[:-1]

        # 建筑类别
        house_type = soup.select(
            'div.main-left > div:nth-of-type(1) > ul > li:nth-of-type(3) > div.list-right > span'
        )[0].text.strip().replace('\n', ' ')
        house_type = ','.join(re.split('\s+', ' '.join(house_type.split(' '))))

        # 装修状况
        house_status = soup.select(
            'div.main-left > div:nth-of-type(1) > ul > li:nth-of-type(4) > div.list-right'
        )[0].text.strip()

        # 产权
        property_rights = soup.select(
            'div.main-left > div:nth-of-type(1) > ul > li:nth-of-type(5) > div.list-right > div > p'
        )
        property_right = ''
        for item in property_rights:
            property_right += item.text + ','
        property_right = property_right[:-1]

        # 环线位置
        location = soup.select(
            'div.main-left > div:nth-of-type(1) > ul > li:nth-of-type(6) > div.list-right'
        )[0].text.strip()

        # 开发商
        developers = soup.select(
            'div.main-left > div:nth-of-type(1) > ul > li:nth-of-type(7) > div.list-right-text > a'
        )
        developer = ''
        for item in developers:
            developer += item.text + ','
        developer = developer[:-1]

        # 楼盘地址
        address = soup.select(
            'div.main-left > div:nth-of-type(1) > ul > li:nth-of-type(8) > div.list-right-text'
        )[0].text

        # 销售状态
        sale_status = soup.select(
            'div.main-left > div:nth-of-type(2) > ul > li:nth-of-type(1) > div.list-right'
        )[0].text.strip()

        # 优惠
        discount = soup.select(
            'div.main-left > div:nth-of-type(2) > ul > li:nth-of-type(2) > div.list-right'
        )[0].text.strip()

        # 开盘时间
        open_time = soup.select(
            'div.main-left > div:nth-of-type(2) > ul > li:nth-of-type(3) > div.list-right'
        )[0].text.replace('[开盘时间详情]', '')

        # 交房时间
        hand_time = soup.select(
            'div.main-left > div:nth-of-type(2) > ul > li:nth-of-type(4) > div.list-right'
        )[0].text

        # 售楼地址
        sale_address = soup.select(
            'div.main-left > div:nth-of-type(2) > ul > li:nth-of-type(5) > div.list-right'
        )[0].text

        # 咨询电话
        phone = soup.select(
            'div.main-left > div:nth-of-type(2) > ul > li:nth-of-type(6) > div.list-right.c00'
        )[0].text

        # 主办户型
        major_apartments = soup.select(
            'div.main-left > div:nth-of-type(2) > ul > li:nth-of-type(7) > div.list-right-text'
        )[0].text
        major_apartment = ''.join(re.split('\s+', major_apartments.strip()))

        # 占地面积
        area_cover = soup.select(
            'div.main-left > div:nth-of-type(4) > ul > li:nth-of-type(1) > div.list-right'
        )[0].text

        # 建筑面积
        area_build = soup.select(
            'div.main-left > div:nth-of-type(4) > ul > li:nth-of-type(2) > div.list-right'
        )[0].text

        # 容积率
        volume_ratio = soup.select(
            'div.main-left > div:nth-of-type(4) > ul > li:nth-of-type(3) > div.list-right'
        )[0].text.strip()

        # 绿化率
        green_ratio = soup.select(
            'div.main-left > div:nth-of-type(4) > ul > li:nth-of-type(4) > div.list-right'
        )[0].text

        print(name, average_price, property_type, feature, house_type, house_status)
        print(property_right, location)
        print(developer, address)
        print(sale_status, discount, open_time, hand_time)
        print(sale_address, phone, major_apartment)
        print(area_cover, area_build, volume_ratio, green_ratio, park_num)

        if len(self.detail_url_list) != 0:
            self.current_url = self.detail_url_list.pop(0)
            yield Request(self.current_url, callback=self.parse, dont_filter=True)
        elif len(self.per_page_url_list) != 0:
            self.current_url = self.per_page_url_list.pop(0)
            yield Request(self.current_url, callback=self.get_detail_url, dont_filter=True)
