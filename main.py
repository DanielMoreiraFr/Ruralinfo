from banco.bancoSQLite import *
from pacote.texto import *
from time import sleep

while True:
    escolha = menu('RURALINFO' ,['Login', 'Cadastrar', 'Entrar como visitante', 'Sair'])

    if escolha == 1:
        tipoLogin = menu('TIPO DE LOGIN', ['Usuário comum', 'Administrador'])
        if tipoLogin == 1:
            print('Entrando como usuário comum')
        elif tipoLogin == 2:
            print('Entrando como administrador')
        else:
            print(f'{cores('vermelho')}ERRO: Digite um número válido!{cores()}')   

    elif escolha == 2:
        cabeçalho('Cadastrar')

        nome = str(input(f'{cores('verde')}Nome: {cores()}'))
        email = str(input(f'{cores('verde')}Email: {cores()}'))
        senha = str(input(f'{cores('verde')}Senha: {cores()}'))
        tipoLogin = menu('TIPO DE CADASTRO', ['Usuário comum', 'Administrador'])

        inserir_usuario(nome, email, senha, tipoLogin)

    elif escolha == 3:
        cabeçalho('Entrando como visitante')
    elif escolha == 4 or escolha == 0:
        cabeçalho('Saindo...')
        break
    else:
        print(f'{cores('vermelho')}ERRO: Digite um número válido!{cores()}')
    sleep(1.5)