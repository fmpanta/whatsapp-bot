from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from kiwi_scraper import search_flights

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot is alive", 200

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg.startswith("search"):
        parts = incoming_msg.split()
        if len(parts) >= 3:
            origin = parts[1].upper()
            destination = parts[2].upper()
            date = parts[3] if len(parts) > 3 else "any"
            flights = search_flights(origin, destination, date)
            msg.body("\n\n".join(flights))
        else:
            msg.body("Please use format: search LIS AMS 2024-06-12 or search LIS AMS any")

    return str(resp)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


