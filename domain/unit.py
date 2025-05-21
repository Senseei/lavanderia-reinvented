from domain.domain_entity import DomainEntity


class Unit(DomainEntity):
    def __init__(self, id: int, local: str):
        super().__init__(id)
        self.local = local