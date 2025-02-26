from flask import Blueprint
from flask import request, jsonify

from langnet.flask_app.core import get_wiring, FlaskAppWiring

app = Blueprint("api", __name__)


@app.route("/q")
def q():
    search = request.args.get("s", None)
    lang = request.args.get("l", None)

    if search is None or lang is None:
        return "Bad Request", 400

    # print(request.data)

    wiring: FlaskAppWiring = get_wiring()
    response = wiring.engine.handle_query(lang, search)
    # print(result)
    return jsonify(response)
