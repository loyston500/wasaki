# A simple module to be used with the wasaki and for those who want everything in stylish.

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
