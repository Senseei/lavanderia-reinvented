from dataclasses import dataclass
from typing import Optional


@dataclass
class NewUserDTO:
    username: str
    name: str
    password: str

    @classmethod
    def from_dict(cls, data: dict) -> Optional['NewUserDTO']:
        username = data.get("username")
        name = data.get("name")
        password = data.get("password")

        if not username or not name or not password:
            return None

        return cls(username=username, name=name, password=password)