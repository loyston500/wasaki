class BaseConverter:
    @staticmethod
    def replier_none() -> dict:
        return {"messages": []}

    @staticmethod
    def parser(response: dict) -> dict:
        # the response should contain the keys listed:
        # "app_package_name" package name of the app which does the automation [optional]
        # "messenger_package_name" package name of thr messenger [optional]
        # "message" the content of the message
        # "is_group" bool that verifies if the message is sent through the group or not
        # "author" name of the author
        return response

    @staticmethod
    def replier(*messages: "list[str]") -> dict:
        return {"messages": messages}
