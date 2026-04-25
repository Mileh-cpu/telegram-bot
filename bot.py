import os
import asyncio
import time

from telegram import Update, ChatPermissions
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
TARGET_USER_ID = 7032615601

user_last_message_time = {}

print("🔥 BOT STARTING...")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if not user or not chat:
        return

    if user.id != TARGET_USER_ID:
        return

    now = time.time()

    last_time = user_last_message_time.get(user.id)

    # сохраняем текущее время
    user_last_message_time[user.id] = now

    # если это первое сообщение → ничего не делаем
    if not last_time:
        print("📩 First message - OK")
        return

    # если второе сообщение быстрее чем за 30 сек → мут
    if now - last_time < 30:
        print("⚠️ Too fast → MUTING")

        try:
            # ❌ МУТ — запрещаем ВСЁ
            await context.bot.restrict_chat_member(
                chat_id=chat.id,
                user_id=user.id,
                permissions=ChatPermissions(
                    can_send_messages=False
                )
            )

            await asyncio.sleep(30)

            # ✅ РАЗМУТ — включаем ВСЁ (ВАЖНО!)
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
                    can_add_web_page_previews=True,
                    can_change_info=False,
                    can_invite_users=True,
                    can_pin_messages=False
                )
            )

            print("🔊 UNMUTED FULL")

        except Exception as e:
            print("❌ ERROR:", e)


app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_message))


if __name__ == "__main__":
    print("🔥 BOT STARTED")
    app.run_polling()