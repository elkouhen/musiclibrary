import json
import uuid


class Song:
    def __init__(self, **kwargs) -> None:
        self.author = kwargs["author"]
        self.title = kwargs["title"]
        self.genre = kwargs["genre"]
        self.genre = kwargs["date"]

        self.uuid = str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Song):
            return NotImplemented

        return self.language == other.language and self.value == other.value
