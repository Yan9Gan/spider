import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup


base_url = 'https://s.taobao.com/search?'

params = {
    'q': '口红',
    'imgfile': '',
    'commend': 'all',
    'ssid': 's5-e',
    'search_type': 'item',
    'sourceId': 'tb.index',
    'spm': 'a21bo.2017.201856-taobao-item.1',
    'ie': 'utf8',
    'initiative_id': 'tbindexz_20170306',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'referer': 'https://www.taobao.com/',
    'cookie': 'miid=452902621275025248; t=473d8363b7f9fdfc007888a9f9548959; hng=CN%7Czh-CN%7CCNY%7C156; cna=t/NnFDBVdmoCAXjFABBQ6qZE; thw=cn; cookie2=1a225b51d183ffcf66c89c0fe145e8d2; _tb_token_=e8b8b0d49ff68; tg=0; enc=jFpzZ9MkDLM5rSDROUaZG7QVpPZ1B7irt999nVBdYz5KcvMvDllcUhHX1Y97btlHtb5%2B1wr68ptExGBzGdMJnA%3D%3D; swfstore=92392; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; v=0; alitrackid=www.taobao.com; unb=3853197365; sg=955; _l_g_=Ug%3D%3D; skt=14f3188d8db55436; cookie1=BxUMXSIyZ4uf0TmhOrmfkhewaEOj9NBVUL9BHje%2Bgwk%3D; csg=a7fad350; uc3=vt3=F8dByRIpaiGtpf6TYX0%3D&id2=UNiBSepnt%2FkWSg%3D%3D&nk2=F5RCZV45vAU5vw%3D%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; existShop=MTU0NjkzMjYzNw%3D%3D; tracknick=tb70642839; lgc=tb70642839; _cc_=UtASsssmfA%3D%3D; dnk=tb70642839; _nk_=tb70642839; cookie17=UNiBSepnt%2FkWSg%3D%3D; JSESSIONID=30D9B282CDAEA8C7ED499DC4D782B2FA; lastalitrackid=login.taobao.com; uc1=cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie21=WqG3DMC9Fb5mPLIQo9kR&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&existShop=false&pas=0&cookie14=UoTYMDKeyGiQuQ%3D%3D&tag=8&lng=zh_CN; mt=ci=3_1; l=aBV5LjD0yiLvm0QXQMaigX_D77076CBPehMF1MaklTEhNPV17RXy17no-Vw6j_qC51cy_K-5F; isg=BEdHqwKT1-o08lNVgc7lpivC1vvR5BlKfcV6NRk0blb9iGdKIR_of6HKLghzYPOm; whl=-1%260%260%261546932645238'
}


def get_first_page():
    url = base_url + urlencode(params)
    print(url)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text


def parse_first_page(html):
    soup = BeautifulSoup(html, 'html5lib')
    brand_codes = soup.select('#J_NavCommonRowItems_0 a')
    for brand_code in brand_codes:
        print(brand_code.get('data-value'))


if __name__ == '__main__':
    html = get_first_page()
    print(html)
    parse_first_page(html)



