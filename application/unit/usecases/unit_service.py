from application.unit.dtos.unit_dto import UnitDTO
from application.unit.interfaces.unit_repository import UnitRepository


class UnitService:
    def __init__(self, repository: UnitRepository):
        self._repository = repository

    def find_all(self) -> list[UnitDTO]:
        return list(map(UnitDTO, self._repository.find_all()))