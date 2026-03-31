from pydantic import BaseModel, SerializeAsAny

from .run_type import RunType
from .whatsapp_message import AnyWhatsappMessage


class WppAssistantState(BaseModel):
    run_type: RunType = RunType.DEFAULT
    messages: list[SerializeAsAny[AnyWhatsappMessage]] = []
