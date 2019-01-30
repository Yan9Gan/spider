# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from urllib.parse import unquote
from jdLipstick.items import JdlipstickItem


class JdLipstickSpider(scrapy.Spider):
    name = 'jd_lipstick'
    allowed_domains = ['https://www.jd.com/']
    base_url = 'https://search.jd.com/'
    start_url = 'https://search.jd.com/Search?keyword=口红&enc=utf-8&wq=口红&pvid=33b0080a6043490faa5c27eb775a0975'

    current_url = ''
    current_brand = ''
    page_url = '&page={}&s=56&click=0'

    brand_url_list = []
    all_page_url_list = []
    all_url_list = []
    all_price_list = []

    head_list = ['商品名称', '商品毛重', '国产/进口', '妆效', '色系', '产品产地']
    head_english_dict = {'商品名称': 'commodity_name',
                         '商品毛重': 'weight',
                         '国产/进口': 'channel',
                         '妆效': 'makeup_effect',
                         '色系': 'color_type',
                         '产品产地': 'origin'}

    colon_split = '：'  # 中文冒号

    brand_extract_compile = re.compile('.*?&ev=exbrand_(.*?)%5E&uc.*?')
    url_split_compile = re.compile('(.*?)(&stock.*?)(&ev.*?)&uc.*?')

    # 开始爬取
    def start_requests(self):
        start_url = self.start_url
        return [scrapy.FormRequest(start_url, callback=self.brand_url_callback)]

    # 获取品牌首页url
    def brand_url_callback(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        # 找到每个品牌的li
        brand_lis = soup.select(
            '#J_selector > div.J_selectorLine.s-brand > div > div.sl-value > div.sl-v-logos > ul > li'
        )
        for li in brand_lis:
            # 获取url并保存在self.brand_url_list中
            brand_url = li.find('a').get('href')
            url = self.base_url + brand_url
            self.brand_url_list.append(url)

        # 推出第一个url，并回调self.per_page_url_callback
        self.current_url = self.brand_url_list.pop(0)
        brand_name = re.search(self.brand_extract_compile, self.current_url).group(1)
        self.current_brand = unquote(brand_name)
        yield Request(self.current_url, callback=self.per_page_url_callback, dont_filter=True)

    # 获取每一页url
    def per_page_url_callback(self, response):
        current_url_split = re.findall(self.url_split_compile, self.current_url)[0]
        base_url = current_url_split[0] + current_url_split[2] + current_url_split[1] + self.page_url

        soup = BeautifulSoup(response.body, 'html5lib')
        # 找到总页数
        pages_num = soup.select('#J_topPage > span > i')[0].text
        # 通过循环枚举所有页码的url
        for i in range(int(pages_num)):
            url = base_url.format(i+2)
            self.all_page_url_list.append(url)

        self.current_url = self.all_page_url_list.pop(0)
        yield Request(self.current_url, callback=self.per_commodity_url_callback, dont_filter=True)

    # 获取每个商品页的url
    def per_commodity_url_callback(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        lis = soup.select('#J_goodsList > ul > li')
        for li in lis:
            commodity_url = li.find('a').get('href')
            # 除去广告url
            if commodity_url.startswith('//item.jd.com'):
                url = 'https:' + commodity_url
                self.all_url_list.append(url)
                # 找到价格节点
                price = li.select('div > div.p-price > strong')[0].text
                self.all_price_list.append(price)
            else:
                continue

        if len(self.all_page_url_list) != 0:
            self.current_url = self.all_page_url_list.pop(0)
            yield Request(self.current_url, callback=self.per_commodity_url_callback, dont_filter=True)
        else:
            self.current_price = self.all_price_list.pop(0)
            self.current_url = self.all_url_list.pop(0)
            yield Request(self.current_url, callback=self.parse, dont_filter=True)

    # 解析每个商品页
    def parse(self, response):
        items = JdlipstickItem()
        soup = BeautifulSoup(response.body, 'html5lib')

        items['brand'] = self.current_brand
        items['price'] = self.current_price

        infos = soup.select(
            '#detail > div.tab-con > div:nth-of-type(1) > div.p-parameter > ul.parameter2.p-parameter-list > li'
        )
        for info in infos:
            temp = info.text
            for i in self.head_list:
                if i in temp:
                    # 只分隔一次，避免要保存的value中也包含了'：'
                    head, content = temp.split(self.colon_split, 1)
                    items[self.head_english_dict.get(head)] = content

        print(items)
        yield items

        if len(self.all_url_list) != 0:
            self.current_url = self.all_url_list.pop(0)
            yield Request(self.current_url, callback=self.parse, dont_filter=True)
        elif len(self.brand_url_list) != 0:
            self.current_url = self.brand_url_list.pop(0)
            brand_name = re.search(self.brand_extract_compile, self.current_url).group(1)
            self.current_brand = unquote(brand_name)
            yield Request(self.current_url, callback=self.per_page_url_callback, dont_filter=True)



