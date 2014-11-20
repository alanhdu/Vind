import random

from flask import Flask, render_template, make_response, session
from flask.ext.socketio import SocketIO, join_room
import redis
import blaze as bz

import compute
from .forms import forms as forms_blueprint

data = {}

app = Flask(__name__)
app.register_blueprint(forms_blueprint, url_prefix="/forms")

socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("app.html")

@socketio.on("compute")
def stat(msg):
    funcs = {"descriptive stat": compute.describe,
             "ttest1": compute.ttest1}
    type = msg.pop("type")
    f = funcs[type]
    result = f(data[session["sid"]], **msg)
    msg["type"] = type

    json = {"safe": True, "type": "stat", "display": result,
            "description": msg}

    socketio.emit("display", json, room=session["sid"])

@socketio.on("begin")
def start(msg):
    bits = random.getrandbits(32)
    while bits in data:
        bits = random.getrandbits(32)

    data[bits] = bz.Data("test/iris.csv")
    session["sid"] = bits
    join_room(bits)
    socketio.emit("register", {"id":bits}, room=bits)
    socketio.emit("data", bz.to_html(data[bits]), room=bits)

@socketio.on("disconnect")
def disconnect():
    data.pop(session["sid"], None)
