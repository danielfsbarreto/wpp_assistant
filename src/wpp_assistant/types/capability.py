from enum import Enum


class Capability(str, Enum):
    WEB_SEARCH = "web_search"
    HISTORY = "history"
    GMAIL = "gmail"
    TODOIST = "todoist"
