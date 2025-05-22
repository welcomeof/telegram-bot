import stripe
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook_received():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature", None)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print("⚠️ Invalid payload:", e)
        return jsonify(success=False), 400
    except stripe.error.SignatureVerificationError as e:
        print("❌ Invalid signature:", e)
        return jsonify(success=False), 400

    # 支払い成功イベントの処理
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_email")
        print(f"✅ Payment succeeded for: {customer_email}")
        # TODO: Telegram Bot で VIP リンク送信処理を追加

    return jsonify(success=True), 200

if __name__ == "__main__":
    app.run(port=5000)
