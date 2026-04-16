def cores(cor='reset'):
    """
    Retorna o código ANSI de uma cor ou estilo para formatação de texto no terminal.
    
    :param cor: O nome da cor ou estilo desejado (ex: 'verde', 'negrito'). 
                Padrão é 'reset'.
    :return: String contendo o código de escape ANSI.
    """
    opcoes = {
        'reset': '\033[0m',
        'preto': '\033[30m',
        'vermelho': '\033[31m',
        'verde': '\033[32m',
        'amarelo': '\033[33m',
        'azul': '\033[34m',
        'magenta': '\033[35m',
        'ciano': '\033[36m',
        'branco': '\033[37m',
        'negrito': '\033[1m'
    }
    
    selecionada = opcoes.get(cor.lower())
    return selecionada

def linha(valor = 42):
    """
    Imprime uma linha horizontal composta por hífens no terminal.
    
    :param valor: Número de caracteres de comprimento da linha (padrão: 42).
    """
    print(f'-' * valor)

def cabeçalho(msg = ''):
    """
    Exibe um cabeçalho visual com uma mensagem centralizada entre duas linhas.
    
    :param msg: O texto que será exibido no centro do cabeçalho.
    """
    linha()
    print(f'{cores('negrito')}{msg.center(42)}{cores()}')
    linha()

def menu(nome = '', lista = []):
    """
    Gera um menu interativo numerado com um título personalizável e 
    solicita a entrada do usuário.

    :param nome: O título que aparecerá no cabeçalho do menu.
    :param lista: Uma lista de strings contendo as opções do menu.
    :return: Um número inteiro correspondente à opção escolhida pelo usuário.
    """
    cabeçalho(nome)
    for cont, item in enumerate(lista):
        print(f'{cores('amarelo')}{cont+1}{cores()} - {cores('azul')}{item}{cores()}')
    linha()
    opc = leiaInt(f'{cores('verde')}Sua opção: {cores()}')
    return opc

def leiaInt(msg = ''):
    """
    Realiza a leitura de um número inteiro do teclado com validação de erro.
    
    O programa continuará pedindo a entrada até que um número inteiro 
    válido seja fornecido. Trata erros de tipo e interrupções de teclado.
    
    :param msg: Mensagem (prompt) que será exibida para o usuário.
    :return: O valor inteiro validado ou 0 em caso de interrupção (Ctrl+C).
    """
    while True:
        try:
            n = int(input(msg))
        except (ValueError, TypeError):
            print(f'{cores('vermelho')}ERRO: por favor, digite um número inteiro válido!{cores()}')
            continue
        except KeyboardInterrupt:
            print(f'{cores('vermelho')}O usuário preferiu não digitar esse número{cores()}')
            return 0
        else:
            return n