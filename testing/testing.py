# this is an example using the current prototype version.
import sys

sys.path.append("../")

from wasaki.command_handler import Bot  # import bot class.
from wasaki.app import auto_responder_wa  # import this shit because you need it
import wasaki.message  # a builtin custom message parser.

# now create a bot object and set the bot name , prefix and the converter.
bot = Bot(
    name="botto", prefix="bt!", app=auto_responder_wa.AutoResponderWA, verbose=True
)


@bot.command(brief="group only command")
@auto_responder_wa.dm_only()
async def grr(ctx):
    return "this command"


@grr.error
async def handler(ctx, error):
    if isinstance(error, auto_responder_wa.NotInDmError):
        return "this command is dm only"
    else:
        raise error


@bot.command(brief="only for owner", hidden=True)
@auto_responder_wa.only_for_users("Own")
async def owner(ctx):
    return "you are the owner"


@owner.error
async def handler(ctx, error):
    if isinstance(error, auto_responder_wa.UnprivilegedUserError):
        return "you aren't my owner, sorry."
    else:
        raise error


# basic ping command which for this instance will reply with "Hello there" for sending "bt!ping"
# you may remember this structure of writing commands if you are familiar with discord.py
@bot.command(brief="check if the bot is alive or not.")
async def ping(ctx):  # ctx stands for context.
    """
    check if the bot is alive or not.
    usage: *
    """
    if ctx.is_group:  # check if the context is from whatsapp group or not.
        print("message was sent in group")
    return "Hello there"
    # notic how this function returns None when a message is sent in the group but this is handled properlly.


@ping.error
async def handler(ctx, error):
    print("error occured in ping", error)


# another command, this one replies back what you sent.
@bot.command()
async def tell(ctx):
    return ctx.rest_message
    # rest_message is basically the message you sent but with prefix and command trimmed.


# this commands showcases the use of custom message parser. A message parser is basically a function that thakes in a string (message) \
# and then parses it according to it's choice and then returns the result.
@bot.command()
@wasaki.message.argify()  # this parses your message just like the args passed for a bash command.
async def say(
    ctx, params, inputs, flags
):  # for example if you send '''bt!say "hi there, this is an input" --reverse''' \
    if inputs:  # the message you wrote in there is considered as an input.
        to_say = inputs[0]
        if "reverse" in flags:
            return to_say[::-1]
        else:
            return to_say
    else:
        return "Please give the input"


@say.error
async def handler(ctx, error):
    return "an error occured in command say", error


######## testing
@bot.command()
async def test1(ctx):
    raise ValueError("tf")


@bot.command()
async def test2(ctx):
    raise TypeError("tf 2")


@test1.error
@test2.error
async def handler(ctx, error):
    return ctx.reply(error)


######## testing


@bot.command(brief="used to remove a command")
async def remove(ctx):
    """
    used to remove a command.
    this is a best bot ever, written in wasaki.
    usage: <command name>
    """
    args = ctx.rest_message.split()
    if len(args) == 0:
        return "please provide a command name."
    else:
        try:
            bot.remove_command(args[0])
        except KeyError:
            return "there's no such command"
        else:
            return "removed the command successfully"


@bot.event  # this event is triggered when the received message is not a command.
async def on_not_command(
    ctx,
):  # keep is mind that rest_mesaage is set to None in events so you should use "message" attribute
    print(f"{ctx.author} said {ctx.message}")


@bot.event  # this event is triggered when an error occures anywhere in the commands.
async def on_error(error):
    raise error


bot.run(debug=True)
