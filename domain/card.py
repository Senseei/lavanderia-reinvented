import datetime

from domain_entity import DomainEntity
from enums.card_brand import CardBrand
from enums.payment_method import PaymentMethod
from user import User


class Card(DomainEntity):
    def __init__(self, id: int, user: User, brand: CardBrand, number: str, method: PaymentMethod, due_date: datetime, cv: str):
        super().__init__(id)
        self.user = user
        self.brand = brand
        self.humber = number
        self.method = method
        self.due_date = due_date
        self.cv = cv