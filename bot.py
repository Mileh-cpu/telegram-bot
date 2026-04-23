import os
import time
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
TARGET_USER_ID = 7032615601

MUTE_TIME = 30
last_time = {}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

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
            try:
                await asyncio.sleep(1)

                await context.bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=int(time.time()) + MUTE_TIME
                )
            except:
                pass
            return

    last_time[user_id] = now


threading.Thread(target=run_server).start()

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("slow", slow_cmd))
app.add_handler(MessageHandler(filters.ALL, handler))

app.run_polling(drop_pending_updates=True)