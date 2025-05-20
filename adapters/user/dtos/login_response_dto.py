from dataclasses import dataclass
from typing import Optional
from application.auth.dtos.authenticated_user_dto import AuthenticatedUserDTO


@dataclass
class LoginResponseDTO:
    success: bool
    message: Optional[str] = None
    user: Optional[AuthenticatedUserDTO] = None

    @classmethod
    def success_response(cls, user: AuthenticatedUserDTO) -> 'LoginResponseDTO':
        return cls(success=True, user=user)

    @classmethod
    def error_response(cls, message: str) -> 'LoginResponseDTO':
        return cls(success=False, message=message)