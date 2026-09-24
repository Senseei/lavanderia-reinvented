from application.errors.entity_not_found_error import EntityNotFoundError
from presentation.dtos.response_dto import ResponseDTO
from presentation.unit.dtos.unit_dto import UnitDTO
from presentation.unit.unit_web_service import UnitWebService

class UnitController:
    def __init__(self, web_service: UnitWebService):
        self._web_service = web_service

    def find_all(self) -> ResponseDTO[list[UnitDTO]]:
        return ResponseDTO.success_response(self._web_service.find_all())

    def find_by_id(self, entity_id: int) -> ResponseDTO[UnitDTO]:
        try:
            unit = self._web_service.find_by_id(entity_id)
            return ResponseDTO.success_response(unit)
        except EntityNotFoundError as e:
            return ResponseDTO.error_response(str(e))