import random

from flask import Flask, render_template, make_response, session
from flask.ext.socketio import SocketIO, join_room
from flask_kvsession import KVSessionExtension
from simplekv.fs import FilesystemStore
import redis

import app.compute
import app.graph
from .forms import forms as forms_blueprint

data = {}
store = FilesystemStore("./data")

app = Flask(__name__)
app.register_blueprint(forms_blueprint, url_prefix="/forms")

KVSessionExtension(store, app)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("app.html")

@socketio.on("compute")
def stat(msg):
    funcs = {"descriptive stat": compute.describe,
             "ttest1": compute.ttest1}
    f = funcs[msg.pop("type")]
    print msg
    result = f(data[session["sid"]], **msg)
    json = {"safe": True, "type": "stat", "display": result}
    socketio.emit("display", json, room=session["sid"])

@socketio.on("begin")
def start(msg):
    bits = random.getrandbits(32)
    while bits in data:
        bits = random.getrandbits(32)

    data[bits] = None
    session["sid"] = bits
    join_room(bits)
    socketio.emit("register", {"id":bits}, room=session["sid"])

@socketio.on("disconnect")
def disconnect():
    data.pop(session["sid"], None)
