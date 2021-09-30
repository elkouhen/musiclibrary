import boto3
import os
import logging

logger = logging.getLogger()


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class ResourcesMgr:
    def __init__(self):
        self.dynamodb_resource = boto3.resource("dynamodb")
        self.dynamodb_client = boto3.client("dynamodb")

    def table_name(self) -> str:

        if "TABLE_NAME" in os.environ:
            return os.environ["TABLE_NAME"]

        return "helloworld"
