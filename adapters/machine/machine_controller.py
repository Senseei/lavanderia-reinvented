from adapters.dtos.response_dto import ResponseDTO
from application.errors.entity_not_found_error import EntityNotFoundError
from application.machine.dtos.machine_details_dto import MachineDetailsDTO
from application.machine.usecases.machine_service import MachineService


class MachineControllerAdapter:
    def __init__(self, service: MachineService):
        self._service = service

    def find_machine_with_prices(self, entity_id: int) -> ResponseDTO[MachineDetailsDTO]:
        try:
            machine_details = self._service.find_machine_with_prices(entity_id)
            return ResponseDTO.success_response(machine_details)
        except EntityNotFoundError as e:
            return ResponseDTO.error_response(str(e))