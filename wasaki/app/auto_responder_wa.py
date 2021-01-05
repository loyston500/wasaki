import typing


class NotInGroupError(Exception):
    pass


class NotInDmError(Exception):
    pass


class UnprivilegedUserError(Exception):
    pass


class AutoResponderWA:
    @staticmethod
    def replier_none() -> dict:
        return {"replies": []}

    @staticmethod
    def request_convert(response: dict) -> dict:
        # the response is something likr this, this needs to be converted to how it's in the base class.
        # {'appPackageName': 'tkstudio.autoresponderforwa', 'messengerPackageName': 'com.whatsapp', 'query': {'sender': 'Own', 'message': 'bt!hi', 'isGroup': False, 'ruleId': 1}}
        return {
            "app_package_name": response.get("appPackageName"),
            "messenger_package_name": response.get("appPackageName"),
            "message": response.get("query").get("message"),
            "author": response.get("query").get("sender"),
            "is_group": response.get("query").get("isGroup"),
            "rule_id": response.get("query").get("ruleId"),
        }

    @staticmethod
    def replier(*messages: typing.List[str]):
        return {"replies": [{"message": str(message)} for message in messages]}


# check functions


def group_only(error=True) -> typing.Callable:
    """
    A check function to ensure if the message is sent in a group or not.
    """

    def decorator(func: typing.Awaitable):
        async def wrap(ctx, *args, **kwargs) -> typing.Any:
            if ctx.is_group:
                return await func(ctx, *args, **kwargs)
            else:
                if error:
                    raise NotInGroupError("message was not sent in a group")

        wrap.__name__ = func.__name__
        wrap.__doc__ = func.__doc__
        return wrap

    return decorator


def dm_only(error=True) -> typing.Callable:
    """
    A check function to ensure if the message is sent in a dm or not.
    """

    def decorator(func: typing.Awaitable):
        async def wrap(ctx, *args, **kwargs) -> typing.Any:
            if not ctx.is_group:
                return await func(ctx, *args, **kwargs)
            else:
                if error:
                    raise NotInDmError("message was not sent in a dm")

        wrap.__name__ = func.__name__
        wrap.__doc__ = func.__doc__
        return wrap

    return decorator


def only_for_users(*names: typing.List[str], error=True) -> typing.Callable:
    """
    A check function to check if the author is the given name or not.
    """

    def decorator(func: typing.Awaitable):
        async def wrap(ctx, *args, **kwargs) -> typing.Any:
            if ctx.author in names:
                return await func(ctx, *args, **kwargs)
            else:
                if error:
                    raise UnprivilegedUserError

        wrap.__name__ = func.__name__
        wrap.__doc__ = func.__doc__
        return wrap

    return decorator
