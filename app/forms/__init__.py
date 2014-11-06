from flask import Blueprint, request, current_app
from werkzeug import secure_filename
import blaze as bz

import app

forms = Blueprint("forms", __name__)

@forms.route("/")
def temp():
    return ""

@forms.route("/file_upload", methods=["POST"])
def file_upload():
    f = request.files["file_upload"]
    fname = "tmp/" + secure_filename(f.filename)
    f.save(fname)

    app.data = bz.Table(fname)
    with current_app.app_context():
        app.socketio.emit("data", app.data.to_html())

    return ""
