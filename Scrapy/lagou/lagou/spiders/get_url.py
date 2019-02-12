import os
import json
import time
from selenium import webdriver


def get_url():
    base_url = 'https://www.lagou.com/jobs/list_python?px=default&city={}#filterBox'
    city_list = ['北京', '上海', '深圳', '杭州', '广州']
    json_path = os.path.join(os.getcwd(), 'lagou_python.json')

    url_dict = {}
    for city in city_list:
        # 相同城市的url保存在一个list中
        url_dict[city] = []
        # 打开chrome
        browser = webdriver.Chrome()

        browser.get(base_url.format(city))
        pages = browser.find_element_by_css_selector(
            '#order > li > div.item.page > div.page-number > span.span.totalNum'
        ).text
        for i in range(int(pages) - 1):
            items = browser.find_elements_by_css_selector('#s_position_list > ul > li')
            for item in items:
                # 找到a标签中的href属性
                url = item.find_element_by_css_selector(
                    'div.list_item_top > div.position > div.p_top > a'
                ).get_attribute('href')
                print(url)
                url_dict[city].append(url)
            # 点击下一页
            browser.find_element_by_css_selector(
                '#s_position_list > div.item_con_pager > div > span.pager_next'
            ).click()
            # 等待1s，防止页面还没完成跳转
            time.sleep(1)
        print(url_dict[city])

        browser.close()

    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(url_dict, indent=4))


if __name__ == '__main__':
    get_url()

