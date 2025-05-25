from adapters.payment.dtos.new_card_dto import NewCardDTO
from application.errors.entity_not_found_error import EntityNotFoundError
from application.payment.dtos.card_dto import CardDTO
from application.payment.interfaces.card_repository import CardRepository
from application.user.interfaces.user_repository import UserRepository
from domain.card import Card
from domain.enums.card_brand import CardBrand


class PaymentService:
    def __init__(self, repository: CardRepository, user_repository: UserRepository):
        self._repository = repository
        self._user_repository = user_repository

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

        print(card)

        return CardDTO(self._repository.save(card))

    def delete_card(self, card_id, owner_id):
        card = self._repository.find_by_id(card_id)
        if not card:
            raise EntityNotFoundError("Card")

        if card.user.id != owner_id:
            raise ValueError("User does not own this card")

        self._repository.delete(card)

    @classmethod
    def get_card_brand(cls, card_number: str) -> CardBrand:
        return CardBrand.VISA

    @classmethod
    def validate_card_number(cls, card_number: str) -> bool:
        # Implement Luhn algorithm or any other card number validation logic
        return True