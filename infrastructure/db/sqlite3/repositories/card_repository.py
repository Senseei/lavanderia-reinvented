from datetime import datetime
from typing import Optional

from application.payment.interfaces.card_repository import CardRepository
from domain.payment.card import Card
from domain.payment.enums.card_brand import CardBrand
from domain.payment.enums.payment_method import PaymentMethod
from infrastructure.db.sqlite3.repositories.sqlite_repository import SqliteRepository
from infrastructure.db.sqlite3.repositories.user_repository import UserRepositoryImpl


class CardRepositoryImpl(CardRepository, SqliteRepository):
    def __init__(self):
        super().__init__()
        self.user_repository = UserRepositoryImpl()

    def save(self, entity: Card) -> Card:
        cursor = self.get_cursor()
        if not entity.id:
            cursor.execute(
                "INSERT INTO cards (user_id, titular, brand, number, method, due_date, cvv) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (entity.user.id, entity.titular, entity.brand.value, entity.number, entity.method.value, entity.due_date, entity.cvv)
            )
            entity.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE cards SET user_id = ?, titular = ?, brand = ?, number = ?, method = ?, due_date = ?, cvv = ? WHERE id = ?",
                (entity.user.id, entity.titular, entity.brand.value, entity.number, entity.method.value, entity.due_date, entity.cvv, entity.id)
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
                titular=row['titular'],
                user=self.user_repository.find_by_id(row['user_id']),
                brand=CardBrand(row['brand']),
                number=row['number'],
                method=PaymentMethod(row['method']),
                due_date=datetime.fromisoformat(row['due_date']),
                cvv=row['cvv']
            )
        return None

    def find_all(self) -> list[Card]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM cards")
        rows = cursor.fetchall()
        return [
            Card(
                id=row['id'],
                user=self.user_repository.find_by_id(row['user_id']),
                titular=row['titular'],
                brand=CardBrand(row['brand']),
                number=row['number'],
                method=PaymentMethod(row['method']),
                due_date=datetime.fromisoformat(row['due_date']),
                cvv=row['cvv']
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
                user=self.user_repository.find_by_id(row['user_id']),
                titular=row['titular'],
                brand=CardBrand(row['brand']),
                number=row['number'],
                method=PaymentMethod(row['method']),
                due_date=datetime.fromisoformat(row['due_date']),
                cvv=row['cvv']
            ) for row in rows
        ]