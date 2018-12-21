# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZufangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    rooms = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    traffic = scrapy.Field()
    region = scrapy.Field()  # 区
    direction = scrapy.Field()  # 房子朝向
