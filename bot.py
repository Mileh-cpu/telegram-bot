import os
import time
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")
MY_ID = 561176995  # <-- ВСТАВЬ СВОЙ TELEGRAM ID

bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)

# Храним время последнего сообщения
last_message_time = {}

# --- ЛОГИ ---
print("🔥 BOT STARTED")

# --- ГЛАВНАЯ СТРАНИЦА ---
@app.route("/", methods=["GET"])
def home():
    return "OK"

# --- WEBHOOK ---
@app.route("/webhook", methods=["POST"])
def webhook():
    print("🔥 WEBHOOK HIT:", request.json)

    update = Update.de_json(request.get_json(force=True), bot)

    if update.message:
        user_id = update.message.from_user.id
        chat_id = update.message.chat.id
        message_id = update.message.message_id

        # Проверка: только ты
        if user_id != MY_ID:
            return "OK"

        now = time.time()

        if user_id in last_message_time:
            diff = now - last_message_time[user_id]

            if diff < 30:
                try:
                    # удаляем сообщение
                    bot.delete_message(chat_id=chat_id, message_id=message_id)

                    # мут на 30 секунд
                    bot.restrict_chat_member(
                        chat_id=chat_id,
                        user_id=user_id,
                        permissions={
                            "can_send_messages": False
                        },
                        until_date=int(now + 30)
                    )

                    print("🚫 MUTED USER")

                except Exception as e:
                    print("ERROR:", e)

        last_message_time[user_id] = now

    return "OK"

print("🔥 ROUTES AFTER LOAD:", app.url_map)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)