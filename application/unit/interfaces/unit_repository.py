from abc import ABC, abstractmethod

from adapters.repository import Repository, T
from domain.unit import Unit


class UnitRepository(Repository[Unit], ABC):
    """
    UnitRepository is an abstract base class that defines the interface for unit-related data access operations.
    It extends the Repository class, which provides a generic interface for data access.
    """

    @abstractmethod
    def find_by_name(self, name: str) -> Unit:
        """
        Find a unit by name.
        :param name: The name of the unit to find.
        :return: The unit with the specified name, or None if not found.
        """
        pass