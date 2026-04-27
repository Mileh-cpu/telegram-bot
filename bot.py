import os
from datetime import datetime, timedelta, timezone

from telegram import Update, ChatPermissions
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
TARGET_USER_ID = 561176995

print("🔥 BOT STARTED")

START_TIME = datetime.now(timezone.utc)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.effective_user
    chat = update.effective_chat

    if not user or not chat:
        return

    # ❌ игнор старых сообщений (ВАЖНО — фикс твоей проблемы)
    if update.message.date < START_TIME:
        return

    if user.id != TARGET_USER_ID:
        return

    try:
        # 🔇 мут на 30 секунд (включая медиа)
        await context.bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            permissions=ChatPermissions(),
            until_date=datetime.now(timezone.utc) + timedelta(seconds=30)
        )

        print(f"🔇 MUTED user={user.id} chat={chat.id} for 30s")

    except Exception as e:
        print("❌ ERROR MUTING:", e)


app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.ALL & (~filters.StatusUpdate.ALL), handle_message)
)

if __name__ == "__main__":
    app.run_polling(drop_pending_updates=True)