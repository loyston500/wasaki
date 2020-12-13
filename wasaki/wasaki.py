# A lib for those who use webserver for Whats App autorespoder app.
# An easy to use lib that wraps most of the stuff that can be done through the provided app.

# import flask
import quart
from typing import Any, Optional, Callable
from converters.base_converter import BaseConverter
from wasaki.context import Context


class Bot:
    def __init__(
        self,
        converter: BaseConverter,
        name: str = "Bot",
        prefix: str = "$",
        case_insensitive: bool = True,
    ):
        self.app: quart.Quart = quart.Quart(name)  # changes from flask to quart
        self.converter: BaseConverter = converter
        self.prefix: str = prefix
        self.case_insensitive: bool = case_insensitive

        self.events: dict = {}
        self.commands: dict = {}

    def event(self, func: Callable) -> None:
        self.events[func.__name__] = func

    def command(self, **command_dict) -> None:
        def decorator(func: Callable) -> None:
            command_dict["command"] = func
            self.commands[
                name if command_dict.get("name") else func.__name__
            ] = command_dict

        return decorator

    def _safe_return(self, ret: Any) -> Any:
        if ret is None:
            return self.converter.replier_none()
        else:
            return ret

    def _route(self) -> None:
        @self.app.route("/", methods=["POST"])
        async def routing() -> dict:
            try:
                response = await quart.request.get_json()  # changes from flask to quart

                # there's a lot of stuff that needs to be refactored here.
                response = self.converter.parser(response)
                if response["message"].startswith(self.prefix) and (
                    len(response["message"]) > len(self.prefix)
                ):
                    command_name = response["message"][len(self.prefix) :].split()[0]
                    if command_name in self.commands:
                        command_dict = self.commands[command_name]
                        rest_message = response["message"][
                            len(self.prefix) + len(command_name) :
                        ]
                        return self._safe_return(
                            await command_dict["command"](
                                Context(rest_message, self.converter.replier, response),
                                *command_dict.get(
                                    "message_parser", (lambda message: [])
                                )(rest_message)
                            )
                        )
                else:
                    if "on_not_command" in self.events:
                        return self._safe_return(
                            await self.events["on_not_command"](
                                Context(None, self.converter.replier, response)
                            )
                        )
                    else:
                        return self.converter.replier_none()
            except Exception as error:
                if "on_error" in self.events:
                    return self._safe_return(
                        await self.events["on_error"](
                            Context(None, self.converter.replier, response), error
                        )
                    )
                else:
                    return self.converter.replier_none()

    def run(self) -> None:
        self._route()
        self.app.run(debug=True)
