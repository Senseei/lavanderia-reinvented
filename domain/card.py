import datetime

from domain.domain_entity import DomainEntity
from enums.card_brand import CardBrand
from enums.payment_method import PaymentMethod
from user import User


class Card(DomainEntity):
    def __init__(self, user: User, brand: CardBrand, number: str, method: PaymentMethod, due_date: datetime, cv: str, id: int = None):
        super().__init__(id)
        self.user = user
        self.brand = brand
        self.number = number
        self.method = method
        self.due_date = due_date
        self.cv = cv

    def final(self, mask: bool = True) -> str:
        return f"**** **** **** {self.number[-4:]}" if mask else self.number[-4:]