import os

_AUTHORIZED_USERS = os.getenv("AUTHORIZED_NUMBERS").split(",")


def is_authorized_user(phone_number: str) -> bool:
    return phone_number in _AUTHORIZED_USERS
