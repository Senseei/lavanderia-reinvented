import datetime

from domain.domain_entity import DomainEntity
from domain.enums.card_brand import CardBrand
from domain.enums.payment_method import PaymentMethod
from domain.user import User


class Card(DomainEntity):
    def __init__(self, user: User, titular: str, brand: CardBrand, number: str, method: PaymentMethod, due_date: datetime, cvv: int, id: int = None):
        super().__init__(id)
        self.user = user
        self.titular = titular
        self.brand = brand
        self.number = number
        self.method = method
        self.due_date = due_date
        self.cvv = cvv

    def final(self, mask: bool = True) -> str:
        return f"**** **** **** {self.number[-4:]}" if mask else self.number[-4:]

    def __str__(self):
        return f"Card(titular={self.titular}, brand={self.brand}, number={self.number}, method={self.method}, due_date={self.due_date}, cvv={self.cvv})"