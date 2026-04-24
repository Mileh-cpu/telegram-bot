import os
import asyncio

from telegram import Update, ChatPermissions
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
TARGET_USER_ID = 561176995

print("🔥 BOT STARTING...")
print("TOKEN:", TOKEN)

# 🔴 ВАЖНО
if not TOKEN:
    raise Exception("❌ BOT_TOKEN НЕ НАЙДЕН В RENDER")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if not user or not chat:
        return

    if user.id != TARGET_USER_ID:
        return

    print(f"🔥 MESSAGE FROM TARGET USER: {user.id}")

    try:
        await context.bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            permissions=ChatPermissions(can_send_messages=False)
        )

        print("🔇 MUTED")

        await asyncio.sleep(30)

        await context.bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            permissions=ChatPermissions(can_send_messages=True)
        )

        print("🔊 UNMUTED")

    except Exception as e:
        print("❌ ERROR:", e)


app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))


if __name__ == "__main__":
    print("🔥 BOT STARTED")
    app.run_polling()