# -*- coding: utf-8 -*-
import scrapy
from scrapy_practice.items import ScrapyPracticeItem


class PracticeSpider(scrapy.Spider):
    name = 'practice'
    allowed_domains = ['http://lab.scrapyd.cn/']
    start_urls = ['http://lab.scrapyd.cn/']

    def parse(self, response):
        items = ScrapyPracticeItem()

        all_infos = response.css('#main > div')
        for info in all_infos:
            content = info.css('span.text::text').extract_first().replace('scrapy中文网（http://www.scrapyd.cn）整理', '')
            author = info.css('span > small.author::text').extract_first()
            tags = info.css('div.tags > a.tag::text').extract()

            items['content'] = content
            items['author'] = author
            items['tags'] = tags

            yield items
            


