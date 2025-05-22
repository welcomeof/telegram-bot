from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
import stripe

load_dotenv()
TOKEN = os.getenv("TOKEN")
stripe.api_key = os.getenv("STRIPE_SECRET")

# ユーザーごとの言語設定を保持
user_languages = {}

# StripeプランごとのPrice ID（テスト用）
PRICE_IDS = {
    "1": "price_1RRTL7FoXHAo9SCHDmOJBi8o",
    "3": "price_1RRTPzFoXHAo9SCH8tPoj7HM",
    "6": "price_1RRTgiFoXHAo9SCHYXTyT0c0",
    "99": "price_1RRTQxFoXHAo9SCH3waWiNyU"
}

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
            "💫 *VIP Access Plans* 💫\n\n"
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
    }
}

def get_lang(user_id):
    return user_languages.get(user_id, "en")

async def lang_eg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_languages[update.effective_user.id] = "en"
    await update.message.reply_text(messages["en"]["lang_set"])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(messages[lang]["start"])

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(messages[lang]["help"])

async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(messages[lang]["vip"], parse_mode="Markdown")

async def create_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE, period: str):
    try:
        chat_id = update.effective_chat.id
        price_id = PRICE_IDS[period]

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            metadata={"telegram_id": str(chat_id)},
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )

        await update.message.reply_text(f"💳 Please complete your payment:\n{session.url}")
    except Exception as e:
        print("❌ Stripe error:", e)
        await update.message.reply_text("❌ Failed to create payment link. Please try again later.")

async def vip1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await create_checkout(update, context, "1")

async def vip3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await create_checkout(update, context, "3")

async def vip6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await create_checkout(update, context, "6")

async def vip99(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await create_checkout(update, context, "99")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CommandHandler("vip1", vip1))
    app.add_handler(CommandHandler("vip3", vip3))
    app.add_handler(CommandHandler("vip6", vip6))
    app.add_handler(CommandHandler("vip99", vip99))
    app.add_handler(CommandHandler("langEG", lang_eg))
    app.run_polling()
