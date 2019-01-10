import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import json
from multiprocessing import Pool


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
url_compile = re.compile('(.*?)(stock=1&)(ev=.*?&).*?')
all_brand_page_url_list = []
all_url_list = []

# browser = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe',
#                               service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])


# 获取口红首页
def get_first_page():
    url = base_url + urlencode(params)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text

    print("首页访问失败")
    return None


# 获取每个品牌页面url
def get_brand_url(html):
    if html:
        brand_url_list = []
        soup = BeautifulSoup(html, 'html5lib')
        brand_as = soup.select('#J_selector > div.J_selectorLine.s-brand > div > div.sl-value > div.sl-v-logos > ul > li')
        for brand_a in brand_as:
            brand_url = brand_a.find('a').get('href')
            brand_url = base_url + brand_url[7:]
            brand_url_list.append(brand_url)

        return brand_url_list


# 获取每个品牌所有页面url
def get_all_brand_page_url(brand_url):
    response = requests.get(brand_url, headers=headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html5lib')
        pages = soup.select('#J_topPage > span > i')[0].get_text()
        brand_url_tuple = re.findall(url_compile, brand_url)[0]
        # 重构url，将品牌名和stock交换位置，后面再补上固定数据，page处用{}占位
        brand_url = brand_url_tuple[0] + brand_url_tuple[2] + brand_url_tuple[1] + 'page={}&s=1&click=0'
        for page in range(int(pages)):
            url = brand_url.format(int(page)+2)
            all_brand_page_url_list.append(url)

    else:
        print("访问：" + brand_url + "失败")
        return None


# 获取每个商品页面url
def get_per_page_url(brand_url):
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
                        print(url)
                        all_url_list.append(url)
                except:
                    continue
        finally:
            browser.close()


def main():
    html = get_first_page()
    brand_url_list = get_brand_url(html)

    for brand_url in brand_url_list:
        print(brand_url)
        get_all_brand_page_url(brand_url)

    # for brand_url in all_brand_page_url_list:
    #     get_per_page_url(brand_url)

    pool = Pool(processes=2)
    pool.map(get_per_page_url, all_brand_page_url_list)
    pool.close()
    pool.join()

    all_url_dict = {'urls': all_url_list}
    with open('urls.json', 'w') as f:
        f.write(json.dumps(all_url_dict))
        print("成功写入json文件")


if __name__ == '__main__':
    main()



