from application.unit.dtos.unit_dto import UnitDTO
from application.unit.usecases.unit_service import UnitService

class UnitControllerAdapter:
    def __init__(self, service: UnitService):
        self._service = service

    def find_all(self) -> list[UnitDTO]:
        return self._service.find_all()