from application.unit.usecases.unit_service import UnitService
from presentation.unit.dtos.unit_dto import UnitDTO


class UnitWebService:
    def __init__(self, unit_service: UnitService):
        self._unit_service = unit_service

    def find_all(self) -> list[UnitDTO]:
        return [UnitDTO(unit) for unit in self._unit_service.find_all()]

    def find_by_id(self, entity_id: int) -> UnitDTO:
        return UnitDTO(self._unit_service.find_by_id(entity_id))
