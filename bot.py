import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# 🔒 Kalitlarni atrof-muhit o'zgaruvchisidan olish
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# OpenAI mijozini ishga tushirish
client = OpenAI(api_key=OPENAI_API_KEY)

# Loglarni yoqish
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! Men G‘afur G‘ulom haqida ma’lumot beruvchi sun’iy intellekt botman.\nIltimos, savolingizni yozing.")

# Har qanday matnga javob berish
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Sun’iy intellektdan javob olish
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Siz G‘afur G‘ulom hayoti va ijodi bo‘yicha bilimli sun’iy intellektsiz."},
            {"role": "user", "content": user_message}
        ]
    )

    ai_reply = response.choices[0].message.content
    await update.message.reply_text(ai_reply)

# Botni ishga tushirish
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
