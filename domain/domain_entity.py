from datetime import datetime
from abc import ABC

class DomainEntity(ABC):
    def __init__(self, id: int, created_at: datetime = datetime.now(), updated_at: datetime = datetime.now()):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at