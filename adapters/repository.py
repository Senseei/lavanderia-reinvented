from abc import ABC, abstractmethod

from domain.domain_entity import DomainEntity


class Repository(ABC):

    @abstractmethod
    def save(self, entity: DomainEntity) -> DomainEntity:
        """
        Save a domain entity to the repository.
        :param entity: The domain entity to save.
        :return: The saved domain entity.
        """
        pass

    @abstractmethod
    def find_by_id(self, entity_id: int) -> DomainEntity:
        """
        Find a domain entity by its ID.
        :param entity_id: The ID of the domain entity to find.
        :return: The domain entity with the specified ID, or None if not found.
        """
        pass

    @abstractmethod
    def find_all(self):
        """
        Find all domain entities in the repository.
        :return: A list of all domain entities.
        """
        pass

    @abstractmethod
    def delete(self, entity: DomainEntity):
        """
        Delete a domain entity from the repository.
        :param entity: The domain entity to delete.
        """
        pass

    @abstractmethod
    def delete_by_id(self, entity_id: int):
        """
        Delete a domain entity by its ID.
        :param entity_id: The ID of the domain entity to delete.
        """
        pass

    @abstractmethod
    def update(self, entity: DomainEntity) -> DomainEntity:
        """
        Update a domain entity in the repository.
        :param entity: The domain entity to update.
        :return: The updated domain entity.
        """
        pass