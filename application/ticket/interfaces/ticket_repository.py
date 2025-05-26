from abc import ABC, abstractmethod
from typing import Optional

from adapters.repository import Repository
from domain.ticket import Ticket


class TicketRepository(Repository[Ticket], ABC):
    @abstractmethod
    def find_by_code(self, code: str) -> Optional[Ticket]:
        """
        Find a ticket by its code.

        :param code: The code of the ticket to find.
        :return: The found ticket.
        """
        pass

    @abstractmethod
    def delete_by_code(self, code: str):
        """
        Delete a ticket by its code.

        :param code: The code of the ticket to delete.
        """
        pass

    @abstractmethod
    def can_user_use_ticket(self, user_id: int, ticket_id: int) -> bool:
        """
        Check if a user can use a ticket.

        :param ticket_id: The ID of the ticket.
        :param user_id: The ID of the user.
        :return: True if the user can use the ticket, False otherwise.
        """
        pass

    @abstractmethod
    def use_ticket(self, user_id: int, ticket_id: int) -> None:
        """
        Mark a ticket as used by a user.

        :param user_id: The ID of the user using the ticket.
        :param ticket_id: The ID of the ticket to use.
        :return: The updated Ticket object.
        """
        pass