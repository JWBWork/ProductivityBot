from twilio.rest import Client
from src.config import config

account = config['twilio']['creds']['account']
token = config['twilio']['creds']['token']
client = Client(account, token)
TESTING = False


def send_message(message, number=None, from_=None):
    if not TESTING:
        to = number or config['twilio']['numbers']['to']
        from_ = from_ or config['twilio']['numbers']['from']
        message = client.messages.create(
            to=to,
            from_=from_,
            body=message
        )
        return message
    else:
        print(f"\n🤖 <('{message}')\n")
