from typing import Any


class Context:
    def __init__(self, rest_message: str, reply, response) -> None:
        self.rest_message = rest_message
        self.response = response
        self.reply = reply

    def __getattr__(self, key) -> Any:
        return self.response[key]
