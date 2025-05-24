from domain.machine import Machine


class MachineDTO:
    def __init__(self, machine: Machine):
        self.id = machine.id
        self.type = machine.type
        self.unit_id = machine.unit_id
        self.locked = machine.locked
        self.created_at = machine.created_at
        self.updated_at = machine.updated_at

    def __eq__(self, other):
        if not isinstance(other, MachineDTO):
            return False
        return self.id == other.id