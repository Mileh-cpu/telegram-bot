import os
import time
from flask import Flask, request
from telegram import Bot, Update, ChatPermissions

# TOKEN из Render Environment Variables
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN is missing in environment variables!")

bot = Bot(token=TOKEN)
app = Flask(__name__)

user_data = {}
MUTE_TIME = 30

print("🔥 BOT STARTED")


@app.route("/")
def home():
    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook():
    print("🔥 WEBHOOK HIT:", request.data)

    update = Update.de_json(request.get_json(force=True), bot)

    if not update.message:
        return "OK"

    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    now = time.time()

    print("MSG FROM:", user_id)

    # 👉 ТОЛЬКО ТВОЙ ID
    if user_id != 561176995:
        return "OK"

    if user_id not in user_data:
        user_data[user_id] = {"last": 0}

    last_time = user_data[user_id]["last"]

    if now - last_time < MUTE_TIME:
        print("🔇 MUTE TRIGGERED")

        bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=int(time.time()) + MUTE_TIME
        )

    user_data[user_id]["last"] = now

    return "OK"


print("ROUTES LOADED:", app.url_map)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)