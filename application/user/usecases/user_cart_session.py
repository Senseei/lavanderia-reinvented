from application.errors.entity_not_found_error import EntityNotFoundError
from application.machine.dtos.cycle_dto import CycleDTO
from application.machine.dtos.machine_dto import MachineDTO
from application.machine.interfaces.cycle_repository import CycleRepository
from application.machine.interfaces.machine_repository import MachineRepository
from application.user.dtos.session_cart_item import SessionCartItem
from application.util.currency import br


class UserCartSession:
    def __init__(self, machine_repository: MachineRepository, cycle_repository: CycleRepository):
        self._machine_repository = machine_repository
        self._cycle_repository = cycle_repository
        self._cart: list[SessionCartItem] = []

    def add_item(self, machine_id: int, cycle_id: int) -> bool:
        machine = self._machine_repository.find_by_id(machine_id)
        cycle = self._cycle_repository.find_by_id(cycle_id)

        if not machine or not cycle:
            raise EntityNotFoundError("Machine or Cycle")

        cart_item = SessionCartItem(MachineDTO(machine), CycleDTO(cycle))
        if cart_item not in self._cart:
            self._cart.append(cart_item)
            return True

        return False

    def remove_item(self, machine_id: int, cycle_id: int) -> bool:
        for item in self._cart:
            if item.machine.id == machine_id and item.cycle.id == cycle_id:
                self._cart.remove(item)
                return True
        return False

    def get_items(self):
        return self._cart

    def get_total(self) -> float:
        total = 0.0
        for item in self._cart:
            total += item.cycle.price
        return total

    def get_formatted_total(self) -> str:
        return br(self.get_total())