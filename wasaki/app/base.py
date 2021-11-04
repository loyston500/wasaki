from typing import *

Request = Dict[Any, Any]
Response = Dict[Any, Any]


class App:
    def request_to_default(self, request: Request) -> Request:
        return request

    def request_default(self) -> Request:
        raise NotImplementedError

    def default_to_response(self, response: Response) -> Response:
        return response

    def response_default(self) -> Request:
        raise NotImplementedError

    @staticmethod
    def build(*args, **kwargs) -> Request:
        raise NotImplementedError
