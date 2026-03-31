from .text_body import TextBody
from .whatsapp_message import WhatsappMessage


class TextMessage(WhatsappMessage):
    text: TextBody
