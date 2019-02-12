import re
import pyecharts
from pymongo import MongoClient


client = MongoClient()


class Analysis(object):

    def __init__(self):
        self.db = client['lianjia_zufang']
        self.collection_name_list = self.db.list_collection_names()

    def show_all(self):
        for collection_name in self.collection_name_list:
            for info in self.db[collection_name].find():
                print(info)

    def average_price(self):
        average_price_list = []
        for collection_name in self.collection_name_list:
            total_price = 0
            for info in self.db[collection_name].find():
                total_price += int(info.get("house_price", 1)) / int(info.get("area", 1))
            average_price_list.append(round(total_price/self.db[collection_name].count(), 2))

        bar = pyecharts.Bar('广州租房信息分析')
        bar.use_theme('dark')
        bar.add('每月每平方平均价格', self.collection_name_list, average_price_list)
        bar.render('./analysis_html/average_price.visualization')

    def area_range(self):
        area_head_list = ['0-25平方米', '25-50平方米', '50-70平方米', '70-100平方米',
                          '100-140平方米', '140-200平方米', '200+平方米']
        range_list = [range(0, 25), range(25, 50), range(50, 70),
                      range(70, 100), range(100, 140), range(140, 200)]
        area_list = [0] * len(area_head_list)
        for collection_name in self.collection_name_list:
            for info in self.db[collection_name].find():
                area = int(info['area'])
                for i in range_list:
                    if area in i:
                        index = range_list.index(i)
                        area_list[index] += 1
                        break
                else:
                    area_list[6] += 1

        pie = pyecharts.Pie()
        pie.add('面积分布情况', area_head_list, area_list, is_label_show=True)
        pie.render('./analysis_html/area_range.visualization')

    def house_scale(self):
        pattern_compile = re.compile('.*?(\d+)室.*?(\d+)厅')

        pre_scale = [('1', '0'), ('1', '1'), ('2', '0'), ('2', '1'),
                     ('2', '2'), ('3', '1'), ('3', '2'), ('4', '1'),
                     ('4', '2'), ('5', '1'), ('5', '2')]
        scale_head = ['1室0厅', '1室1厅', '2室0厅', '2室1厅', '2室2厅', '3室1厅',
                      '3室2厅', '4室1厅', '4室2厅', '5室1厅', '5室2厅', '其他']
        scale_sum = [0] * len(scale_head)

        for collection_name in self.collection_name_list:
            for info in self.db[collection_name].find():
                pattern = info['pattern']

                try:
                    scale = re.findall(pattern_compile, pattern)[0]
                except:
                    continue
                else:
                    for i in pre_scale:
                        if scale == i:
                            index = pre_scale.index(i)
                            scale_sum[index] += 1
                            break
                    else:
                        index = len(scale_head) - 1
                        scale_sum[index] += 1

        pie = pyecharts.Pie()
        pie.add('房屋规模分布', scale_head, scale_sum, is_label_show=True)
        pie.render('./analysis_html/house_scale.visualization')


if __name__ == '__main__':
    als = Analysis()
    als.average_price()




