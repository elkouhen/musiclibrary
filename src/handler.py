from src.domain.song import Song
from src.domain.song_dao import SongDao
from src.core.resources_mgr import ResourcesMgr

import logging
import json

logger = logging.getLogger()
print("create dynamodb resources")
resources_mgr = ResourcesMgr()


def create_song(event, context):
    print(event)

    body = json.loads(event["body"])

    song = Song(author=body["author"], title=body["title"], genre=body["genre"], date=body["date"])

    dao = SongDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
        table_name=resources_mgr.table_name(),
    )

    dao.create(song)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": song.to_json(),
    }


def delete_song(event, context):
    print(event)

    dao = SongDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
        table_name=resources_mgr.table_name(),
    )

    dao.delete(uuid=event["pathParameters"]["song_id"])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": "",
    }


def find_by_author_and_title(event, context):
    print(event)

    dao = SongDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
        table_name=resources_mgr.table_name(),
    )

    entities = dao.find_by_author_and_title(event["queryStringParameters"]["author"],
                                            event["queryStringParameters"]["title"])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(entities, default=lambda entity: entity.to_json()),
    }
