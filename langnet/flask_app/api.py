from flask import Flask, Blueprint
from flask import request, jsonify

from langnet.flask_app import get_wiring
from langnet.diogenes import DiogenesLanguages

app = Blueprint("api", __name__)


@app.route("/ping")
def ping():
    return "pong"


@app.route("/q")
def q():
    search = request.args.get("s", "Ἀσίας")
    lang = request.args.get("l", DiogenesLanguages.GREEK)
    print("got query:", search, lang)

    wiring = get_wiring()
    result = wiring.scraper.parse_word(search, lang)
    print(result)
    return jsonify(result)
