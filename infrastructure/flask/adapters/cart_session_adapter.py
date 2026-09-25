from flask import session

from application.machine.interfaces.cycle_repository import CycleRepository
from application.machine.interfaces.machine_repository import MachineRepository
from application.ticket.usecases.ticket_service import TicketService
from application.user.usecases.user_cart_session import UserCartSession
from di.decorators import component


@component
class CartSessionAdapter:
    def __init__(self, machine_repository: MachineRepository, cycle_repository: CycleRepository, ticket_service: TicketService):
        self._machine_repository = machine_repository
        self._cycle_repository = cycle_repository
        self._ticket_service = ticket_service

    def get_cart(self) -> UserCartSession:
        cart = UserCartSession(self._machine_repository, self._cycle_repository, self._ticket_service)

        if "cart_items" in session:
            cart.sync_items(session["cart_items"])

        if "discounts" in session:
            cart.sync_discounts(session["discounts"])

        if "applied_ticket" in session:
            cart.applied_ticket = session["applied_ticket"]

        return cart

    def save_cart(self, cart: UserCartSession) -> None:
        session["cart_items"] = [
            {
                "machine_id": item.machine.id,
                "cycle_id": item.cycle.id
            }
            for item in cart.get_items()
        ]

        session["discounts"] = cart.get_discounts()
        session["applied_ticket"] = cart.applied_ticket

    def clear_cart(self) -> None:
        session.pop("cart_items", None)
        session.pop("discounts", None)
        session.pop("applied_ticket", None)