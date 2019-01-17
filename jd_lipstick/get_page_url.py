import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
from multiprocessing import Pool
from pymongo import MongoClient
from functools import partial


# 基础信息
base_url = 'https://search.jd.com/search?'
params = {
    'keyword': '口红',
    'enc': 'utf-8',
    'wq': '口红',
    'pvid': 'e2d50b628f024c3ab7305f29fedc5c4e',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'referer': 'https://www.jd.com/?cu=true&utm_source=baidu-search&utm_medium=cpc&utm_campaign=t_262767352_baidusearch&utm_term=106807362512_0_8529cea1a94b49f4a3c590484b92f623',
    'cookie': 'shshshfpa=953e8d25-60e0-b22f-1257-709613744249-1544175519; xtest=3849.cf6b6759; cn=0; qrsc=3; __jdu=1544175519090151046347; shshshfpb=jfZWHxwyMOLD5NpNK7jXlHQ%3D%3D; PCSYCityID=1601; ipLoc-djd=1-72-2799-0; unpl=V2_ZzNtbUtTQB0nXBZUKxFZVmILRVgSVRERfQlDXX5KVAYwBBFfclRCFX0UR1RnGFUUZwoZXkZcQxxFCEdkeB5fA2AFEFlBZxBFLV0CFi9JH1c%2bbRJcRV5CE3cPRVB7Gmw1ZAMiXUNnQxFwDUZSfx1cDWYLE11GV0IQcgpDUkspWzVXMxFcS1dGHEUJdlVLWwhZZQcXVUNeDhVxDUNUfR1YBW8CGlxCU0MUcA9EUX0pXTVk; __jda=122270672.1544175519090151046347.1544175519.1546933799.1546943120.12; __jdc=122270672; __jdv=122270672|baidu-search|t_262767352_baidusearch|cpc|106807362512_0_8529cea1a94b49f4a3c590484b92f623|1546943119539; __jdb=122270672.2.1544175519090151046347|12.1546943120; shshshfp=9547204bb990f25f550a6b237f272d82; shshshsID=6a85d710953b0e76022d6742dc39b7d2_2_1546943143292; rkv=V0900; 3AB9D23F7A4B3C9B=M7E73QMR2UZZGHIVSA6TXFUUOV7Y3AONXSZD5YN3PRW73FICPNSUKGIEZ2CHU4Y3ZBKPKA4P7G6XAJCFNMSQ5V2VNQ'
}

# url匹配
url_compile = re.compile('(.*?)(stock=1&)(ev=.*?&).*?')
# 判断是否存在括号
brackets_compile = re.compile('.*?\（(.*?)\）')

# 连接MongoDB
client = MongoClient()
db = client['jdLipstick']
collection = db['data']

base_url_dict = {}
compare_list = []
brand_name_list = []
all_brand_page_url_dict = {}


def get_url():
    """主函数"""
    html = get_first_page()
    get_brand_url(html)

    for brand_name, brand_url_list in base_url_dict.items():
        for brand_url in brand_url_list:
            get_all_brand_page_url(brand_name, brand_url)

    for brand_name, all_page_url_list in all_brand_page_url_dict.items():
        print(brand_name)

        # for page_url in all_page_url_list:
            # get_per_page_url(page_url)

        pool = Pool()
        pool.map(partial(get_per_page_url, brand_name=brand_name), all_page_url_list)
        pool.close()
        pool.join()

# ----------------------------------分割线----------------------------------


# 获取口红首页
def get_first_page():
    url = base_url + urlencode(params)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response.text

    print("首页访问失败")
    return None


# 获取每个品牌页面url
def get_brand_url(html):
    if html:
        # 定义BeautifulSoup对象
        soup = BeautifulSoup(html, 'html5lib')
        # 查找品牌所在的li并遍历提取url和品牌名
        brand_lis = soup.select('#J_selector > div.J_selectorLine.s-brand > div > div.sl-value > div.sl-v-logos > ul > li')
        for brand_li in brand_lis:
            brand_url = brand_li.find('a').get('href')
            brand_url = base_url + brand_url[7:]
            brand_name = brand_li.find('a').get('title')
            # 判断品牌名是否存在括号
            has_brackets = re.search(brackets_compile, brand_name)
            brand_name = brand_name.replace('（', '_').replace('）', '').replace(' ', '')
            # 判断是否存在相同品牌的url，相同则比较url是否相同，不同则加入同一个列表中
            # 有括号的提取括号里的英文小写进行比较，没有括号的直接比较
            is_same = False
            if has_brackets:
                compare_name = has_brackets.group(1)
                for compare in compare_list:
                    if compare_name.lower() == compare.lower():
                        same_name = brand_name_list[compare_list.index(compare)]
                        base_url_dict.get(same_name).append(brand_url)

                        is_same = True
                    else:
                        continue
            else:
                compare_name = brand_name
                for compare in compare_list:
                    if compare_name == compare:
                        same_name = brand_name_list[compare_list.index(compare)]
                        base_url_dict.get(same_name).append(brand_url)

                        is_same = True
                    else:
                        continue

            brand_name_list.append(brand_name)
            compare_list.append(compare_name)

            if not is_same:
                base_url_dict[brand_name] = [brand_url]


# 获取每个品牌所有页面url
def get_all_brand_page_url(brand_name, brand_url):
    response = requests.get(brand_url, headers=headers)
    if response.status_code == 200:
        if brand_name not in all_brand_page_url_dict.keys():
            all_brand_page_url_dict[brand_name] = []
        html = response.text
        # 定义BeautifulSoup对象
        soup = BeautifulSoup(html, 'html5lib')
        # 找到该url的总页数
        pages = soup.select('#J_topPage > span > i')[0].get_text()
        brand_url_tuple = re.findall(url_compile, brand_url)[0]
        # 重构url，将品牌名和stock交换位置，后面再补上固定数据，page处用{}占位
        brand_url = brand_url_tuple[0] + brand_url_tuple[2] + brand_url_tuple[1] + 'page={}&s=1&click=0'
        # 定义所有url
        for page in range(int(pages)):
            url = brand_url.format(int(page)+2)
            all_brand_page_url_dict[brand_name].append(url)

    else:
        print("访问：" + brand_url + "失败")
        return None


# 获取每个商品页面url
def get_per_page_url(brand_url, brand_name):
    try:
        browser = webdriver.Chrome()

    except:
        pass

    else:
        try:
            browser.get(brand_url)

        except:
            print('error')

        else:
            # 下拉至底部，下拉后等待2秒，防止页面还没加载全导致页面html没有刷新
            js = "window.scrollTo(0, document.body.scrollHeight)"
            browser.execute_script(js)
            time.sleep(2)
            # 查找每个商店页面的li
            lis = browser.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')
            for li in lis:
                try:
                    url = li.find_element_by_xpath('./div/div[1]/a').get_attribute('href')
                    # 去除广告url
                    if url.startswith('https://item'):
                        item = {}
                        print(url)
                        item['url'] = url
                        collection = db[brand_name]
                        if collection.insert(item):
                            print('ok')
                except:
                    continue
        finally:
            browser.close()


if __name__ == '__main__':
    get_url()



