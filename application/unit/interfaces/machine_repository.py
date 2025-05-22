from abc import ABC, abstractmethod

from adapters.repository import Repository
from domain.machine import Machine


class MachineRepository(Repository[Machine], ABC):

    @abstractmethod
    def find_by_unit_id(self, unit_id: int) -> list[Machine]:
        """
        Find all machines by unit id.
        :param unit_id: The id of the unit.
        :return: A list of machines.
        """
        pass

    @abstractmethod
    def delete_by_unit_id(self, unit_id: int):
        """
        Delete all machines by unit id.
        :param unit_id: The id of the unit.
        """
        pass