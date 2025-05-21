from abc import ABC

from infrastructure.db.sqlite3.database_config import DatabaseConfig


class SqliteRepository(ABC):
    def __init__(self):
        self.db_config: DatabaseConfig = DatabaseConfig()

    def get_cursor(self):
        return self.db_config.get_connection().cursor()

    def commit(self):
        self.db_config.get_connection().commit()