import re
from selenium import webdriver
from pymongo import MongoClient


client = MongoClient()
db = client['jdLipstick']
collections_name = db.list_collection_names()

# browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])


def parse_page(url):
    browser = webdriver.Chrome()
    try:
        browser.get(url)

    except:
        print('打开' + url + '失败')

    else:
        print(url)
        infos_div = browser.find_element_by_class_name('itemInfo-wrap')
        # 标题
        title = infos_div.find_element_by_class_name('sku-name').get_attribute('innerText')
        # 价格
        price = infos_div.find_element_by_class_name('p-price').get_attribute('innerText')
        print(title)
        good_introduces = browser.find_element_by_class_name('parameter2')
        # 商品毛重
        gross_weight = good_introduces.find_element_by_xpath('./li[4]').text.split('：')[1]
        # 妆效
        makeup_effect = good_introduces.find_element_by_xpath('./li[5]').text.split('：')[1]
        # 色系
        color_system = good_introduces.find_element_by_xpath('./li[7]').text.split('：')[1]
        # 产地
        origin = good_introduces.find_element_by_xpath('./li[8]').text.split('：')[1]
        print('价格：', price)
        print('商品毛重：', gross_weight)
        print('妆效：', makeup_effect)
        print('色系：', color_system)
        print('产地：', origin)

    finally:
        browser.close()


if __name__ == '__main__':
    sum = 0
    for collection_name in collections_name:
        collection = db[collection_name]
        print(collection_name, ':', collection.count())
        sum += collection.count()
        for data in collection.find():
            url = data.get('url')
            parse_page(url)
    print(sum)



