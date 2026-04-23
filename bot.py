from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import time

TOKEN = "8701759559:AAE3y8WlKHc_TCGBEot0PVdz5B-FcRegCPQ"
TARGET_USER_ID = 7032615601

# ⏱ по умолчанию 30 секунд
MUTE_TIME = 30

last_time = {}

# 🔧 управление из Telegram
async def slow_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global MUTE_TIME

    if not context.args:
        await update.message.reply_text("Используй: /slow 30 | 60 | 120 | off")
        return

    arg = context.args[0]

    if arg == "off":
        MUTE_TIME = 0
        await update.message.reply_text("⛔ мут отключён")
        return

    try:
        MUTE_TIME = int(arg)
        await update.message.reply_text(f"✅ мут установлен: {MUTE_TIME} сек")
    except:
        await update.message.reply_text("Ошибка. Пример: /slow 60")


# 🧠 контроль сообщений
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_time, MUTE_TIME

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

    if user_id in last_time:
        if now - last_time[user_id] < MUTE_TIME:
            await context.bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=int(time.time()) + MUTE_TIME
            )

            await msg.reply_text(f"⏳ мут на {MUTE_TIME} сек")
            return

    last_time[user_id] = now


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("slow", slow_cmd))
app.add_handler(MessageHandler(filters.ALL, handler))

app.run_polling()