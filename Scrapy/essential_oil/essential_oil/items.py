# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EssentialOilItem(scrapy.Item):

    brand = scrapy.Field()  # 品牌
    url = scrapy.Field()  # 链接
    title = scrapy.Field()  # 标题
    price = scrapy.Field()  # 价格
    name = scrapy.Field()  # 商品名称
    number = scrapy.Field()  # 商品编号
    weight = scrapy.Field()  # 商品毛重
    origin = scrapy.Field()  # 商品产地
    item_num = scrapy.Field()  # 货号
    skin_suitable = scrapy.Field()  # 适合肤质
    effect = scrapy.Field()  # 功效
    type = scrapy.Field()  # 香型
    source = scrapy.Field()  # 国产/进口
    classify = scrapy.Field()  # 分类
    people_suitable = scrapy.Field()  # 适用人群
    position_suitable = scrapy.Field()  # 适用部位
    net_content = scrapy.Field()  # 净含量
    good_rate = scrapy.Field()  # 好评率
