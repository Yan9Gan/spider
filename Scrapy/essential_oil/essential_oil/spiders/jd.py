# -*- coding: utf-8 -*-
import re
import random
import string
import scrapy
import logging
from selenium import webdriver
from scrapy.http import Request
from urllib.parse import urlencode


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['www.jd.com']
    base_url = 'https://search.jd.com/Search?'

    params = {
        'keyword': '',
        'enc': 'utf-8',
        'wq': '',
        'pvid': '3dc381b4b6c847b8a1ebdf9c31e6fce3'
    }

    logger = logging.getLogger('jd')

    def __init__(self, keyword, *args, **kwargs):
        super(JdSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.params['keyword'] = self.keyword
        self.json_path = 'brand_url.json'

        self.start_url = self.base_url + urlencode(self.params)

        self.current_name = self.current_url = ''

        self.page_url_list = []
        self.detail_url_list = []

        self.url_compile = re.compile('(.*?)(&wq=.*)(&pvid=.*)')
        self.comment_compile = re.compile('\((.*)\)')

        self.chinese_to_english_dict = {
            '商品名称': 'name',
            '商品编号': 'number',
            '商品毛重': 'weight',
            '净含量': 'net_content',
            '商品产地': 'origin',
            '货号': 'item_num',
            '适合肤质': 'skin_suitable',
            '功效': 'effect',
            '香型': 'type',
            '国产/进口': 'source',
            '分类': 'classify',
            '适用人群': 'people_suitable',
            '适用部位': 'position_suitable',
            '晒图': 'image',
            '视频晒单': 'video',
            '追评': 'add',
            '好评': 'good',
            '中评': 'normal',
            '差评': 'bad',
        }

        self.colon_split = '：'

        self.browser = webdriver.PhantomJS()
        # self.browser.set_page_load_timeout(30)

    def closed(self, spider):
        print("spider closed")
        self.browser.close()

    def get_random_digits(self):
        n = random.choice([2, 3])
        digits = ''.join(random.sample(string.digits, n))

        return digits

    def start_requests(self):
        self.current_url = self.start_url
        yield Request(self.current_url, callback=self.get_page, dont_filter=True)

    def get_page(self, response):
        print(response.body)
        pages = int(response.xpath('//*[@id="J_topPage"]/span/i/text()').extract_first())
        for page in range(pages):
            url_list = re.findall(self.url_compile, self.current_url)[0]
            digit = self.get_random_digits()
            url = url_list[0] + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2' + url_list[1] + '&stock=1&page={}&s={}&click=0'.format(page+2, digit)
            self.page_url_list.append(url)

        if len(self.page_url_list) != 0:
            self.current_url = self.page_url_list.pop(0)
            yield Request(self.current_url, callback=self.get_detail, dont_filter=True)

    def get_detail(self, response):
        if response.status == 500:
            if len(self.page_url_list) != 0:
                self.current_url = self.page_url_list.pop(0)
                yield Request(self.current_url, callback=self.get_detail, dont_filter=True)
        else:
            detail_lis = response.xpath('//*[@id="J_goodsList"]/ul/li')
            for li in detail_lis:
                url = li.xpath('./div/div/a/@href').extract_first()
                if url and url.startswith('//item'):
                    self.detail_url_list.append('https:' + url)

            if len(self.detail_url_list) != 0:
                self.current_url = self.detail_url_list.pop(0)
                yield Request(self.current_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        self.logger.info(response.status)
        if response.status == 500:
            if len(self.detail_url_list) != 0:
                self.current_url = self.detail_url_list.pop(0)
                yield Request(self.current_url, callback=self.parse, dont_filter=True)
        else:
            items = {'brand': '', 'url': '', 'title': '', 'price': '', 'name': '', 'number': '',
                     'weight': '', 'net_content': '', 'origin': '', 'item_num': '',
                     'skin_suitable': '', 'effect': '', 'type': '', 'source': '', 'classify': '',
                     'people_suitable': '', 'position_suitable': '', 'good_rate': '', 'impression': '',
                     'image': '', 'video': '', 'add': '', 'good': '', 'normal': '', 'bad': ''}

            title = response.xpath('/html/body/div[8]/div/div[2]/div[1]/text()').extract_first()
            if title:
                items['title'] = title.strip()
            price = response.xpath('/html/body/div[8]/div/div[2]/div[4]/div/div[1]/div[2]/span[1]/span[2]/text()').extract_first()

            brand = response.xpath('//*[@id="parameter-brand"]/li/a/text()').extract_first()
            items['brand'] = brand

            infos = response.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li')
            for info in infos:
                contents = info.xpath('./text()').extract_first()
                try:
                    head, content = contents.split(self.colon_split)
                    if head in self.chinese_to_english_dict.keys():
                        head = self.chinese_to_english_dict.get(head)
                        items[head] = content
                except ValueError:
                    continue

            try:
                impression_tags = response.xpath('//*[@id="comment"]/div[2]/div[1]/div[2]/div/span')
                temp_list = []
                for tag in impression_tags:
                    temp_list.append(tag.xpath('./text()').extract_first())
            except:
                impression = ''
            else:
                impression = ','.join(temp_list)
            items['impression'] = impression

            comment_infos = response.xpath('//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li')
            for comment in comment_infos:
                head = comment.xpath('./a/text()').extract_first()
                num = comment.xpath('./a/em/text()').extract_first()
                if head in self.chinese_to_english_dict.keys():
                    head = self.chinese_to_english_dict.get(head)
                    num = re.search(self.comment_compile, num).group(1)
                    items[head] = num

            items['url'] = self.current_url
            items['price'] = price

            good_rate = response.xpath('//*[@id="comment"]/div[2]/div[1]/div[1]/div/text()').extract_first()
            if good_rate:
                items['good_rate'] = good_rate + '%'

            yield items

        if len(self.detail_url_list) != 0:
            self.current_url = self.detail_url_list.pop(0)
            yield Request(self.current_url, callback=self.parse, dont_filter=True)

        elif len(self.page_url_list) != 0:
            self.current_url = self.page_url_list.pop(0)
            yield Request(self.current_url, callback=self.get_detail, dont_filter=True)


