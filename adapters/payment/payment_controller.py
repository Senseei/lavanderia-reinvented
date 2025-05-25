from adapters.dtos.response_dto import ResponseDTO
from application.payment.dtos.card_dto import CardDTO
from application.payment.usecases.payment_service import PaymentService


class PaymentControllerAdapter:
    def __init__(self, service: PaymentService):
        self._service = service

    def find_user_cards(self, user_id: int) -> ResponseDTO[list[CardDTO]]:
        """
        Find all cards for a given user.
        :param user_id: The ID of the user.
        :return: A list of cards associated with the user.
        """
        return ResponseDTO.success_response(self._service.find_user_cards(user_id))