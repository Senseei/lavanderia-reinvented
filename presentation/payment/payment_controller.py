from presentation.dtos.request_dto import RequestDTO
from presentation.dtos.response_dto import ResponseDTO
from presentation.payment.dtos.card_dto import CardDTO
from presentation.payment.dtos.new_card_dto import NewCardDTO
from presentation.payment.dtos.payment_request_dto import PaymentRequestDTO
from presentation.payment.payment_web_service import PaymentWebService

class PaymentController:
    def __init__(self, web_service: PaymentWebService):
        self._web_service = web_service

    def find_user_cards(self, user_id: int) -> ResponseDTO[list[CardDTO]]:
        """
        Find all cards for a given user.
        :param user_id: The ID of the user.
        :return: A list of cards associated with the user.
        """
        return ResponseDTO.success_response(self._web_service.find_user_cards(user_id))

    def add_card(self, request: RequestDTO, owner_id: int) -> ResponseDTO[CardDTO]:
        """
        Add a new card for a user.
        :param request:
        :param owner_id: The ID of the user who owns the card.
        :return: The added card data transfer object.
        """
        card_dto = NewCardDTO.from_dict(request.body)

        if not card_dto:
            return ResponseDTO.error_response("There are missing fields! Please, fill each one of them.")

        try:
            return ResponseDTO.success_response(self._web_service.add_card(card_dto, owner_id))
        except Exception as e:
            return ResponseDTO.error_response(str(e))

    def delete_card(self, card_id: str, owner_id: int) -> ResponseDTO[None]:
        """
        Delete a card for a user.
        :param card_id: The ID of the card to be deleted.
        :param owner_id: The ID of the user who owns the card.
        :return: None
        """
        try:
            self._web_service.delete_card(card_id, owner_id)
            return ResponseDTO.success_response(None)
        except Exception as e:
            return ResponseDTO.error_response(str(e))

    def process_payment(self, request: PaymentRequestDTO) -> ResponseDTO[None]:
        """
        Process a payment for a user's cart.
        :param request: The request containing payment details.
        :return: None
        """
        try:
            self._web_service.process_payment(request)
            return ResponseDTO.success_response(None)
        except Exception as e:
            return ResponseDTO.error_response(str(e))