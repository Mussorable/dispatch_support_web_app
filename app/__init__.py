from flask import Flask, request
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_assets import Bundle, Environment

from config import Config

babel = Babel()
db = SQLAlchemy()
migrate = Migrate()
assets = Environment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    def get_locale():
        return request.accept_languages.best_match(app.config['LANGUAGES'])

    assets.init_app(app)
    babel.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        @app.before_request
        def before_request():
            from flask import g
            g.locale = str(get_locale())

    if not app.config['TESTING']:
        js_bundle = Bundle('js/main.js', filters='jsmin', output='js/main.min.js')
        assets.register('js_all', js_bundle)

        css_bundle = Bundle('css/main.scss', filters='libsass', output='css/main.min.css')
        assets.register('css_all', css_bundle)

    return app