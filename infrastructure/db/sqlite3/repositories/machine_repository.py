from typing import Optional

from application.machine.interfaces.machine_repository import MachineRepository
from domain.enums.machine_type import MachineType
from domain.machine import Machine
from infrastructure.db.sqlite3.repositories.sqlite_repository import SqliteRepository


class MachineRepositoryImpl(MachineRepository, SqliteRepository):
    def save(self, entity: Machine) -> Machine:
        cursor = self.get_cursor()
        if not entity.id:
            cursor.execute("INSERT INTO machines (unit_id, type) VALUES (?, ?)", (entity.unit_id, entity.type))
            entity.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE machines SET unit_id = ?, type = ? WHERE id = ?",
                (entity.unit_id, entity.type, entity.id)
            )
        self.commit()
        return entity

    def find_by_id(self, entity_id: int) -> Optional[Machine]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM machines WHERE id = ?", (entity_id,))
        row = cursor.fetchone()
        if row:
            return Machine(
                id=row['id'],
                identifier=row['identifier'],
                type=MachineType(row['type']),
                locked=row['locked'],
                unit_id=row['unit_id']
            )
        return None

    def find_all(self) -> list[Machine]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM machines")
        rows = cursor.fetchall()
        return [
            Machine(
                id=row['id'],
                identifier=row['identifier'],
                type=MachineType(row['type']),
                locked=row['locked'],
                unit_id=row['unit_id']
            ) for row in rows
        ]

    def delete(self, entity: Machine):
        self.delete_by_id(entity.id)

    def delete_by_id(self, entity_id: int):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM machines WHERE id = ?", (entity_id,))
        self.commit()

    def find_by_unit_id(self, unit_id: int) -> list[Machine]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM machines WHERE unit_id = ?", (unit_id,))
        rows = cursor.fetchall()
        return [
            Machine(
                id=row['id'],
                identifier=row['identifier'],
                type=MachineType(row['type']),
                locked=row['locked'],
                unit_id=row['unit_id']
            ) for row in rows
        ]

    def delete_by_unit_id(self, unit_id: int):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM machines WHERE unit_id = ?", (unit_id,))
        self.commit()