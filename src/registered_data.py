from typing import ClassVar, List

class RegisteredFeed:
    uid: ClassVar[int]
    type: ClassVar[int]
    name: ClassVar[str]
    url: ClassVar[str]
    registered_channels: ClassVar[List[int]]

    def __init__(self, uid: int, type: int, name: str, url: str, registered_channel: int) -> None:
        self.uid = uid
        self.type = type
        self.name = name
        self.url = url
        self.registered_channels = [registered_channel]

class RegisteredServer:
    id: ClassVar[int]
    name: ClassVar[str]
    feeds: ClassVar[List[RegisteredFeed]] = []

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name