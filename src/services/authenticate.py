class Authenticate:

    def __init__(self, song_dao):
        self.song_dao = song_dao

    def import_file(self, bucket: str, key: str):