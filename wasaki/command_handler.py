# A lib for those who use webserver for Whats App autorespoder app.
# An easy to use lib that wraps most of the stuff that can be done through the provided app.

# import flask
# import quart
import aiohttp
from aiohttp import web
import typing
from wasaki.context import Context
from wasaki.styles import bootup_showcase, Console, TermColor, color
import wasaki.exceptions
import wasaki.sembed


class Bot:
    def __init__(
        self,
        app,
        name: str = "Bot",
        prefix: str = "$",
        verbose: bool = False,
        endpoint: str = "/",
        case_insensitive: bool = True,
    ):
        self.web_server = web.Application()
        self.app = app
        self.prefix: str = prefix
        self.endpoint: str = endpoint
        self.verbose: bool = verbose
        self.case_insensitive: bool = case_insensitive

        self.events: dict = {}
        self.commands: dict = {}

        # behold the default nonviable help command.
        @self.command()
        async def help(ctx):
            """
            shows you this message.
            """
            # this thing is to check if the message is sent in a group or not,
            # important because the author's name is unknown in that context.
            if ctx.is_group:
                sembed = wasaki.sembed.Sembed(title="Here's the help for y'all:")
            else:
                sembed = wasaki.sembed.Sembed(
                    title=f"{ctx.author}, here's the help for you:"
                )

            # no there isn't any default parser, problem???
            arg = ctx.rest_message.split()
            if len(arg) == 0:  # holy thing to do
                for command_name in self.commands:
                    command_dict = self.commands[command_name]
                    if not command_dict.get("hidden"):
                        sembed.add_field(
                            name=self.prefix + command_name,
                            value=command_dict.get("brief", "no info."),
                        )
                return ctx.reply(sembed)
            else:
                command_name = arg[0]
                if command_name in self.commands:
                    command_dict = self.commands[command_name]
                    sembed.add_field(name="brief", value=command_dict.get("brief", ""))
                    sembed.add_field(
                        name="complete help",
                        value=command_dict.get("help", "no help provided."),
                    )
                    return ctx.reply(sembed)
                else:
                    return ctx.reply("command not found.")

    def _v(self, func) -> None:
        if self.verbose:
            func()

    def event(self, func: typing.Awaitable) -> None:
        """
        Used to register an event.
        example:
        @Bot.event
        async def on_ready():
            print("the bot has started")
        """
        if func.__name__ not in self.events:
            self.events[func.__name__] = func

            # verbose
            self._v(lambda: Console.ok(f"registered event '{func.__name__}'"))

        else:
            Console.error()
            raise wasaki.exceptions.AlreadyRegisteredError(
                f"event '{func.__name__}' is already registered."
            )

    # remove functions
    def remove_command(self, command_name: str) -> dict:
        """
        used to remove (unregister) a command.
        """
        try:
            ret = self.commands.pop(command_name)
        except KeyError:
            raise KeyError
        else:

            # verbose
            self._v(lambda: Console.ok(f"unregistered command '{command_name}'"))

            return ret

    def remove_event(self, event_name: str) -> dict:
        """
        used to remove (unregister) an event. (not recommended to do so)
        """
        try:
            ret = self.commands.pop(event_name)
        except KeyError:
            raise KeyError
        else:

            # verbose
            self._v(
                lambda: Console.warn(
                    f"unregistered event '{event_name}' (you have been warned)"
                )
            )

            return ret

    # used to register a command
    # command_dict will hold the mapped function and some information about the function
    # ~~~~~~~~~~~~
    #   ^------------------☟
    def command(self, **command_dict) -> typing.Callable:
        """
        Used to register a command.
        example:
        @Bot.command()
        async def ping(ctx):
            ctx.reply("pong!!")
        """
        # @Bot.command()
        # async def example_command(...) -> ...:
        #           ~~~~~~~~~~~~~~~    this function you write for the command is
        #                ^------------ passed to the decorator function
        #     ctx.reply("something") |
        #              ---------------
        #              ☟
        def decorator(func: typing.Awaitable) -> typing.Awaitable:
            # the function is assigned to the key "command" of command_dict
            command_dict["command"] = func
            command_dict["help"] = (
                "\n".join(doc.strip() for doc in func.__doc__.strip().splitlines())
                if func.__doc__
                else "no help provided."
            )
            command_name = (
                command_dict.get("name") if command_dict.get("name") else func.__name__
            )
            if command_name not in self.commands:
                self.commands[command_name] = command_dict

                # verbose
                self._v(lambda: Console.ok(f"registered command '{command_name}'"))

            else:
                Console.error()
                raise wasaki.exceptions.AlreadyRegisteredError(
                    f"command '{command_name}' is already registered."
                )

            # this function below will be set as an attribute to the user defined command function
            # it will be used to decorate the error handling function
            # example:
            # @ping.error
            # async def handler(ctx, error):
            #     print(f"an error occured in command ping")
            #     return ctx.reply("an error occured")
            def error(error_handling_func):
                self.commands[command_name]["error_handler"] = error_handling_func

                # verbose
                self._v(
                    lambda: Console.ok(
                        f"registered error handler for command '{command_name}'"
                    )
                )

                return error_handling_func

            func.error = error
            return func

        return decorator

    # this function checks if the received thing is None or not
    # gives back the empty reply if it is
    def _safe_return(self, ret: typing.Any) -> typing.Any:
        if ret is None:
            return self.app.replier_none()
        elif type(ret) == tuple:
            return self.app.replier(*ret)
        else:
            return self.app.replier(ret)

    # this function receives the request from the _global_error_handler
    # this function splits the reveived message into commands and calls the command mapped to it
    async def _request_message_handler(self, request: dict):
        if request["message"].startswith(self.prefix) and (
            len(request["message"]) > len(self.prefix)
        ):

            command_name = request["message"][len(self.prefix) :].split()[0]
            try:
                command_dict = self.commands[command_name]
            except KeyError:

                # verbose
                self._v(
                    lambda: Console.warn(
                        f"occurance of a call for an unregistered command '{command_name}'"
                    )
                )

            else:
                rest_message = request["message"][
                    len(self.prefix) + len(command_name) :
                ]
                try:
                    # return await command_dict["command"](
                    #    Context(rest_message, self.app.replier, request),
                    # )
                    return await command_dict["command"](
                        Context(rest_message, request),
                    )
                except Exception as error:
                    try:
                        error_handler = self.commands[command_name]["error_handler"]
                    except KeyError:
                        try:
                            on_command_error = self.events["on_command_error"]
                        except KeyError:

                            # verbose
                            self._v(
                                lambda: Console.error(
                                    f"occurance of an error in command '{command_name}', error: {error}"
                                )
                            )

                            raise error
                        else:
                            # return await on_command_error(Context(rest_message, self.app.replier, request), error)
                            return await on_command_error(
                                Context(rest_message, request), error
                            )

                    else:
                        # return await error_handler(
                        #    Context(rest_message, self.app.replier, request), error
                        # )
                        return await error_handler(
                            Context(rest_message, request), error
                        )
        else:
            try:
                on_not_command = self.events["on_not_command"]
            except KeyError:

                # verbose
                self._v(
                    lambda: Console.warn(
                        f"received a message which isn't a command, message: '{request['message']}'"
                    )
                )

            else:
                # return await on_not_command(
                #    Context(None, self.app.replier, request)
                # )
                return await on_not_command(Context(None, request))

    # this function receives the request from the request_conversion_handler
    # this function passes error to the on_error event which occured in the _request_message_handler
    async def _global_error_handler(self, request):
        try:
            return await self._request_message_handler(request)
        except Exception as error:
            try:
                on_error = self.events["on_error"]
            except Exception as error:
                raise error
            else:
                await on_error(error)

    def _route(self) -> None:
        # this function receives the request from the request_handler
        # this checks and ensures the request, for example,
        #     if the request is valid (is a valid) or not
        # this request is then sent to _global_error_handler, which sends back an typing.Any
        # this typing.Any is passed to _safe_return which returns the empty reply if the passed arguent is None
        async def request_conversion_handler(request) -> dict:
            request: dict = await request.json()
            try:
                request: dict = self.app.request_convert(
                    request
                )  # conversion happens here
            except Exception as error:
                try:
                    return await self.events["on_conversion_error"](request, error)
                except Exception:
                    raise wasaki.exceptions.ConversionError("conversion failure.")
            else:
                return self._safe_return(await self._global_error_handler(request))

        # everything starts here, the request is first sent to this function
        # this (request) is then sent to request_conversion_handler
        # after receiving the dict, it processes the returned dict to a json response
        async def request_handler(request):
            return web.json_response(await request_conversion_handler(request))

        self.web_server.add_routes([web.post(self.endpoint, request_handler)])

    def run(self, *args, **kwargs) -> None:
        print(color("Starting the web server...", TermColor.HEADER))
        # the routing is done.
        self._route()
        # then a quick showcase of the logo.
        bootup_showcase(clear=False)
        # call the on_ready event because why not.
        try:
            on_ready = self.events["on_ready"]
        except KeyError:

            # verbose
            self._v(lambda: Console.ok("bot is ready"))

        else:
            on_ready()

        # then it'll start running.
        web.run_app(self.web_server)
