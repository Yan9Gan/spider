import jieba
import pyecharts
from fuzzywuzzy import fuzz
from pymongo import MongoClient
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator


class Analysis(object):

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['jd_lipstick']
        self.collections = self.db.list_collection_names()

    def show_all(self):
        for collection_name in self.collections:
            for item in self.db[collection_name].find():
                if 'commodity_name' not in item.keys():
                    continue
                print(item)

    def average_price(self):
        head_list = []
        price_list = []
        for collection_name in self.collections:
            collection = self.db[collection_name]
            sum = 0
            count = 0
            for item in collection.find():
                if 'commodity_name' not in item.keys():
                    continue
                if len(item['price']) <= 1:
                    continue

                price = float(item['price'][1:])
                sum += price
                count += 1
            if count != 0:
                head_list.append(collection_name)
                price_list.append(round(sum / count, 2))

        bar = pyecharts.Bar('京东口红')
        bar.add('各品牌平均价格', head_list, price_list, is_more_utils=True, xaxis_rotate=50, xaxis_name_size=8)
        bar.render('html/average.html')

    def amount(self):
        head_list = []
        count_list = []
        for collection_name in self.collections:
            count = 0
            for item in self.db[collection_name].find():
                if 'commodity_name' not in item.keys():
                    continue
                count += 1

            if count != 0:
                head_list.append(collection_name)
                count_list.append(count)

        pie = pyecharts.Pie('京东口红')
        pie.add('数量', head_list, count_list, is_label_show=True)
        pie.render('html/amount.html')

    def title_extract(self):
        string = ''
        for collection_name in self.collections:
            for item in self.db[collection_name].find():
                if 'commodity_name' not in item.keys():
                    continue
                title = item.get('commodity_name', '')
                color_type = item.get('color_type', '')
                string += title
                string += color_type

        image_path = 'kouhong.jpg'
        backgroud_image = plt.imread(image_path)
        collection_string = ' '.join(self.collections)
        stop_list = list(jieba.cut(collection_string))
        stop_list += ['正常发货', '顺丰配送', '京东配达', '国内专柜', '京东送达', '专柜正品', '其它']

        wc = WordCloud(
            background_color="white",
            mask=backgroud_image,
            max_words=2000,
            stopwords=stop_list,
            max_font_size=100,
            random_state=30
        )
        wc.generate_from_text(string)
        img_colors = ImageColorGenerator(backgroud_image)
        wc.recolor(color_func=img_colors)
        wc.to_file('temp.jpg')


if __name__ == '__main__':
    al = Analysis()
    al.title_extract()


