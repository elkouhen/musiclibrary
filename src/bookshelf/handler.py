from src.bookshelf.domain.book_dao import BookDao
from src.bookshelf.domain.book import Book
import boto3

dynamodb_resource = boto3.resource("dynamodb")
dynamodb_client = boto3.client("dynamodb")


def create_book(event, context):
    book = Book(title=event["title"], author=event["author"])
    book_dao = BookDao(
        dynamodb_resource=dynamodb_resource, dynamodb_client=dynamodb_client
    )
    book_dao.create_book(book)

def delete_book(event, context):
    book = Book(title=event["title"], author=event["author"])
    book_dao = BookDao(
        dynamodb_resource=dynamodb_resource, dynamodb_client=dynamodb_client
    )
    book_dao.delete_book(book)
