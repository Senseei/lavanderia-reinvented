from application.user.session_cart_item import SessionCartItem
from presentation.machine.dtos.cycle_dto import CycleDTO
from presentation.machine.dtos.machine_dto import MachineDTO


class CartItemDTO:
    def __init__(self, item: SessionCartItem):
        self.machine = MachineDTO(item.machine)
        self.cycle = CycleDTO(item.cycle)
