from abc import ABC, abstractmethod

from application.user.interfaces.user_repository import UserRepository
from domain.user import User


class PaymentMethodStrategy(ABC):
    def __init__(self, user_repository: UserRepository, user: User):
        self._user_repository = user_repository
        self._user = user

    @abstractmethod
    def pay(self, total: float):
        """
        Process the payment using the specific payment method strategy.
        This method should be implemented by subclasses to handle the payment logic.
        """
        pass