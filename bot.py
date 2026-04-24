import os
import asyncio

from telegram import Update, ChatPermissions
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

# === НАСТРОЙКИ ===
TOKEN = os.getenv("BOT_TOKEN")
TARGET_USER_ID = 561176995


# === СОЗДАНИЕ БОТА ===
app = Application.builder().token(TOKEN).build()


# === ЛОГИКА МУТА ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if not user or not chat:
        return

    # только твой ID
    if user.id != TARGET_USER_ID:
        return

    print(f"🔥 TRIGGER MUT: user={user.id}, chat={chat.id}")

    try:
        # мут на 30 секунд
        await context.bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            permissions=ChatPermissions(
                can_send_messages=False
            ),
        )

        print("🔇 Muted for 30 seconds")

        await asyncio.sleep(30)

        # размут
        await context.bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            permissions=ChatPermissions(
                can_send_messages=True
            ),
        )

        print("🔊 Unmuted")

    except Exception as e:
        print("❌ ERROR:", e)


# === ХЕНДЛЕР ===
app.add_handler(MessageHandler(filters.ALL, handle_message))


# === ЗАПУСК ===
if __name__ == "__main__":
    print("🔥 BOT STARTED")

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url="https://telegram-bot-ktr9.onrender.com/webhook"
    )