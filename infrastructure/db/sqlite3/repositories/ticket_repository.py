from datetime import datetime
from typing import Optional

from application.ticket.interfaces.ticket_repository import TicketRepository
from application.util.dates import parse_datetime
from domain.enums.discount_type import DiscountType
from domain.ticket import Ticket
from infrastructure.db.sqlite3.repositories.sqlite_repository import SqliteRepository


class TicketRepositoryImpl(TicketRepository, SqliteRepository):
    def save(self, entity: Ticket) -> Ticket:
        cursor = self.get_cursor()
        if not entity.id:
            cursor.execute("INSERT INTO tickets (type, discount, code, expires_at) VALUES (?, ?, ?, ?)",
                           (entity.type.value, entity.discount, entity.code, int(entity.expires_at.timestamp())))
            entity.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE tickets SET type = ?, discount = ?, code = ?, expires_at = ? WHERE id = ?",
                (entity.type.value, entity.discount, entity.code, int(entity.expires_at.timestamp()), entity.id)
            )
        self.commit()
        return entity

    def find_by_id(self, entity_id: int) -> Optional[Ticket]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM tickets WHERE id = ?", (entity_id,))
        row = cursor.fetchone()
        if row:
            return Ticket(
                id=row['id'],
                type=DiscountType(row['type']),
                discount=row['discount'],
                code=row['code'],
                expires_at= parse_datetime(row['expires_at'])
            )
        return None

    def find_all(self) -> list[Ticket]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM tickets")
        rows = cursor.fetchall()
        return [
            Ticket(
                id=row['id'],
                type=DiscountType(row['type']),
                discount=row['discount'],
                code=row['code'],
                expires_at=parse_datetime(row['expires_at'])
            ) for row in rows
        ]

    def delete(self, entity: Ticket):
        self.delete_by_id(entity.id)

    def delete_by_id(self, entity_id: int):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM tickets WHERE id = ?", (entity_id,))
        self.commit()

    def find_by_code(self, code: str) -> Optional[Ticket]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM tickets WHERE code = ?", (code,))
        row = cursor.fetchone()
        if row:
            return Ticket(
                id=row['id'],
                type=DiscountType(row['type']),
                discount=row['discount'],
                code=row['code'],
                expires_at=parse_datetime(row['expires_at'])
            )
        return None

    def delete_by_code(self, code: str):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM tickets WHERE code = ?", (code,))
        self.commit()

    def can_user_use_ticket(self, user_id: int, ticket_id: int) -> bool:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM used_tickets WHERE ticket_id = ? and user_id = ?", (ticket_id, user_id))
        row = cursor.fetchone()
        return row is None

    def use_ticket(self, user_id: int, ticket_id: int) -> None:
        cursor = self.get_cursor()
        cursor.execute("INSERT INTO used_tickets (user_id, ticket_id) VALUES (?, ?)", (user_id, ticket_id))
        self.commit()