# this is an example using the current prototype version.
from wasaki.wasaki import Bot  # import bot class.
from converters import (
    auto_responder_for_wa,
)  # import the converter which is app secfic.
from wasaki.message_parsers import arg_parser  # a builtin custom message parser.

# now create a bot object and set the bot name , prefix and the converter.
bot = Bot(
    name="botto", prefix="bt!", converter=auto_responder_for_wa.AutoResponderForWA
)

# basic ping command which for this instance will reply with "Hello there" for sending "bt!ping"
# you may remember this structure of writing commands if you are familiar with discord.py
@bot.command()
async def ping(ctx):  # ctx stands for context.
    if ctx.is_group:  # check if the context is from whatsapp group or not.
        print("message was sent in group")
    return ctx.reply(
        "Hello there"
    )  # notic how this function returns None when a message is sent in the group but this is handled properlly.


# another command, this one replies back what you sent.
@bot.command()
async def tell(ctx):
    return ctx.reply(
        ctx.rest_message
    )  # rest_message is basically the message you sent but with prefix and command trimmed.


# this commands showcases the use of custom message parser. A message parser is basically a function that thakes in a string (message) \
# and then parses it according to it's choice and then returns the result.
# this arg_parser used below parses your message just like the args passed for a bash command.
@bot.command(message_parser=arg_parser)
async def say(
    ctx, params, inputs, flags
):  # for example if you send '''bt!say "hi there, this is an input" --reverse''' \
    if inputs:  # the message you wrote in there is conidered as an input.
        to_say = inputs[0]
        if "reverse" in flags:
            return ctx.reply(to_say[::-1])
        else:
            return ctx.reply(to_say)
    else:
        return ctx.reply("Please give the input")


@bot.event  # this event is triggered when the received message is not a command.
async def on_not_command(
    ctx,
):  # keep is mind that rest_mesaage is set to None in events so you should use "message" attribute
    print(f"{ctx.author} said {ctx.message}")


@bot.event  # this event is triggered when an error occures anywhere in the commands.
async def on_error(ctx, error):
    print("error occured", ctx.message, error)
    return ctx.reply(f"an error occured somewhere, {error}")


bot.run(debug=True)
