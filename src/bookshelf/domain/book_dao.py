from src.bookshelf.domain.book import Book
from boto3.dynamodb.conditions import Key


class BookDao:
    def __init__(self, dynamodb_resource, dynamodb_client):
        self.dynamodb_resource = dynamodb_resource
        self.dynamodb_client = dynamodb_client
        self.table = self.dynamodb_resource.Table("books")

    def delete_table(self):
        self.dynamodb_client.delete_table(TableName="books")

    def create_table(self):
        self.dynamodb_client.create_table(
            TableName="books",
            KeySchema=[
                {"AttributeName": "author", "KeyType": "HASH"},
                {"AttributeName": "title", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "author", "AttributeType": "S"},
                {"AttributeName": "title", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

    def create_book(self, book: Book) -> None:
        self.table.put_item(Item=book.to_dict())

    def update_book(self, book: Book) -> None:
        self.table.update_item(
            Key={"author": book.author, "title": book.title},
            UpdateExpression="SET genre = :val1, publication_date = :val2",
            ExpressionAttributeValues={
                ":val1": book.genre,
                ":val2": book.publication_date,
            },
        )

    def find_book(self, book: Book) -> Book:
        result = self.table.get_item(Key={"author": book.author, "title": book.title})

        print(result)

        return result["Item"] if "Item" in result else None

    def find_by_author_and_genre(self, author, genre) -> Book:
        print(author)
        print(genre)
        result = self.table.query(
            IndexName="author-genre",
            KeyConditionExpression=Key("author").eq(author) & Key("genre").eq(genre),
        )

        print(result)

        return result["Items"][0] if "Items" in result else None

    def find_book_by_author_and_publication(self, author, publication) -> Book:
        result = self.table.get_item(
            Key={"author": book.author, "publication": publication}
        )

        print(result)

        return result["Item"] if "Item" in result else None

    def delete_book(self, book: Book) -> None:
        self.table.delete_item(Key={"author": book.author, "title": book.title})
