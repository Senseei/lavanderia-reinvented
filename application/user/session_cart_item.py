from domain.cycle import Cycle
from domain.machine import Machine


class SessionCartItem:
    def __init__(self, machine: Machine, cycle: Cycle):
        self.machine = machine
        self.cycle = cycle

    def __eq__(self, other):
        return self.machine.id == other.machine.id and self.cycle.id == other.cycle.id
