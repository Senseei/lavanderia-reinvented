from application.unit.interfaces.unit_repository import UnitRepository
from domain.unit import Unit


class UnitRepositoryImpl(UnitRepository):

    def save(self, entity: Unit) -> Unit:
        pass

    def find_by_id(self, entity_id: int) -> Unit:
        pass

    def find_all(self) -> list[Unit]:
        pass

    def delete(self, entity: Unit):
        pass

    def delete_by_id(self, entity_id: int):
        pass

    def update(self, entity: Unit) -> Unit:
        pass

    def find_by_name(self, name: str) -> Unit:
        pass