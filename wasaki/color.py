from typing import *
from enum import Enum


class Color:
    pass


class Color(Enum):
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @classmethod
    def print(
        cls,
        *args: Any,
        color: Optional[Type[Color]] = None,
        end: str = "\n",
        **kwargs: Any
    ):
        if color is None:
            color = Color.OKGREEN
        print(color.value, end="")
        print(*args, **kwargs, end="")
        print(cls.ENDC.value, end=end)

    @classmethod
    def pretty(cls, *args: Any):
        color: Type[Color] = None
        for arg in args:
            if arg.__class__ == cls:
                color = arg
            else:
                cls.print(arg, color=color, end="  ")
        print()


def main():
    Color.pretty(Color.WARNING, "hi fooo", Color.FAIL, "lmao")


if __name__ == "__main__":
    main()
