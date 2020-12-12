class Context:

    def __init__(self, rest_content: str, reply, response) -> None:
        self.rest_content = rest_content
        self.response = response
        self.reply = reply

    def __getattr__(self, key) -> "Any":
        return self.response[key]