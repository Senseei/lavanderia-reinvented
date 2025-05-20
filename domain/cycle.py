from domain.domain_entity import DomainEntity

class Cycle(DomainEntity):
    def __init__(self, id: int, price: float, time: int):
        super().__init__(id)
        self.price = price
        self.time = time