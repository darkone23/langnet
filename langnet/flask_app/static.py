from flask import Flask, Blueprint, send_from_directory, current_app

app = Blueprint("static", __name__)


@app.route("/")
def index():
    # print("wow you got to the index")
    # print(current_app.config)
    webroot = current_app.config["STATIC_WEBROOT"]
    # print(webroot)
    return send_from_directory(webroot, "index.html")
