from domain_entity import DomainEntity
from enums.machine_type import MachineType
from unit import Unit


class Machine(DomainEntity):
    def __init__(self, id: int, identifier: str, type: MachineType, locked: bool, unit: Unit):
        super().__init__(id)
        self.identifier = identifier
        self.type = type
        self.locked = locked
        self.unit = unit