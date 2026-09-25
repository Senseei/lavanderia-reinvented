from application.errors.entity_not_found_error import EntityNotFoundError
from application.user.interfaces.user_repository import UserRepository
from domain.user import User
from di.decorators import component


@component
class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def find_by_id(self, user_id: int) -> User:
        user = self._repository.find_by_id(user_id)
        if user is None:
            raise EntityNotFoundError("User", user_id)
        return user
