from domain.domain_entity import DomainEntity
from domain.enums.machine_type import MachineType


class Machine(DomainEntity):
    def __init__(self, identifier: str, type: MachineType, locked: bool, unit_id: int, id: int = None):
        super().__init__(id)
        self.identifier = identifier
        self.type = type
        self.locked = locked
        self.unit_id = unit_id