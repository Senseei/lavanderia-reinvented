from application.machine.usecases.machine_service import MachineService
from presentation.machine.dtos.cycle_dto import CycleDTO
from presentation.machine.dtos.machine_details_dto import MachineDetailsDTO
from presentation.machine.dtos.machine_dto import MachineDTO


class MachineWebService:
    def __init__(self, machine_service: MachineService):
        self._machine_service = machine_service

    def find_machine_with_prices(self, entity_id: int) -> MachineDetailsDTO:
        machine = self._machine_service.find_by_id(entity_id)
        cycles = self._machine_service.find_all_cycles()
        return MachineDetailsDTO(machine=MachineDTO(machine), prices=[CycleDTO(cycle) for cycle in cycles])
