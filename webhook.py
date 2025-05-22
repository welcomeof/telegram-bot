import os
import stripe
import telegram
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from telegram.constants import ParseMode

load_dotenv()

app = Flask(__name__)

# 環境変数からキーを取得
stripe.api_key = os.getenv("STRIPE_SECRET")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
VIP_LINK = "https://t.me/+irG97ViEiqJhZjM1"  # ← あなたのVIPリンクに変更！

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

@app.route("/webhook", methods=["POST"])
def webhook_received():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature", None)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        print("⚠️ Invalid payload:", e)
        return jsonify(success=False), 400
    except stripe.error.SignatureVerificationError as e:
        print("❌ Invalid signature:", e)
        return jsonify(success=False), 400

    # 支払い成功時の処理
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        telegram_id = session.get("metadata", {}).get("telegram_id")
        print("✅ Payment completed by:", telegram_id)

        if telegram_id:
            try:
                bot.send_message(
                    chat_id=telegram_id,
                    text=f"🎉 Payment confirmed! Welcome to VIP!\nJoin here: {VIP_LINK}",
                    parse_mode=ParseMode.HTML,
                )
                print(f"✅ VIP link sent to Telegram ID: {telegram_id}")
            except Exception as e:
                print("❌ Error sending Telegram message:", e)
        else:
            print("⚠️ No telegram_id in metadata")

    return jsonify(success=True), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
