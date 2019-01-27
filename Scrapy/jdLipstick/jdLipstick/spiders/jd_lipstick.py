# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request


class JdLipstickSpider(scrapy.Spider):
    name = 'jd_lipstick'
    allowed_domains = ['https://www.jd.com/']
    # start_urls = ['http://https://www.jd.com//']
    base_url = 'https://search.jd.com/'
    start_url = 'https://search.jd.com/Search?keyword=口红&enc=utf-8&wq=口红&pvid=33b0080a6043490faa5c27eb775a0975'

    current_url = ''
    page_url = '&page={}&s=56&click=0'

    brand_url_list = []
    all_page_url_list = []
    all_url_list = []

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
        yield Request(self.current_url, callback=self.per_page_url_callback, dont_filter=True)

    # 获取每一页url
    def per_page_url_callback(self, response):
        current_url_split = re.findall(self.url_split_compile, self.current_url)[0]
        base_url = current_url_split[0] + current_url_split[2] + current_url_split[1] + self.page_url

        soup = BeautifulSoup(response.body, 'html5lib')
        pages_num = soup.select('#J_topPage > span > i')[0].text
        for i in range(int(pages_num)):
            url = base_url.format(i+2)
            self.all_page_url_list.append(url)

        if len(self.brand_url_list) != 0:
            self.current_url = self.brand_url_list.pop(0)
            yield Request(self.current_url, callback=self.per_page_url_callback, dont_filter=True)
        else:
            self.current_url = self.all_page_url_list.pop(0)
            yield Request(self.current_url, callback=self.per_commodity_url_callback, dont_filter=True)

    # 获取每个商品页的url
    def per_commodity_url_callback(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        lis = soup.select('#J_goodsList > ul > li')
        for li in lis:
            commodity_url = li.find('a').get('href')
            if commodity_url.startswith('//item'):
                url = 'https:' + commodity_url
                self.all_url_list.append(url)
            else:
                continue

        if len(self.all_page_url_list) != 0:
            self.current_url = self.all_page_url_list.pop(0)
            yield Request(self.current_url, callback=self.per_commodity_url_callback, dont_filter=True)
        else:
            self.current_url = self.all_url_list.pop(0)
            yield Request(self.current_url, callback=self.parse, dont_filter=True)

    # 解析每个商品页
    def parse(self, response):
        if len(self.all_url_list) != 0:
            self.current_url = self.all_url_list.pop(0)
            yield Request(self.current_url, callback=self.parse, dont_filter=True)



