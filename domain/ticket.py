from datetime import datetime

from domain.domain_entity import DomainEntity
from domain.enums.discount_type import DiscountType


class Ticket(DomainEntity):
    def __init__(self, type: DiscountType, discount: float, code: str, expires_at: datetime, id: int = None):
        super().__init__(id)
        self.type = type
        self.discount = discount
        self.code = code
        self.expires_at = expires_at

    def apply(self, value: float) -> float:
        if self.type == DiscountType.PERCENTAGE:
            return value - (value * (self.discount / 100))
        elif self.type == DiscountType.FLAT:
            return value - self.discount
        else:
            return value