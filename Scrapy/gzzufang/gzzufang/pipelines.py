# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from pymongo import MongoClient


base_dir = os.getcwd()


class ZufangPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline():
    collection = 'zufang'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

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
        self.collection = item['region']
        if item['region'] == '不限':
            item['region'] = item['address'][0:2]
        self.db[self.collection].insert({
            "title": item["title"].strip(),
            "rooms": item["rooms"],
            "area": item["area"],
            "price": item["price"],
            "address": item["address"],
            "traffic": item["traffic"],
            "region": item["region"],
            "direction": item["direction"],
        })

        return item

    def close_spider(self, spider):
        self.client.close()




