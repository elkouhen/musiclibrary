# -*- coding: utf-8 -*-

import pytest
from bookshelf.core.resources_mgr import ResourcesMgr
from bookshelf.domain.book import Book
from bookshelf.domain.book_dao import BookDao

resources_mgr = ResourcesMgr()


class TestBookDao:
    @classmethod
    def setup_class(cls):
        book_dao = BookDao(
            dynamodb_resource=resources_mgr.dynamodb_resource,
            dynamodb_client=resources_mgr.dynamodb_client,
        )

        book = Book(title="toto", author="toto", genre="SF", publication_date="1975")

        book_dao.create(book)

    @classmethod
    def teardown_class(cls):
        book_dao = BookDao(
            dynamodb_resource=resources_mgr.dynamodb_resource,
            dynamodb_client=resources_mgr.dynamodb_client,
        )

        book = Book(title="toto", author="toto")

        book_dao.delete(book)

    def test_find_book_by_author_and_title_should_return_book_when_it_exists(self):
        # given
        book_dao = BookDao(
            dynamodb_resource=resources_mgr.dynamodb_resource,
            dynamodb_client=resources_mgr.dynamodb_client,
        )

        book = Book(title="toto", author="toto")

        # when
        abook = book_dao.find_by_author_and_title(book)

        # then
        assert abook is not None

    def test_find_book_by_author_and_title_should_return_none_when_it_not_exist(
            self,
    ):
        # given
        book_dao = BookDao(
            dynamodb_resource=resources_mgr.dynamodb_resource,
            dynamodb_client=resources_mgr.dynamodb_client,
        )
        book = Book(title="toto_ne_doit_pas_exister", author="toto_ne_doit_pas_exister")

        # when
        abook = book_dao.find_by_author_and_title(book)

        # then
        assert abook is None

    def test_find_book_by_author_and_genre_should_return_book_when_it_exists(self):
        # given
        book_dao = BookDao(
            dynamodb_resource=resources_mgr.dynamodb_resource,
            dynamodb_client=resources_mgr.dynamodb_client,
        )

        # when
        abook = book_dao.find_by_author_and_genre(author="toto", genre="SF")

        # then
        assert abook is not None

    def test_find_book_by_author_and_genre_should_return_none_when_it_not_exists(self):
        # given
        book_dao = BookDao(
            dynamodb_resource=resources_mgr.dynamodb_resource,
            dynamodb_client=resources_mgr.dynamodb_client,
        )

        # when
        abook = book_dao.find_by_author_and_genre(author="toto", genre="SF1")

        # then
        assert abook is None

    def test_find_book_by_author_and_publication_date_should_return_book_when_it_exists(self):
        # given
        book_dao = BookDao(
            dynamodb_resource=resources_mgr.dynamodb_resource,
            dynamodb_client=resources_mgr.dynamodb_client,
        )

        # when
        abook = book_dao.find_by_genre_and_publication_date(genre="SF", publication_date="1975")

        # then
        assert abook is not None

    def test_find_book_by_author_and_publication_date_should_return_none_when_it_not_exists(self):
        # given
        book_dao = BookDao(
            dynamodb_resource=resources_mgr.dynamodb_resource,
            dynamodb_client=resources_mgr.dynamodb_client,
        )

        # when
        abook = book_dao.find_by_genre_and_publication_date(genre="SF", publication_date="1974")

        # then
        assert abook is None
