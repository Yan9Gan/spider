# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdlipstickItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    brand = scrapy.Field()
    price = scrapy.Field()
    commodity_name = scrapy.Field()
    weight = scrapy.Field()
    channel = scrapy.Field()
    makeup_effect = scrapy.Field()
    color_type = scrapy.Field()
    origin = scrapy.Field()
