from src.domain.song import Song
from src.domain.song_dao import SongDao
from src.services.csv_importer import CSVImporter
from src.core.resources_mgr import ResourcesMgr

import logging
import json

logger = logging.getLogger()
print("create dynamodb resources")
resources_mgr = ResourcesMgr()

dao = SongDao(
    dynamodb_resource=resources_mgr.dynamodb_resource,
    dynamodb_client=resources_mgr.dynamodb_client,
    table_name=resources_mgr.table_name(),
)


def create_song(event, context):
    body = json.loads(event["body"])

    try:

        song = Song(author=body["author"], title=body["title"], genre=body["genre"], date=body["date"])
        dao.create(song)

    except BaseException as e:
        logging.critical(e, exc_info=True)
        resources_mgr.metrics.put_metric(
            namespace="musiclibrary", operation="create", is_exception=True
        )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": song.to_json(),
    }


def delete_song(event, context):
    try:
        dao.delete(uuid=event["pathParameters"]["song_id"])

    except BaseException as e:
        logging.critical(e, exc_info=True)
        resources_mgr.metrics.put_metric(
            namespace="musiclibrary", operation="delete", is_exception=True
        )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": "",
    }


def find_by_author_and_title(event, context):
    try:
        entities = dao.find_by_author_and_title(event["queryStringParameters"]["author"],
                                                event["queryStringParameters"]["title"])

    except BaseException as e:
        logging.critical(e, exc_info=True)
        resources_mgr.metrics.put_metric(
            namespace="musiclibrary", operation="find", is_exception=True
        )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(entities, default=lambda entity: entity.to_json()),
    }


def import_csv(event, context):
    try:
        CSVImporter(song_dao=dao).import_file(
            event["Records"][0]["s3"]["bucket"]["name"],
            event["Records"][0]["s3"]["object"]["key"],
        )

    except BaseException as e:
        logging.critical(e, exc_info=True)
        resources_mgr.metrics.put_metric(
            namespace="musiclibrary", operation="import", is_exception=True
        )
