from flask import Flask, render_template
from flask.ext.socketio import SocketIO

import compute
import graph

socketio = SocketIO()

def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug

    socketio.init_app(app)

    @app.route("/")
    def index():
        return render_template("app.html")

    return app


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
