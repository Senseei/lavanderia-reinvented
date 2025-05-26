from application.payment.usecases.strategy.payment_method_strategy import PaymentMethodStrategy
from application.user.interfaces.user_repository import UserRepository
from domain.user import User


class Wallet(PaymentMethodStrategy):
    def __init__(self, user_repository: UserRepository, user: User):
        super().__init__(user_repository, user)

    def pay(self, total: float):
        """
        Process the payment using the wallet method.
        This method should implement the logic for paying with a user's wallet.
        """
        if self._user.cash < total:
            raise ValueError("Insufficient wallet balance")

        self._user.cash -= total
        self._user_repository.save(self._user)