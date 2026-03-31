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

    @property
    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def send_text_message(self, to: PhoneNumber, content: str) -> dict:
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "body": content,
            },
        }
        response = requests.post(self.url, json=payload, headers=self._headers)
        response.raise_for_status()
        if not response.content:
            return {}
        return response.json()

    def mark_as_read(self, message_id: str) -> dict:
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
            "typing_indicator": {"type": "text"},
        }
        response = requests.post(self.url, json=payload, headers=self._headers)
        response.raise_for_status()
        if not response.content:
            return {}
        return response.json()
