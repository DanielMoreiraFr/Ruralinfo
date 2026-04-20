from src.banco_usuarios import *
from src.banco_infos import *
from src.texto import *
from time import sleep

while True:
    escolha = menu('RURALINFO' ,['Login', 'Cadastrar', 'Entrar como visitante', 'Sair'])

    if escolha == 1: #LOGIN
        while True:
            tipoLogin = menu('TIPO DE LOGIN', ['Usuário comum', 'Administrador'])
            if tipoLogin == 1:
                print('Entrando como usuário comum...')
                break
            elif tipoLogin == 2:
                print('Entrando como administrador...')
                break
            else:
                print(f'{cores('vermelho')}ERRO: Digite um número válido!{cores()}')
                sleep(1)   

        email = str(input(f'{cores('verde')}Email: {cores()}'))
        senha = str(input(f'{cores('verde')}Senha: {cores()}'))
        valid, objeto = validação_login(email, senha, tipoLogin)

        if valid:
            print(f"Bem-vindo, {objeto['nome']} (ID: {objeto['id']})")
            # postagem('mensagem de teste 1', None, None)
        else:
            print(f'{cores('vermelho')}ERRO: Email não encontrado, senha incorreta ou tipo de conta errado!{cores()}')

    elif escolha == 2: #CADASTRO    
        cabeçalho('Cadastrar')  

        nome = str(input(f'{cores('verde')}Nome: {cores()}'))
        email = str(input(f'{cores('verde')}Email: {cores()}'))
        senha = str(input(f'{cores('verde')}Senha: {cores()}'))
        tipoLogin = menu('TIPO DE CADASTRO', ['Usuário comum', 'Administrador'])

        inserir_usuario(nome, email, senha, tipoLogin)

    elif escolha == 3: #ENTRAR COMO VISITANTE
        cabeçalho('Entrando como visitante')

    elif escolha == 4 or escolha == 0: #SAIR DO SISTEMA
        cabeçalho('Saindo...')
        break
    else:
        print(f'{cores('vermelho')}ERRO: Digite um número válido!{cores()}')
    sleep(1.5)