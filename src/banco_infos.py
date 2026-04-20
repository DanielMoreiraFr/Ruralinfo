import sqlite3
from datetime import datetime
from contextlib import contextmanager
try:
    from texto import cores
except ImportError:
    def cores(cor=None): return ""

DB_PATH = 'src/banco.db'

@contextmanager
def gerenciar_db():
    """
    Gerenciador de contexto para operações no banco de dados SQLite.
    
    Abre uma conexão, cria um cursor e gerencia o ciclo de vida da transação.
    Realiza commit automaticamente se não houver erros ou rollback em caso de falha.
    Garante que a conexão seja fechada ao final da execução.

    Yields:
        sqlite3.Cursor: Um objeto cursor para execução de comandos SQL.

    Raises:
        sqlite3.Error: Propaga erros do banco de dados após o rollback.
    """
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    try:
        yield cursor
        conexao.commit()
    except sqlite3.Error as e:
        conexao.rollback()
        raise e
    finally:
        conexao.close()

query_criar_infos = """
CREATE TABLE IF NOT EXISTS infos (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    mensagem TEXT NOT NULL,
    img_url TEXT,
    alt TEXT,
    data DATETIME NOT NULL,
    estado INTEGER NOT NULL)"""


with gerenciar_db() as cursor:
    cursor.execute(query_criar_infos)
