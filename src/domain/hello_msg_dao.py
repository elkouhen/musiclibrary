import logging

from src.domain.hello_msg import HelloMsg

logger = logging.getLogger()


class HelloMsgDao:
    def __init__(self, dynamodb_resource, dynamodb_client, table_name):
        self.dynamodb_resource = dynamodb_resource
        self.dynamodb_client = dynamodb_client
        self.table = self.dynamodb_resource.Table(table_name)

    def create(self, entity: HelloMsg) -> None:
        logger.info("[entity] create")
        self.table.put_item(Item=entity.to_dict())

    def delete(self, language) -> None:
        logger.info("[entity] delete")

        self.table.delete_item(Key={"language": language})

        return None

    def find_by_language(self, language) -> HelloMsg:
        logger.info("[entity] entity")
        result = self.table.get_item(Key={"language": language})

        print(result)

        return result["Item"] if "Item" in result else None
