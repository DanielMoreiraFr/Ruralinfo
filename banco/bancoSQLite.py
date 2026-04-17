import sqlite3
from pacote.texto import cores

conexão = sqlite3.connect('banco/banco.db')
cursor = conexão.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS contasUsuarios (
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               nome TEXT NOT NULL,
               email TEXT NOT NULL,
               senha TEXT NOT NULL,
               tipoConta INTEGER NOT NULL
               )""")

def inserirUsuario(nome, email, senha, tipoC):
    try:
        # Usamos ? como placeholders e passamos os dados em uma tupla no segundo argumento
        cursor.execute("""
            INSERT INTO contasUsuarios (nome, email, senha, tipoConta) 
            VALUES (?, ?, ?, ?)
        """, (nome, email, senha, tipoC))
        
    except sqlite3.Error as erro:
        print(f'{cores("vermelho")}ERRO: {erro}{cores()}')
    else:
        try:    
            conexão.commit()
        except sqlite3.Error as erro:
            print(f'{cores('veremelho')}ERRO: {erro}{cores()}')
        else:
            print(f'{cores('verde')}Dados inseridos com sucesso!{cores()}')