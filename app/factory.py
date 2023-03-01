# factory.py

from flask import Flask, request, g, url_for, current_app, render_template
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap


from .extensions import app_logging, app_db
from .model import Switch

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

    # blueprints
    from .blueprints.manage_data.views import manage_data_blueprint
    app.register_blueprint(manage_data_blueprint, url_prefix='/manage_data')

    @app.teardown_appcontext
    def teardown_db(response_or_exception):
        if hasattr(app_db, 'session'):
            app_db.session.remove()

    @app.route('/')
    def index():
        switches = app_db.session.query(Switch).order_by(Switch.name).all()
        return render_template(
            'home.html',
            welcome_message='Hello world',
            switches=switches
        )

    return app