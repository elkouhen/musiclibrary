from src.bookshelf.domain.book_dao import BookDao
from src.bookshelf.domain.book import Book
from src.bookshelf.core.resources_mgr import ResourcesMgr

import logging
import json

logger = logging.getLogger()
print("create dynamodb resources")
resources_mgr = ResourcesMgr()


def create_book(event, context):
    body = json.loads(event["body"])

    book = Book(
        author=body["author"],
        title=body["title"],
        genre=body["genre"],
        publication_date=body["publication_date"],
    )

    book_dao = BookDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
    )

    book_dao.create(book)

    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json"},
        "body": book.to_json(),
    }


def delete_book(event, context):
    logger.info(event)

    book_dao = BookDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
    )
    book_dao.delete(event["pathParameters"]["book_index"])

    return {
        "statusCode": 204,
        "headers": {"Content-Type": "application/json"},
        "body": "",
    }
