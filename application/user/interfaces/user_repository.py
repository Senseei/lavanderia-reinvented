from abc import ABC, abstractmethod
from typing import Optional

from adapters.repository import Repository
from domain.user import User


class UserRepository(Repository[User], ABC):
    """
    UserRepository is an abstract base class that defines the interface for user-related data access operations.
    It extends the Repository class, which provides a generic interface for data access.
    """

    @abstractmethod
    def find_by_username_and_password(self, username: str, password: str) -> Optional[User]:
        """
        Find a user by username and password.
        :param username: The username of the user to find.
        :param password: The password of the user to find.
        :return: The user with the specified username and password, or None if not found.
        """
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        """
        Find a user by username.
        :param username: The username of the user to find.
        :return: The user with the specified username, or None if not found.
        """
        pass