import blaze as bz
import pandas as pd

from flask import Flask, render_template
from flask.ext.socketio import SocketIO


data = bz.Table("test/iris.csv")
app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index(interval=0.05):
    return render_template("app.html")

@socketio.on("max")
def max(msg):
    result = bz.compute(data.max())
    df = pd.DataFrame(index=data.columns)
    df["Max"] = result
    socketio.emit("display", {"safe":True, "display":df.to_html()})

@socketio.on("begin")
def begin(msg):
    socketio.emit("data", data.to_html())



if __name__ == "__main__":
    debug = True
    socketio.run(app, port=8080)
