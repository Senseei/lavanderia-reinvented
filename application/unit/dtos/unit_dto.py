from application.machine.dtos.machine_dto import MachineDTO
from domain.unit import Unit


class UnitDTO:
    def __init__(self, unit: Unit):
        self.id = unit.id
        self.local = unit.local
        self.machines = [MachineDTO(machine) for machine in unit.machines]