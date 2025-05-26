import os
import sqlite3


class DatabaseInitializer:
    @staticmethod
    def initialize_database(db_path='database.db'):
        """Verifica se o banco existe e o cria se necessário"""

        if os.path.exists(db_path):
            print(f"Banco de dados encontrado em {db_path}")
            return

        print(f"Criando novo banco de dados em {db_path}")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(current_dir, 'schema.sql')

        with open(schema_path, 'r') as f:
            sql_script = f.read()

        conn = sqlite3.connect(db_path)
        conn.executescript(sql_script)
        conn.commit()
        conn.close()

        print(f"Banco de dados inicializado com sucesso em {db_path}")