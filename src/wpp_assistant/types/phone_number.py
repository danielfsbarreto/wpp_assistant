from typing import Annotated

from pydantic import Field

PhoneNumber = Annotated[
    str,
    Field(
        description="Phone number in E.164 format (e.g. +[COUNTRY_CODE][AREA_CODE][PHONE_NUMBER])",
        pattern=r"^\d{7,15}$",
    ),
]
