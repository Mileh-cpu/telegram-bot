import os
import time
from flask import Flask, request

from telegram import Bot, Update, ChatPermissions

# =====================
# CONFIG
# =====================
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ BOT_TOKEN NOT SET")
    exit()

bot = Bot(token=TOKEN)
app = Flask(__name__)

MUTE_TIME = 30
TARGET_USER_ID = 561176995

user_last_message = {}

print("🔥 BOT STARTED")
print("ROUTES LOADED:", app.url_map)


# =====================
# WEBHOOK
# =====================
@app.route("/", methods=["GET"])
def home():
    return "OK", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    print("🔥 WEBHOOK HIT")

    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)

        if not update or not update.message:
            return "OK", 200

        user_id = update.message.from_user.id
        chat_id = update.message.chat.id
        now = time.time()

        print("📩 MSG FROM:", user_id)

        # только нужный пользователь
        if user_id != TARGET_USER_ID:
            return "OK", 200

        last = user_last_message.get(user_id, 0)

        # антиспам 30 сек
        if now - last < MUTE_TIME:
            print("🔇 MUTE TRIGGER")

            bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=int(time.time()) + MUTE_TIME
            )

        user_last_message[user_id] = now

        return "OK", 200

    except Exception as e:
        print("❌ ERROR:", e)
        return "OK", 200


# =====================
# RUN (локально, Render игнорирует)
# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)