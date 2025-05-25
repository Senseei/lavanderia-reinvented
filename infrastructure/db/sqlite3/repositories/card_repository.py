from datetime import datetime
from typing import Optional

from application.payment.interfaces.card_repository import CardRepository
from domain.card import Card
from infrastructure.db.sqlite3.repositories.sqlite_repository import SqliteRepository


class CardRepositoryImpl(CardRepository, SqliteRepository):
    def save(self, entity: Card) -> Card:
        cursor = self.get_cursor()
        if not entity.id:
            cursor.execute(
                "INSERT INTO cards (user_id, brand, number, method, due_date, cv) VALUES (?, ?, ?, ?, ?, ?)",
                (entity.user.id, entity.brand.value, entity.number, entity.method.value, entity.due_date, entity.cv)
            )
            entity.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE cards SET user_id = ?, brand = ?, number = ?, method = ?, due_date = ?, cv = ? WHERE id = ?",
                (entity.user.id, entity.brand.value, entity.number, entity.method.value, entity.due_date, entity.cv, entity.id)
            )
        self.commit()
        return entity

    def find_by_id(self, entity_id: int) -> Optional[Card]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM cards WHERE id = ?", (entity_id,))
        row = cursor.fetchone()
        if row:
            return Card(
                id=row['id'],
                user=row['user_id'],
                brand=row['brand'],
                number=row['number'],
                method=row['method'],
                due_date=datetime.fromisoformat(row['due_date']),
                cv=row['cv']
            )
        return None

    def find_all(self) -> list[Card]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM cards")
        rows = cursor.fetchall()
        return [
            Card(
                id=row['id'],
                user=row['user_id'],
                brand=row['brand'],
                number=row['number'],
                method=row['method'],
                due_date=datetime.fromisoformat(row['due_date']),
                cv=row['cv']
            ) for row in rows
        ]

    def delete(self, entity: Card):
        self.delete_by_id(entity.id)

    def delete_by_id(self, entity_id: int):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM cards WHERE id = ?", (entity_id,))
        self.commit()

    def find_user_cards(self, user_id: int):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM cards WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        return [
            Card(
                id=row['id'],
                user=row['user_id'],
                brand=row['brand'],
                number=row['number'],
                method=row['method'],
                due_date=datetime.fromisoformat(row['due_date']),
                cv=row['cv']
            ) for row in rows
        ]