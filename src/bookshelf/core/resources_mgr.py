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

        print(os.environ.get("AWS_SAM_LOCAL"))

        if os.environ.get("AWS_SAM_LOCAL") is not None:
            logger.info("local aws resources")
            endpoint_url = "http://localhost:8080"
            self.dynamodb_resource = boto3.resource(
                "dynamodb", endpoint_url=f"{endpoint_url}"
            )
            self.dynamodb_client = boto3.client(
                "dynamodb", endpoint_url=f"{endpoint_url}"
            )
        else:
            logger.info("remote aws resources")
            self.dynamodb_resource = boto3.resource("dynamodb")
            self.dynamodb_client = boto3.client("dynamodb")
