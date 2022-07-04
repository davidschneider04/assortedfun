from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import numpy as np


app = Flask(__name__,
        template_folder='html/templates',
        static_url_path='',
        static_folder='html/static')
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    from .dashmodule.dashboard import init_dashboard
    app = init_dashboard(app)

db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template('index.html', **locals())


@app.route("/tv")
def tv():
    return render_template('tv.html', **locals())

@app.route('/live_cam')
def plantcam():
    return render_template('live_cam.html', **locals())


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# blueprints
#from app.auth.controllers import auth as auth_module
#app.register_blueprint(auth_module)

db.create_all()
