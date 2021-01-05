import sys

sys.path.append("../")

from wasaki.command_handler import Bot
from wasaki.app.auto_responder_wa import AutoResponderWA
from wasaki.message import argify

bot = Bot(name="botto", prefix="bt!", app=AutoResponderWA, verbose=True)


@bot.command(brief="speed up test for arg_parser located in message.py")
@argify()
async def testarg(ctx, params, inputs, flags):
    return str((params, inputs, flags))


@testarg.error
async def handler(ctx, error):
    return error


bot.run()
