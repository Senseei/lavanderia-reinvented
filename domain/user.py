from domain_entity import DomainEntity


class User(DomainEntity):
    def __init__(self, id: int, username: str, name: str, password: str, cash: float):
        super().__init__(id)
        self.name = name
        self.username = username
        self.password = password
        self.cash = cash