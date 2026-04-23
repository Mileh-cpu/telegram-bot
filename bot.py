import os
import time
import asyncio
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
TARGET_USER_ID = 561176995

MUTE_TIME = 10
last_time = {}

async def slow_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global MUTE_TIME

    if not context.args:
        await update.message.reply_text("Используй: /slow 10 | 30 | 60 | off")
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

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_time, MUTE_TIME

    msg = update.message
    if not msg:
        return

    user_id = msg.from_user.id
    chat_id = msg.chat.id

    print("MESSAGE FROM:", user_id)

    if user_id != TARGET_USER_ID:
        print("NOT TARGET USER")
        return

    if MUTE_TIME == 0:
        print("MUTE OFF")
        return

    now = time.time()

    if user_id in last_time:
        print("CHECK TIME")

        if now - last_time[user_id] < MUTE_TIME:
            print("MUTE TRIGGERED")

            try:
                await asyncio.sleep(1)

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
    print("FIRST MESSAGE SAVED")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("slow", slow_cmd))
app.add_handler(MessageHandler(filters.ALL, handler))

app.run_polling(drop_pending_updates=True)