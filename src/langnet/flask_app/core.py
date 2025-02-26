from flask import Flask
from flask import g as flask_globals

from werkzeug.middleware.proxy_fix import ProxyFix

from .config import FlaskAppConfig

from langnet.diogenes.core import DiogenesScraper
from langnet.whitakers_words.core import WhitakersWords
from langnet.classics_toolkit.core import ClassicsToolkit
from langnet.cologne.core import SanskritCologneLexicon

from langnet.engine.core import LanguageEngine


class FlaskAppWiring:

    config = FlaskAppConfig()

    scraper = DiogenesScraper()
    whitakers = WhitakersWords()
    cltk = ClassicsToolkit()
    cdsl = SanskritCologneLexicon()

    engine = LanguageEngine(scraper, whitakers, cltk, cdsl)

    def init_flask_app(self, app: Flask):
        # do plugin init app stuff here...
        app.wsgi_app = ProxyFix(app.wsgi_app, x_host=1)
        from .api import app as api_blueprint
        from .svelte import app as svelte_blueprint

        app.register_blueprint(api_blueprint, url_prefix="/api")
        app.register_blueprint(svelte_blueprint, url_prefix="/")


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
