import blaze as bz
from bokeh import plotting
from bokeh import embed
from bokeh.server import bokeh_app

from flask import Flask, render_template
from flask.ext.socketio import SocketIO

import compute
import graph

data = bz.Table("test/iris.csv")
app = Flask(__name__)
app.register_blueprint(bokeh_app, url_prefix="/bokeh")
socketio = SocketIO(app)

@app.route("/")
def index(interval=0.05):
    return render_template("app.html")

@socketio.on("stat")
def stat(msg):
    funcs = {"tukey five number summary" : compute.tukeyFiveNum,
            "mean and standard deviation" : compute.meanStd}

    f = funcs[msg]
    socketio.emit("display", {"safe":True, "type": "stat", "display":f(data).to_html()})

@socketio.on("graph")
def plot(msg):
    funcs = {"scatter plot": graph.scatter}
    f = funcs[msg]
    tag = embed.autoload_server(*f(data))
    socketio.emit("display", {"safe":True, "type": "graph", "display":tag})

@socketio.on("begin")
def begin(msg):
    socketio.emit("data", data.to_html())

if __name__ == "__main__":
    debug = True
    socketio.run(app, port=8080)
