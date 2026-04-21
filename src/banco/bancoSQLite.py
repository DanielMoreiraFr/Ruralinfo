import sqlite3
import os
from pacote import texto

# 1. Descobre o caminho da pasta onde o bancoSQLite.py está (a pasta 'banco')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Une esse caminho ao nome do arquivo .db
# Isso garante que o banco sempre fique na mesma pasta do script de banco
db_path = os.path.join(BASE_DIR, 'banco.db')

# 3. Conecta usando o caminho completo
conexão = sqlite3.connect(db_path)
cursor = conexão.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS contasUsuarios (
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               nome TEXT NOT NULL,
               email TEXT NOT NULL,
               senha TEXT NOT NULL,
               tipoConta INTEGER NOT NULL
               )""")

# função para verificar se um usuário já existe no banco de dados
def usuarioExiste(email, tipoC):
    cursor.execute("SELECT email FROM contasUsuarios WHERE email = ? AND tipoConta = ?", (email, tipoC))
    resultado = cursor.fetchone() # Tenta buscar uma linha
    return resultado is not None # Retorna True se achar algo, False se não

# função para inserir um novo usuário no banco de dados
def inserirUsuario(nome, email, senha, tipoC):
    try:
        # Usamos ? como placeholders e passamos os dados em uma tupla no segundo argumento
        cursor.execute("""
            INSERT INTO contasUsuarios (nome, email, senha, tipoConta) 
            VALUES (?, ?, ?, ?)
        """, (nome, email, senha, tipoC))
        
    except sqlite3.Error as erro:
        print(f'{texto.cores("vermelho")}ERRO: {erro}{texto.cores()}')
    else:
        try:    
            conexão.commit()
        except sqlite3.Error as erro:
            print(f'{texto.cores('veremelho')}ERRO: {erro}{texto.cores()}')
        else:
            print(f'{texto.cores('verde')}Dados inseridos com sucesso!{texto.cores()}')