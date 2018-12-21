# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
from gzzufang.items import ZufangItem


class ZufangSpider(scrapy.Spider):
    name = 'zufang'
    allowed_domains = ['gz.zu.fang.com']
    # start_urls = ['http://gz.zu.fang.com/']
    baseUrl = 'http://gz.zu.fang.com/'
    allUrlList = []
    headUrlList = []

    def start_requests(self):
        start_url = self.baseUrl
        return [scrapy.FormRequest(start_url, callback=self.head_url_callback)]

    def head_url_callback(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        dl = soup.find_all('dl', attrs={'id': 'rentid_D04_01'})
        areas = dl[0].find_all('a')
        for area in areas:
            if area.text == '不限':
                self.headUrlList.append(self.baseUrl)
                continue
            if '周边' in area.text:
                continue
            self.headUrlList.append(self.baseUrl + area['href'])

        # self.logger.info('area root url', self.allUrlList)

        url = self.headUrlList.pop(0)
        yield Request(url, callback=self.all_url_callback, dont_filter=True)

    def all_url_callback(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        div = soup.find_all(id='rentid_D10_01')
        span = div[0].find_all('span')
        span_text = span[0].text[1:-1]

        for index in range(int(span_text)):
            if index == 0:
                pass
            else:
                if self.baseUrl == response.url:
                    self.allUrlList.append(response.url + 'house/i3'+str(index+1)+'/')
                    continue
                self.allUrlList.append(response.url + 'i3'+str(index+1)+'/')

        self.logger.info('per page url', self.allUrlList)

        if len(self.headUrlList) == 0:
            url = self.allUrlList.pop(0)
            # self.logger.info(url)
            yield Request(url, callback=self.parse, dont_filter=True)
        else:
            url = self.headUrlList.pop(0)
            yield Request(url, callback=self.all_url_callback, dont_filter=True)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        dds = soup.find_all('dd', attrs={'class': 'info rel'})
        for dd in dds:
            item = ZufangItem()
            roomMsg = dd.find_all('p', attrs={'class': 'font15 mt12 bold'})[0].text.strip().split('|')

            # 每个取值都做一次异常捕获（有些信息不全，用None代替）
            try:
                title = dd.find_all('p', attrs={'class': 'title'})[0].text.strip()
            except:
                title = None

            try:
                room = roomMsg[1].strip()
            except:
                room = None

            try:
                area = roomMsg[2].strip()[:len(roomMsg[2]) - 1]
            except:
                area = None

            try:
                price = dd.find_all('div', attrs={'class': 'moreInfo'})[0].text.strip()
                price = int(float(price[:len(price) - 3]))
            except:
                price = None

            try:
                address = dd.find_all('p', attrs={'class': 'gray6 mt12'})[0].text.strip()
            except:
                address = None

            try:
                traffic = dd.find_all('span', attrs={'class': 'note subInfor'})[0].text.strip()
            except:
                traffic = None

            try:
                region = address.split('-')[0].strip()
            except:
                region = None

            try:
                direction = roomMsg[3].strip()
            except:
                direction = None

            item['title'] = title
            item['room'] = room
            item['area'] = area
            item['price'] = price
            item['address'] = address
            item['traffic'] = traffic
            item['region'] = region
            item['direction'] = direction

            print(item)
        if len(self.allUrlList) != 0:
            url = self.allUrlList.pop(0)
            yield Request(url, callback=self.parse, dont_filter=True)



