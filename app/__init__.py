from flask import Flask, render_template, request, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from urlparse import urlparse, urljoin


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


# Define the WSGI application object
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
#from app.mod_auth.controllers import mod_auth as auth_module

# Register blueprint(s)
#app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
#db.create_all()
