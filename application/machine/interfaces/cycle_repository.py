from abc import ABC

from application.repository import Repository
from domain.cycle import Cycle


class CycleRepository(Repository[Cycle], ABC):
    """
    Interface for Cycle repository.
    """