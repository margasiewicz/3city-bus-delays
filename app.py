from rozklad import Timetable
from flask import Flask, render_template, request, redirect, json, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    data = Timetable()
    data = json.loads(data.json_delay(39100))
    colnames=['route_id', 'headsign', 'delay_mins']
    return render_template('index.html', data=data, colnames=colnames)

if __name__ == '__main__':
    app.debug = True
    app.run()
