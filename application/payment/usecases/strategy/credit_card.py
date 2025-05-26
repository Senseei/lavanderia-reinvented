from application.payment.usecases.strategy.payment_method_strategy import PaymentMethodStrategy
from application.user.interfaces.user_repository import UserRepository
from application.util.currency import br
from domain.payment.card import Card
from domain.user import User


class CreditCard(PaymentMethodStrategy):
    def __init__(self, user_repository: UserRepository, user: User, card: Card):
        super().__init__(user_repository, user)
        self._card = card

    def pay(self, total: float):
        """
        Process the payment using the credit card method.
        This method should implement the logic for processing a credit card payment.
        """
        # Here you would implement the logic to process the credit card payment.
        # This could involve calling an external payment gateway API, etc.
        print(f"Processing credit card payment of {br(total)} for user {self._user.name} using card {self._card.final()}.")