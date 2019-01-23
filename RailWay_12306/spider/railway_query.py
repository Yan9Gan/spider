import os
import re
import json
import requests
from urllib.parse import urlencode
import prettytable as pt

current_path = os.path.dirname(__file__)


class RailWayQuery(object):

    base_url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Cookie': 'JSESSIONID=B9FFED936A77CD0CAECC897B5A88D700; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u6F6E%u6C55%2CCBQ; _jc_save_toStation=%u5E7F%u5DDE%2CGZQ; BIGipServerportal=2949906698.17183.0000; BIGipServerotn=1691943178.64545.0000; RAIL_EXPIRATION=1548496240161; RAIL_DEVICEID=cjWczPgn8Hj0jMnTVhQGNQBWH9Tnzh5JA1L0nyIdyF9C-teL-YFzzooddGwewDt9DSdC17mYOyd8XnQgUnx6DQNonyilj7M_EBhYmQhU1DnkMT4fT89FjIL2e22FKiJ7motbQwwKUvHGtdJyLTxo5jnRuXVmOYS6; BIGipServerpassport=887619850.50215.0000; route=6f50b51faa11b987e576cdb301e545c4; _jc_save_fromDate=2019-01-30; _jc_save_toDate=2019-01-23',
        'Host': 'kyfw.12306.cn',
        'Referer': 'https://www.12306.cn/index/',
        'Connection': 'keep-alive',
    }

    params = {
        'leftTicketDTO.train_date': '',
        'leftTicketDTO.from_station': '',
        'leftTicketDTO.to_station': '',
        'purpose_codes': 'ADULT'
    }

    json_compile = re.compile('(\'.*\')')
    gd_compile = re.compile('G|D\d+')

    with open(os.path.join(current_path, 'station_code.json'), 'r', encoding='utf-8') as f:
        station_code_dict = json.load(f)

    def __init__(self, START, END, DATE):
        self.START = START
        self.END = END
        self.DATE = DATE

    def get_json(self):
        self.params['leftTicketDTO.train_date'] = self.DATE
        self.params['leftTicketDTO.from_station'] = self.station_code_dict.get(self.START)
        self.params['leftTicketDTO.to_station'] = self.station_code_dict.get(self.END)

        url = self.base_url + urlencode(self.params)

        print(url)

        try:
            response = requests.get(url, headers=self.headers, allow_redirects=False)
            print(response.status_code)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            print('ERROR')
            return None

    def parse_json(self, json):
        items_list = []
        tb = pt.PrettyTable(['车次', '出发站', '到达站', '出发时间', '到达时间', '历时',
                             '商务座/特等座', '一等座', '二等座', '高级软卧', '软卧', '动卧',
                             '硬卧', '软座', '硬座', '无座', '其他'])
        data = json['data']
        station_code_dict = data['map']
        ticket_info_list = data['result']
        for ticket_info in ticket_info_list:
            items = ticket_info.split('|')
            train_number = items[3]
            start_station = station_code_dict[items[6]]
            end_station = station_code_dict[items[7]]
            start_time = items[8]
            end_time = items[9]
            duration = items[10]
            if re.match(self.gd_compile, train_number):
                td = items[32] or '-'
                yid = items[31] or '-'
                erd = items[30] or '-'
                gjrw = items[29] or '-'
                rw = items[28] or '-'
                dw = items[27] or '-'
                wz = items[26] or '-'
                yw = items[25] or '-'
                rz = items[24] or '-'
                yz = items[23] or '-'
                qt = items[22] or '-'
            else:
                td = '-'
                yid = '-'
                erd = '-'
                gjrw = '-'
                rw = items[23] or '-'
                dw = '-'
                wz = items[26] or '-'
                yw = items[28] or '-'
                rz = items[24] or '-'
                yz = items[29] or '-'
                qt = '-'
            item = [train_number, start_station, end_station, start_time, end_time,
                        duration, td, yid, erd, gjrw, rw, dw, yw, rz, yz, wz, qt]
            tb.add_row(item)
            items_list.append(item)

        tb.align = 'c'
        tb.valign = 'm'
        return tb, items_list

    def get_city_code(self):
        station_code_dict = {}

        url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9083'
        response = requests.get(url, headers=self.headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            text = response.text
            text = re.search(self.json_compile, text).group(1)
            code_list = text.split('|')
            for _1, city, code, _2, _3 in zip(code_list[0::5], code_list[1::5], code_list[2::5],
                                              code_list[3::5], code_list[4::5]):
                if city not in station_code_dict.keys():
                    station_code_dict[city] = code

        json_str = json.dumps(station_code_dict, indent=4)
        with open('station_code.json', 'w') as json_file:
            json_file.write(json_str)


if __name__ == '__main__':
    start = input('请输入出发站：')
    end = input('请输入到达站：')
    date = input('请输入出发日期(格式为年-月-日，数字不足两位数时前面加0)：\n')
    RWQ = RailWayQuery(start, end, date)
    json = RWQ.get_json()
    table, items_list = RWQ.parse_json(json)
    print(table, items_list)

    # RWQ.get_city_code()


