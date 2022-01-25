from flask import Flask
from threading import Thread

app = Flask("")


@app.route("/")
def home():
    return "So, you're tired of PSL as well?"


def runserver():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=runserver)
    t.start()
