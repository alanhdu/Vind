from app import app

if __name__ == "__main__":
    app.secret_key = "it's a secret"
    app.run(debug=True)
