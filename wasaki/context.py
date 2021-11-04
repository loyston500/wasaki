from typing import *
from .app.base import Request, Response

__all__ = ("Context",)


class Context:
    def __init__(self, request: Request) -> None:
        self.request: Request = request

    def __getattr__(self, attr: str) -> Any:
        try:
            return self.request[attr]
        except KeyError:
            raise AttributeError(f"attribute `{attr}` not found in the request")

    def __str__(self):
        return self.request["content"]
