from domain_entity import DomainEntity

class Ticket(DomainEntity):
    def __init__(self, id: int, discount: float, code: str):
        super().__init__(id)
        self.discount = discount
        self.code = code