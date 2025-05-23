from application.machine.dtos.cycle_dto import CycleDTO
from application.machine.dtos.machine_dto import MachineDTO


class MachineDetailsDTO:
    def __init__(self, machine: MachineDTO, prices: list[CycleDTO]):
        self.machine = machine
        self.prices = sorted(prices, key=lambda price: price.time)