import sqlite3
from datetime import datetime
from contextlib import *
from banco.banco_usuarios import gerenciar_db
try:
    from utils import texto
except ImportError:
    def cores(cor=None): return ""

DB_PATH = 'src/banco/banco.db'

def criar_table_criar_infos():
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

def postagem(msg = '', img_url = '', alt = ''):
    criar_table_criar_infos()

    query = 'INSERT INTO infos (mensagem, img_url, alt, data, estado) VALUES (?,?,?,?,?)'
    with gerenciar_db() as cursor:
        agora = datetime.now()
        cursor.execute(query, (msg, img_url, alt, agora, 1))



def atualizar_posatagem(id_postagem, coluna = 'estado', estado_postagem = 0):
    criar_table_criar_infos()

    query = f'UPDATE infos SET {coluna} = ? WHERE id = ?'

    with gerenciar_db() as cursor:
        try:
            cursor.execute(query, (estado_postagem, id_postagem))
        except:
            print('ERRO ao tentar atualizar a coluna!')
        else:
            print(f'Coluna "{coluna}" atualizada com sucesso para o ID {id_postagem}!')


def apagar_postagem(id_postagem):
    criar_table_criar_infos()
    
    query = 'DELETE FROM infos WHERE id = ?'

    with gerenciar_db() as cursor:
        try:
            cursor.execute(query, (id_postagem, ))
        except:
            print('ERRO ao deletar linha da tabela')
        else:
            print('Linha deletada com sucesso!')

def exibir_postagem():
    criar_table_criar_infos()

    query = 'SELECT * from infos'
    try:
        with gerenciar_db() as cursor:
            cursor.execute(query)
            informacoes = cursor.fetchall()

            for msg, img, alt, data, estado in informacoes:
                print(msg, img, alt, data, estado)
    except sqlite3.Error as erro:
        print(f'ERRO: {erro}')
        

