# -*- coding: utf-8 -*-
import scrapy


class JdipadSpider(scrapy.Spider):
    name = 'jdipad'
    allowed_domains = ['https://www.jd.com/']
    start_urls = ['http://https://www.jd.com//']

    def parse(self, response):
        pass
