# A lib for those who use webserver for Whats App autorespoder app.
# An easy to use lib that wraps most of the stuff that can be done through the provided app.

import flask
from converters.base_converter import BaseConverter
from wasaki.context import Context

class Bot:
    def __init__(self, converter:BaseConverter, name:str="bot", prefix: str="$", case_insensitive: bool=True):
        self.app = flask.Flask(name)
        self.converter = converter
        self.prefix = prefix
        self.case_insensitive = case_insensitive

        self.events = {}
        self.commands = {}

    def event(self, func) -> None:
        self.events[func.__name__] = func

    def command(self, name: str='') -> None:
        def decorator(func):
            self.commands[name if name else func.__name__] = func
        return decorator

    def route(self) -> None:
        @self.app.route('/', methods=['POST'])
        def routing() -> dict:
            response = flask.request.get_json()
            if not response:
                raise Exception("empty response")
            
            # there's a lot of stuff that needs to be refactored here.
            response = self.converter.parser(response)
            if response["message"].startswith(self.prefix):
                command, rest_content = response["message"][len(self.prefix):].split(' ', 1)
                print("the command", command,"restcontent", rest_content,)
                func = self.commands.get(command)
                if func:
                    ret = func(Context(rest_content, self.converter.replier, response))
                    if ret is None:
                        return self.converter.replier_none()
                    return ret
                else:
                    # not properlly implemented
                    return self.converter.replier_none()
                

    def run(self) -> None:
        self.route()
        self.app.run(debug=True)

