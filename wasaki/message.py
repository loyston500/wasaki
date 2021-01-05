import re

from typing import Callable


def _arg_parser(mes: str) -> (dict, list, set):
    """
    an argument parser written in python
    """
    mes = re.findall(r'[^\s"]+|"[^"]*"', mes)
    i = 0
    length = len(mes)
    flags = set()
    params = {}
    inputs = []
    try:
        while i < length:
            if mes[i].startswith("--"):
                flags.add(mes[i][2:])
            elif mes[i].startswith("-"):
                params[mes[i][1:]] = mes[i + 1].replace('"', "")
                i += 1
            elif mes[i].startswith('"') and mes[i].endswith('"'):
                inputs.append(mes[i][1:-1])
            else:
                inputs.append(mes[i])
            i += 1
    except IndexError:
        raise Exception("Invalid Syntax")
    return (params, inputs, flags)


try:
    from wasaki.speedups.speedups import arg_parser as _arg_parser
except ImportError:
    pass
else:
    print("message module using speedups")


def parse_using(parser):
    def decorator(func) -> Callable:
        async def wrap(ctx) -> dict:
            return await func(ctx, *parser(ctx.rest_message))

        wrap.__name__ = func.__name__
        wrap.__doc__ = func.__doc__
        return wrap

    return decorator


def argify():
    return parse_using(_arg_parser)
