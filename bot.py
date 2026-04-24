import os
import time
import requests
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")
YOUR_ID = 561176995

app = Flask(__name__)

last_message_time = {}

@app.route("/", methods=["GET"])
def home():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    print("🔥 WEBHOOK HIT:", data)

    if "message" not in data:
        return "OK"

    message = data["message"]
    user_id = message["from"]["id"]
    chat_id = message["chat"]["id"]

    # работает только для тебя
    if user_id != YOUR_ID:
        return "OK"

    now = time.time()

    if user_id in last_message_time:
        if now - last_message_time[user_id] < 30:
            print("🚫 MUTE USER")

            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/restrictChatMember",
                json={
                    "chat_id": chat_id,
                    "user_id": user_id,
                    "permissions": {
                        "can_send_messages": False
                    },
                    "until_date": int(now) + 30
                }
            )

    last_message_time[user_id] = now

    return "OK"

if __name__ == "__main__":
    print("🔥 BOT STARTED")
    print("🔥 ROUTES:", app.url_map)
    app.run(host="0.0.0.0", port=10000)