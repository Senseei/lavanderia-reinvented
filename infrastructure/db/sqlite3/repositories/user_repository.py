from application.user.user_repository import UserRepository
from domain.domain_entity import DomainEntity


class UserRepositoryImpl(UserRepository):
    def save(self, entity: DomainEntity) -> DomainEntity:
        pass

    def find_by_id(self, entity_id: int) -> DomainEntity:
        pass

    def find_all(self):
        pass

    def delete(self, entity: DomainEntity):
        pass

    def delete_by_id(self, entity_id: int):
        pass

    def update(self, entity: DomainEntity) -> DomainEntity:
        pass

    def find_by_username_and_password(self, username: str, password: str):
        pass