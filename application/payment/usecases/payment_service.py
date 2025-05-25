from application.payment.dtos.card_dto import CardDTO
from application.payment.interfaces.card_repository import CardRepository


class PaymentService:
    def __init__(self, repository: CardRepository):
        self._repository = repository

    def find_user_cards(self, user_id: int) -> list[CardDTO]:
        return [CardDTO(card) for card in self._repository.find_user_cards(user_id)]