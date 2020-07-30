from rozklad import Timetable
from flask import Flask, render_template, request, redirect, url_for, Response
import json
from wtforms import TextField, Form
app = Flask(__name__)

class SearchForm(Form):
    autocomp = TextField('Insert Bus Stop', id='stop_autocomplete')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        number = request.form['autocomp']
        return redirect(url_for('bus', number=number))
    else:
        form = SearchForm(request.form)
        data = Timetable()
        data = json.loads(data.json_delay(36050))
        return render_template('index.html', data=data, form=form)

@app.route('/bus/<number>', methods=['GET','POST'])
def bus(number):
    form = SearchForm(request.form)
    data = Timetable()
    data = json.loads(data.json_delay(number))
    return render_template('bus.html', data=data, form=form)


@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    with open('stops.json') as json_file:
        stops = json.load(json_file)
    
    stops = [item for item in stops]

    return Response(json.dumps(stops), mimetype='application/json')
if __name__ == '__main__':
    app.debug = True
    app.run()