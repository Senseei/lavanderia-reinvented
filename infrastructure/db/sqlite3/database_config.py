import sqlite3
from typing import Optional
from threading import Lock


class DatabaseConfig:
    _instance: Optional['DatabaseConfig'] = None
    _lock: Lock = Lock()
    _connection: Optional[sqlite3.Connection] = None

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseConfig, cls).__new__(cls)
                cls._instance._connection = None
                cls._instance._db_file = 'database.db' # TODO alterar para usar do .env
            return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        """Obtém a conexão com o banco de dados"""
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_file)
            # Para retornar resultados como dicionários
            self._connection.row_factory = sqlite3.Row
        return self._connection

    def close(self) -> None:
        """Fecha a conexão com o banco de dados"""
        if self._connection:
            self._connection.close()
            self._connection = None