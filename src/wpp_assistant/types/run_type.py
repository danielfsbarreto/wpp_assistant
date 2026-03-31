from enum import Enum


class RunType(str, Enum):
    DEFAULT = "DEFAULT"
    RESET_MEMORY = "RESET_MEMORY"
