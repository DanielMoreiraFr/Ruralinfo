import sqlite3
from contextlib import contextmanager
try:
    from pacote.texto import cores
except ImportError:
    def cores(cor=None): return ""

DB_PATH = 'banco/banco.db'

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

def criar_db():
    """
    Cria a tabela 'contasUsuarios' caso ela não exista no banco de dados.
    
    A tabela contém os campos: id (PK), nome, email, senha e tipoConta.
    """
    query = """
    CREATE TABLE IF NOT EXISTS contasUsuarios (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL,
        tipoConta INTEGER NOT NULL
    )"""
    with gerenciar_db() as cursor:
        cursor.execute(query)

def inserir_usuario(nome, email, senha, tipo_c):
    """
    Insere um novo registro de usuário na tabela 'contasUsuarios'.

    Args:
        nome (str): O nome completo do usuário.
        email (str): O endereço de e-mail do usuário.
        senha (str): A senha (preferencialmente já criptografada).
        tipo_c (int): O nível de acesso ou tipo da conta.
    """
    query = "INSERT INTO contasUsuarios (nome, email, senha, tipoConta) VALUES (?, ?, ?, ?)"
    try:
        with gerenciar_db() as cursor:
            cursor.execute(query, (nome, email, senha, tipo_c))
        print(f'{cores("verde")}Dados inseridos com sucesso!{cores()}')
    except sqlite3.Error as erro:
        print(f'{cores("vermelho")}ERRO ao inserir: {erro}{cores()}')

def obter_dados():
    """
    Recupera e exibe no terminal todos os usuários cadastrados.
    
    Lista ID, Nome, Email e Tipo de Conta. A senha é omitida por segurança.
    """
    query = "SELECT id, nome, email, tipoConta FROM contasUsuarios"
    try:
        with gerenciar_db() as cursor:
            cursor.execute(query)
            contas = cursor.fetchall()
            
            for id, nome, email, tipo in contas:
                print(f"ID: {id} | Nome: {nome} | Email: {email} | Tipo: {tipo}")
    except sqlite3.Error as erro:
        print(f"Erro ao buscar dados: {erro}")

def deletar_usuario(id_usuario):
    """
    Remove um usuário permanentemente do banco de dados através do ID.

    Args:
        id_usuario (int): O identificador único do usuário a ser removido.
    """
    query = "DELETE FROM contasUsuarios WHERE id = ?"
    try:
        with gerenciar_db() as cursor:
            cursor.execute(query, (id_usuario))
        print(f'Usuário {id_usuario} deletado com sucesso')
    except sqlite3.Error as erro:
        print(f"Erro ao deletar: {erro}")

def atualizar_usuario(coluna, valor, id_usuario):
    """
    Atualiza um campo específico de um usuário baseado no ID.

    Args:
        coluna (str): O nome da coluna a ser alterada (ex: 'nome', 'senha').
        valor (any): O novo valor a ser inserido no campo.
        id_usuario (int): O ID do usuário que sofrerá a alteração.
    """
    query = f'UPDATE contasUsuarios SET {coluna} = ? WHERE id = ?'
    
    try:
        with gerenciar_db() as cursor:
            cursor.execute(query, (valor, id_usuario))
        print(f'Coluna "{coluna}" atualizada com sucesso para o ID {id_usuario}!')
    except sqlite3.Error as erro:
        print(f"Erro ao atualizar: {erro}")