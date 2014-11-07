from flask import Blueprint, request
from werkzeug import secure_filename
import blaze as bz

import app

forms = Blueprint("forms", __name__)

@forms.route("/file_upload", methods=["POST"])
def file_upload():
    f = request.files["file_upload"]
    fname = "tmp/" + secure_filename(f.filename)
    f.save(fname)

    sid = int(request.form["id"])
    app.data[sid] = bz.Table(fname)
    app.socketio.emit("data", app.data[sid].to_html())

    return ""
