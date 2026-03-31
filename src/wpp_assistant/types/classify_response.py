from pydantic import BaseModel

from .capability import Capability


class ClassifyResponse(BaseModel):
    capabilities: list[Capability]
