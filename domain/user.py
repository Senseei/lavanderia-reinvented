from domain.domain_entity import DomainEntity


class User(DomainEntity):
    def __init__(self, username: str, name: str, password: str, cash: float = 0, id: int = None):
        super().__init__(id)
        self.name = name
        self.username = username
        self.password = password
        self.cash = cash