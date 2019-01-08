import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup


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
brand_url_list = []


def get_first_page():
    url = base_url + urlencode(params)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text

    print("首页访问失败")
    return None


def get_brand_url(html):
    soup = BeautifulSoup(html, 'html5lib')
    brand_as = soup.select('#J_selector > div.J_selectorLine.s-brand > div > div.sl-value > div.sl-v-logos > ul > li')
    for brand_a in brand_as:
        brand_url = brand_a.find('a').get('href')
        brand_url = base_url + brand_url[7:]
        brand_url_list.append(brand_url)
        return brand_url_list


def get_per_page_url(brand_url):
    response = requests.get(brand_url, headers=headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html5lib')
        pages = soup.select('#J_goodsList > ul > li')
        for page in pages:
            pass

    print("访问" + brand_url + "失败")


if __name__ == '__main__':
    html = get_first_page()
    brand_url_list = get_brand_url(html)



