import os
import time
import asyncio
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
TARGET_USER_ID = 7032615601

MUTE_TIME = 30
mute_until = {}

async def slow_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global MUTE_TIME

    if not context.args:
        await update.message.reply_text("30 | 60 | 120 | off")
        return

    arg = context.args[0]

    if arg == "off":
        MUTE_TIME = 0
        return

    try:
        MUTE_TIME = int(arg)
    except:
        pass

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global mute_until, MUTE_TIME

    msg = update.message
    if not msg:
        return

    user_id = msg.from_user.id
    chat_id = msg.chat.id

    if user_id != TARGET_USER_ID:
        return

    if MUTE_TIME == 0:
        return

    now = time.time()

    if user_id in mute_until and now < mute_until[user_id]:
        return

    if user_id in mute_until and now >= mute_until[user_id]:
        del mute_until[user_id]

    try:
        await asyncio.sleep(1)

        mute_until[user_id] = now + MUTE_TIME

        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=int(mute_until[user_id])
        )

    except Exception as e:
        print(e)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("slow", slow_cmd))
app.add_handler(MessageHandler(filters.ALL, handler))

app.run_polling(drop_pending_updates=True)