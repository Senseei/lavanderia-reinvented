from typing import Optional

from application.user.interfaces.user_repository import UserRepository
from domain.user import User
from infrastructure.db.sqlite3.repositories.sqlite_repository import SqliteRepository


class UserRepositoryImpl(UserRepository, SqliteRepository):

    def save(self, entity: User) -> User:
        cursor = self.get_cursor()

        if entity.id is None:
            cursor.execute(
                "INSERT INTO users (username, name, password, cash) VALUES (?, ?, ?, ?)",
                (entity.username, entity.name, entity.password, entity.cash)
            )
            entity.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE users SET username = ?, name = ?, password = ?, cash = ? WHERE id = ?",
                (entity.username, entity.name, entity.password, entity.cash, entity.id)
            )
        self.commit()
        return entity


    def find_by_id(self, entity_id: int) -> Optional[User]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (entity_id,))
        row = cursor.fetchone()
        if row:
            return User(
                id=row['id'],
                username=row['username'],
                name=row['name'],
                password=row['password'],
                cash=row['cash']
            )
        return None

    def find_all(self) -> list[User]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return [
            User(
                id=row['id'],
                username=row['username'],
                name=row['name'],
                password=row['password'],
                cash=row['cash']
            ) for row in rows
        ]

    def delete(self, entity: User):
        self.delete_by_id(entity.id)

    def delete_by_id(self, entity_id: int):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (entity_id,))
        self.commit()

    def find_by_username_and_password(self, username: str, password: str) -> Optional[User]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        row = cursor.fetchone()
        if row:
            return User(
                id=row['id'],
                username=row['username'],
                name=row['name'],
                password=row['password'],
                cash=row['cash']
            )
        return None

    def find_by_username(self, username: str) -> Optional[User]:
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            return User(
                id=row['id'],
                username=row['username'],
                name=row['name'],
                password=row['password'],
                cash=row['cash']
            )
        return None
