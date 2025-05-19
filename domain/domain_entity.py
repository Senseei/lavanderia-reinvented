from abc import ABC

class DomainEntity(ABC):
    def __init__(self, id: int):
        self.id = id