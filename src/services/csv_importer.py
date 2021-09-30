import csv
import tempfile

import boto3
from src.domain.song import Song


class CSVImporter:
    def __init__(self, song_dao):
        self.song_dao = song_dao

    def import_file(self, bucket: str, key: str):

        print("import file")

        with tempfile.NamedTemporaryFile("w") as f:
            boto3.client("s3").download_file(bucket, key, f.name)

            with open(f.name, newline="") as csvfile:
                reader = csv.DictReader(csvfile, delimiter=";")

                print("parse file")

                for row in reader:

                    try:

                        print("handle row")

                        song = Song(
                            author=row["author"],
                            title=row["title"],
                            genre=row["genre"],
                            date=row["date"],
                        )

                        self.song_dao.create(song)
                    except BaseException as e:
                        print(str(e))
