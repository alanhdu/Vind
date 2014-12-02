import json

from flask import Blueprint, request, session
from werkzeug import secure_filename
import blaze as bz

import app
import compute

forms = Blueprint("forms", __name__)

@forms.route("/file_upload", methods=["POST"])
def file_upload():
    f = request.files["file_upload"]
    fname = "tmp/" + secure_filename(f.filename)
    f.save(fname)

    sid = session["sid"]
    app.data[sid] = bz.Data(fname)
    return bz.to_html(app.data[sid])

@forms.route("/statistics", methods=["POST"])
def stat():
    funcs = {"descriptive-stat": compute.describe,
             "ttest1": compute.ttest1}
    msg = json.loads(request.data)
    f = funcs[msg["type"]]
    result = f(app.data[session["sid"]], msg["data"], msg["parameters"])

    return json.dumps({"result": result})
