from typing import *
from enum import Enum

__all__ = ("Event", "EventType", "Events")


class Event:
    def __init__(self, coro: Coroutine) -> None:
        self.coro = coro

    def __call__(self, *args: Any, **kwargs: Any) -> Awaitable:
        return self.coro(*args, **kwargs)


class EventType:
    pass


class EventType(Enum):
    ON_REQUEST = "ON_REQUEST"  # Triggered when the default request is formed
    ON_RAW_REQUEST = "ON_RAW_REQUEST"  # Triggered when the request is just received
    ON_COMMAND_ERROR = "ON_COMMAND_ERROR"  # Triggered when there is an error in a command and command.error is not registered
    ON_CONVERSION_ERROR = (
        "ON_CONVERSION_ERROR"  # Triggered when the conversion to default request fails
    )
    ON_REQUEST_ERROR = "ON_REQUEST_ERROR"  # Triggered on failure to create a request (maybe triggered when the received response is not a json)
    ON_NOT_COMMAND = (
        "ON_NOT_COMMAND"  # Triggered when the received message is not a command
    )
    ON_ERROR = "ON_ERROR"  # Triggered when there is an error related to command, ex: on invalid command

    @classmethod
    def try_str_to_variant(cls, string: str) -> Type[EventType]:
        col: Dict[str, Type[EventType]] = EventType._value2member_map_
        try:
            return col[(string := string.upper())]
        except KeyError:
            raise InvalidEventError(f"event named '{string}' does not exist")


Events = Dict[Type[EventType], Event]
