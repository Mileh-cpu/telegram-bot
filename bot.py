import os
import time
from flask import Flask, request
from telegram import Bot, Update, ChatPermissions

TOKEN = os.getenv("BOT_TOKEN")

# 👉 твой ID
ALLOWED_USER_ID = 561176995

MUTE_TIME = 30

bot = Bot(token=TOKEN)
app = Flask(__name__)

last_time = {}

print("🔥 BOT STARTED")


@app.route("/", methods=["GET"])
def home():
    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    print("🔥 UPDATE RECEIVED")

    update = Update.de_json(data, bot)

    if not update.message:
        return "OK"

    user_id = update.message.from_user.id
    chat_id = update.message.chat.id

    print("👤 USER:", user_id)

    if user_id != ALLOWED_USER_ID:
        return "OK"

    now = time.time()
    last = last_time.get(user_id, 0)

    if now - last < MUTE_TIME:
        try:
            print("🔇 MUTING 30s")

            bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=int(time.time()) + MUTE_TIME
            )
        except Exception as e:
            print("❌ ERROR:", e)

    last_time[user_id] = now

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)