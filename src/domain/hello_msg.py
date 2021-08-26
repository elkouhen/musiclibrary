import json
import uuid


class HelloMsg:
    def __init__(self, **kwargs) -> None:
        self.language = kwargs["language"]
        self.value = kwargs["value"]
        self.uuid = str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __eq__(self, other) -> bool:
        if not isinstance(other, HelloMsg):
            return NotImplemented

        return self.language == other.language and self.value == other.value
