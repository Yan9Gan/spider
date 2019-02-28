import requests
from bs4 import BeautifulSoup


class NationalStatics(object):

    def __init__(self):
        self.base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'
        self.headers = {
            'Content-Type': 'text/html;',
            'Cookie': '_trs_uv=js73uxr7_6_9ff5; AD_RS_COOKIE=20081944',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        }

        self.directly_under_list = ['北京市', '天津市', '上海市', '重庆市']
        self.directly_under_dict = {
            'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/11.html': '北京市',
            'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/12.html': '天津市',
            'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/31.html': '上海市',
            'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/50.html': '重庆市',
        }
        self.all_dict = {}

    def spider(self):
        url = self.base_url + 'index.html'
        province_url_list, province_list = self.get_province(url)
        for province_url, province in zip(province_url_list, province_list):
            self.all_dict[province] = {}

            print(province_url, province)

            city_url_list, city_list = self.get_city(province_url)
            for city_url, city in zip(city_url_list, city_list):
                if city_url != '':
                    self.all_dict[province][city] = {}
                else:
                    self.all_dict[province][city] = ''

                print(city_url, city)

                county_url_list, county_list = self.get_county(city_url, province_url)
                # for county_url, county in zip(county_url_list, county_list):
                #     street_url_list, street_list = self.get_street(county_url, province_url)

    def get_province(self, url):
        url_list = []
        province_list = []
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            response.encoding = 'gbk'
            soup = BeautifulSoup(response.text, 'html5lib')
            trs = soup.select(
                'table[class="provincetable"] > tbody > tr[class="provincetr"]'
            )
            for tr in trs:
                for td in tr.select('td'):
                    province_url = self.base_url + td.a.get('href')
                    province = td.text
                    if province in self.directly_under_list:
                        province = '直辖市'
                    url_list.append(province_url)
                    province_list.append(province)

        return url_list, province_list

    def get_city(self, url):
        url_list = []
        city_list = []
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            response.encoding = 'gbk'
            soup = BeautifulSoup(response.text, 'html5lib')
            trs = soup.select(
                'table[class="citytable"] > tbody > tr[class="citytr"]'
            )
            for tr in trs:
                for td in tr.select('td:nth-of-type(2)'):
                    city_url = self.base_url + td.a.get('href')
                    city = td.text
                    if url in self.directly_under_dict.keys():
                        url_list.append(city_url)
                        city_list.append(self.directly_under_dict.get(url))
                        break
                    url_list.append(city_url)
                    city_list.append(city)

        return url_list, city_list

    def get_county(self, url, province_url):
        url_list = []
        county_list = []
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            response.encoding = 'gbk'
            soup = BeautifulSoup(response.text, 'html5lib')
            trs = soup.select(
                'table[class="countytable"] > tbody > tr[class="countytr"]'
            )
            for tr in trs:
                for td in tr.select('td'):
                    county = td.text
                    if county.isdigit() or county == '市辖区':
                        continue
                    print(county)
                    try:
                        county_url = province_url + td.a.get('href')
                    except AttributeError:
                        county_url = ''
                    url_list.append(county_url)
                    county_list.append(county)

        return url_list, county_list

    def get_street(self, url, province_url):
        street_url_list = []
        street_list = []
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            response.encoding = 'gbk'
            soup = BeautifulSoup(response.text, 'html5lib')
            trs = soup.select(
                'table[class="countytable"] > tbody > tr[class="countytr"]'
            )
            for tr in trs:
                for td in tr.select('td'):
                    street = td.text
                    street_url = province_url.split('.')[0] + '/' + td.a.get('href')
                    street_url_list.append(street_url)
                    street_list.append(street)

        return street_url_list, street_list

    def get_committee(self, url):
        pass


if __name__ == '__main__':
    ns = NationalStatics()
    ns.spider()
