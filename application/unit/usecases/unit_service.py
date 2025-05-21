from application.errors.entity_not_found_error import EntityNotFoundError
from application.unit.dtos.unit_dto import UnitDTO
from application.unit.interfaces.unit_repository import UnitRepository
from domain.unit import Unit


class UnitService:
    def __init__(self, repository: UnitRepository):
        self._repository = repository

    def find_all(self) -> list[UnitDTO]:
        return list(map(UnitDTO, self._repository.find_all()))

    def find_by_id(self, entity_id: int) -> UnitDTO:
        unit = self._repository.find_by_id(entity_id)
        if unit is None:
            raise EntityNotFoundError(Unit.__class__.__name__, entity_id)
        return UnitDTO(unit)