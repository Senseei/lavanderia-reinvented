from domain_entity import DomainEntity
from user import User
from machine import Machine
from cycle import Cycle


class History(DomainEntity):
    def __init__(self, id: int, user: User, machine: Machine, cycle: Cycle):
        super().__init__(id)
        self.user = user
        self.machine = machine
        self.cycle = cycle