from flask import Flask, render_template, request
from flask_wtf import CsrfProtect
from RailWay_12306.spider import railway_query as rq

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

    RWQ = rq.RailWayQuery(from_station, to_station, date)
    json = RWQ.get_json()
    table, items_list = RWQ.parse_json(json)

    return render_template('show.html', items_list=items_list, from_station=from_station,
                           to_station=to_station, date=date)


if __name__ == '__main__':
    app.run()


