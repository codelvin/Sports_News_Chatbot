from flask import Flask, request, render_template, redirect, url_for
from flask_wtf import FlaskForm 
from wtforms import FloatField
from wtforms.validators import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('demo.html')

@app.route('/hello', methods=['POST'])
def hello():
    result = None
    textinput = request.form['textinput']
    print '%s' % textinput
    result = textinput
    return render_template('demo.html', result=result)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)

hello()