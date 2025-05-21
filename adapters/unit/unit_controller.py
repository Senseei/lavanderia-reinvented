from adapters.dtos.response_dto import ResponseDTO
from application.errors.entity_not_found_error import EntityNotFoundError
from application.unit.dtos.unit_dto import UnitDTO
from application.unit.usecases.unit_service import UnitService

class UnitControllerAdapter:
    def __init__(self, service: UnitService):
        self._service = service

    def find_all(self) -> ResponseDTO[list[UnitDTO]]:
        return ResponseDTO.success_response(self._service.find_all())

    def find_by_id(self, entity_id: int) -> ResponseDTO[UnitDTO]:
        try:
            unit = self._service.find_by_id(entity_id)
            return ResponseDTO.success_response(unit)
        except EntityNotFoundError as e:
            return ResponseDTO.error_response(str(e))