from wasaki.wasaki import Bot
from converters import auto_responder_for_wa

bot = Bot(name="botto", prefix="bt!", converter=auto_responder_for_wa.AutoResponderForWA)

@bot.command()
def ping(this):
    if this.is_group:
        print("message was sent in group")
    print(this.content)
    return this.reply("Hello there", 'hi')

bot.run()