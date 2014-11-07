from app import app, socketio


if __name__ == "__main__":
    app.secret_key = "it's a secret"
    socketio.run(app)
