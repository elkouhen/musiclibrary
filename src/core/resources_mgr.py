import boto3
from aws_xray_sdk.core import patch_all
from src.core.metrics import Metrics
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
    def __init__(self, patch=True, enable_cloudwatch=True):

        self.dynamodb_resource = boto3.resource("dynamodb")
        self.dynamodb_client = boto3.client("dynamodb")

        if patch:
            patch_all()

        if enable_cloudwatch:
            self.metrics = Metrics(cloudwatch=boto3.client("cloudwatch"))
        else:
            self.metrics = None

    def table_name(self) -> str:

        if "TABLE_NAME" in os.environ:
            return os.environ["TABLE_NAME"]

        return "musiclibrary"
