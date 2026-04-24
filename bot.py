import os
import time
from flask import Flask, request
from telegram import Bot, Update

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
app = Flask(__name__)

print("BOT STARTED")

user_data = {}
MUTE_TIME = 30

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)

    if update.message:
        user_id = update.message.from_user.id
        chat_id = update.message.chat.id
        now = time.time()

        print("MSG FROM:", user_id)

        if user_id not in user_data:
            user_data[user_id] = {"last": 0}

        if now - user_data[user_id]["last"] < MUTE_TIME:
            bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions={"can_send_messages": False},
                until_date=int(time.time()) + MUTE_TIME
            )

        user_data[user_id]["last"] = now

    return "OK"


@app.route("/")
def home():
    return "OK"