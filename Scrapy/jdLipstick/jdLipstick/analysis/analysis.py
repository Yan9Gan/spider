import pyecharts
from pymongo import MongoClient


class Analysis(object):

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['jd_lipstick']
        self.collections = self.db.list_collection_names()

    def show_all(self):
        for collection_name in self.collections:
            for item in self.db[collection_name].find():
                print(item)

    def average_price(self):
        price_list = []
        for collection_name in self.collections:
            collection = self.db[collection_name]
            sum = 0
            for item in collection.find():
                price = float(item['price'][1:])
                sum += price
            price_list.append(round(sum / collection.count(), 2))

        bar = pyecharts.Bar('京东口红')
        bar.add('各品牌平均价格', self.collections, price_list, is_more_utils=True, xaxis_rotate=50, xaxis_name_size=8)
        bar.render('html/average.html')

    def amount(self):
        count_list = []
        for collection_name in self.collections:
            count_list.append(self.db[collection_name].count())

        pie = pyecharts.Pie('京东口红')
        pie.add('数量', self.collections, count_list, is_label_show=True)
        pie.render('html/amount.html')

    def check(self):
        for collection_name in self.collections:
            if 'VNK' in collection_name:
                print(collection_name)
                collection = self.db[collection_name]
                for item in collection.find():
                    print(item)
                    price = float(item['price'][1:])
                    print(price)


if __name__ == '__main__':
    al = Analysis()
    al.check()


