import os
import time
from flask import Flask, request
from telegram import Bot, Update, ChatPermissions

# 🔥 ВАЖНО: у тебя в Render переменная BOT_TOKEN
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN not found in environment variables")

bot = Bot(token=TOKEN)
app = Flask(__name__)

# твой Telegram ID
ALLOWED_USER_ID = 561176995

# 30 секунд между сообщениями
MUTE_TIME = 30

# хранение времени сообщений
user_data = {}

print("🔥 BOT STARTED")
print("ROUTES LOADED:", app.url_map)


@app.route("/")
def home():
    return "OK"


@app.route("/health")
def health():
    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook():
    print("🔥 WEBHOOK HIT")

    data = request.get_json(force=True)
    update = Update.de_json(data, bot)

    if not update.message:
        return "OK"

    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    now = time.time()

    print("MSG FROM:", user_id)

    # 👉 фильтр только на тебя
    if user_id != ALLOWED_USER_ID:
        return "OK"

    last_time = user_data.get(user_id, 0)

    # 👉 если пишешь быстрее чем 30 сек
    if now - last_time < MUTE_TIME:
        print("MUTE TRIGGERED")

        bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=False
            ),
            until_date=int(now + MUTE_TIME)
        )

    user_data[user_id] = now

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)