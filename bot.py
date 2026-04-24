import os
import time
from flask import Flask, request
from telegram import Bot, Update, ChatPermissions

# =====================
# CONFIG
# =====================

TOKEN = os.getenv("BOT_TOKEN")  # В Render переменная BOT_TOKEN
MY_ID = 561176995              # твой Telegram ID
MUTE_TIME = 30                 # 30 секунд

bot = Bot(token=TOKEN)
app = Flask(__name__)

user_last_message_time = {}

print("🔥 BOT STARTED")
print("ROUTES:", app.url_map)


# =====================
# WEBHOOK
# =====================

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)

    if not update.message:
        return "OK"

    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    now = time.time()

    print(f"📩 MESSAGE FROM {user_id}")

    # 👉 работаем только с тобой
    if user_id != MY_ID:
        return "OK"

    last_time = user_last_message_time.get(user_id, 0)

    # 👉 если пишешь слишком часто — мут
    if now - last_time < MUTE_TIME:
        try:
            print("🔇 MUTING USER")

            bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(
                    can_send_messages=False
                ),
                until_date=int(time.time()) + MUTE_TIME
            )

        except Exception as e:
            print("ERROR MUTING:", e)

    user_last_message_time[user_id] = now

    return "OK"


# =====================
# HEALTH CHECK
# =====================

@app.route("/", methods=["GET"])
def home():
    return "OK"


# =====================
# RUN (local only)
# =====================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)