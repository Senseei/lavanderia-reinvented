from application.user.dtos.session_cart_item import SessionCartItem
from domain.payment.enums.payment_method import PaymentMethod


class PaymentRequestDTO:
    def __init__(self, user_id: int, method: PaymentMethod, card_id: str=None):
        self.user_id = user_id
        self.method = method
        self.card_id = card_id