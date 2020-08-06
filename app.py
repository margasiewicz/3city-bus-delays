from timetable import Timetable
from flask import Flask, render_template, request, redirect, url_for, Response
import json
from wtforms import TextField, Form


app = Flask(__name__)

class SearchForm(Form):
    autocomp = TextField('Przystanek', id='stop_autocomplete')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        stop_name = request.form['autocomp']
        return redirect(url_for('bus', stop_name=stop_name))
    else:
        form = SearchForm(request.form)
        return render_template('index.html',form=form)

@app.route('/bus/<stop_name>', methods=['GET'])
def bus(stop_name):
    form = SearchForm(request.form)
    timetable = Timetable()
    data = timetable.json_delay_from_name(stop_name)
    # data = json.loads(data)
    data = [x for x in data if x != []]
    return render_template('bus.html', data=data, form=form)


@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    with open('json_files/stops.json') as json_file:
        stops = json.load(json_file)
    
    stops = [item for item in stops]

    return Response(json.dumps(stops), mimetype='application/json')
    
if __name__ == '__main__':
    app.debug = True
    app.run()