from flask import session

from application.user.usecases.user_cart_session import UserCartSession
from infrastructure.db.sqlite3.repositories.cycle_repository import CycleRepositoryImpl
from infrastructure.db.sqlite3.repositories.machine_repository import MachineRepositoryImpl
from infrastructure.db.sqlite3.repositories.ticket_repository import TicketRepositoryImpl


class CartSessionAdapter:
    @staticmethod
    def get_cart() -> UserCartSession:
        """Recupera ou cria um novo carrinho baseado na sessão atual"""
        machine_repository = MachineRepositoryImpl()
        cycle_repository = CycleRepositoryImpl()
        ticket_repository = TicketRepositoryImpl()

        cart = UserCartSession(machine_repository, cycle_repository, ticket_repository)

        if "cart_items" in session:
            for item_data in session["cart_items"]:
                cart.add_item(item_data["machine_id"], item_data["cycle_id"])

        if "discounts" in session:
            cart._discounts = session["discounts"]

        return cart

    @staticmethod
    def save_cart(cart: UserCartSession) -> None:
        """Salva o estado do carrinho na sessão"""
        session["cart_items"] = [
            {
                "machine_id": item.machine.id,
                "cycle_id": item.cycle.id
            }
            for item in cart.get_items()
        ]

        session["discounts"] = cart.get_discounts()