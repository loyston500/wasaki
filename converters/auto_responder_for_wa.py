from typing import List
from wasaki.converters.base_converter import BaseConverter
from wasaki.wasaki.sembed import Sembed


class AutoResponderForWA(BaseConverter):
    @staticmethod
    def replier_none() -> dict:
        return {"replies": []}

    @staticmethod
    def parser(response: dict) -> dict:
        # the response is something likr this, this needs to be converted to how it's in the base class.
        # {'appPackageName': 'tkstudio.autoresponderforwa', 'messengerPackageName': 'com.whatsapp', 'query': {'sender': 'Own', 'message': 'bt!hi', 'isGroup': False, 'ruleId': 1}}
        return {
            "app_package_name": response.get("appPackageName"),
            "messenger_package_name": response.get("appPackageName"),
            "message": response.get("query").get("message"),
            "author": response.get("query").get("sender"),
            "is_group": response.get("query").get("isGroup"),
            "rule_id": response.get("query").get("ruleId"),
        }

    @staticmethod
    def replier(*messages: List[str]):
        return {"replies": [{"message": str(message)} for message in messages]}
