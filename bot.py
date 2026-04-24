import os
import time
from flask import Flask, request
from telegram import Bot, Update, ChatPermissions

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
app = Flask(__name__)

# твой Telegram ID
TARGET_USER_ID = 561176995

# время последнего сообщения
user_last_msg_time = {}

MUTE_TIME = 30  # 30 секунд

print("🔥 BOT STARTED")


@app.route("/", methods=["GET"])
def home():
    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)

    if not update.message:
        return "OK"

    user_id = update.message.from_user.id
    chat_id = update.message.chat.id

    # 👉 фильтр: работаем только с твоим ID
    if user_id != TARGET_USER_ID:
        return "OK"

    now = time.time()

    print("📩 MSG FROM TARGET USER:", user_id)

    last_time = user_last_msg_time.get(user_id, 0)

    # если меньше 30 секунд — мут
    if now - last_time < MUTE_TIME:
        print("🔇 MUTE:", user_id)

        try:
            bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=int(time.time()) + MUTE_TIME
            )
        except Exception as e:
            print("❌ ERROR:", e)

    # обновляем время
    user_last_msg_time[user_id] = now

    return "OK"


print("ROUTES LOADED:", app.url_map)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)