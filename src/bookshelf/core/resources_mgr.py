import boto3


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
        self.dynamodb_resource = boto3.resource("dynamodb", endpoint_url="http://172.17.0.1:8080")
        self.dynamodb_client = boto3.client("dynamodb", endpoint_url="http://172.17.0.1:8080")
