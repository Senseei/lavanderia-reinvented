from application.errors.entity_not_found_error import EntityNotFoundError
from presentation.dtos.response_dto import ResponseDTO
from presentation.machine.dtos.machine_details_dto import MachineDetailsDTO
from presentation.machine.machine_web_service import MachineWebService


class MachineController:
    def __init__(self, web_service: MachineWebService):
        self._web_service = web_service

    def find_machine_with_prices(self, entity_id: int) -> ResponseDTO[MachineDetailsDTO]:
        try:
            machine_details = self._web_service.find_machine_with_prices(entity_id)
            return ResponseDTO.success_response(machine_details)
        except EntityNotFoundError as e:
            return ResponseDTO.error_response(str(e))