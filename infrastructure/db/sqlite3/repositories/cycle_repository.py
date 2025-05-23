from typing import Optional

from adapters.repository import T
from application.machine.interfaces.cycle_repository import CycleRepository
from domain.cycle import Cycle
from infrastructure.db.sqlite3.repositories.sqlite_repository import SqliteRepository


class CycleRepositoryImpl(CycleRepository, SqliteRepository):
    def save(self, entity: Cycle) -> Cycle:
        cursor = self.get_cursor()
        if not entity.id:
            cursor.execute("INSERT INTO cycles (time, price) VALUES (?, ?)", (entity.time, entity.price))
            entity.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE cycles SET time = ?, price = ? WHERE id = ?",
                (entity.time, entity.price, entity.id)
            )
        self.commit()
        return entity

    def find_by_id(self, entity_id: int) -> Optional[Cycle]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM cycles WHERE id = ?", (entity_id,))
        row = cursor.fetchone()
        if row:
            return Cycle(
                id=row['id'],
                price=row['price'],
                time=row['time']
            )
        return None

    def find_all(self) -> list[Cycle]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM cycles")
        rows = cursor.fetchall()
        return [
            Cycle(
                id=row['id'],
                price=row['price'],
                time=row['time']
            ) for row in rows
        ]

    def delete(self, entity: T):
        self.delete_by_id(entity.id)

    def delete_by_id(self, entity_id: int):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM cycles WHERE id = ?", (entity_id,))
        self.commit()