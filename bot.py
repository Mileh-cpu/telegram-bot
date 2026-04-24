import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from telegram.constants import ChatPermissions

TOKEN = os.getenv("BOT_TOKEN")

TARGET_USER_ID = 561176995

app = Application.builder().token(TOKEN).build()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if not user or not chat:
        return

    # только твой ID
    if user.id != TARGET_USER_ID:
        return

    print(f"TRIGGER: {user.id} in chat {chat.id}")

    try:
        # мут
        await context.bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            permissions=ChatPermissions(can_send_messages=False)
        )

        await asyncio.sleep(30)

        # размут
        await context.bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            permissions=ChatPermissions(can_send_messages=True)
        )

    except Exception as e:
        print("ERROR:", e)


app.add_handler(MessageHandler(filters.ALL, handle_message))


if __name__ == "__main__":
    print("🔥 BOT STARTED")

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url="https://telegram-bot-ktr9.onrender.com/"
    )