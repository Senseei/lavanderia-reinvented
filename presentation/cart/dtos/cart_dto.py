from application.user.usecases.user_cart_session import UserCartSession
from application.util.currency import br
from presentation.cart.dtos.cart_item_dto import CartItemDTO


class CartDTO:
    def __init__(self, cart: UserCartSession):
        self.items = [CartItemDTO(item) for item in cart.get_items()]
        self.total = cart.get_total()
        self.discounts = cart.get_discounts()
        self.total_with_discounts = cart.get_total_with_discounts()

    def get_formatted_total(self) -> str:
        return br(self.total)

    def get_formatted_discounts(self) -> str:
        return br(self.discounts)

    def get_formatted_total_with_discounts(self) -> str:
        return br(self.total_with_discounts)
