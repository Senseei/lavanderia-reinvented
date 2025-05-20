from domain.unit import Unit


class UnitDTO:
    def __init__(self, unit: Unit):
        self.id = unit.id
        self.name = unit.name
        self.created_at = unit.created_at
        self.updated_at = unit.updated_at