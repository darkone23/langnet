from flask import Flask, Blueprint
from flask import request, jsonify

from langnet.flask_app import get_wiring
from langnet.diogenes import DiogenesLanguages
from langnet.whitakers_words.core import WhitakersWords

app = Blueprint("api", __name__)


@app.route("/ping")
def ping():
    return "pong"


@app.route("/q")
def q():
    search = request.args.get("s", "Ἀσίας")
    lang = request.args.get("l", DiogenesLanguages.GREEK)
    print("got query:", search, lang)
    # print(request.data)

    wiring = get_wiring()
    result = wiring.scraper.parse_word(search, lang)

    response = dict(diogenes=result)

    if lang == DiogenesLanguages.LATIN:
        result["whitakers"] = WhitakersWords.words([search])
    # print(result)
    return jsonify(response)
