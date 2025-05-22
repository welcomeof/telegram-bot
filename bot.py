from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

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
    "ja": {
        "start": (
            "👋 ようこそ！\n\n"
            "このアカウントでは、世界各国の特別な動画コンテンツを無料でご覧いただけます🌍\n"
            "リアルな映像をすぐ体験してください！\n\n"
            "言語を変更 ➡️\n"
            "➡️English🇺🇸/langEG\n"
            "➡️日本語🇯🇵/langJP\n"
            "➡️ประเทศไทย🇹🇭/langTH\n"
            "VIPはこちら ➡️ /vip\n\n"
            "👇 お好きな国を選んでチェック：\n\n"
            "🌏 世界の動画：https://t.me/+A_k5WIBrwlNhMTE9\n"
            "🇹🇭 タイの動画：https://t.me/+fz1MxCOAzrsyZmJl\n"
            "🇯🇵 日本の動画：https://t.me/+WSC5-RAM1Yo4MDM1\n"
            "🇨🇳 中国の動画：https://t.me/+tZVW2pFqG2djODU1\n"
            "🇰🇷 韓国の動画：近日公開予定"
        ),
        "help": (
            "🛠 Botの使い方：\n\n"
            "/start - 最初の案内メッセージ\n"
            "/help - このヘルプを表示します\n"
            "/vip - VIPプランと支払いリンク\n"
            "/langEG /langJP /langTH - 言語を変更"
        ),
        "vip": (
            "💎 *VIPアクセスプラン* 💎\n\n"
            "限定VIPコンテンツへのアクセスを解除：\n\n"
            "🔹 1ヶ月：$4.99\n"
            "🔹 3ヶ月：$13.99\n"
            "🔹 6ヶ月：$24.99\n"
            "🔹 永久アクセス：$99（買い切り）\n\n"
            "👇 プランを選んで決済してください：\n"
            "[1ヶ月プラン](https://buy.stripe.com/test_6oUeVd3Ej8eKfkKav938405)\n"
            "[3ヶ月プラン](https://buy.stripe.com/test_fZu5kD7Uz66C4G67iX38404)\n"
            "[6ヶ月プラン](https://buy.stripe.com/test_dRm9ATfn10Mic8y7iX38403)\n"
            "[永久プラン](https://buy.stripe.com/test_9B69AT3Ej8eKc8ydHl38400)"
        ),
        "lang_set": "✅ 言語が日本語に設定されました\n"
        "👋 ようこそ！\n\n"
            "このアカウントでは、世界各国の特別な動画コンテンツを無料でご覧いただけます🌍\n"
            "リアルな映像をすぐ体験してください！\n\n"
            "言語を変更 ➡️\n"
            "➡️English🇺🇸/langEG\n"
            "➡️日本語🇯🇵/langJP\n"
            "➡️ประเทศไทย🇹🇭/langTH\n"
            "VIPはこちら ➡️ /vip\n\n"
            "👇 お好きな国を選んでチェック：\n\n"
            "🌏 世界の動画：https://t.me/+A_k5WIBrwlNhMTE9\n"
            "🇹🇭 タイの動画：https://t.me/+fz1MxCOAzrsyZmJl\n"
            "🇯🇵 日本の動画：https://t.me/+WSC5-RAM1Yo4MDM1\n"
            "🇨🇳 中国の動画：https://t.me/+tZVW2pFqG2djODU1\n"
            "🇰🇷 韓国の動画：近日公開予定"
    },
    "th": {
        "start": (
            "👋 ยินดีต้อนรับ!\n\n"
            "บัญชีนี้ให้คุณรับชมวิดีโอสุดพิเศษจากทั่วโลกได้ฟรี 🌍\n"
            "รับชมภาพจริงแบบเรียลไทม์ได้ทันที!\n\n"
            "เปลี่ยนภาษา ➡️ \n"
            "➡️English🇺🇸/langEG\n"
            "➡️日本語🇯🇵/langJP\n"
            "➡️ประเทศไทย🇹🇭/langTH\n"
            "สำหรับ VIP ➡️ /vip\n\n"
            "👇 เลือกประเทศที่คุณสนใจ:\n\n"
            "🌏 วิดีโอทั่วโลก: https://t.me/+A_k5WIBrwlNhMTE9\n"
            "🇹🇭 วิดีโอประเทศไทย: https://t.me/+fz1MxCOAzrsyZmJl\n"
            "🇯🇵 วิดีโอญี่ปุ่น: https://t.me/+WSC5-RAM1Yo4MDM1\n"
            "🇨🇳 วิดีโอประเทศจีน: https://t.me/+tZVW2pFqG2djODU1\n"
            "🇰🇷 วิดีโอเกาหลี: เร็วๆ นี้"
        ),
        "help": (
            "🛠 วิธีใช้งานบอท:\n\n"
            "/start - แสดงข้อความต้อนรับ\n"
            "/help - แสดงคู่มือการใช้งาน\n"
            "/vip - แสดงแผน VIP และลิงก์ชำระเงิน\n"
            "/langEG /langJP /langTH - เปลี่ยนภาษา"
        ),
        "vip": (
    "💫 *แผนการเข้าถึง VIP* 💫\n\n"
    "ปลดล็อกการเข้าถึงวิดีโอ VIP สุดพิเศษ:\n\n"
    "🔹 1 เดือน: $4.99\n"
    "🔹 3 เดือน: $13.99\n"
    "🔹 6 เดือน: $24.99\n"
    "🔹 เข้าถึงตลอดชีพ: $99 (ชำระครั้งเดียว)\n\n"
    "👇 เลือกแผนและชำระเงิน:\n"
    "[แผน 1 เดือน](https://buy.stripe.com/test_6oUeVd3Ej8eKfkKav938405)\n"
    "[แผน 3 เดือน](https://buy.stripe.com/test_fZu5kD7Uz66C4G67iX38404)\n"
    "[แผน 6 เดือน](https://buy.stripe.com/test_dRm9ATfn10Mic8y7iX38403)\n"
    "[แผนตลอดชีพ](https://buy.stripe.com/test_9B69AT3Ej8eKc8ydHl38400)"
),
        "lang_set": "✅ ตั้งค่าภาษาเป็นภาษาไทยแล้ว\n"
        "👋 ยินดีต้อนรับ!\n\n"
            "บัญชีนี้ให้คุณรับชมวิดีโอสุดพิเศษจากทั่วโลกได้ฟรี 🌍\n"
            "รับชมภาพจริงแบบเรียลไทม์ได้ทันที!\n\n"
            "เปลี่ยนภาษา ➡️ \n"
            "➡️English🇺🇸/langEG\n"
            "➡️日本語🇯🇵/langJP\n"
            "➡️ประเทศไทย🇹🇭/langTH\n"
            "สำหรับ VIP ➡️ /vip\n\n"
            "👇 เลือกประเทศที่คุณสนใจ:\n\n"
            "🌏 วิดีโอทั่วโลก: https://t.me/+A_k5WIBrwlNhMTE9\n"
            "🇹🇭 วิดีโอประเทศไทย: https://t.me/+fz1MxCOAzrsyZmJl\n"
            "🇯🇵 วิดีโอญี่ปุ่น: https://t.me/+WSC5-RAM1Yo4MDM1\n"
            "🇨🇳 วิดีโอประเทศจีน: https://t.me/+tZVW2pFqG2djODU1\n"
            "🇰🇷 วิดีโอเกาหลี: เร็วๆ นี้"
    }
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
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(messages[lang]["vip"], parse_mode="Markdown")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CommandHandler("langEG", lang_eg))
    app.add_handler(CommandHandler("langJP", lang_jp))
    app.add_handler(CommandHandler("langTH", lang_th))
    app.run_polling()

