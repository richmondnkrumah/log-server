from flask import Flask, request, send_from_directory, abort
from datetime import datetime
import os

app = Flask(__name__)

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return "Log server is running."

@app.route("/upload", methods=["POST"])
def upload():
    content = request.data.decode("utf-8")
    timestamp = datetime.utcnow()
    date_str = timestamp.strftime("%d_%B_%Y")  # e.g., 29_June_2025
    filename = f"log_{date_str}.txt"
    filepath = os.path.join(LOG_DIR, filename)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}]\n")
        f.write(content)
        f.write("\n\n")

    return "OK", 200

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    if not filename.endswith(".txt"):
        abort(400, description="Invalid file extension.")
    
    try:
        return send_from_directory(LOG_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404, description="File not found.")
