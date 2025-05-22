import sqlite3
from typing import Optional
from threading import Lock
import threading


class DatabaseConfig:
    _instance: Optional['DatabaseConfig'] = None
    _lock: Lock = Lock()
    _local = threading.local()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseConfig, cls).__new__(cls)
                cls._instance._db_file = 'database.db'  # TODO alterar para usar do .env
            return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        """Obtém a conexão com o banco de dados específica para cada thread"""
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(self._db_file)
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection

    def close(self) -> None:
        """Fecha a conexão com o banco de dados para a thread atual"""
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            delattr(self._local, 'connection')