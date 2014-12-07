import random

from flask import Flask, render_template, make_response, session
from IPython.nbformat import current
import blaze as bz

from .forms import forms as forms_blueprint

data = {}
worksheets = {}

app = Flask(__name__)
app.register_blueprint(forms_blueprint, url_prefix="/forms")
app.secret_key = "It's a secret!"

@app.route("/")
def index():
    session["sid"] = len(worksheets)
    worksheets[session["sid"]] = current.new_worksheet()

    return render_template("app.html")
