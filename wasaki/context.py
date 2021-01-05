import typing


class Context:
    def __init__(self, rest_message: str, request: dict) -> None:
        self.rest_message = rest_message
        self.request = request
        # self.reply = reply

    @staticmethod
    def reply(*messages):
        return messages

    def __getattr__(self, key: str) -> typing.Any:
        return self.request[key]
