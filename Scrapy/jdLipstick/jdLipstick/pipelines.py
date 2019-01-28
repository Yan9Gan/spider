# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from pymongo import MongoClient


class JdlipstickPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    collection = 'lipstick'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

        self.collection_list = []
        self.extract_list = []
        self.brand_compile = re.compile('.*?\（(.*?)\）')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.collection = item['brand']

        try:
            temp = re.search(self.brand_compile, self.collection).group(1)
        except:
            temp = self.collection
        finally:
            is_same = False
            for j in self.extract_list:
                if temp.lower() == j.lower():
                    self.collection = self.collection_list[self.extract_list.index(j)]
                    is_same = True
                    break
            if not is_same:
                self.extract_list.append(temp)
                self.collection_list.append(self.collection)

        # 一部分url会被重定向至广告url，不作存储
        if self.collection != '未知':
            self.db[self.collection].insert(dict(item))

        return item

    def close_spider(self, spider):
        self.client.close()
