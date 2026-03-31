from pydantic import BaseModel, SerializeAsAny

from .whatsapp_message import AnyWhatsappMessage


class WppAssistantState(BaseModel):
    messages: list[SerializeAsAny[AnyWhatsappMessage]] = []
