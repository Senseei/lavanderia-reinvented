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