from typing import Optional

from application.unit.interfaces.unit_repository import UnitRepository
from domain.unit import Unit
from infrastructure.db.sqlite3.repositories.sqlite_repository import SqliteRepository


class UnitRepositoryImpl(UnitRepository, SqliteRepository):
    def __init__(self):
        super().__init__()
        from infrastructure.db.sqlite3.repositories.machine_repository import MachineRepositoryImpl
        self._machine_repository = MachineRepositoryImpl()

    def save(self, entity: Unit) -> Unit:
        cursor = self.get_cursor()
        if not entity.id:
            cursor.execute("INSERT INTO units (local) VALUES (?)", entity.local)
            entity.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE units SET local = ? WHERE id = ?",
                (entity.local, entity.id)
            )

        # Save machines associated with the unit
        for machine in entity.machines:
            machine.unit_id = entity.id
            self._machine_repository.save(machine)

        self.commit()
        return entity

    def find_by_id(self, entity_id: int) -> Optional[Unit]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM units WHERE id = ?", (entity_id,))
        row = cursor.fetchone()
        if row:
            return Unit(
                id=row['id'],
                local=row['local'],
                machines=self._machine_repository.find_by_unit_id(entity_id)
            )
        return None

    def find_all(self) -> list[Unit]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM units")
        rows = cursor.fetchall()
        return [
            Unit(
                id=row['id'],
                local=row['local'],
                machines=self._machine_repository.find_by_unit_id(row['id'])
            ) for row in rows
        ]

    def delete(self, entity: Unit):
        self.delete_by_id(entity.id)

    def delete_by_id(self, entity_id: int):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM units WHERE id = ?", (entity_id,))

        # Also delete associated machines
        self._machine_repository.delete_by_unit_id(entity_id)

        self.commit()

    def find_by_local(self, name: str) -> Optional[Unit]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM units WHERE local = ?", (name,))
        row = cursor.fetchone()
        if row:
            return Unit(
                id=row['id'],
                local=row['local'],
                machines=self._machine_repository.find_by_unit_id(row['id'])
            )
        return None