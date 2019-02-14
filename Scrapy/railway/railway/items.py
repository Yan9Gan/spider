# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RailwayItem(scrapy.Item):

    id = scrapy.Field()  # 标识码
    train_number = scrapy.Field()  # 车次
    from_station = scrapy.Field()  # 出发站
    to_station = scrapy.Field()  # 到达站
    from_time = scrapy.Field()  # 出发时间
    to_time = scrapy.Field()  # 到达时间
    duration = scrapy.Field()  # 历时
    tdz = scrapy.Field()  # 商务座/特等座
    ydz = scrapy.Field()  # 一等座
    edz = scrapy.Field()  # 二等座
    gjrw = scrapy.Field()  # 高级软卧
    rw = scrapy.Field()  # 软卧/一等卧
    dw = scrapy.Field()  # 动卧
    yw = scrapy.Field()  # 硬卧/二等卧
    rz = scrapy.Field()  # 软座
    yz = scrapy.Field()  # 硬座
    wz = scrapy.Field()  # 无座
