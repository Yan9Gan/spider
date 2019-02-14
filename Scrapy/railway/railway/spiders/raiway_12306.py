# -*- coding: utf-8 -*-
import os
import json
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from railway.items import RailwayItem


class Raiway12306Spider(scrapy.Spider):
    name = 'raiway_12306'
    allowed_domains = ['www.12306.cn']
    start_urls = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'

    def __init__(self, fs, ts, date, id, *args, **kwargs):
        super(Raiway12306Spider, self).__init__(*args, **kwargs)
        self.fs = fs
        self.ts = ts
        self.date = date
        self.id = id

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

        items = RailwayItem()

        for item in results:
            item_list = item.split('|')
            train_number = item_list[3]

            from_station = station_dict[item_list[6]]
            to_station = station_dict[item_list[7]]

            from_time = item_list[8]
            to_time = item_list[9]
            duration = item_list[10]

            if train_number[0] in ['C', 'D', 'G']:
                tdz = item_list[32] or '-'  # 商务座/特等座
                ydz = item_list[31] or '-'  # 一等座
                edz = item_list[30] or '-'  # 二等座
                gjrw = '-'  # 高级软卧
                rw = '-'  # 软卧/一等卧
                dw = '-'  # 动卧
                yw = '-'  # 硬卧/二等卧
                rz = '-'  # 软座
                yz = '-'  # 硬座
                wz = item_list[26] or '-'  # 无座

            else:
                tdz = '-'  # 商务座/特等座
                ydz = '-'  # 一等座
                edz = '-'  # 二等座
                gjrw = item_list[21] or '-'  # 高级软卧
                rw = item_list[23] or '-'  # 软卧/一等卧
                dw = '-'  # 动卧
                yw = item_list[28] or '-'  # 硬卧/二等卧
                rz = item_list[24] or '-'  # 软座
                yz = item_list[29] or '-'  # 硬座
                wz = item_list[26] or '-'  # 无座

            items['id'] = self.id
            items['train_number'] = train_number
            items['from_station'] = from_station
            items['to_station'] = to_station
            items['from_time'] = from_time
            items['to_time'] = to_time
            items['duration'] = duration
            items['tdz'] = tdz
            items['ydz'] = ydz
            items['edz'] = edz
            items['gjrw'] = gjrw
            items['rw'] = rw
            items['dw'] = dw
            items['yw'] = yw
            items['rz'] = rz
            items['yz'] = yz
            items['wz'] = wz

            print(self.id, train_number, from_station, to_station, from_time, to_time, duration)
            print(tdz, ydz, edz, gjrw, rw, dw, yw, rz, yz, wz)

            yield items
