from application.errors.entity_not_found_error import EntityNotFoundError
from application.user.dtos.authenticated_user_dto import AuthenticatedUserDTO
from application.user.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def login(self, username, password) -> AuthenticatedUserDTO:
        user = self._user_repository.find_by_username_and_password(username, password)
        if not user:
            raise EntityNotFoundError("Invalid username or password")
        return AuthenticatedUserDTO(user)