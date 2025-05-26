from adapters.payment.dtos.new_card_dto import NewCardDTO
from application.errors.entity_not_found_error import EntityNotFoundError
from application.machine.usecases.machine_service import MachineService
from application.payment.dtos.card_dto import CardDTO
from application.payment.interfaces.card_repository import CardRepository
from application.payment.usecases.strategy.credit_card import CreditCard
from application.payment.usecases.strategy.debit_card import DebitCard
from application.payment.usecases.strategy.wallet import Wallet
from application.user.dtos.session_cart_item import SessionCartItem
from application.user.interfaces.user_repository import UserRepository
from domain.payment.card import Card
from domain.payment.enums.card_brand import CardBrand
from domain.payment.enums.payment_method import PaymentMethod
from application.payment.usecases.strategy.payment_method_strategy import PaymentMethodStrategy
from domain.user import User


class PaymentService:
    def __init__(self, repository: CardRepository, user_repository: UserRepository, machine_service: MachineService):
        self._repository = repository
        self._user_repository = user_repository
        self._machine_service = machine_service

    def find_user_cards(self, user_id: int) -> list[CardDTO]:
        return [CardDTO(card) for card in self._repository.find_user_cards(user_id)]

    def add_card(self, dto: NewCardDTO, owner_id: int) -> CardDTO:
        if not self.validate_card_number(dto.number):
            raise ValueError("Invalid card number")

        user = self._user_repository.find_by_id(owner_id)
        if not user:
            raise ValueError("User not found")

        card = Card(
            user=user,
            brand=self.get_card_brand(dto.number),
            titular=dto.titular,
            number=dto.number,
            method=dto.method,
            due_date=dto.due_date,
            cvv=dto.cvv
        )
        return CardDTO(self._repository.save(card))

    def delete_card(self, card_id, owner_id):
        card = self._repository.find_by_id(card_id)
        if not card:
            raise EntityNotFoundError("Card")

        if card.user.id != owner_id:
            raise ValueError("User does not own this card")

        self._repository.delete(card)

    def process_payment(self, user_id: int, cart: list[SessionCartItem], total: float, payment_method: PaymentMethod, card_id: int=None):
        user = self._user_repository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundError("Usuário")

        strategy_creators = {
            PaymentMethod.CREDIT: lambda: self._create_card_strategy(CreditCard, user, self._repository.find_by_id(card_id)),
            PaymentMethod.DEBIT: lambda: self._create_card_strategy(DebitCard, user, self._repository.find_by_id(card_id)),
            PaymentMethod.WALLET: lambda: Wallet(self._user_repository, user),
        }

        if payment_method not in strategy_creators:
            raise ValueError("Método de pagamento não suportado")

        strategy = strategy_creators[payment_method]()

        self._purchase(strategy, cart, total)


    def _purchase(self, method: PaymentMethodStrategy, cart: list[SessionCartItem], total: float):
        machines_ids = [item.machine.id for item in cart]

        if self._machine_service.is_any_machine_in_list_busy(machines_ids):
            raise Exception("Uma ou mais máquinas estão ocupadas, tente novamente mais tarde, ou escolha outras máquinas.")

        method.pay(total)

        self._machine_service.lock_machines(cart)

    def _create_card_strategy(self, strategy_class, user: User, card: Card) -> PaymentMethodStrategy:
        if not card:
            raise ValueError("Cartão não encontrado")

        if card.user.id != user.id:
            raise ValueError("Este cartão não pertence ao usuário")

        return strategy_class(self._repository, user, card)

    @classmethod
    def get_card_brand(cls, card_number: str) -> CardBrand:
        return CardBrand.VISA

    @classmethod
    def validate_card_number(cls, card_number: str) -> bool:
        # Implement Luhn algorithm or any other card number validation logic
        return True
