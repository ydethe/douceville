from flask import render_template

from CollegesLycees import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Yann'}
    return render_template('index.html', title='Home', user=user)


@app.route('/map')
def map():
    return render_template('map.html')

