from application.errors.entity_not_found_error import EntityNotFoundError
from application.machine.interfaces.cycle_repository import CycleRepository
from application.machine.interfaces.machine_repository import MachineRepository
from application.user.session_cart_item import SessionCartItem
from domain.cycle import Cycle
from domain.machine import Machine
from di.decorators import component


@component
class MachineService:
    def __init__(self, repository: MachineRepository, cycle_repository: CycleRepository):
        self._repository = repository
        self._cycle_repository = cycle_repository

    def find_by_id(self, entity_id: int) -> Machine:
        machine = self._repository.find_by_id(entity_id)
        if machine is None:
            raise EntityNotFoundError(Machine.__name__, entity_id)
        return machine

    def find_all_cycles(self) -> list[Cycle]:
        return self._cycle_repository.find_all()

    def lock_machines(self, machine_cycles: list[SessionCartItem]) -> None:
        self._repository.lock_machines([item.machine.id for item in machine_cycles])
        # we could insert a timer here to unlock them after a certain period

    def is_any_machine_in_list_busy(self, machines: list[int]) -> bool:
        return self._repository.is_any_machine_in_list_busy(machines)

