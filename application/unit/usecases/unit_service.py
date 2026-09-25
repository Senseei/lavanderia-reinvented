from application.errors.entity_not_found_error import EntityNotFoundError
from application.unit.interfaces.unit_repository import UnitRepository
from domain.unit import Unit
from di.decorators import component


@component
class UnitService:
    def __init__(self, repository: UnitRepository):
        self._repository = repository

    def find_all(self) -> list[Unit]:
        return self._repository.find_all()

    def find_by_id(self, entity_id: int) -> Unit:
        unit = self._repository.find_by_id(entity_id)
        if unit is None:
            raise EntityNotFoundError(Unit.__name__, entity_id)
        return unit
