from application.errors.entity_not_found_error import EntityNotFoundError
from application.errors.ticket_already_used_error import TicketAlreadyUsedError
from application.errors.ticket_expired_error import TicketExpiredError
from application.ticket.interfaces.ticket_repository import TicketRepository
from domain.ticket import Ticket


class TicketService:
    def __init__(self, repository: TicketRepository):
        self._repository = repository

    def find_by_code(self, code: str) -> Ticket:
        """
        Retrieves a ticket by its code.

        :param code: The code of the ticket to retrieve.
        :return: The Ticket object if found, otherwise None.
        """
        ticket = self._repository.find_by_code(code)
        if not ticket:
            raise EntityNotFoundError(entity_name="Ticket", message="Código de ticket inválido!")
        return ticket

    def can_user_use_ticket(self, user_id: int, ticket_id: int) -> bool:
        return self._repository.can_user_use_ticket(user_id, ticket_id)

    def apply_ticket(self, ticket_code: str, user_id: int, value: float) -> float:
        """
        Marks a ticket as used by a user.

        :param value: The value to apply from the ticket.
        :param ticket_code: The code of the ticket to use.
        :param user_id: The ID of the user using the ticket.
        :return: The value applied from the ticket.
        """
        ticket = self.find_by_code(ticket_code)
        if not self.can_user_use_ticket(user_id, ticket.id):
            raise TicketAlreadyUsedError()

        if ticket.has_expired():
            raise TicketExpiredError()

        return ticket.apply(value)

    def mark_ticket_as_used(self, ticket_code: str, user_id: int):
        """
        Marks a ticket as used by a user.

        :param ticket_code: The code of the ticket to mark as used.
        :param user_id: The ID of the user using the ticket.
        """
        ticket = self.find_by_code(ticket_code)
        self._repository.use_ticket(ticket.id, user_id)

