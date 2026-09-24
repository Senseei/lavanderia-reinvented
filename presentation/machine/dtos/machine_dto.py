from domain.machine import Machine


class MachineDTO:
    def __init__(self, machine: Machine):
        self.id = machine.id
        self.type = machine.type.value
        self.unit_id = machine.unit_id
        self.locked = machine.locked
        self.identifier = machine.identifier

    def __eq__(self, other):
        if not isinstance(other, MachineDTO):
            return False
        return self.id == other.id