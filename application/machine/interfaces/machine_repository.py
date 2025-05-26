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

    @abstractmethod
    def is_any_machine_in_list_busy(self, machines: list[int]) -> bool:
        """
        Check if any machine in the list is busy.
        :param machines: A list of machine ids.
        :return: True if any machine is busy, False otherwise.
        """
        pass

    @abstractmethod
    def lock_machines(self, machines: list[int]) -> None:
        """
        Lock the machines with the given ids.
        :param machines: A list of machine ids to lock.
        """
        pass