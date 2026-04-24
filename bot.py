import time
from flask import Flask, request
from telegram import Bot, Update

TOKEN = "ТВОЙ_ТОКЕН"

bot = Bot(token=TOKEN)
app = Flask(__name__)

user_data = {}
MUTE_TIME = 30

print("BOT STARTED")

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

        last_time = user_data[user_id]["last"]

        # 👉 ЕСЛИ ПИШЕТ РАНЬШЕ 30 СЕК
        if now - last_time < MUTE_TIME:
            print("MUTE:", user_id)
            bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions={"can_send_messages": False},
                until_date=int(time.time()) + MUTE_TIME
            )

        # обновляем время последнего сообщения
        user_data[user_id]["last"] = now

    return "OK"


@app.route("/")
def home():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)