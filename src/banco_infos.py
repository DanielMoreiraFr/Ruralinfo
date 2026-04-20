import sqlite3
from datetime import datetime
from contextlib import *
from banco_usuarios import gerenciar_db
try:
    from texto import cores
except ImportError:
    def cores(cor=None): return ""

DB_PATH = 'src/banco.db'

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
