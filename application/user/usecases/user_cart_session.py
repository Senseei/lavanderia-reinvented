from application.errors.entity_not_found_error import EntityNotFoundError
from application.machine.interfaces.cycle_repository import CycleRepository
from application.machine.interfaces.machine_repository import MachineRepository
from application.ticket.usecases.ticket_service import TicketService
from application.user.session_cart_item import SessionCartItem


class UserCartSession:
    """
    One user's cart for the current request. The adapter rebuilds it from the HTTP session
    on every request, so it is never shared between users or requests.
    """

    def __init__(self, machine_repository: MachineRepository, cycle_repository: CycleRepository,
                 ticket_service: TicketService):
        self._machine_repository = machine_repository
        self._cycle_repository = cycle_repository
        self._ticket_service = ticket_service

        self._cart: list[SessionCartItem] = []
        self._discounts: float = 0.0
        self.applied_ticket = None

    def sync_items(self, items_data: list[dict]):
        self._cart.clear()
        for item_data in items_data:
            self.add_item(item_data["machine_id"], item_data["cycle_id"])

    def sync_discounts(self, discounts: float):
        self._discounts = discounts

    def add_item(self, machine_id: int, cycle_id: int) -> bool:
        machine = self._machine_repository.find_by_id(machine_id)
        cycle = self._cycle_repository.find_by_id(cycle_id)

        if not machine or not cycle:
            raise EntityNotFoundError("Machine or Cycle")

        cart_item = SessionCartItem(machine, cycle)
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

    def get_total_with_discounts(self) -> float:
        return self.get_total() - self._discounts

    def get_discounts(self) -> float:
        return self._discounts

    def apply_discount(self, code: str, user_id: int) -> None:
        self._discounts = self._ticket_service.apply_ticket(code, user_id, self.get_total())
        self.applied_ticket = code

    def remove_discount(self) -> None:
        self.applied_ticket = None
        self._discounts = 0.0

    def marked_ticket_as_used_if_any(self, user_id: int) -> None:
        if self.applied_ticket:
            self._ticket_service.mark_ticket_as_used(self.applied_ticket, user_id)

    def clear(self):
        self._cart.clear()
        self._discounts = 0.0
