from src.domain.hello_msg import HelloMsg
from src.domain.hello_msg_dao import HelloMsgDao
from src.core.resources_mgr import ResourcesMgr

import logging
import json

logger = logging.getLogger()
print("create dynamodb resources")
resources_mgr = ResourcesMgr()


def create_hello_msg(event, context):
    print(event)

    body = json.loads(event["body"])

    book = HelloMsg(language=body["language"], value=body["value"])

    dao = HelloMsgDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
        table_name=resources_mgr.table_name(),
    )

    dao.create(book)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": book.to_json(),
    }


def find_hello_msg(event, context):
    print(event)

    dao = HelloMsgDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
        table_name=resources_mgr.table_name(),
    )

    entities = dao.find_by_language(event["queryStringParameters"]["language"])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(entities, default=lambda entity: entity.to_json()),
    }
