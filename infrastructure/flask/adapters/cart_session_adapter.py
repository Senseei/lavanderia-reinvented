from flask import session, has_request_context

from application.ticket.usecases.ticket_service import TicketService
from application.user.usecases.user_cart_session import UserCartSession
from infrastructure.db.sqlite3.repositories.cycle_repository import CycleRepositoryImpl
from infrastructure.db.sqlite3.repositories.machine_repository import MachineRepositoryImpl
from infrastructure.db.sqlite3.repositories.ticket_repository import TicketRepositoryImpl


class CartSessionAdapter:
    @staticmethod
    def get_cart() -> UserCartSession:
        machine_repository = MachineRepositoryImpl()
        cycle_repository = CycleRepositoryImpl()
        ticket_repository = TicketRepositoryImpl()
        ticket_service = TicketService(ticket_repository)

        cart = UserCartSession.get_instance(machine_repository, cycle_repository, ticket_service)

        if has_request_context():
            if "cart_items" in session:
                cart.sync_items(session["cart_items"])

            if "discounts" in session:
                cart.sync_discounts(session["discounts"])

            if "applied_ticket" in session:
                cart.applied_ticket = session["applied_ticket"]

        return cart

    @staticmethod
    def save_cart(cart: UserCartSession) -> None:
        if has_request_context():
            session["cart_items"] = [
                {
                    "machine_id": item.machine.id,
                    "cycle_id": item.cycle.id
                }
                for item in cart.get_items()
            ]

            session["discounts"] = cart.get_discounts()
            session["applied_ticket"] = cart.applied_ticket

    @staticmethod
    def clear_cart() -> None:
        if has_request_context():
            if "cart_items" in session:
                session.pop("cart_items")
            if "discounts" in session:
                session.pop("discounts")
            if "applied_ticket" in session:
                session.pop("applied_ticket")

        UserCartSession.reset_instance()