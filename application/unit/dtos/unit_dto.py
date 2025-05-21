from domain.unit import Unit


class UnitDTO:
    def __init__(self, unit: Unit):
        self.id = unit.id
        self.local = unit.local
        self.created_at = unit.created_at
        self.updated_at = unit.updated_at