from flask import Flask
from flask import g as flask_globals

from werkzeug.middleware.proxy_fix import ProxyFix

from .config import FlaskAppConfig

from langnet.diogenes import DiogenesScraper


class FlaskAppWiring:

    config = FlaskAppConfig()
    scraper = DiogenesScraper()

    def init_flask_app(self, app: Flask):
        # do plugin init app stuff here...
        app.wsgi_app = ProxyFix(app.wsgi_app, x_host=1)
        from .api import app as api_blueprint
        from .static import app as static_blueprint

        app.register_blueprint(static_blueprint, url_prefix="/")
        app.register_blueprint(api_blueprint, url_prefix="/api")


def get_wiring() -> FlaskAppWiring:
    wiring = getattr(flask_globals, "__wiring", None)
    if wiring is None:
        wiring = flask_globals.__wiring = FlaskAppWiring()
    return wiring


def create_flask_app():

    config = FlaskAppWiring.config
    flask_kwargs = config.get_flask_kwargs(__name__)
    app = Flask(**flask_kwargs)
    app.config.from_object(config)

    with app.app_context():
        wiring = get_wiring()
        wiring.init_flask_app(app)
        return app
