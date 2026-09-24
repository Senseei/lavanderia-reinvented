from application.payment.usecases.payment_service import PaymentService
from presentation.payment.dtos.card_dto import CardDTO
from presentation.payment.dtos.new_card_dto import NewCardDTO
from presentation.payment.dtos.payment_request_dto import PaymentRequestDTO


class PaymentWebService:
    def __init__(self, payment_service: PaymentService):
        self._payment_service = payment_service

    def find_user_cards(self, user_id: int) -> list[CardDTO]:
        return [CardDTO(card) for card in self._payment_service.find_user_cards(user_id)]

    def add_card(self, dto: NewCardDTO, owner_id: int) -> CardDTO:
        card = self._payment_service.add_card(
            owner_id=owner_id,
            titular=dto.titular,
            number=dto.number,
            method=dto.method,
            due_date=dto.due_date,
            cvv=dto.cvv
        )
        return CardDTO(card)

    def delete_card(self, card_id: str, owner_id: int) -> None:
        self._payment_service.delete_card(card_id, owner_id)

    def process_payment(self, request: PaymentRequestDTO) -> None:
        self._payment_service.process_payment(
            user_id=request.user_id,
            payment_method=request.method,
            card_id=request.card_id
        )
