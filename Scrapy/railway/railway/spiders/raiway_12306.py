# -*- coding: utf-8 -*-
import os
import json
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request


class Raiway12306Spider(scrapy.Spider):
    name = 'raiway_12306'
    allowed_domains = ['www.12306.cn']
    start_urls = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'

    def __init__(self, fs, ts, date, *args, **kwargs):
        super(Raiway12306Spider, self).__init__(*args, **kwargs)
        self.fs = fs
        self.ts = ts
        self.date = date

        self.json_path = os.path.join(os.getcwd(), 'station_code.json')
        with open(self.json_path, 'r') as json_file:
            json_data = json.loads(json_file.read())

        self.fs_code = json_data[self.fs]
        self.ts_code = json_data[self.ts]

        self.url = self.start_urls.format(self.date, self.fs_code, self.ts_code)

    def start_requests(self):
        yield Request(self.url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        infos = json.loads(response.body)
        data = infos['data']
        station_dict = data['map']
        results = data['result']
        for item in results:
            item_list = item.split('|')
            print(item_list)
            train_number = item_list[3]

            from_station = station_dict[item_list[6]]
            to_station = station_dict[item_list[7]]

            from_time = item_list[8]
            to_time = item_list[9]
            duration = item_list[10]

            if train_number[0] in ['C', 'D', 'G']:
                tdz = item_list[32]  # 商务座/特等座
                ydz = item_list[31]  # 一等座
                edz = item_list[30]  # 硬卧/二等座
                wz = item_list[26]  # 无座

                print(train_number, from_station, to_station, from_time, to_time, duration)
                print(tdz, ydz, edz, wz, wz)

