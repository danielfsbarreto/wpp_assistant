from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field


class WhatsappMessage(BaseModel):
    model_config = {"populate_by_name": True, "serialize_by_alias": True}

    from_: str = Field(alias="from")
    id: str = ""
    timestamp: str
    type: str


def _resolve_message(v):
    if isinstance(v, dict):
        if v.get("type") == "text":
            from .text_message import TextMessage

            return TextMessage.model_validate(v)
        return WhatsappMessage.model_validate(v)
    return v


AnyWhatsappMessage = Annotated[WhatsappMessage, BeforeValidator(_resolve_message)]
