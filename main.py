from lib.texto import *

while True:
    escolha = menu('Ruralinfo' ,['Login', 'Cadastrar', 'Entrar como visitante', 'Sair'])
    if escolha == 1:
        cabeçalho('Login')
    elif escolha == 2:
        cabeçalho('Cadastrar')
    elif escolha == 3:
        cabeçalho('Entrar como visitante')
    elif escolha == 4 or escolha == 0:
        cabeçalho('Saindo...')
        break
    else:
        print(f'{cores('vermelho')}ERRO: Digite um número válido!{cores()}')