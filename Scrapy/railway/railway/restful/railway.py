import os
import random
import string
from pymongo import MongoClient
from flask_wtf import CsrfProtect
from flask import Flask, render_template, request

app = Flask(__name__)

app.secret_key = "436fs3sdcvr3+=)%$$#l54,5"
CsrfProtect(app)


@app.route('/')
def railway():
    return render_template('home.html')


@app.route('/show', methods=['GET', 'POST'])
def show_data():
    from_station = request.form['from']
    to_station = request.form['to']
    date = request.form['date']
    id = ''.join(random.sample(string.ascii_letters, 9))

    scrapy_shell = 'scrapy crawl railway_12306 -a fs={} -a ts={} -a date={} -a id={}'

    client = MongoClient()
    db = client['railway']
    items_list = []

    while id in db.collection_names():
        id = ''.join(random.sample(string.ascii_letters, 9))

    os.chdir('/home/ghosque/crawl/Scrapy/railway/railway/spiders')
    print(os.getcwd())
    if os.system(scrapy_shell.format(from_station, to_station, date, id)) == 0:
        for item in db[id].find():
            temp_list = [item['train_number'], item['from_station'], item['to_station'],
                         item['from_time'], item['to_time'], item['duration'], item['tdz'],
                         item['ydz'], item['edz'], item['gjrw'], item['rw'], item['dw'],
                         item['yw'], item['rz'], item['yz'], item['wz']]
            items_list.append(temp_list)

        db[id].drop()

        head_list = ['车次', '出发站', '到达站', '出发时间', '到达时间', '历时',
                     '商务座/特等座', '一等座', '二等座', '高级软卧', '软卧/一等卧',
                     '动卧', '硬卧/二等卧', '软座', '硬座', '无座']

        return render_template('show.html', head_list=head_list, items_list=items_list,
                               colspan=len(head_list), from_station=from_station,
                               to_station=to_station, date=date)


if __name__ == '__main__':
    app.run('0.0.0.0', port=2450)


