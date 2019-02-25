# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request


class StatisticsSpider(scrapy.Spider):
    name = 'statistics'
    allowed_domains = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html']
    base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'

    def start_requests(self):
        url = self.base_url + 'index.html'
        yield Request(url, callback=self.get_city)

    def get_city(self, response):
        soup = BeautifulSoup(response.body, 'html5lb')
        trs = soup.select(
            'body > table:nth-of-type(3) > tbody > tr:nth-of-type(1) > td > table > tbody > tr:nth-of-type(2) > td > table > tbody > tr > td > table > tbody > tr[class="provincetr"]'
        )
        for tr in trs:
            for td in tr.find('td'):
                print(td.text)

    def parse(self, response):
        pass
