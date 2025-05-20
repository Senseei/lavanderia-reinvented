from domain.domain_entity import DomainEntity


class Unit(DomainEntity):
    def __init__(self, id: int, name: str):
        super().__init__(id)
        self.name = name