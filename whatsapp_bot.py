from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "hello" in incoming_msg:
        msg.body("👋 Hi! This is your WhatsApp bot. How can I help?")
    elif "price" in incoming_msg:
        msg.body("✈️ The cheapest flight today is €67.")
    else:
        msg.body("🤖 Sorry, I didn't understand that. Type 'hello' or 'price'.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

