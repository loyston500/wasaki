__all__ = (
    "NotInDmError",
    "NotInGroupError",
    "UnprivilegedUserError",
    "AutoResponderWA",
    "group_only",
    "dm_only",
    "only_for_users",
)

from typing import *
from .base import App, Request, Response
from ..context import Context


class NotInGroupError(Exception):
    pass


class NotInDmError(Exception):
    pass


class UnprivilegedUserError(Exception):
    pass


class AutoResponderWA(App):
    def request_to_default(self, request: Request) -> Request:
        query: Dict[Any, Any] = request["query"]
        return dict(
            message=query["message"],
            author=query.get("sender"),
            is_group=query.get("isGroup"),
            rule_id=query.get("ruleId"),
            app_package_name=request.get("appPackageName"),
            messenger_package_name=request.get("messengerPackageName"),
        )

    def request_default(self) -> Request:
        return NotImplementedError

    def default_to_response(self, response: Response) -> Response:
        return dict(replies=[dict(message=message) for message in response["messages"]])

    def response_default(self) -> Response:
        return dict(replies=[])

    def return_to_response(self, _return: Any) -> Response:
        if isinstance(_return, str):
            return dict(replies=[dict(message=_return)])
        elif isinstance(_return, tuple):
            return dict(replies=[dict(message=str(message)) for message in _return])
        elif _return is None:
            return self.response_default()
        elif isinstance(_return, dict):
            return _return
        else:
            return dict(replies=[dict(message=str(_return))])

    @staticmethod
    def build(*messages: List[Any]) -> Response:
        return dict(replies=[dict(message=str(message)) for message in messages])


def group_only(quiet: bool = False) -> Callable:
    """
    A check function to ensure if the message is sent in a group or not.
    """

    def factory(coro: Awaitable) -> Awaitable:
        async def wrap(ctx: Context, *args: Any, **kwargs: Any) -> Any:
            if ctx.is_group:
                return await coro(ctx, *args, **kwargs)
            elif not quiet:
                raise NotInGroupError("message was not sent in a group")

        wrap.__name__ = coro.__name__
        wrap.__doc__ = coro.__doc__
        return wrap

    return factory


def dm_only(quiet: bool = False) -> Callable:
    """
    A check function to ensure if the message is sent in dms or not.
    """

    def factory(coro: Awaitable) -> Awaitable:
        async def wrap(ctx: Context, *args: Any, **kwargs: Any) -> Any:
            if not ctx.is_group:
                return await coro(ctx, *args, **kwargs)
            elif not quiet:
                raise NotInGroupError("message was not sent in dms")

        wrap.__name__ = coro.__name__
        wrap.__doc__ = coro.__doc__
        return wrap

    return factory


def only_for_users(names: Iterable[str], silent: bool = False) -> Callable:
    """
    A check function to check if the author is the given name or not.
    """

    def factory(coro: Awaitable) -> Awaitable:
        async def wrap(ctx, *args: Any, **kwargs: Any) -> Any:
            if ctx.author in names:
                return await func(ctx, *args, **kwargs)
            elif not silent:
                raise UnprivilegedUserError(
                    f"unprivilaged access by author/user '{ctx.author}'"
                )

        wrap.__name__ = func.__name__
        wrap.__doc__ = func.__doc__
        return wrap

    return decorator
