from flask import Blueprint, send_from_directory, current_app, render_template
from pathlib import Path

app = Blueprint("htmx", __name__, template_folder="htmx_templates")


@app.route("")
@app.route("/q")
@app.route("/about")
def index():
    return render_template("langnet.html.j2")
    # print("wow you got to the index")
    # print(current_app.config)
    # webroot = current_app.config["STATIC_WEBROOT"]
    # if not (Path(webroot) / "langnet.html").exists():
    #     return "langnet-web unavailable", 503
    # return send_from_directory(webroot, "langnet.html")
