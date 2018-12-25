import re
import pymongo


class Analysis(object):

    def __init__(self, MONGO_DB):
        self.MONGO_CLIENT = pymongo.MongoClient('localhost', 27017)
        self.db = self.MONGO_CLIENT[MONGO_DB]
        self.COLLECTIONS_LIST = self.db.list_collection_names(session=None)
        self.ROOMS = 1

    def get_info(self):
        for region in self.COLLECTIONS_LIST:
            if len(region) > 2 or region in ['白云', '黄埔', '萝岗']:
                continue
            collection = self.db[region]
            cursor = collection.find({'traffic': re.compile('距[123568]?号线'),
                                      'rooms': re.compile(str(self.ROOMS)+'室1厅'),
                                      'price': {'$lte': 1200 * self.ROOMS}})
            print(region, ':', cursor.count())
            for item in cursor:
                print(item)

    def get_histogram(self):
        from pyecharts import Bar

        region_list = []
        count_list = []

        for region in self.COLLECTIONS_LIST:
            if len(region) > 2:
                continue

            collection = self.db[region]
            cursor = collection.find()

            region_list.append(region)
            count_list.append(cursor.count())

        bar = Bar('样本数量', '')
        bar.use_theme('light')
        bar.add('广州租房信息', region_list, count_list, is_more_utils=True)
        bar.render('count.templates')

    def statistics_average_price(self):
        from pyecharts import Bar

        region_list = []
        average_price_list = []

        for region in self.COLLECTIONS_LIST:
            if len(region) > 2:
                continue

            region_list.append(region)
            single_average_price_list = []

            collection = self.db[region]
            cursor = collection.find()
            for item in cursor:
                area = int(item.get('area'))
                price = int(item.get('price'))

                single_average_price = price / area
                single_average_price_list.append(single_average_price)

            average_price = sum(single_average_price_list) / len(single_average_price_list)
            average_price_list.append(average_price)

        bar = Bar('每平米价格', '')
        bar.use_theme('light')
        bar.add('广州租房信息', region_list, average_price_list, is_more_utils=True)
        bar.render('average_price_histogram.templates')

    def statistics_areas(self):
        from pyecharts import Pie

        areas_round_list = ['0-30平方米', '30-60平方米', '60-90平方米', '90-120平方米',
                            '120-180平方米', '180-300平方米', '300+平方米']
        areas_count_list = [0] * 7

        for region in self.COLLECTIONS_LIST:
            if len(region) > 2:
                continue

            collection = self.db[region]
            cursor = collection.find()
            for item in cursor:
                area = int(item.get('area'))
                if area < 120:
                    areas_count_list[area//30] += 1
                elif area < 300:
                    areas_count_list[area//60+2] += 1
                else:
                    areas_count_list[6] += 1

        pie = Pie('租房面积统计')
        pie.add('广州租房信息', areas_round_list, areas_count_list, is_label_show=True)
        pie.render('areas_round.templates')


if __name__ == '__main__':
    zf = Analysis('ZuFang')
    zf.statistics_areas()







