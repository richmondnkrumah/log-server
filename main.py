from flask import Flask, request
from datetime import datetime
import dropbox
import os
from dotenv import load_dotenv

load_dotenv()  # 🔐 Loads from .env

app = Flask(__name__)

DROPBOX_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
dbx = dropbox.Dropbox(DROPBOX_TOKEN)

@app.route("/", methods=["GET"])
def index():
    return "Dropbox log server is running."

@app.route("/upload", methods=["POST"])
def upload():
    content = request.data.decode("utf-8")
    now = datetime.utcnow()
    date_str = now.strftime("%d_%B_%Y")  # e.g. 29_June_2025
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S UTC")

    folder_path = f"/{date_str}"
    file_path = f"{folder_path}/log_{date_str}.txt"

    log_entry = f"[{timestamp}]\n{content}\n\n"

    try:
        # Try to get and append to existing file
        _, res = dbx.files_download(file_path)
        existing_data = res.content.decode("utf-8")
        updated_data = existing_data + log_entry
        dbx.files_upload(updated_data.encode("utf-8"), file_path, mode=dropbox.files.WriteMode.overwrite)
    except dropbox.exceptions.ApiError as e:
        if "path/not_found" in str(e):
            # File doesn't exist — create it
            dbx.files_upload(log_entry.encode("utf-8"), file_path, mode=dropbox.files.WriteMode.add)
        else:
            return f"Dropbox API error: {e}", 500

    return "OK", 200
