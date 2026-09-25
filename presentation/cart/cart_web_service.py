from application.user.usecases.user_cart_session import UserCartSession
from presentation.cart.dtos.cart_dto import CartDTO
from di.decorators import component


@component
class CartWebService:
    def get_cart(self, cart: UserCartSession) -> CartDTO:
        return CartDTO(cart)
