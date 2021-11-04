__all__ = ("PREFIX", "log", "setup")

from typing import *
from .color import Color
from .context import Context
from .events import EventType
from .app.base import Request, Response

PREFIX: str = "$"


def logger(kind: str, msg: str) -> None:
    kind = kind.upper()
    if kind == "OK":
        Color.print(f"OK: {msg}", color=Color.OKGREEN)
    elif kind == "WARNING":
        Color.print(f"WARNING: {msg}", color=Color.WARNING)
    elif kind in ("ERROR", "FAIL"):
        Color.print(f"ERROR: {msg}", color=Color.FAIL)
    else:
        Color.print(f"{kind}: {msg}", color=Color.HEADER)


def setup(bot) -> None:
    @bot.event(EventType.ON_RAW_REQUEST)
    async def handler(req: Request) -> Optional[Response]:
        bot.logger("ok", f"raw request received; {req}")
        return await bot.process_raw_request(req)

    @bot.event(EventType.ON_REQUEST)
    async def handler(req: Request) -> Optional[Response]:
        bot.logger("ok", f"request received; {req}")
        return await bot.process_commands(req)

    @bot.event(EventType.ON_REQUEST_ERROR)
    async def handler(req: Request, err: Exception) -> Optional[Response]:
        bot.logger("error", f"error while processing the request {req} {err}")

    @bot.event(EventType.ON_CONVERSION_ERROR)
    async def handler(req: Request, err: Exception) -> Optional[Response]:
        bot.logger("error", f"error while converting the request {req} {err}")

    @bot.event(EventType.ON_ERROR)
    async def handler(req: Request, err: Exception) -> Optional[Response]:
        bot.logger("error", f"error while procesing commands {req} {err}")

    @bot.event(EventType.ON_COMMAND_ERROR)
    async def handler(req: Request, err: Exception) -> Optional[Response]:
        bot.logger("error", f"error occured while handling stuff {req} {err}")

    @bot.event(EventType.ON_NOT_COMMAND)
    async def handler(req: Request) -> Optional[Response]:
        bot.logger(
            "error", f"message received is not a command `{Context(req).message}`"
        )

    @bot.command(name="help", aliases=["man", "info", "tldr"])
    async def _help(ctx):
        return "\n".join(f"{name}" for name, command in bot.commands.items())


def main():
    log("ok", "This is a message")
    log("error", "This is an error")
    log("log", "some logging")


if __name__ == "__main__":
    main()
