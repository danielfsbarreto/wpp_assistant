import os

import requests

from wpp_assistant.types import PhoneNumber


class WhatsappMessenger:
    def __init__(self):
        url = os.getenv("WHATSAPP_MESSENGER_URL")
        token = os.getenv("WHATSAPP_MESSENGER_TOKEN")
        missing = [name for name, val in (("url", url), ("token", token)) if not val]
        if missing:
            raise ValueError(
                f"WhatsappMessenger requires non-empty values for: {', '.join(missing)}"
            )

        self.url = url
        self.token = token

    def send_text_message(self, to: PhoneNumber, content: str) -> dict:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "body": content,
            },
        }
        response = requests.post(self.url, json=payload, headers=headers)
        response.raise_for_status()
        if not response.content:
            return {}
        return response.json()
