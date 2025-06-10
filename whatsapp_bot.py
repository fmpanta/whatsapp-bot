from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from kiwi_scraper import search_flights

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot is alive", 200

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    from twilio.twiml.messaging_response import MessagingResponse
    
    incoming_msg = request.values.get('Body', '').strip().lower()
    print(f"📩 Incoming: {incoming_msg})

    resp = MessagingResponse()
    msg = resp.messsage()

    match = re.search(r'flight from (\w+) to (\w+)(?: on (\d{4}-\d{2}-\d{2}))?', incoming_msg)
    if match:
        origin, destination, date = match.groups()
        date = date or None
        print(f"🔍 Searching: {origin} → {destination}, date: {date}")

        try:
            results = search_flights(origin, destination, date)
            if results:
                msg.body(f"✈️ Cheapest flight:\n{results}")
            else:
                msg.body("No flights found")
        except Exception as e:
            print(f"❗ Scraper error: {e}")
            msg.body("Failed to fetch flight info.")
    else:
        msg.body("🤖 Try:\nflight from lisbon to madrid on 2025-06-15")

    return str(resp)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


