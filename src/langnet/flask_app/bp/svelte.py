from flask import Blueprint, send_from_directory, current_app
from pathlib import Path

app = Blueprint("svelte", __name__)


@app.route("/")
@app.route("/q")
@app.route("/about")
def index():
    # print("wow you got to the index")
    # print(current_app.config)
    webroot = current_app.config["STATIC_WEBROOT"]
    if not (Path(webroot) / "index.html").exists():
        return "langnet-web unavailable", 503
    return send_from_directory(webroot, "index.html")
