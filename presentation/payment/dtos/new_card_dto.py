from datetime import datetime
from typing import Optional

from domain.payment.enums.payment_method import PaymentMethod


class NewCardDTO:
    def __init__(self, titular: str, number: str, method: PaymentMethod, due_date: datetime, cvv: int):
        self.titular = titular
        self.number = number
        self.due_date = due_date
        self.method = method
        self.cvv = cvv

    @classmethod
    def from_dict(cls, body: dict) -> Optional['NewCardDTO']:
        titular = body.get("titular")
        number = body.get("number")
        method = body.get("method")
        due_date = body.get("due_date")
        cvv = body.get("cvv")

        if not titular or not number or not method or not due_date or not cvv:
            return None

        if len(due_date.split('/')[1]) == 2:
            month, short_year = due_date.split('/')
            full_year = '20' + short_year
            due_date = f"{month}/{full_year}"

        return cls(
            titular=titular,
            number=number.replace(" ", ""),
            method=PaymentMethod(method),
            due_date=datetime.strptime(due_date, "%m/%Y"),
            cvv=cvv
        )