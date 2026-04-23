import os
import time
import asyncio
from flask import Flask, request
from telegram import Update, Bot, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")
TARGET_USER_ID = 561176995
MUTE_TIME = 30

last_time = {}

bot = Bot(token=TOKEN)
app = Flask(__name__)

application = Application.builder().token(TOKEN).build()

print("BOT STARTED")

async def slow_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global MUTE_TIME

    if not context.args:
        await update.message.reply_text("Используй: /slow 30 | 60 | off")
        return

    arg = context.args[0]

    if arg == "off":
        MUTE_TIME = 0
        await update.message.reply_text("мут выключен")
        return

    try:
        MUTE_TIME = int(arg)
        await update.message.reply_text(f"мут: {MUTE_TIME} сек")
    except:
        await update.message.reply_text("ошибка")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_time, MUTE_TIME

    msg = update.message
    if not msg:
        return

    user_id = msg.from_user.id
    chat_id = msg.chat.id

    print("MSG FROM:", user_id)

    if user_id != TARGET_USER_ID:
        return

    now = time.time()

    if user_id in last_time:
        if now - last_time[user_id] < MUTE_TIME:
            try:
                await context.bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=int(time.time()) + MUTE_TIME
                )
            except Exception as e:
                print("ERROR:", e)
            return

    last_time[user_id] = now


application.add_handler(CommandHandler("slow", slow_cmd))
application.add_handler(MessageHandler(filters.ALL, handle_message))


@app.route("/", methods=["GET"])
def home():
    return "OK"


@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(application.process_update(update))
    return "OK"


if __name__ == "__main__":
    asyncio.run(application.initialize())
    asyncio.run(application.start())

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)