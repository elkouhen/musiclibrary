from src.bookshelf.domain.book_dao import BookDao
from src.bookshelf.domain.book import Book
import boto3

# Get the service resource.
dynamodb_resource = boto3.resource("dynamodb")
dynamodb_client = boto3.client("dynamodb")

book_dao = BookDao(dynamodb_resource=dynamodb_resource, dynamodb_client=dynamodb_client)
book = Book(title="kkk", author="tootoot")

# book_dao.create_table()
# dynamodb_resource.Table("books").wait_until_exists()


book_dao.create_book(book)
book_dao.find_book(book)
book.genre = "tech"
book.publication_date = "19-08-2021"
book_dao.update_book(book)
book_dao.delete_book(book)

# book_dao.delete_table()
