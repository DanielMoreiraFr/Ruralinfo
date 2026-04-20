import sqlite3
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


query_criar_usuarios = """
CREATE TABLE IF NOT EXISTS contas_usuarios (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL,
    tipoConta INTEGER NOT NULL
)"""
with gerenciar_db() as cursor:
    cursor.execute(query_criar_usuarios)

def inserir_usuario(nome, email, senha, tipo_c):
    """
    Insere um novo registro de usuário na tabela 'contas_usuarios'.

    Args:
        nome (str): O nome completo do usuário.
        email (str): O endereço de e-mail do usuário.
        senha (str): A senha (preferencialmente já criptografada).
        tipo_c (int): O nível de acesso ou tipo da conta.
    """
    query = "INSERT INTO contas_usuarios (nome, email, senha, tipoConta) VALUES (?, ?, ?, ?)"
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
    query = "SELECT id, nome, email, tipoConta FROM contas_usuarios"
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
    query = "DELETE FROM contas_usuarios WHERE id = ?"
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
    query = f'UPDATE contas_usuarios SET {coluna} = ? WHERE id = ?'
    
    try:
        with gerenciar_db() as cursor:
            cursor.execute(query, (valor, id_usuario))
        print(f'Coluna "{coluna}" atualizada com sucesso para o ID {id_usuario}!')
    except sqlite3.Error as erro:
        print(f"Erro ao atualizar: {erro}")

def validação_login(email, senha, tipo_conta):
    query = f'SELECT * FROM contas_usuarios WHERE tipoConta = {tipo_conta}'
    
    usuario_encontrado = None 
    
    try:
        with gerenciar_db() as cursor:
            cursor.execute(query)
            contas = cursor.fetchall()

            for id_db, nome_db, email_db, senha_db, tipo_db in contas:
                if email_db == email and senha_db == senha:
                    usuario_encontrado = {
                        'id': id_db,
                        'nome': nome_db,
                        'tipo': tipo_db
                    }
                    break

        if usuario_encontrado:
            return [True, usuario_encontrado]
        else:
            return [False, False]

    except sqlite3.Error as erro:
        print(f"Erro: {erro}")
