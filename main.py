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
        inserirUsuario('Luck', 'meufilho@gmail.com', 'teamo', 1)
    elif escolha == 3:
        cabeçalho('Entrando como visitante')
    elif escolha == 4 or escolha == 0:
        cabeçalho('Saindo...')
        break
    else:
        print(f'{cores('vermelho')}ERRO: Digite um número válido!{cores()}')
    sleep(1.5)