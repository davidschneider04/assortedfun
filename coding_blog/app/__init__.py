from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import numpy as np


app = Flask(__name__,
        template_folder='html/templates',
        static_url_path='',
        static_folder='html/static')
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route("/")
def index():
    return render_template('index.html', **locals())


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
