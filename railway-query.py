import re
import requests
from urllib.parse import urlencode


base_url = 'https://kyfw.12306.cn/otn/leftTicket/init?'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=BFB8FF0CBDB8919CCBBBBA2E095D089B; RAIL_EXPIRATION=1545975064794; RAIL_DEVICEID=mTkwpVXI-j_oiEprxRaHAIDnDTPi3kowGfy6rgag8TDABvtmdmLj05Cu5P5jQU6yYkjm1jfEcNMEEBDR1egVITD_1sQFoj_s3FiPyMT9x6wfycvBDq4RK_75xqq_gnplnxNdIi7awe4yiLTamg5uRkrARB8fJj7L; _jc_save_toDate=2018-12-24; _jc_save_wfdc_flag=dc; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=367526154.50210.0000; BIGipServerpassport=887619850.50215.0000; _jc_save_fromDate=2019-01-01; _jc_save_fromStation=%u5317%u4EAC%2CGZQ; _jc_save_toStation=%u4E0A%u6D77%2CCBQ',
    'Host': 'kyfw.12306.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
}

params = {
    'linktypeid': 'dc'
}

START = input('请输入出发站：')
END = input('请输入到达站：')
DATE = input('请输入出发日期(格式为年-月-日，数字不足两位数时前面加0)：\n')

json_compile = re.compile('(\'.*?\')')


def get_html():
    city_code_dict = get_city_code()
    print(city_code_dict.get(START))
    print(city_code_dict.get(END))
    url = base_url + urlencode(params) + '&fs=' + START + ',' + city_code_dict.get(START) +\
          '&ts=' + END + ',' + city_code_dict.get(END) + '&date=' + DATE + '&flag=N,N,Y'
    print(url)
    response = requests.get(url, headers=headers)


def get_city_code():
    city_code_dict = {}
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/favorite_name.js'
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        text = response.text
        text = re.search(json_compile, text).group(1)
        code_list = text.split('|')
        for _, city, code in zip(code_list[0::3], code_list[1::3], code_list[2::3]):
            city_code_dict[city] = code
        city_code_dict['厦门'] = 'XMS'

        return city_code_dict
    return None


if __name__ == '__main__':
    get_html()



