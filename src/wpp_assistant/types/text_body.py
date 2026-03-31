from pydantic import BaseModel


class TextBody(BaseModel):
    body: str
