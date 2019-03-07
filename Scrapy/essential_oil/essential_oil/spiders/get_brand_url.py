import json
from selenium import webdriver


class GetBrandUrl(object):

    def __init__(self, url, json_path):
        self.url = url
        self.browser = webdriver.PhantomJS()
        self.brand_dict = {}
        self.json_path = json_path

        self.get_brand_url()

    def get_brand_url(self):
        self.browser.get(self.url)
        self.browser.find_element_by_xpath('//*[@id="J_selector"]/div[1]/div/div[3]/a[1]').click()
        brand_lis = self.browser.find_elements_by_xpath('//*[@id="J_selector"]/div[1]/div/div[2]/div[2]/ul/li')
        for li in brand_lis:
            brand_url = li.find_element_by_xpath('./a').get_attribute('href')
            brand_name = li.find_element_by_xpath('./a').get_attribute('title')
            print(brand_name, brand_url)

            self.brand_dict[brand_name] = brand_url

        with open(self.json_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.brand_dict, indent=4))


if __name__ == '__main__':
    url = 'https://search.jd.com/search?keyword=%E8%96%B0%E8%A1%A3%E8%8D%89%E7%B2%BE%E6%B2%B9&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.def.0.V19%3B&stock=1&uc=0#J_searchWrap'
    json_path = 'brand_url.json'
    gbu = GetBrandUrl(url, json_path)


