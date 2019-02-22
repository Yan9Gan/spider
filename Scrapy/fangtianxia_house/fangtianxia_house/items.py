# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangtianxiaHouseItem(scrapy.Item):

    name = scrapy.Field()  # 名字
    average_price = scrapy.Field()  # 均价
    property_type = scrapy.Field()  # 物业类别
    feature = scrapy.Field()  # 项目特色
    house_type = scrapy.Field()  # 建筑类别
    decoration_status = scrapy.Field()  # 装修状况
    property_right = scrapy.Field()  # 产权年限
    location = scrapy.Field()  # 环线位置
    developers = scrapy.Field()  # 开发商
    house_address = scrapy.Field()  # 楼盘地址
    sale_status = scrapy.Field()  # 销售状态
    sale_discount = scrapy.Field()  # 销售优惠
    open_time = scrapy.Field()  # 开盘时间
    hand_time = scrapy.Field()  # 交房时间
    sale_address = scrapy.Field()  # 售楼地址
    phone = scrapy.Field()  # 咨询电话
    main_house_type = scrapy.Field()  # 主力户型
    area_cover = scrapy.Field()  # 占地面积
    area_build = scrapy.Field()  # 建筑面积
    plot_rate = scrapy.Field()  # 容积率
    green_rate = scrapy.Field()  # 绿化率
    park = scrapy.Field()  # 停车位
    house_num = scrapy.Field()  # 楼栋总数
    room_num = scrapy.Field()  # 总户数
    property_company = scrapy.Field()  # 物业公司
    property_cost = scrapy.Field()  # 物业费
    property_cost_description = scrapy.Field()  # 物业费描述
    floor_status = scrapy.Field()  # 楼层状况
    facilities = scrapy.Field()  # 周边设施
