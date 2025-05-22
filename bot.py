from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "👋 ようこそ！\n\n"
        "このBotでは、世界各国の特別な動画コンテンツを無料でご覧いただけます🌍\n"
        "リアルな映像をすぐ体験してください！\n\n"
        "👇 以下のリンクからお好きな国をチェック：\n\n"
        "🌏 世界の人気動画：https://t.me/+A_k5WIBrwlNhMTE9\n"
        "🇹🇭 タイの話題動画：https://t.me/+fz1MxCOAzrsyZmJl\n"
        "🇯🇵 日本の最新バズ動画：https://t.me/+WSC5-RAM1Yo4MDM1\n"
        "🇨🇳 中国で人気の映像：https://t.me/+tZVW2pFqG2djODU1\n"
        "🇰🇷 韓国の動画：近日公開予定"
    )

    await update.message.reply_text(message)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
