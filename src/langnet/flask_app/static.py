from flask import Blueprint, send_from_directory, current_app

app = Blueprint("static", __name__)


@app.route("/")
def index():
    # print("wow you got to the index")
    # print(current_app.config)
    webroot = current_app.config["STATIC_WEBROOT"]
    # print(webroot)
    return send_from_directory(webroot, "index.html")


# TODO: can alternatively create a dynamic "catch-all" index for SPA


@app.route("/q")
def q():
    # print("wow you got to the index")
    # print(current_app.config)
    webroot = current_app.config["STATIC_WEBROOT"]
    # print(webroot)
    return send_from_directory(webroot, "index.html")


@app.route("/about")
def about():
    # print("wow you got to the index")
    # print(current_app.config)
    webroot = current_app.config["STATIC_WEBROOT"]
    # print(webroot)
    return send_from_directory(webroot, "index.html")
