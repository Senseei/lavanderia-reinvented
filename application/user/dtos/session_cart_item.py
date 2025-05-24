from application.machine.dtos.cycle_dto import CycleDTO
from application.machine.dtos.machine_dto import MachineDTO


class SessionCartItem:
    def __init__(self, machine: MachineDTO, cycle: CycleDTO):
        self.machine = machine
        self.cycle = cycle

    def __eq__(self, other):
        return self.machine == other.machine and self.cycle == other.cycle