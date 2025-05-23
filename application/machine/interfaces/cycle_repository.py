from abc import ABC

from adapters.repository import Repository


class CycleRepository(Repository, ABC):
    """
    Interface for Cycle repository.
    """