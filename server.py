import blaze as bz

from flask import Flask, render_template
from flask.ext.socketio import SocketIO

import compute


data = bz.Table("test/iris.csv")
app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index(interval=0.05):
    return render_template("app.html")

@socketio.on("stat")
def stat(msg):
    funcs = {"tukey five number summary" : compute.tukeyFiveNum,
            "mean and standard deviation" : compute.meanStd}

    f = funcs[msg]
    socketio.emit("display", {"safe":True, "display":f(data).to_html()})

@server.on("graph")
def graph(msg):
    pass

@socketio.on("begin")
def begin(msg):
    socketio.emit("data", data.to_html())

if __name__ == "__main__":
    debug = True
    socketio.run(app, port=8080)
