from typing import Optional

from application.unit.interfaces.unit_repository import UnitRepository
from domain.unit import Unit
from infrastructure.db.sqlite3.repositories.sqlite_repository import SqliteRepository


class UnitRepositoryImpl(UnitRepository, SqliteRepository):

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
        self.commit()
        return entity

    def find_by_id(self, entity_id: int) -> Optional[Unit]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM units WHERE id = ?", (entity_id,))
        row = cursor.fetchone()
        if row:
            return Unit(
                id=row['id'],
                local=row['local']
            )
        return None

    def find_all(self) -> list[Unit]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM units")
        rows = cursor.fetchall()
        return [
            Unit(
                id=row['id'],
                local=row['local']
            ) for row in rows
        ]

    def delete(self, entity: Unit):
        self.delete_by_id(entity.id)

    def delete_by_id(self, entity_id: int):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM units WHERE id = ?", (entity_id,))
        self.commit()

    def find_by_local(self, name: str) -> Optional[Unit]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM units WHERE local = ?", (name,))
        row = cursor.fetchone()
        if row:
            return Unit(
                id=row['id'],
                local=row['local']
            )
        return None