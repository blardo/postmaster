from twilio.rest import TwilioRestClient
from nameko.events import event_handler


class TextService(object):
    name = "text_service"

    ACCOUNT_SID = ""
    AUTH_TOKEN = ""

    twilio = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    @event_handler("event_dispatcher", "send_text")
    def send_text(self, payload):
        recipient = payload.get('recipient')
        body = payload.get('body')

        self.twilio.messages.create(
            from_=85159,
            to=recipient,
            body=body
        )

    @event_handler("event_dispatcher", "debug_text")
    def debug_text(self, payload):
        print("service b received:", payload)
