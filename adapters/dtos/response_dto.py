from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')

@dataclass
class ResponseDTO(Generic[T]):
    success: bool
    message: str = None
    data: T = None

    @classmethod
    def success_response(cls, data: T) -> 'ResponseDTO[T]':
        return cls(success=True, data=data)

    @classmethod
    def error_response(cls, message: str) -> 'ResponseDTO[T]':
        return cls(success=False, message=message)