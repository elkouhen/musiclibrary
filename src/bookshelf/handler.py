from src.bookshelf.domain.book_dao import BookDao
from src.bookshelf.domain.book import Book
from src.bookshelf.core.resources_mgr import ResourcesMgr
import boto3

print("create dynamodb resources")
resources_mgr = ResourcesMgr()


def create_book(event, context):
    book = Book(title=event["title"], author=event["author"])
    book_dao = BookDao(
        dynamodb_resource=resources_mgr.dynamodb_resource, dynamodb_client=resources_mgr.dynamodb_client
    )
    book_dao.create_book(book)


def delete_book(event, context):
    book = Book(title=event["title"], author=event["author"])
    book_dao = BookDao(
        dynamodb_resource=resources_mgr.dynamodb_resource, dynamodb_client=resources_mgr.dynamodb_client
    )
    book_dao.delete_book(book)
