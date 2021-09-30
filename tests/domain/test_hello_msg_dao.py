# -*- coding: utf-8 -*-

from src.core.resources_mgr import ResourcesMgr
from src.domain.hello_msg import HelloMsg
from src.domain.hello_msg_dao import HelloMsgDao

resources_mgr = ResourcesMgr()


def book_dao_test():
    return HelloMsgDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
        table_name=resources_mgr.table_name(),
    )


class TestBookDao:

    def test_find_book_by_uuid_should_return_hello_msg_when_it_exists(self):
        # given
        book_dao = book_dao_test()
        book = HelloMsg(language="fr", value="bonjour tout le monde")
        book_dao.create(book)

        # when
        abook = book_dao.find_by_uuid(uuid=book.uuid)

        # then
        assert abook is not None
        book_dao.delete(uuid=book.uuid)

    def test_find_book_by_uuid_should_return_none_when_not_it_exists(
            self,
    ):
        # given

        # when
        abook = book_dao_test().find_by_uuid(uuid="pipouuid")

        # then
        assert abook is None
