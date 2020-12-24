# Wasaki
wasaki is a powerful, multi purpose lib made to be used with automation apps like auto responder apps etc.., to be more specfic, it can be used with `AutoResponder WA`
(this release is a prototype and it may or may not have a breaking update in the future)

## Basic Usage
This is going to be easy if you are familiar with discord.py, as you are going to write this bot in a similar structure.
Before getting started, make sure you have:

1. Cloned this repo in a certain folder.
    To clone, just run `mkdir myfolder; cd myfolder; git clone https://github.com/loyston500/wasaki`.
    This will create a folder called `myfolder` in your current directory and then clone the repo inside it.
    
2. Quart installed.
    If you don't know what quart is, it's a lib which we gonna use to host our webserver.
    To install it, run `pip install quart`    
    
3. ngrok downloaded.
    Ngrok is a tool that is used to forward our localhost to a public address so that it can be accessed by other devices over the internet.
    You can download it from https://ngrok.com/        
    
4. Auto Responder app which supportes interaction with web servers.
    I'd recommend `AutoResponder WA`
    
Now on the `myfolder`, create a python file, for example: `main.py`. You are going to write your bot's code here.

### A ping pong bot example
```py
from wasaki.wasaki.wasaki import Bot
from wasaki.converters.auto_responder_for_wa import AutoResponderForWA

bot = Bot(prefix="bt!", converter=AutoResponderForWA)

@bot.command()
async def ping(ctx):
    return ctx.reply("pong!")
    
bot.run(debug=True)
```

Now once you run your bot file, you'll see some weird text poping out, don't worry about that, It means your webserver has been started and it can be accessed using the local host address (127.0.0.1).
Now open up another terminal, locate to the directory where you have extracted ngrok, and then run 
`ngrok http 5000` if you are on windows.
`./ngrok http 5000` if you are on linux.

This should show you something like ![screenshot](https://media.discordapp.net/attachments/781733449656041482/791547198868815922/Screenshot_4.png)
Copy the url.
Now open the `AutoResponder WA` app, click one the `+` icon located at the bottom right, select `pattern matching` option and on the `Should be answered` section, write `bt!*`. Now scroll down and click on `Connect your web server`. Now click on the `url` section, paste the url and click the tick mark. You are done.

Assuming that you did everything right, if you send `bt!ping` to your whatsapp from another device, it should respond with `pong!`.

