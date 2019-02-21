import re
import jieba
import pyecharts
from pymongo import MongoClient
from wordcloud import WordCloud


class Analysis(object):

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['lagou_python']
        self.collections = ['北京', '上海', '深圳', '杭州', '广州']

    def show_all(self):
        for collection_name in self.collections:
            for item in self.db[collection_name].find():
                print(item)

    def average(self):
        min_and_max_compile_1 = re.compile('(\d+)k-(\d+)k', re.I)
        min_and_max_compile_2 = re.compile('(\d+)k以上', re.I)

        head_list = []
        average_list = []

        for collection_name in self.collections:
            head_list.append(collection_name)
            total_average = 0

            for item in self.db[collection_name].find():
                salary = item['salary']
                if re.match(min_and_max_compile_1, salary):
                    min, max = re.findall(min_and_max_compile_1, salary)[0]
                elif re.match(min_and_max_compile_2, salary):
                    min, max = re.findall(min_and_max_compile_2, salary)[0]
                else:
                    min = max = 0

                average = (int(max) + int(min)) / 2
                total_average += average

            average_list.append(round(total_average / self.db[collection_name].count() * 1000, 2))

        bar = pyecharts.Bar('python岗位分析')
        bar.add('平均月薪', head_list, average_list, is_more_utils=True)
        bar.render('visualization/average.visualization')

    def experience_distribution(self):
        distribution_dict = {}

        for collection_name in self.collections:
            for item in self.db[collection_name].find():
                experience = item['experience']
                if experience in distribution_dict.keys():
                    distribution_dict[experience] += 1
                else:
                    distribution_dict[experience] = 1

        pie = pyecharts.Pie()
        pie.add('工作经验需求分布', list(distribution_dict.keys()), list(distribution_dict.values()), is_label_show=True)
        pie.render('visualization/experience_distribution.visualization')

    def education_needs(self):
        needs_dict = {}

        for collection_name in self.collections:
            for item in self.db[collection_name].find():
                education = item['education']
                if education in needs_dict.keys():
                    needs_dict[education] += 1
                else:
                    needs_dict[education] = 1

        pie = pyecharts.Pie()
        pie.add('学历需求', list(needs_dict.keys()), list(needs_dict.values()), is_label_show=True)
        pie.render('visualization/education_needs.visualization')

    def labels(self):
        labels_string = ''

        for collection_name in self.collections:
            for item in self.db[collection_name].find():
                labels = item['labels']
                temp = ' '.join(labels) + ' '
                labels_string += temp

        wc = WordCloud(
            max_words=2000,
            max_font_size=100,
            random_state=30
        )
        wc.generate_from_text(labels_string)
        wc.to_file('visualization/labels.jpg')

    def advantage(self):
        advantage_string = ''

        for collection_name in self.collections:
            for item in self.db[collection_name].find():
                advantage = item['advantage'].replace('，', '').replace(',', '') + ' '
                advantage_string += advantage

        wc = WordCloud(
            max_words=2000,
            max_font_size=100,
            random_state=30
        )
        wc.generate_from_text(advantage_string)
        wc.to_file('visualization/advantage.jpg')

    def describe(self):
        describe_string = ''

        for collection_name in self.collections:
            for item in self.db[collection_name].find():
                describe = item['describe'].replace('\n', '').replace(' ', '') + ' '
                describe_string += describe

        describe_string_list = jieba.cut(describe_string)
        new_string = ' '.join(describe_string_list)

        stop_list = ['任职', '要求', '优先']
        wc = WordCloud(
            max_words=2000,
            max_font_size=100,
            stopwords=stop_list,
            random_state=30,
        )
        wc.generate_from_text(new_string)
        wc.to_file('visualization/describe.jpg')


if __name__ == '__main__':
    al = Analysis()
    al.describe()


