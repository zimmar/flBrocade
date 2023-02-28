# factory.py

from flask import Flask, request, g, url_for, current_app, render_template
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap


from .extensions import app_logging, app_db

def create_app():

    app = Flask(__name__)

    app.config.from_object('config.ConfigDevelopment')

    # services
    app.logger = app_logging.init_app(app)
    app_db.init_app(app)
    app.logger.debug('test debug message')

    Bootstrap(app)

    csrf = CSRFProtect()
    csrf.init_app(app)

    @app.teardown_appcontext
    def teardown_db(response_or_exception):
        if hasattr(app_db, 'session'):
            app_db.session.remove()

    @app.route('/')
    def index():
        return render_template(
            'home.html',
            welcome_message='Hello world',
        )

    return app