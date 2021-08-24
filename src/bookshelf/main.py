from src.bookshelf.domain.book_dao import BookDao
from src.bookshelf.domain.book import Book

from src.bookshelf.core.resources_mgr import ResourcesMgr

# Get the service resource.
print("create dynamodb resources")
resources_mgr = ResourcesMgr()

book_dao = BookDao(
    dynamodb_resource=resources_mgr.dynamodb_resource,
    dynamodb_client=resources_mgr.dynamodb_client,
)
book = Book(title="kkk", author="tootoot")

# book_dao.create_table()
# dynamodb_resource.Table("books").wait_until_exists()


book_dao.create_book(book)
book_dao.find_book(book)
book.genre = "tech"
book.publication_date = "19-08-2021"
book_dao.update_book(book)
# book_dao.delete_book(book)

# book_dao.delete_table()
