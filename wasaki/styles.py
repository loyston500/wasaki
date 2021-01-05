# A simple module to be used with the wasaki and for those who want everything in stylish.

import os
from base64 import b64decode as _b64decode

# list of all fonts
normal_font = "abcdefghijklmnopqrstuvwxyz"
small_font = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"


def converter(source: str, from_font: str, to_font: str) -> str:
    for fr, to in zip(from_font, to_font):
        source = source.replace(fr, to)
    return source


class Fonts:
    @staticmethod
    def small(text: str) -> str:
        return converter(text, normal_font, small_font)


class TermColor:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def cprint(*args, color=None):
    print(color, *args, "\033[0m")


def color(arg, color):
    return f"{color}{arg}\033[0m"


class Console:
    @staticmethod
    def error(arg=""):
        print(color("Error:", TermColor.FAIL), arg)

    @staticmethod
    def warn(arg=""):
        print(color("Warning:", TermColor.WARNING), arg)

    @staticmethod
    def ok(arg=""):
        print(color("Ok:", TermColor.OKGREEN), arg)


logo = b"ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgChtbMDsxOzMxOzkxbW0bWzBtICAgICAbWzA7MTszNjs5Nm1tG1swbSAgICAgICAgICAgICAgICAgICAgICAbWzA7MTszMjs5Mm0jG1swbSAgICAgICAgG1swOzE7MzM7OTNtIhtbMG0gICAKG1swOzE7MzM7OTNtIxtbMG0gIBtbMDsxOzMyOzkybSMbWzBtICAbWzA7MTszNDs5NG0jG1swbSAgG1swOzE7MzU7OTVtbRtbMDsxOzMxOzkxbW1tG1swbSAgICAbWzA7MTszNjs5Nm1tbRtbMDsxOzM0Ozk0bW0bWzBtICAgIBtbMDsxOzMxOzkxbW0bWzA7MTszMzs5M21tbRtbMG0gICAbWzA7MTszNjs5Nm0jG1swbSAgIBtbMDsxOzM1Ozk1bW0bWzBtICAbWzA7MTszMzs5M21tbRtbMDsxOzMyOzkybW0bWzBtICAgChtbMDsxOzMyOzkybSIbWzBtIBtbMDsxOzM2Ozk2bSMiG1swOzE7MzQ7OTRtIxtbMG0gG1swOzE7MzU7OTVtIxtbMG0gG1swOzE7MzE7OTFtIhtbMG0gICAbWzA7MTszMjs5Mm0jG1swbSAgG1swOzE7MzY7OTZtIxtbMG0gICAbWzA7MTszNTs5NW0iG1swbSAgG1swOzE7MzM7OTNtIhtbMG0gICAbWzA7MTszNjs5Nm0jG1swbSAgG1swOzE7MzQ7OTRtIxtbMG0gG1swOzE7MzU7OTVtbRtbMDsxOzMxOzkxbSIbWzBtICAgICAbWzA7MTszNjs5Nm0jG1swbSAgIAogG1swOzE7MzY7OTZtIxtbMDsxOzM0Ozk0bSMbWzBtIBtbMDsxOzM1Ozk1bSMjG1swOzE7MzE7OTFtIhtbMG0gG1swOzE7MzM7OTNtbSIbWzA7MTszMjs5Mm0iIhtbMDsxOzM2Ozk2bSMbWzBtICAgG1swOzE7MzU7OTVtIiIbWzA7MTszMTs5MW0ibRtbMG0gIBtbMDsxOzMyOzkybW0iG1swOzE7MzY7OTZtIiIbWzA7MTszNDs5NG0jG1swbSAgG1swOzE7MzU7OTVtIxtbMDsxOzMxOzkxbSIjG1swbSAgICAgIBtbMDsxOzM0Ozk0bSMbWzBtICAgCiAbWzA7MTszNDs5NG0jG1swbSAgIBtbMDsxOzMxOzkxbSMbWzBtICAbWzA7MTszMjs5Mm0ibRtbMDsxOzM2Ozk2bW0iG1swOzE7MzQ7OTRtIxtbMG0gIBtbMDsxOzM1Ozk1bSIbWzA7MTszMTs5MW1tbRtbMDsxOzMzOzkzbW0iG1swbSAgG1swOzE7MzY7OTZtIm0bWzA7MTszNDs5NG1tIhtbMDsxOzM1Ozk1bSMbWzBtICAbWzA7MTszMTs5MW0jG1swbSAgG1swOzE7MzI7OTJtIm0bWzBtICAbWzA7MTszNDs5NG1tbRtbMDsxOzM1Ozk1bSNtG1swOzE7MzE7OTFtbRtbMG0gCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAK"


def bootup_showcase(clear=True):
    if clear:
        os.system("clear")
    print(_b64decode(logo).decode())
