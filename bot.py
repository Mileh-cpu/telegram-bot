import os
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

    try:
        # мут на 30 секунд
        await context.bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            permissions=ChatPermissions(
                can_send_messages=False
            )
        )

        # через 30 сек размут
        import asyncio
        await asyncio.sleep(30)

        await context.bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            permissions=ChatPermissions(
                can_send_messages=True
            )
        )

    except Exception as e:
        print("ERROR:", e)


app.add_handler(MessageHandler(filters.ALL, handle_message))


if __name__ == "__main__":
    print("BOT STARTED")
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=f"https://telegram-bot-ktr9.onrender.com/webhook"
    )