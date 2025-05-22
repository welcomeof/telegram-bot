import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌏 世界の動画はこちら", url="https://t.me/+A_k5WIBrwlNhMTE9")],
        [InlineKeyboardButton("🇹🇭 タイの動画はこちら", url="https://t.me/+fz1MxCOAzrsyZmJl")],
        [InlineKeyboardButton("🇯🇵 日本の動画はこちら", url="https://t.me/+WSC5-RAM1Yo4MDM1")],
        [InlineKeyboardButton("🇨🇳 中国の動画はこちら", url="https://t.me/+tZVW2pFqG2djODU1")],
        [InlineKeyboardButton("🇰🇷 韓国の動画はこちら（近日公開）", url="https://t.me/dailyhomework")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        "📍 Message:\n"
        "👋 ようこそ！\n\n"
        "このBotでは、世界各国の特別な動画コンテンツを無料でご覧いただけます🌍\n"
        "リアルな映像をすぐ体験してください！\n\n"
        "👇 下のボタンからお好きな国を選んで、今すぐチェック！\n\n"
        "⬇️ Inline buttons:"
    )

    await update.message.reply_text(message, reply_markup=reply_markup)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
