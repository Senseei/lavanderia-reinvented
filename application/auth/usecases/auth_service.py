from application.errors.invalid_credentials_error import InvalidCredentialsError
from application.errors.duplicate_entity_error import DuplicateEntityError
from application.user.interfaces.user_repository import UserRepository
from domain.user import User
from di.decorators import component


@component
class AuthService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def login(self, username: str, password: str) -> User:
        user = self._user_repository.find_by_username_and_password(username, password)
        if not user:
            raise InvalidCredentialsError("Invalid username or password")
        return user

    def register(self, username: str, name: str, password: str) -> User:
        if self._user_repository.find_by_username(username):
            raise DuplicateEntityError("User", "A user with the given username already exists")

        new_user = User(username, name, password)
        return self._user_repository.save(new_user)
