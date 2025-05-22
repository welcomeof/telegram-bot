from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
import stripe

load_dotenv()
TOKEN = os.getenv("TOKEN")
stripe.api_key = os.getenv("STRIPE_SECRET")

# ユーザーごとの言語設定を保持（簡易的にメモリ保持）
user_languages = {}

# 言語別メッセージ定義
messages = {
    "en": {
        "start": (
            "👋 Welcome!\n\n"
            "With this account, you can enjoy exclusive video content from around the world for free 🌍\n"
            "Experience real scenes instantly!\n\n"
            "Change Language\n"
            "➡️English🇺🇸/langEG\n"
            "➡️日本語🇯🇵/langJP\n"
            "➡️ประเทศไทย🇹🇭/langTH\n"
            "for VIP Channel Access➡️ /VIP\n\n"
            "👇 Choose your preferred country from the links below:\n\n"
            "🌏 Global Videos: https://t.me/+A_k5WIBrwlNhMTE9\n"
            "🇹🇭 Thailand Videos: https://t.me/+fz1MxCOAzrsyZmJl\n"
            "🇯🇵 Japan Videos: https://t.me/+WSC5-RAM1Yo4MDM1\n"
            "🇨🇳 China Videos: https://t.me/+tZVW2pFqG2djODU1\n"
            "🇰🇷 Korea Videos: Coming Soon"
        ),
        "help": (
            "🛠 How to use this bot:\n\n"
            "/start - Shows the welcome message\n"
            "/help - Displays this help guide\n"
            "/vip - Shows subscription plans and payment link\n"
            "/langEG /langJP /langTH - Change language"
        ),
        "vip": (
            "💎 *VIP Access Plans* 💎\n\n"
            "Unlock access to exclusive VIP content:\n\n"
            "🔹 1 Month: $4.99\n"
            "🔹 3 Months: $13.99\n"
            "🔹 6 Months: $24.99\n"
            "🔹 Lifetime Access: $99 (One-time payment)\n\n"
            "👇 Choose a plan and complete the payment:\n"
            "[1 Month Plan](https://buy.stripe.com/test_6oUeVd3Ej8eKfkKav938405)\n"
            "[3 Months Plan](https://buy.stripe.com/test_fZu5kD7Uz66C4G67iX38404)\n"
            "[6 Months Plan](https://buy.stripe.com/test_dRm9ATfn10Mic8y7iX38403)\n"
            "[Lifetime Plan](https://buy.stripe.com/test_9B69AT3Ej8eKc8ydHl38400)"
        ),
        "lang_set": "✅ Language set to English."
    },
    "ja": {...},  # 省略（同じ）
    "th": {...}   # 省略（同じ）
}

def get_lang(user_id):
    return user_languages.get(user_id, "en")

# 各言語切替コマンド
async def lang_eg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_languages[update.effective_user.id] = "en"
    await update.message.reply_text(messages["en"]["lang_set"])

async def lang_jp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_languages[update.effective_user.id] = "ja"
    await update.message.reply_text(messages["ja"]["lang_set"])

async def lang_th(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_languages[update.effective_user.id] = "th"
    await update.message.reply_text(messages["th"]["lang_set"])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(messages[lang]["start"])

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(messages[lang]["help"])

async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        telegram_id = update.effective_chat.id
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price": "price_XXXXXXXXXXXX",  # ← あなたの価格IDに置き換えてください
                "quantity": 1,
            }],
            metadata={"telegram_id": str(telegram_id)},
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )
        await update.message.reply_text(f"💳 Please complete payment:\n{session.url}")
    except Exception as e:
        await update.message.reply_text("❌ Failed to create Stripe session.")
        print(e)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CommandHandler("langEG", lang_eg))
    app.add_handler(CommandHandler("langJP", lang_jp))
    app.add_handler(CommandHandler("langTH", lang_th))
    app.run_polling()
