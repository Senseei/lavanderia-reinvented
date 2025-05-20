from dataclasses import dataclass
from typing import Optional

@dataclass
class LoginCredentialsDTO:
    username: str
    password: str

    @classmethod
    def from_dict(cls, data: dict) -> Optional['LoginCredentialsDTO']:
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return None

        return cls(username=username, password=password)