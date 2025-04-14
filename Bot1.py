from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
import logging

# تنظیمات لاگ
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
TOKEN = ""

# ---------- دستورات پایه ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["آبوهوا ☁️", "اخبار 📰"], ["درباره ما ❓"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("خوش آمدید! گزینه مورد نظر را انتخاب کنید:", reply_markup=reply_markup)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("راهنما:\n/start - شروع\n/help - راهنما")

# ---------- پاسخ به پیامها ----------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if user_text == "آبوهوا ☁️":
        # مثال: دریافت آبوهوا از یک API خارجی
        await update.message.reply_text("دمای تهران: ۲۵°C ☀️")
    elif user_text == "اخبار 📰":
        await update.message.reply_text("آخرین اخبار: ...")
    else:
        await update.message.reply_text("پیام شما دریافت شد!")

# ---------- ذخیرهسازی دادهها در SQLite ----------
def save_to_db(user_id, message):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (user_id INT, message TEXT)''')
    cursor.execute("INSERT INTO messages VALUES (?, ?)", (user_id, message))
    conn.commit()
    conn.close()

# ---------- اجرای بات ----------
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()