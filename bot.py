import os
import asyncio
from datetime import datetime, timezone

from telegram import Update, ChatPermissions
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
TARGET_USER_ID = 7032615601

print("🔥 BOT STARTING...")

# фикс: стартовое время, чтобы игнорировать старые сообщения
START_TIME = datetime.now(timezone.utc)

# защита от повторных запусков мута
active_mutes = set()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.effective_user
    chat = update.effective_chat

    if not user or not chat:
        return

    # 🚨 ВАЖНО: игнор старых сообщений
    if update.message.date.replace(tzinfo=timezone.utc) < START_TIME:
        return

    if user.id != TARGET_USER_ID:
        return

    # защита от параллельных мутов
    if user.id in active_mutes:
        return

    print(f"🔥 MESSAGE FROM TARGET USER: {user.id}")

    active_mutes.add(user.id)

    try:
        # 🔇 МУТ (полный запрет включая медиа)
        await context.bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            permissions=ChatPermissions()
        )

        print("🔇 MUTED")

        # ⏳ ждём 45 секунд
        await asyncio.sleep(45)

        # 🔊 РАЗМУТ (всё возвращаем)
        await context.bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_audios=True,
                can_send_documents=True,
                can_send_photos=True,
                can_send_videos=True,
                can_send_video_notes=True,
                can_send_voice_notes=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )

        print("🔊 UNMUTED")

    except Exception as e:
        print("❌ ERROR:", e)

    finally:
        active_mutes.discard(user.id)


app = Application.builder().token(TOKEN).build()

# 🚨 убираем старые апдейты + фильтруем системные события
app.add_handler(
    MessageHandler(filters.ALL & (~filters.StatusUpdate.ALL), handle_message)
)

if __name__ == "__main__":
    print("🔥 BOT STARTED")
    app.run_polling(drop_pending_updates=True)