import os
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient


class LagouPython(object):
    def __init__(self):
        self.url = 'https://www.lagou.com/jobs/list_python?px=default&city={}#filterBox'
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': '_ga=GA1.2.1095685692.1546593145; user_trace_token=20190104171224-d9a30f30-1000-11e9-bb9c-525400f775ce; LGUID=20190104171224-d9a3142f-1000-11e9-bb9c-525400f775ce; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216818243795170-0849d5e07fa35d-b781636-2073600-168182437964bb%22%2C%22%24device_id%22%3A%2216818243795170-0849d5e07fa35d-b781636-2073600-168182437964bb%22%7D; JSESSIONID=ABAAABAAAGGABCB518A3EF177FC192C2CCAFC3F96A96433; _gid=GA1.2.50133432.1548900617; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=search_code; X_MIDDLE_TOKEN=1559d83776ad1865f0ad3fb084158970; SEARCH_ID=1b9d0c9f8de040dd80225eeec33284a9; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1546593243,1548900617,1548901354,1548918473; LGSID=20190131155300-3ae51828-252d-11e9-bcae-525400f775ce; _gat=1; LG_LOGIN_USER_ID=2b8565f561e20df4f878970dd539a2082edfbc563ca681be8ca41451040a4dd6; _putrc=B84992A2181BF4C6123F89F2B170EADC; login=true; unick=%E6%9D%A8%E6%B7%A6; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=74; gate_login_token=4f97cdf18419091eb9eca968f116fca64a6eab01ae40c678528aa5da1777995c; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1548923336; LGRID=20190131162914-4aeeda3d-2532-11e9-bcb9-525400f775ce',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.lagou.com/jobs/list_python?px=default&city=%E6%9D%AD%E5%B7%9E',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': 'None',
            'X-Requested-With': 'XMLHttpRequest',
        }

        self.city_list = ['北京', '上海', '深圳', '杭州', '广州']
        self.json_path = os.path.join(os.getcwd(), 'lagou_python.json')

        self.client = MongoClient()
        self.db = self.client['lagou_python']

        self.spider()

    def spider(self):
        # 获取json数据
        with open(self.json_path, 'r', encoding='utf-8') as f:
            json_data = f.read()
        url_dict = json.loads(json_data)

        for city, url_list in url_dict.items():
            collection = self.db[city]
            for url in url_list:
                print(url)
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    html = response.text
                    soup = BeautifulSoup(html, 'html5lib')
                    items = {}

                    head_infos = soup.select(
                        'body > div.position-head > div > div.position-content-l'
                    )[0]

                    # 工作职位名称
                    job_name = head_infos.select(
                        'div > span'
                    )[0].text

                    # 薪资
                    salary = head_infos.select(
                        'dd > p:nth-of-type(1) > span.salary'
                    )[0].text

                    # 工作经验
                    experiment = head_infos.select(
                        'dd > p:nth-of-type(1) > span:nth-of-type(3)'
                    )[0].text.replace('/', '').replace(' ', '').replace('经验', '')

                    # 学历要求
                    education_need = head_infos.select(
                        'dd > p:nth-of-type(1) > span:nth-of-type(4)'
                    )[0].text.replace('/', '').replace(' ', '')

                    # 岗位类型（全职、兼职）
                    type = head_infos.select(
                        'dd > p:nth-of-type(1) > span:nth-of-type(5)'
                    )[0].text

                    # 标签
                    try:
                        labels = head_infos.select(
                            'dd > ul'
                        )[0].text.strip().replace('\n', '|').replace(' ', '')
                    except IndexError:
                        labels = ''

                    job_infos = soup.select(
                        '#job_detail'
                    )[0]

                    # 职位优势
                    advantage = job_infos.select(
                        'dd.job-advantage > p'
                    )[0].text.replace(',', '|').replace('，', '|').replace('；', '|').replace(' ', '')

                    # 任职要求
                    duty_and_requirements = job_infos.select(
                        'dd.job_bt > div'
                    )[0]
                    requirements = ''
                    flag = False
                    count = 1
                    while 1:
                        try:
                            p_line = duty_and_requirements.select(
                                'p:nth-of-type({})'.format(count)
                            )[0].text
                        except:
                            break
                        else:
                            if '要求' in p_line or '资格' in p_line or '加分' in p_line:
                                flag = True
                            elif '职责' in p_line:
                                flag = False
                            elif flag:
                                requirements += p_line
                            else:
                                pass
                        finally:
                            count += 1

                    print(job_name, salary, experiment, education_need, type, labels, advantage)
                    items['job_name'] = job_name
                    items['salary'] = salary
                    items['experiment'] = experiment
                    items['education_need'] = education_need
                    items['type'] = type
                    items['labels'] = labels
                    items['advantage'] = advantage
                    items['requirements'] = requirements

                    if collection.insert(items):
                        print('ok')

    def get_url(self):
        url_dict = {}
        for city in self.city_list:
            # 相同城市的url保存在一个list中
            url_dict[city] = []
            # 打开chrome
            browser = webdriver.Chrome()

            browser.get(self.url.format(city))
            pages = browser.find_element_by_css_selector('#order > li > div.item.page > div.page-number > span.span.totalNum').text
            for i in range(int(pages)-1):
                items = browser.find_elements_by_css_selector('#s_position_list > ul > li')
                for item in items:
                    # 找到a标签中的href属性
                    url = item.find_element_by_css_selector('div.list_item_top > div.position > div.p_top > a').get_attribute('href')
                    print(url)
                    url_dict[city].append(url)
                # 点击下一页
                browser.find_element_by_css_selector('#s_position_list > div.item_con_pager > div > span.pager_next').click()
                # 等待1s，防止页面还没完成跳转
                time.sleep(1)
            print(url_dict[city])

            browser.close()

        with open(self.json_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(url_dict, indent=4))


if __name__ == '__main__':
    lgp = LagouPython()

