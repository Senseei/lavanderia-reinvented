from domain.domain_entity import DomainEntity
from domain.machine import Machine


class Unit(DomainEntity):
    def __init__(self, local: str, machines: list[Machine]=None, id: int = None):
        super().__init__(id)
        self.machines = machines if machines is not None else []
        self.local = local