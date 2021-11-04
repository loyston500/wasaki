__all__ = ("Command", "Commands", "Bot", "Prefix", "CommandResponse")

from typing import *

import aiohttp
from aiohttp import web

from .defaults import PREFIX, logger as default_logger, setup
from .events import *
from .exceptions import *
from .context import Context
from .app.base import Request, Response, App

Prefix = Union[Callable, str]
CommandResponse = Any


class Command:
    def __init__(
        self,
        coro: Coroutine,
        name: Optional[str] = None,
        doc: Optional[str] = None,
        aliases: Optional[Iterable[str]] = None,
        app: App = App(),
        logger: Optional[Callable] = None,
    ) -> None:
        self.coro: Coroutine = coro
        self.name: str = name if name is not None else coro.__name__
        self.doc: Optional[str] = doc
        self.aliases: Set = set(aliases) if aliases is not None else set()
        self.error_coro: Optional[Coroutine] = None
        self.app = app

        if logger is None:
            self.logger = default_logger
        else:
            self.logger = logger

    def __call__(self, *args: Any, **kwargs: Any) -> Awaitable:
        return self.coro(*args, **kwargs)

    def on_error(self, coro: Coroutine) -> Coroutine:
        if self.error_coro is None:

            async def error_coro_wrap(*args: Any, **kwargs: Any):
                return self.app.return_to_response(await coro(*args, **kwargs))

            self.error_coro = error_coro_wrap
            self.logger("ok", f"registered on_error event for command `{self.name}`")
        return coro


Commands = Dict[str, Command]


class Bot:
    def __init__(
        self,
        prefix: Prefix,
        case_insensitive: bool = True,
        app: App = App(),
        logger: Optional[Callable] = None,
    ) -> None:
        if callable(prefix):
            matcher: Callable = prefix
        elif isinstance(prefix, str):

            def matcher(content: str) -> Optional[List[str]]:
                if content.startswith(prefix):
                    return [prefix, content[len(prefix) :]]
                return

        elif prefix is None:

            def matcher(content: str) -> Optional[List[str]]:
                if content.startswith(PREFIX):
                    return [PREFIX, content[1:]]
                return

        else:
            raise TypeError("A prefix must be a str or a callable function")

        self.prefix: Callable = matcher
        self.events: Events = {}
        self.commands: Commands = {}
        self.web_server = web.Application()
        self.app: App = app

        if logger is not None:
            self.logger = logger
        else:
            self.logger = default_logger

        setup(self)

    def event(
        self, event_type: Optional[Type[EventType]] = None, override: bool = False
    ) -> Callable:
        """registers an event"""

        def wrap(coro: Coroutine) -> Coroutine:
            coro_name: str = coro.__name__
            if event_type is None:
                _event_type: Type[EventType] = EventType.try_str_to_variant(coro_name)
            else:
                _event_type: Type[EventType] = event_type

            async def coro_wrap(*args: Any, **kwargs) -> Response:
                ret = await coro(*args, **kwargs)
                if ret is None:
                    return self.app.response_default()
                else:
                    return ret

            self.add_event(_event_type, coro_wrap, override=override)
            ov: str = "overridden" if override else "registered"
            self.logger("ok", f"{ov} event `{_event_type.value}`")

            return coro

        return wrap

    def add_event(
        self, event_type: Type[EventType], coro: Coroutine, override: bool = False
    ) -> Event:
        if event_type in self.events and not override:
            raise AlreadyRegisteredError(
                f"the event `{event_type}` is already registered. NOTE: pass override=True to override anyway"
            )
        else:
            self.events[event_type] = coro

    def get_event(self, event_type: Type[EventType]) -> Event:
        if event_type in self.events:
            return self.events[event_type]
        else:
            raise EventNotRegisteredError(f"the event `{event_type}` is not registered")

    def remove_event(self, event_type: Type[EventType]) -> Event:
        """unregisters an event and returns it"""

        return self.events.pop(event_type)

    def command(
        self,
        name: Optional[str] = None,
        aliases: Optional[Iterable[str]] = None,
        override: bool = False,
    ) -> Callable:
        """registers a command"""

        def wrap(coro: Coroutine) -> Coroutine:
            coro_name: str = coro.__name__
            coro_doc: Optional[str] = coro.__doc__
            if name is not None:
                coro_name = name

            async def coro_wrap(*args: Any, **kwargs: Any) -> Response:
                try:
                    return self.app.return_to_response(await coro(*args, **kwargs))
                except Exception as error:
                    raise error

            self.add_command(
                command := Command(
                    coro_wrap, coro_name, coro_doc, aliases, self.app, self.logger
                ),
                override=override,
            )
            return command

        return wrap

    def add_command(self, command: Command, override: bool = False) -> Event:
        if command.name in self.commands and not override:
            raise AlreadyRegisteredError(
                f"the command `{command.name}` is already registered. NOTE: pass override=True to override anyway"
            )
        else:
            aliases: Set = {command.name} | set(command.aliases)
            for alias in aliases:
                self.commands[alias] = command
        self.logger("ok", f"registered command `{command.name}`")

    async def process_commands(self, request: Request) -> Response:
        message: str = request["message"]
        author: str = request["author"]
        check: Optional[List[str]] = self.prefix(message)
        if check is not None:
            prefix, content = check
            command_name, *content = content.split(None, 1)
            if command_name not in self.commands:
                return await self.get_event(EventType.ON_ERROR)(
                    request,
                    CommandNotRegisteredError(
                        f"command named `{command_name}` is unknown"
                    ),
                )
            command: Command = self.commands[command_name]
            request["content"] = content = "".join(content)
            try:
                return await command.coro(Context(request))
            except Exception as error:
                if command.error_coro is not None:
                    return await command.error_coro(Context(request), error)
                else:
                    return await self.get_event(EventType.ON_COMMAND_ERROR)(
                        request, error
                    )
        else:
            return await self.get_event(EventType.ON_NOT_COMMAND)(request)

    def run(
        self,
        *args: Any,
        endpoint: str = "/",
        run_on: Optional[Callable] = None,
        **kwargs: Any,
    ) -> None:
        self._route(endpoint)

        if run_on is None:
            web.run_app(self.web_server, *args, **kwargs)
        else:
            run_on(self.web_server, *args, **kwargs)

    def _route(self, endpoint: str) -> None:
        self.web_server.add_routes([web.post(endpoint, self.to_json_response)])

    async def process_raw_request(self, request: Request) -> Response:
        try:
            request: Request = self.app.request_to_default(request)
        except Exception as error:
            return await self.get_event(EventType.ON_CONVERSION_ERROR)(request, error)
        else:
            return await self.get_event(EventType.ON_REQUEST)(request)

    async def to_json_response(self, response: Response) -> Any:
        return web.json_response(await self._request_handler(response))

    async def _request_handler(self, request: Any) -> Response:
        try:
            request: Request = await request.json()
        except Exception as error:
            return await self.get_event(EventType.ON_REQUEST_ERROR)(request, error)
        else:
            return await self.get_event(EventType.ON_RAW_REQUEST)(request)
