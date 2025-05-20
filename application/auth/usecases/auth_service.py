from application.auth.dtos.new_user_dto import NewUserDTO
from application.errors.invalid_credentials_error import InvalidCredentialsError
from application.user.dtos.user_dto import UserDTO
from application.errors.duplicate_entity_error import DuplicateEntityError
from application.auth.dtos.authenticated_user_dto import AuthenticatedUserDTO
from application.user.interfaces.user_repository import UserRepository
from domain.user import User


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def login(self, username, password) -> AuthenticatedUserDTO:
        user = self._user_repository.find_by_username_and_password(username, password)
        if not user:
            raise InvalidCredentialsError("Invalid username or password")
        return AuthenticatedUserDTO(user)

    def register(self, dto: NewUserDTO) -> UserDTO:
        if self._user_repository.find_by_username(dto.username):
            raise DuplicateEntityError("A user with the given username already exists")

        new_user = User(dto.username, dto.name, dto.password)
        return UserDTO(self._user_repository.save(new_user))