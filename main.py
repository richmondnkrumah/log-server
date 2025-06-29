from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Log server is running."

@app.route("/upload", methods=["POST"])
def upload():
    content = request.data.decode("utf-8")
    timestamp = datetime.utcnow().strftime("[%Y-%m-%d %H:%M:%S UTC]")
    with open("logs.txt", "a") as f:
        f.write(f"{timestamp}\n{content}\n\n")
    return "OK", 200
