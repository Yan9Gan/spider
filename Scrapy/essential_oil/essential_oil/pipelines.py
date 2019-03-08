# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook


class EssentialOilPipeline(object):
    def process_item(self, item, spider):
        return item


class ExcelPipeline(object):

    def __init__(self):
        self.excel_path = 'EssentialOil.xlsx'
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['品牌', '链接', '标题', '价格', '商品名称', '商品编号',
                        '商品毛重', '净含量', '商品产地', '货号', '适合肤质',
                        '功效', '香型', '国产/进口', '分类', '适用人群', '适用部位',
                        '好评率', '买家印象', '晒图', '视频晒单', '追评', '好评',
                        '中评', '差评'])

    def process_item(self, item, spider):
        content = list(item.values())
        self.ws.append(content)

        return item

    def close_spider(self, spider):
        self.wb.save(self.excel_path)
