# -*- coding: utf-8 -*-
import os
import json
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from lagou.items import LagouItem


class LagouPythonSpider(scrapy.Spider):
    name = 'lagou_python'
    allowed_domains = ['https://www.lagou.com/']
    start_url = 'https://www.lagou.com/jobs/list_python?px=default&city={}#filterBox'
    city_list = ['北京', '上海', '深圳', '杭州', '广州']
    json_path = os.path.join(os.getcwd(), 'lagou_python.json')

    url_dict = {}

    current_city_list = []
    current_city = ''
    current_url_list = []
    current_url = ''

    def start_requests(self):
        # 获取json数据
        with open(self.json_path, 'r', encoding='utf-8') as f:
            json_data = f.read()
        self.url_dict = json.loads(json_data)

        self.current_city_list = list(self.url_dict.keys())
        self.current_city = self.current_city_list.pop(0)
        self.current_url_list = self.url_dict.get(self.current_city)
        self.current_url = self.current_url_list.pop(0)

        return [scrapy.FormRequest(self.current_url, callback=self.parse)]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')

        try:
            items = LagouItem()

            position_name = soup.select(
                'body > div.position-head > div > div.position-content-l > div > span'
            )[0].text

            salary = soup.select(
                'body > div.position-head > div > div.position-content-l > dd > p:nth-of-type(1) > span.salary'
            )[0].text.replace(' ', '')

            experience = soup.select(
                'body > div.position-head > div > div.position-content-l > dd > p:nth-of-type(1) > span:nth-of-type(3)'
            )[0].text.replace('经验', '').replace(' /', '')

            education = soup.select(
                'body > div.position-head > div > div.position-content-l > dd > p:nth-of-type(1) > span:nth-of-type(4)'
            )[0].text.replace(' /', '')

            labels_li = soup.select(
                'body > div.position-head > div > div.position-content-l > dd > ul > li'
            )
            labels = []
            for li in labels_li:
                labels.append(li.text)

            advantage = soup.select(
                '#job_detail > dd.job-advantage > p'
            )[0].text

            describe = soup.select(
                '#job_detail > dd.job_bt > div'
            )[0].text

            items['city'] = self.current_city
            items['position_name'] = position_name
            items['salary'] = salary
            items['experience'] = experience
            items['education'] = education
            items['labels'] = labels
            items['advantage'] = advantage
            items['describe'] = describe

            yield items

        except:
            pass

        if len(self.current_url_list) != 0:
            self.current_url = self.current_url_list.pop(0)
            yield Request(self.current_url, callback=self.parse, dont_filter=True)
        elif len(self.current_city_list) != 0:
            self.current_city = self.current_city_list.pop(0)
            self.current_url_list = self.url_dict.get(self.current_city)
            self.current_url = self.current_url_list.pop(0)
            yield Request(self.current_url, callback=self.parse, dont_filter=True)


