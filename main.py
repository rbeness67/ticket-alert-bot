from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

message = client.messages.create(
    from_=os.getenv("TWILIO_FROM_NUMBER"),
    to=os.getenv("TWILIO_TO_NUMBER"),
    body="✅ Test WhatsApp Twilio depuis mon script local !"
)

print(f"Message SID: {message.sid}")
