from src.bookshelf.domain.book_dao import BookDao
from src.bookshelf.domain.book import Book
from src.bookshelf.core.resources_mgr import ResourcesMgr
import boto3
import logging

logger = logging.getLogger()
print("create dynamodb resources")
resources_mgr = ResourcesMgr()


def create_book(event, context):
    logger.info("create book")
    logger.info(event)
    book = Book(
        author=event["author"],
        title=event["title"],
        genre=event["genre"],
        publication_date=event["publication_date"],
    )
    book_dao = BookDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
    )
    book_dao.create(book)


def delete_book(event, context):
    logger.info(event)
    book = Book(author=event["author"], title=event["title"])
    book_dao = BookDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
    )
    book_dao.delete(book)

