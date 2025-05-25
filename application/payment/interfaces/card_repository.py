from abc import ABC, abstractmethod

from adapters.repository import Repository


class CardRepository(Repository, ABC):
    """
    Interface for the Card repository.
    """

    @abstractmethod
    def find_user_cards(self, user_id: int):
        """
        Find all cards for a given user.
        :param user_id: The ID of the user.
        :return: A list of cards associated with the user.
        """
        pass