# -*- coding: utf-8 -*-

from src.core.resources_mgr import ResourcesMgr
from src.domain.song import Song
from src.domain.song_dao import SongDao

resources_mgr = ResourcesMgr()


def song_dao_test():
    return SongDao(
        dynamodb_resource=resources_mgr.dynamodb_resource,
        dynamodb_client=resources_mgr.dynamodb_client,
        table_name=resources_mgr.table_name(),
    )


class TestsongDao:

    def test_find_song_by_uuid_should_return_song_when_it_exists(self):
        # given
        song_dao = song_dao_test()
        song = Song(author="XXX", title="bonjour tout le monde", genre="contry", date="1974")
        song_dao.create(song)

        # when
        asong = song_dao.find_by_uuid(uuid=song.uuid)

        # then
        assert asong is not None
        song_dao.delete(uuid=song.uuid)

    def test_find_song_by_uuid_should_return_none_when_not_it_exists(
            self,
    ):
        # given

        # when
        asong = song_dao_test().find_by_uuid(uuid="pipouuid")

        # then
        assert asong is None
