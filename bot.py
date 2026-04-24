import os
import time
from flask import Flask, request
from telegram import Bot, Update, ChatPermissions

# 👉 ВАЖНО: Render переменная называется BOT_TOKEN
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN is not set in environment variables")

bot = Bot(token=TOKEN)
app = Flask(__name__)

# 👉 ТВОЙ Telegram ID
TARGET_USER_ID = 561176995

# хранение времени последнего сообщения
last_message_time = {}

MUTE_TIME = 30  # 30 секунд

print("🔥 BOT STARTED")
print("ROUTES:", app.url_map)


@app.route("/")
def home():
    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)

    if not update.message:
        return "OK", 200

    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    now = time.time()

    print("📩 MESSAGE FROM:", user_id)

    # 👉 только твой пользователь
    if user_id != TARGET_USER_ID:
        return "OK", 200

    last_time = last_message_time.get(user_id, 0)

    # 👉 если прошло меньше 30 секунд → мут
    if now - last_time < MUTE_TIME:
        print("🔇 MUTING USER:", user_id)

        bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=False
            ),
            until_date=int(time.time()) + 30
        )

    # обновляем время
    last_message_time[user_id] = now

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)