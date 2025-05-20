from application.user.user_repository import UserRepository
from domain.user import User


class UserRepositoryImpl(UserRepository):

    def save(self, entity: User) -> User:
        pass

    def find_by_id(self, entity_id: int) -> User:
        pass

    def find_all(self) -> list[User]:
        pass

    def delete(self, entity: User):
        pass

    def delete_by_id(self, entity_id: int):
        pass

    def update(self, entity: User) -> User:
        pass

    def find_by_username_and_password(self, username: str, password: str) -> User:
        pass

    def find_by_username(self, username: str) -> User:
        pass
