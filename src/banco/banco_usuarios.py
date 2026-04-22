import sqlite3
from contextlib import contextmanager
from utils.texto import *
try:
    from utils.texto import *
except ImportError:
    def cores(cor=None): return ""

DB_PATH = 'src/banco/banco.db'

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

def criar_table_contas_usuarios():
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
    criar_table_contas_usuarios()

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
    criar_table_contas_usuarios()

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
    criar_table_contas_usuarios()

    query = "DELETE FROM contas_usuarios WHERE id = ?"
    try:
        with gerenciar_db() as cursor:
            cursor.execute(query, (id_usuario,))
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
    criar_table_contas_usuarios()

    query = f'UPDATE contas_usuarios SET {coluna} = ? WHERE id = ?'
    
    try:
        with gerenciar_db() as cursor:
            cursor.execute(query, (valor, id_usuario))
        print(f'Coluna "{coluna}" atualizada com sucesso para o ID {id_usuario}!')
    except sqlite3.Error as erro:
        print(f"Erro ao atualizar: {erro}")

def validação_login(email, senha, tipo_conta):
    """
    Verifica se as credenciais de login são válidas no banco de dados.

    A função filtra os usuários pelo tipo de conta diretamente na query SQL e, 
    em seguida, percorre os resultados para validar o e-mail e a senha.

    Args:
        email (str): O endereço de e-mail fornecido pelo usuário.
        senha (str): A senha fornecida pelo usuário.
        tipo_conta (int): O nível de acesso (ex: 1 para comum, 2 para administrador).

    Returns:
        list: Uma lista contendo dois elementos:
            - [0] (bool): True se o login for bem-sucedido, False caso contrário.
            - [1] (dict|bool): Dicionário com dados do usuário (id, nome, tipo) 
              em caso de sucesso, ou False em caso de falha.
    """
    criar_table_contas_usuarios()

    query = 'SELECT id, email, senha, tipoConta FROM contas_usuarios WHERE tipoConta = ?' # lembrar de usar placeholder '?' no lugar de fstring
    
    usuario_encontrado = None 
    
    try:
        with gerenciar_db() as cursor:
            cursor.execute(query, (tipo_conta,))
            contas = cursor.fetchall()

            for id_db, email_db, senha_db, tipo_db in contas:
                if email_db == email and senha_db == senha:
                    usuario_encontrado = {
                        'id': id_db,
                        'email': email_db,
                        'senha': senha_db,
                        'tipo': tipo_db
                    }
                    break

        if usuario_encontrado:
            return [True, usuario_encontrado]
        else:
            return [False, False]

    except sqlite3.Error as erro:
        print(f"Erro no banco de dados: {erro}")
        return [False, False]


# função para verificar se um usuário já existe no banco de dados
def usuario_existe(email, tipoC):
    criar_table_contas_usuarios()
    
    query = "SELECT email FROM contasUsuarios WHERE email = ? AND tipoConta = ?"
    with gerenciar_db() as cursor:
        try:
            cursor.execute(query, (email, tipoC))
            resultado = cursor.fetchone() # Tenta buscar uma linha
            return resultado is not None # Retorna True se achar algo, False se não
        except sqlite3.Error as erro:
            print(f'ERRO ao procurar usuário: {erro}')