import os
import time
from flask import Flask, request
from telegram import Bot, Update, ChatPermissions

# ===== CONFIG =====
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ BOT_TOKEN NOT FOUND")
    exit()

bot = Bot(token=TOKEN)
app = Flask(__name__)

user_data = {}
MUTE_TIME = 30
TARGET_USER_ID = 561176995

print("🔥 BOT STARTED")
print("ROUTES LOADED")
print(app.url_map)

# ===== ROUTES =====

@app.route("/", methods=["GET", "POST"])
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    print("🔥 WEBHOOK HIT:", request.method, request.path)

    try:
        data = request.get_json(force=True, silent=True)

        if not data:
            print("⚠️ EMPTY REQUEST")
            return "OK", 200

        update = Update.de_json(data, bot)

        if not update or not update.message:
            return "OK", 200

        user_id = update.message.from_user.id
        chat_id = update.message.chat.id
        now = time.time()

        print("📩 MSG FROM:", user_id)

        # 👉 только один пользователь
        if user_id != TARGET_USER_ID:
            return "OK", 200

        last_time = user_data.get(user_id, 0)

        # 👉 антиспам 30 сек
        if now - last_time < MUTE_TIME:
            print("🔇 MUTE TRIGGERED")

            bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=int(time.time()) + MUTE_TIME
            )

        user_data[user_id] = now

        return "OK", 200

    except Exception as e:
        print("❌ ERROR:", e)
        return "OK", 200


# ===== HEALTH CHECK =====
@app.route("/health")
def health():
    return "OK", 200


# ===== RUN =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)