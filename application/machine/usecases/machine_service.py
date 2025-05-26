from application.errors.entity_not_found_error import EntityNotFoundError
from application.machine.dtos.cycle_dto import CycleDTO
from application.machine.dtos.machine_details_dto import MachineDetailsDTO
from application.machine.dtos.machine_dto import MachineDTO
from application.machine.interfaces.cycle_repository import CycleRepository
from application.machine.interfaces.machine_repository import MachineRepository
from application.user.dtos.session_cart_item import SessionCartItem
from domain.machine import Machine


class MachineService:
    def __init__(self, repository: MachineRepository, cycle_repository: CycleRepository):
        self._repository = repository
        self._cycle_repository = cycle_repository

    def find_by_id(self, entity_id: int) -> MachineDTO:
        machine = self._repository.find_by_id(entity_id)
        if machine is None:
            raise EntityNotFoundError(Machine.__class__.__name__, entity_id)
        return MachineDTO(machine)

    def find_machine_with_prices(self, entity_id: int) -> MachineDetailsDTO:
        machine_dto = self.find_by_id(entity_id)
        cycles = self._cycle_repository.find_all()
        return MachineDetailsDTO(machine=machine_dto, prices=list(map(CycleDTO, cycles)))

    def lock_machines(self, machine_cycles: list[SessionCartItem]) -> None:
        self._repository.lock_machines([item.machine.id for item in machine_cycles])
        # we could insert a timer here to unlock them after a certain period

    def is_any_machine_in_list_busy(self, machines: list[int]) -> bool:
        return self._repository.is_any_machine_in_list_busy(machines)

