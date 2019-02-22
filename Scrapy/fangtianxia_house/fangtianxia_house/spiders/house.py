# -*- coding: utf-8 -*-
import os
import re
import json
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from fangtianxia_house.items import FangtianxiaHouseItem


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
        self.blank_compile = re.compile('\s+')

        self.key_correspondence = {
            '物业类别': 'property_type',
            '项目特色': 'feature',
            '建筑类别': 'house_type',
            '装修状况': 'decoration_status',
            '产权年限': 'property_right',
            '环线位置': 'location',
            '开发商': 'developers',
            '楼盘地址': 'house_address',
            '销售状态': 'sale_status',
            '楼盘优惠': 'sale_discount',
            '开盘时间': 'open_time',
            '交房时间': 'hand_time',
            '售楼地址': 'sale_address',
            '咨询电话': 'phone',
            '主力户型': 'main_house_type',
            '占地面积': 'area_cover',
            '建筑面积': 'area_build',
            '容积率': 'plot_rate',
            '绿化率': 'green_rate',
            '停车位': 'park',
            '楼栋总数': 'house_num',
            '总户数': 'room_num',
            '物业公司': 'property_company',
            '物业费': 'property_cost',
            '物业费描述': 'property_cost_description',
            '楼层状况': 'floor_status',
        }

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
        item = FangtianxiaHouseItem()

        soup = BeautifulSoup(response.body, 'html5lib')

        # 名字
        name = soup.select(
            '#daohang > div > div.lpname.fl > dl > dd > div.lpbt.tf.jq_nav > h1 > a'
        )[0].text
        item['name'] = name

        # 均价
        average_price = soup.select(
            'div.main-left > div:nth-of-type(1) > div > div > em'
        )[0].text.strip()
        try:
            average_price = re.search(self.price_compile, average_price).group(1)
        except AttributeError:
            average_price = average_price
        item['average_price'] = average_price

        # 楼盘信息
        house_infos = soup.select(
            'div.main-left > div:nth-of-type(1) > ul > li'
        )
        # 销售信息
        sale_infos = soup.select(
            'div.main-left > div:nth-of-type(2) > ul > li'
        )
        # 小区规划
        community_planning = soup.select(
            'div.main-left > div:nth-of-type(4) > ul > li'
        )
        # 周边设施
        periphery_facilities_infos = soup.select(
            'div.main-left > div:nth-of-type(3) > ul > li'
        )

        for infos in [house_infos, sale_infos, community_planning]:
            for info in infos:
                content = info.text
                key = content.split('：')[0].strip()
                key = ''.join(re.split(self.blank_compile, key))

                value = content.split('：')[1].strip()
                value = ','.join(re.split(self.blank_compile, value))

                if value == '':
                    continue

                print(key)
                item[self.key_correspondence.get(key)] = value

        facilities = ''
        for info in periphery_facilities_infos:
            content = info.text
            facilities += content
        item['facilities'] = facilities

        yield item

        if len(self.detail_url_list) != 0:
            self.current_url = self.detail_url_list.pop(0)
            yield Request(self.current_url, callback=self.parse, dont_filter=True)
        elif len(self.per_page_url_list) != 0:
            self.current_url = self.per_page_url_list.pop(0)
            yield Request(self.current_url, callback=self.get_detail_url, dont_filter=True)
