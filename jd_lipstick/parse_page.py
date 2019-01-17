from selenium import webdriver
from pymongo import MongoClient


client = MongoClient()
db = client['jdLipstick']
collections_name = db.list_collection_names()

browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])


def parse_page(url):
    try:
        browser.get(url)

    except:
        print('打开' + url + '失败')

    else:
        print(url)
        infos_div = browser.find_element_by_class_name('itemInfo-wrap')
        title = infos_div.find_element_by_class_name('sku-name').get_attribute('innerText')
        price = infos_div.find_element_by_class_name('p-price').get_attribute('innerText')
        print(title, price)


if __name__ == '__main__':
    for collection_name in collections_name:
        collection = db[collection_name]
        for data in collection.find():
            url = data.get('url')
            parse_page(url)



