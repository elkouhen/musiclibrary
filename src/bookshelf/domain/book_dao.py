from src.bookshelf.domain.book import Book
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()


class BookDao:
    def __init__(self, dynamodb_resource, dynamodb_client):
        self.dynamodb_resource = dynamodb_resource
        self.dynamodb_client = dynamodb_client
        self.table = self.dynamodb_resource.Table("books")

    def create(self, book: Book) -> None:
        logger.info("[book] create")
        self.table.put_item(Item=book.to_dict())

    def delete(self, uuid) -> None:
        logger.info("[book] delete")

        result = self.table.query(
            IndexName="uuid",
            KeyConditionExpression=Key("uuid").eq(uuid),
        )

        assert len(result["Items"]) == 1

        book = result["Items"][0]

        print(book)

        self.table.delete_item(Key={"author": book["author"], "title": book["title"]})

        return None

    def update(self, book: Book) -> None:
        logger.info("[book] update")
        self.table.update_item(
            Key={"author": book.author, "title": book.title},
            UpdateExpression="SET genre = :val1, publication_date = :val2",
            ExpressionAttributeValues={
                ":val1": book.genre,
                ":val2": book.publication_date,
            },
        )

    def find_by_author_and_title(self, book: Book) -> Book:
        logger.info("[book] find_by_author_and_title")
        result = self.table.get_item(Key={"author": book.author, "title": book.title})

        print(result)

        return result["Item"] if "Item" in result else None

    def find_by_author_and_genre(self, author, genre) -> Book:
        logger.info("[book] find_by_author_and_genre")
        result = self.table.query(
            IndexName="author-genre",
            KeyConditionExpression=Key("author").eq(author) & Key("genre").eq(genre),
        )

        return result["Items"]

    def find_by_genre_and_publication_date(self, genre, publication_date) -> Book:
        print(
            f"[book] find_by_genre_and_publication_date genre={genre} publication_date={publication_date}"
        )

        result = self.table.query(
            IndexName="genre-publication",
            KeyConditionExpression=Key("genre").eq(genre)
            & Key("publication_date").eq(publication_date),
        )

        return result["Items"]
