import boto3
import os


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

        if "AWS_SAM_LOCAL" in os.environ:
            print("local aws resources")
            endpoint_url = "http://172.17.0.1:8080"
            self.dynamodb_resource = boto3.resource("dynamodb", endpoint_url=f"http://{endpoint_url}")
            self.dynamodb_client = boto3.client("dynamodb", endpoint_url=f"http://{endpoint_url}")
        else:
            print("remote aws resources")
            self.dynamodb_resource = boto3.resource("dynamodb")
            self.dynamodb_client = boto3.client("dynamodb")
