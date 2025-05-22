import os
import stripe
import asyncio
from flask import Flask, request, jsonify
from telegram import Bot
from dotenv import load_dotenv

# .envから環境変数を読み込み
load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
bot_token = os.getenv("TOKEN")
vip_link = os.getenv("VIP_LINK")

app = Flask(__name__)
bot = Bot(token=bot_token)

@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        print("❌ Invalid payload")
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        print("❌ Invalid signature:", str(e))
        return "Invalid signature", 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        telegram_id = session["metadata"].get("telegram_id")
        customer_email = session.get("customer_email")

        print(f"✅ Payment completed by: {customer_email or 'Unknown'}")

        if telegram_id:
            try:
                asyncio.run(bot.send_message(
                    chat_id=int(telegram_id),
                    text=f"🎉 Thank you for your payment!\nHere is your VIP link:\n{vip_link}"
                ))
                print(f"✅ VIP link sent to Telegram ID: {telegram_id}")
            except Exception as e:
                print("❌ Failed to send Telegram message:", e)
        else:
            print("⚠️ No telegram_id in metadata")

    return jsonify(success=True)

if __name__ == "__main__":
    app.run(port=5000)
