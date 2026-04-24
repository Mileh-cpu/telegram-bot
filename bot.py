import os
import time
from flask import Flask, request
from telegram import Bot, Update, ChatPermissions

# ⚠️ важно: имя должно совпадать с Render variable
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ TOKEN NOT FOUND IN ENV")
    exit()

bot = Bot(token=TOKEN)
app = Flask(__name__)

user_data = {}

MUTE_TIME = 30
TARGET_USER_ID = 561176995

print("BOT STARTED")

@app.route("/")
def home():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)

        if not update.message:
            return "OK", 200

        user_id = update.message.from_user.id
        chat_id = update.message.chat.id
        now = time.time()

        print("MSG FROM:", user_id)

        # 👉 только твой пользователь
        if user_id != TARGET_USER_ID:
            return "OK", 200

        last_time = user_data.get(user_id, 0)

        # 👉 если прошло меньше 30 сек → мут
        if now - last_time < MUTE_TIME:
            print("MUTE TRIGGERED")

            bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=int(time.time()) + MUTE_TIME
            )

        # обновляем время
        user_data[user_id] = now

        return "OK", 200

    except Exception as e:
        print("ERROR:", e)
        return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)