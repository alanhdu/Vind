import random

from flask import Flask, render_template, make_response, session
from flask.ext.socketio import SocketIO, join_room
import blaze as bz

from .forms import forms as forms_blueprint

data = {}

app = Flask(__name__)
app.register_blueprint(forms_blueprint, url_prefix="/forms")
app.secret_key = "It's a secret!"

@app.route("/")
def index():
    bits = random.getrandbits(32)
    while bits in data:
        bits = random.getrandbits(32)

    session["sid"] = bits

    return render_template("app.html")
