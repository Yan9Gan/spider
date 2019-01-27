import re
from functools import partial
from selenium import webdriver
from pymongo import MongoClient
from multiprocessing import Pool


client = MongoClient()
db1 = client['jdLipstick']
collections_name_list1 = db1.list_collection_names()

db2 = client['jdLipstickData']

# browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
data_head = ['商品毛重', '国产/进口', '妆效', '色系', '产品产地']


def parse_page():
    for collection_name in collections_name_list1:
        collection = db1[collection_name]
        # for data in collection.find():
        #     parse_one_page(data, collection_name)

        pool = Pool(processes=8)
        pool.map(partial(parse_one_page, collection_name=collection_name), collection.find())
        pool.close()
        pool.join()


def parse_one_page(data, collection_name):
    url = data.get('url')
    try:
        browser = webdriver.Chrome()

    except:
        print('打开chrome失败')

    else:
        try:
            browser.get(url)

        except:
            print('打开' + url + '失败')

        else:
            print(url)
            item = {}
            item['url'] = url
            try:
                infos_div = browser.find_element_by_class_name('itemInfo-wrap')

            except:
                print('该页面没有商品信息')

            else:
                # 价格
                price = infos_div.find_element_by_class_name('p-price').get_attribute('innerText')
                item['价格'] = price
                try:
                    color_num = browser.find_element_by_xpath(
                        '//*[@id="choose-attr-1"]/div[2]/div[@class="item  selected"]'
                    ).text
                    item['色号'] = color_num
                except:
                    item['色号'] = None
                good_introduces = browser.find_element_by_class_name('parameter2')
                for li in good_introduces.find_elements_by_tag_name('li'):
                    if li.text.split('：')[0] in data_head:
                        head = li.text.split('：')[0]
                        data = li.text.split('：')[1]
                        item[head] = data
                collection = db2[collection_name]
                print(item)
                if item and collection.insert_one(item):
                    print('ok')

        finally:
            browser.close()


if __name__ == '__main__':
    parse_page()



