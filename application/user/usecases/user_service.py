from application.auth.dtos.authenticated_user_dto import AuthenticatedUserDTO
from application.user.dtos.user_dto import UserDTO
from application.user.interfaces.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def find_by_id(self, user_id: int) -> UserDTO:
        return UserDTO(self._repository.find_by_id(user_id))

    def update_user_session(self, user_id: int) -> AuthenticatedUserDTO:
        return AuthenticatedUserDTO(self._repository.find_by_id(user_id))
