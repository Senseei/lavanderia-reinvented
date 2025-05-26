from adapters.dtos.request_dto import RequestDTO
from adapters.dtos.response_dto import ResponseDTO
from adapters.payment.dtos.new_card_dto import NewCardDTO
from adapters.payment.dtos.payment_request_dto import PaymentRequestDTO
from application.payment.dtos.card_dto import CardDTO
from application.payment.usecases.payment_service import PaymentService
from infrastructure.flask.adapters.cart_session_adapter import CartSessionAdapter


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

    def add_card(self, request: RequestDTO, owner_id: int) -> ResponseDTO[CardDTO]:
        """
        Add a new card for a user.
        :param request:
        :param owner_id: The ID of the user who owns the card.
        :return: The added card data transfer object.
        """
        card_dto = NewCardDTO.from_dict(request.body)
        try:
            return ResponseDTO.success_response(self._service.add_card(card_dto, owner_id))
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
            self._service.delete_card(card_id, owner_id)
            return ResponseDTO.success_response(None)
        except Exception as e:
            return ResponseDTO.error_response(str(e))

    def process_payment(self, request: PaymentRequestDTO) -> ResponseDTO[None]:
        """
        Process a payment for a user's cart.
        :param request: The request containing payment details.
        :return: None
        """
        cart_session = CartSessionAdapter.get_cart()

        try:
            self._service.process_payment(
                user_id=request.user_id,
                cart=cart_session.get_items(),
                total=cart_session.get_total(),
                payment_method=request.method,
                card_id=request.card_id
            )
            return ResponseDTO.success_response(None)
        except Exception as e:
            return ResponseDTO.error_response(str(e))