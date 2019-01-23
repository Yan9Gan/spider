import pyecharts
from pymongo import MongoClient


client = MongoClient('172.18.115.200', 27017)


class Analysis(object):

    def __init__(self):
        self.db = client['lianjia_zufang']
        self.collection_name_list = self.db.list_collection_names()

    def average_price(self):
        average_price_list = []
        for collection_name in self.collection_name_list:
            total_price = 0
            for info in self.db[collection_name].find():
                total_price += int(info.get("house_price", 1)) / int(info.get("area", 1))
            average_price_list.append(round(total_price/self.db[collection_name].count(), 2))

        bar = pyecharts.Bar('广州租房信息分析')
        bar.add('每月每平方平均价格', self.collection_name_list, average_price_list)
        bar.render('./analysis_html/average_price.html')


if __name__ == '__main__':
    als = Analysis()
    als.average_price()




