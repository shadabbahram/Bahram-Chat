from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import json
import os
import uuid

app = Flask(__name__)
app.secret_key = "bahram_secret_key"

messages = []
users = {}

def load_messages():
    if os.path.exists("messages.json"):
        with open("messages.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_messages():
    with open("messages.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False)

messages = load_messages()

# 🌐 صفحه اصلی
@app.route("/")
def home():
    return render_template("index.html")

# 🔐 لاگین واقعی (ساخت user id)
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    phone = data.get("phone")

    if not phone:
        return {"error": "no phone"}, 400

    user_id = str(uuid.uuid4())[:8]

    return {
        "user_id": user_id,
        "phone": phone
    }

    # ساخت user id منحصر به فرد
    user_id = str(uuid.uuid4())[:8]

    users[user_id] = phone

    session["user_id"] = user_id

    return {
        "user_id": user_id,
        "phone": phone
    }

# 💬 ارسال پیام
@app.route("/send", methods=["POST"])
def send():
    data = request.json

    user_id = data.get("user_id")
    msg = data.get("msg")

    if not user_id or not msg:
        return {"error": "invalid"}, 400

    message = {
        "user_id": user_id,
        "msg": msg,
        "time": datetime.now().strftime("%H:%M")
    }

    messages.append(message)
    save_messages()

    return {"status": "ok"}

# 📥 گرفتن پیام‌ها
@app.route("/get", methods=["GET"])
def get():
    return jsonify(messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)