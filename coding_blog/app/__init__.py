from flask import Blueprint, Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import numpy as np


app = Flask(__name__,
        template_folder='html/templates',
        static_url_path='',
        static_folder='html/static')
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


blog_bp = Blueprint('blog', __name__, template_folder='_build/html/html/templates')
app.register_blueprint(blog_bp)

@app.route("/blog")
def index():
    print('index')
    return render_template('index.html', **locals())

@app.route('/blog/<entry>')
def blog_entry(entry):
    print(entry)
    return render_template(f'blog_entries/{entry}.html', **locals())


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
