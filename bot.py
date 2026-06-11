import os
import asyncio

from telegram import Update, ChatPermissions
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
TARGET_USER_ID = 7032615601

print("🔥 BOT STARTING...")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if not user or not chat:
        return

    # только нужный пользователь
    if user.id != TARGET_USER_ID:
        return

    print(f"🔥 MESSAGE FROM TARGET USER: {user.id}")

    try:
        # --- МУТ ---
        # сообщения и медиа запрещаем
        # реакции останутся
        await context.bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            permissions=ChatPermissions(
                can_send_messages=False,
                can_send_audios=False,
                can_send_documents=False,
                can_send_photos=False,
                can_send_videos=False,
                can_send_video_notes=False,
                can_send_voice_notes=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False
            )
        )

        print("🔇 MUTED")

        # --- ЖДЁМ 180 СЕК ---
        await asyncio.sleep(180)

        # --- РАЗМУТ ---
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


app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.ALL, handle_message))


if __name__ == "__main__":
    print("🔥 BOT STARTED")
    app.run_polling()