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
    @classmethod
    def setup_class(cls):
        book_dao = book_dao_test()

        book = HelloMsg(language="fr", value="bonjour tout le monde")

        book_dao.create(book)

    @classmethod
    def teardown_class(cls):
        book_dao = book_dao_test()

        book_dao.delete("fr")

    def test_find_book_by_language_should_return_hello_msg_when_it_exists(self):
        # given
        book_dao = book_dao_test()

        # when
        abook = book_dao.find_by_language(language="fr")

        # then
        assert abook is not None

    def test_find_book_by_language_should_return_non_when_not_it_exists(
            self,
    ):
        # given
        book_dao = book_dao_test()

        # when
        abook = book_dao.find_by_language(language="fra")

        # then
        assert abook is None
