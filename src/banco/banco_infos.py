import sqlite3
from datetime import datetime
from contextlib import *
from banco.banco_usuarios import gerenciar_db
try:
    from utils import texto
except ImportError:
    def cores(cor=None): return ""

DB_PATH = 'src/banco/banco.db'

# cria a tabela de infos, caso ela ainda não exista
def criar_table_criar_infos():
    """
    Cria a tabela 'infos' no banco de dados caso ela ainda não exista.
    
    A tabela contém colunas para ID (automático), mensagem, URL da imagem,
    texto alternativo, data de criação e o estado (ativo/inativo).
    """
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

# insere uma nova postagem na tabela de infos
def postagem(msg = '', img_url = '', alt = ''):
    """
    Insere uma nova postagem na tabela de informações.

    Args:
        msg (str): O conteúdo de texto da postagem.
        img_url (str): O link ou caminho para a imagem da postagem.
        alt (str): O texto alternativo para acessibilidade da imagem.
    """
    criar_table_criar_infos()

    query = 'INSERT INTO infos (mensagem, img_url, alt, data, estado) VALUES (?,?,?,?,?)'
    with gerenciar_db() as cursor:
        agora = datetime.now()
        cursor.execute(query, (msg, img_url, alt, agora, 1))

# atualiza o estado de uma postagem, com base no ID, para 0 ou 1 (inativa ou ativa)
def atualizar_posatagem(id_postagem, coluna = 'estado', estado_postagem = 0):
    """
    Atualiza um valor específico de uma postagem existente através do ID.

    Args:
        id_postagem (int): O identificador único da postagem.
        coluna (str): O nome da coluna a ser alterada (padrão é 'estado').
        estado_postagem (int/str): O novo valor para a coluna especificada.
    """
    criar_table_criar_infos()

    query = f'UPDATE infos SET {coluna} = ? WHERE id = ?'

    with gerenciar_db() as cursor:
        try:
            cursor.execute(query, (estado_postagem, id_postagem))
        except:
            print('ERRO ao tentar atualizar a coluna!')
        else:
            print(f'Coluna "{coluna}" atualizada com sucesso para o ID {id_postagem}!')

# deleta uma postagem da tabela, com base no ID
def apagar_postagem(id_postagem):
    """
    Remove permanentemente uma postagem do banco de dados.

    Args:
        id_postagem (int): O identificador único da postagem que será deletada.
    """
    criar_table_criar_infos()
    
    query = 'DELETE FROM infos WHERE id = ?'

    with gerenciar_db() as cursor:
        try:
            cursor.execute(query, (id_postagem, ))
        except:
            print('ERRO ao deletar linha da tabela')
        else:
            print('Linha deletada com sucesso!')

# exibe as postagens ativas (estado = 1) no terminal
def exibir_postagem():
    """
    Recupera todas as postagens do banco de dados e as exibe no terminal.
    
    Busca todas as colunas da tabela 'infos' e imprime os valores linha por linha.
    """
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