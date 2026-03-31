from pydantic import BaseModel, SerializeAsAny

from .whatsapp_message import AnyWhatsappMessage


class Conversation(BaseModel):
    id: str = ""
    phone_number: str = ""
    messages: list[SerializeAsAny[AnyWhatsappMessage]] = []
