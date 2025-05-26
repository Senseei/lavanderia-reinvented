from application.payment.usecases.strategy.payment_method_strategy import PaymentMethodStrategy
from application.user.interfaces.user_repository import UserRepository
from application.util.currency import br
from domain.payment.card import Card
from domain.user import User


class DebitCard(PaymentMethodStrategy):
    def __init__(self, user_repository: UserRepository, user: User, card: Card):
        super().__init__(user_repository, user)
        self._card = card

    def pay(self, total: float):
        """
        Process the payment using the debit card method.
        This method should implement the logic for processing a debit card payment.
        """
        # Here you would implement the logic to process a debit card payment.
        # For example, you might interact with a payment gateway API.
        print(f"Processing debit card payment of {br(total)} for user {self._user.name} using card {self._card.final()}.")